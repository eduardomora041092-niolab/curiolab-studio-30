"""Offline tests for the 2026-10-25 fixes: metrics-due ids, Buffer create gate, run lock.

Run: python3 pipeline/test_runfixes.py <repo>
Everything happens in a temporary sandbox (local clones + a local bare remote). No Buffer, Drive or GitHub call is
made and nothing is written to the real repository. The Buffer responses used here are SYNTHETIC test fixtures,
built in memory and kept only inside the sandbox; they are never archived as evidence of the real queue.
"""
import datetime as dt, json, os, shutil, subprocess, sys, tempfile

SRC = os.path.abspath(sys.argv[1]); TMP = tempfile.mkdtemp(prefix="curiolab_test_")
YT, TT = "6ad73b1a778b240e2f677dbf", "6ad739bd778b240e2f677654"; ORG = "6ad737f3bb7377f2534a518d"
results = {}

def sh(*a, cwd=None, check=True):
    r = subprocess.run(list(a), cwd=cwd, capture_output=True, text=True)
    if check and r.returncode: raise SystemExit(f"{a}: {r.stderr}")
    return r

def daily(clone, *a):
    r = subprocess.run([sys.executable, f"{clone}/pipeline/daily.py", *a], capture_output=True, text=True)
    return r.returncode, (r.stdout + r.stderr).strip()

def setup():
    src = f"{TMP}/src"; sh("git", "clone", "-q", SRC, src)
    for d in ("pipeline",):   # overlay the working-tree code under test (may be uncommitted)
        for f in os.listdir(f"{SRC}/{d}"):
            if f.endswith(".py"): shutil.copy(f"{SRC}/{d}/{f}", f"{src}/{d}/{f}")
    if os.path.exists(f"{src}/pipeline/lock.json"): os.remove(f"{src}/pipeline/lock.json")
    sh("git", "-C", src, "add", "-A"); sh("git", "-C", src, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "test base", check=False)
    sh("git", "clone", "-q", "--bare", src, f"{TMP}/remote.git")
    for c in ("A", "B"):
        sh("git", "clone", "-q", f"{TMP}/remote.git", f"{TMP}/{c}")
        sh("git", "-C", f"{TMP}/{c}", "config", "user.name", "t"); sh("git", "-C", f"{TMP}/{c}", "config", "user.email", "t@t")

def node(pid, ch, vid, status, due, sent=None, link=None, dur=26833):
    return {"id": pid, "channelId": ch, "status": status, "dueAt": due, "sentAt": sent, "externalLink": link, "error": None,
            "assets": [{"video": {"title": f"CurioLab_{vid}.mp4", "durationMs": dur}}]}

def snapshot(nodes_, nonce=None):
    e = lambda L: {"pageInfo": {"hasNextPage": False}, "edges": [{"node": n} for n in L]}
    s = {"account": {"organizations": [{"id": ORG, "limits": {"scheduledPosts": 10}}]},
         "limits": [{"channelId": YT, "isAtLimit": False, "limit": 10, "scheduled": 0, "sent": 0},
                    {"channelId": TT, "isAtLimit": False, "limit": 25, "scheduled": 0, "sent": 0}],
         "open": e([n for n in nodes_ if n["status"] in ("scheduled", "sending")]), "errors": e([]), "recent": e(nodes_)}
    if nonce: s = {f"req_{nonce}": {"id": "x"}, **s}
    return json.dumps(s) + '{"rateLimit":[{"remaining":99}]}'   # trailing object, as the MCP tool prints it

def iso(t): return t.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")

# ------------------------------------------------------------------ 1. metrics-due returns plain ids
def test_metrics(A):
    now = dt.datetime.now(dt.timezone.utc)
    ns = [node("p008tt", TT, "008", "sent", iso(now - dt.timedelta(hours=72)), iso(now - dt.timedelta(hours=72)), "https://t/8"),
          node("p008yt", YT, "008", "sent", iso(now - dt.timedelta(hours=72)), iso(now - dt.timedelta(hours=72)), "https://y/8"),
          node("p014tt", TT, "014", "sent", iso(now - dt.timedelta(hours=24)), iso(now - dt.timedelta(hours=24)), "https://t/14", 26733),
          node("p014yt", YT, "014", "sent", iso(now - dt.timedelta(hours=24)), iso(now - dt.timedelta(hours=24)), "https://y/14", 26733),
          {**node("other", YT, "x", "sent", iso(now - dt.timedelta(hours=30)), iso(now - dt.timedelta(hours=30))), "assets": []}]
    open(f"{TMP}/m_snap.json", "w").write(snapshot(ns))
    os.remove(f"{A}/logs/metrics.csv") if os.path.exists(f"{A}/logs/metrics.csv") else None   # sandbox only
    rc, out = daily(A, "metrics-due", f"{TMP}/m_snap.json"); due = json.loads(out)
    ids = sorted((d["video_id"], d["platform"], d["band"]) for d in due)
    results["1a_metrics_due_ids"] = ids
    assert ids == [("008", "tiktok", "72h"), ("008", "youtube", "72h"), ("014", "tiktok", "24h"), ("014", "youtube", "24h")], ids
    assert all(isinstance(d["video_id"], str) for d in due)
    # consumer: metrics accepts the fixed output and the legacy [id, durationMs] shape, writes plain ids
    rows = [{"video_id": d["video_id"], "platform": d["platform"], "post_id": d["post_id"], "metrics": [{"type": "views", "value": 1}]} for d in due]
    rows[0]["video_id"] = ["008", 26833]
    json.dump(rows, open(f"{TMP}/m.json", "w")); rc, out = daily(A, "metrics", f"{TMP}/m.json")
    csv_ids = sorted({l.split(",")[1] for l in open(f"{A}/logs/metrics.csv").read().splitlines()[1:]})
    results["1b_metrics_written_ids"] = (rc, csv_ids)
    assert rc == 0 and csv_ids == ["008", "014"], (rc, out, csv_ids)
    # invalid id -> refused, nothing appended
    before = open(f"{A}/logs/metrics.csv").read()
    json.dump([{"video_id": [None, None], "platform": "youtube", "post_id": "p", "metrics": [{"type": "views", "value": 1}]}], open(f"{TMP}/bad.json", "w"))
    rc, out = daily(A, "metrics", f"{TMP}/bad.json")
    results["1c_metrics_invalid_refused"] = rc
    assert rc == 2 and open(f"{A}/logs/metrics.csv").read() == before
    # compare (consumer of metrics.csv) still runs
    rc, out = daily(A, "compare", "24h"); results["1d_compare_runs"] = rc; assert rc == 0, out

# ------------------------------------------------------------------ 2. Buffer create gate
def test_gate(A):
    st = json.load(open(f"{A}/pipeline/state.json"))
    live = []
    for vid, v in sorted(st["videos"].items()):   # every recorded live post of the real state appears in the fake queue
        for plat, p in v["posts"].items():
            if p.get("status") in ("scheduled", "sending"):
                live.append(node(p["post_id"], YT if plat == "youtube" else TT, vid, "scheduled", "2026-12-01T13:00:00.000Z"))
    live = live[:4]   # 4 occupied -> free 10 - 1 - 4 = 5, enough room for the 4 test items
    for vid in ("022", "023"):   # pretend these are produced + hosted (sandbox only)
        st["videos"][vid].update(media_url=f"https://example.invalid/CurioLab_{vid}.mp4", qa={"all_pass": True, "duration_s": 26.0}, posts={})
    json.dump(st, open(f"{A}/pipeline/state.json", "w"))
    def fresh(purpose, extra=()):
        rc, out = daily(A, "snapshot-query", purpose, "--graphql"); q = json.loads(out)
        assert f"req_{q['nonce']}: account" in q["query"]
        p = f"{TMP}/snap_{q['nonce']}.json"; open(p, "w").write(snapshot(live + list(extra), q["nonce"])); return p, q["nonce"]
    # informative plan (step 2) never authorises creates
    p, _ = fresh("reconcile"); rc, out = daily(A, "queue", p); assert rc == 0, out
    rc, out = daily(A, "create-next"); results["2a_plan_without_flag"] = out.split(":")[0]; assert rc == 5 and out.startswith("REFUSED")
    # snapshot without nonce / reused / old -> refused for creating
    open(f"{TMP}/nononce.json", "w").write(snapshot(live))
    rc, out = daily(A, "queue", f"{TMP}/nononce.json", "--for-create"); results["2b_no_nonce"] = out; assert rc == 5
    rc, out = daily(A, "queue", p, "--for-create"); results["2c_reused_snapshot"] = out; assert rc == 5 and "ya se usó" in out
    p_old, n_old = fresh("pre-create"); reqs = json.load(open(f"{A}/pipeline/snapshot_requests.json"))
    for r in reqs:
        if r["nonce"] == n_old: r["issued"] = (dt.datetime.fromisoformat(r["issued"]) - dt.timedelta(minutes=11)).isoformat()
    json.dump(reqs, open(f"{A}/pipeline/snapshot_requests.json", "w"))
    rc, out = daily(A, "queue", p_old, "--for-create"); results["2d_old_snapshot"] = out; assert rc == 5 and "min" in out
    # fresh snapshot -> plan authorised; items handed out one at a time
    p1, n1 = fresh("pre-create"); rc, out = daily(A, "queue", p1, "--for-create"); plan = json.loads(out)
    todo = [(c["id"], c["platform"]) for c in plan["create"]]
    results["2e_fresh_plan"] = {"occupied": plan["occupied"], "create": todo}
    assert todo and plan["for_create"] and plan["snapshots"][0]["nonce"] == n1
    arch = f"{A}/{plan['snapshots'][0]['file']}"
    assert open(arch, "rb").read() == open(p1, "rb").read()          # archived byte for byte
    rc, out = daily(A, "create-next"); first = json.loads(out)
    rc2, out2 = daily(A, "create-next"); results["2f_second_offer_blocked"] = out2.split(":")[0]
    assert rc2 == 6 and out2.startswith("PENDING_RECORD")
    rc, out = daily(A, "record", first["id"], first["platform"], "newpost1", "scheduled"); assert rc == 0, out
    rc, out = daily(A, "create-next"); second = json.loads(out)
    assert (second["id"], second["platform"]) != (first["id"], first["platform"])
    # --- interruption: the run dies after create_post of `second` but before `record` -------------------------
    created = node("newpost2", YT if second["platform"] == "youtube" else TT, second["id"], "scheduled", "2026-12-02T13:00:00.000Z")
    created1 = node("newpost1", YT if first["platform"] == "youtube" else TT, first["id"], "scheduled", "2026-12-02T13:00:00.000Z")
    p2, _ = fresh("pre-create", [created1, created]); rc, out = daily(A, "queue", p2, "--for-create"); plan2 = json.loads(out)
    again = [(c["id"], c["platform"]) for c in plan2["create"]]
    results["2g_restart_after_interruption"] = {"create": again, "reconciled": plan2["reconciled"], "warnings": plan2["warnings"]}
    assert (first["id"], first["platform"]) not in again and (second["id"], second["platform"]) not in again
    assert any("newpost2" in r for r in plan2["reconciled"]) and not any(w.startswith("DUPLICADO") for w in plan2["warnings"])
    # failed create (e.g. LimitReachedError) -> no more creates in this plan
    rc, out = daily(A, "create-next")
    if rc == 0:
        it = json.loads(out); daily(A, "record", it["id"], it["platform"], "-", "failed", "LimitReachedError")
        rc, out = daily(A, "create-next"); results["2h_after_failure"] = out.split(":")[0]; assert rc == 3 and out.startswith("STOP")
    # expired plan
    plan3 = json.load(open(f"{A}/pipeline/queue_plan.json")); plan3["valid_until"] = "2000-01-01T00:00:00-05:00"; plan3.pop("stop", None)
    json.dump(plan3, open(f"{A}/pipeline/queue_plan.json", "w"))
    rc, out = daily(A, "create-next"); results["2i_expired_plan"] = out.split(":")[0]; assert rc == 5 and out.startswith("STALE")

# ------------------------------------------------------------------ 3. run lock
def test_lock(A, B):
    r = {}
    r["A_acquire"] = daily(A, "lock", "acquire"); r["B_acquire_busy"] = daily(B, "lock", "acquire")
    r["B_release_not_owner"] = daily(B, "lock", "release"); r["A_check"] = daily(A, "lock", "check")
    open(f"{A}/scratch.txt", "w").write("x")
    r["A_release_dirty_refused"] = daily(A, "lock", "release"); os.remove(f"{A}/scratch.txt")
    sh("git", "-C", A, "checkout", "-q", "--", "."); sh("git", "-C", A, "clean", "-qfd")   # drop sandbox test files
    r["A_release_ok"] = daily(A, "lock", "release")
    sh("git", "-C", B, "fetch", "-q", "origin", "main")
    r["lock_gone_after_release"] = sh("git", "-C", B, "show", "origin/main:pipeline/lock.json", check=False).returncode != 0
    sh("git", "-C", B, "checkout", "-q", "--", "."); sh("git", "-C", B, "pull", "-q", "--rebase", "origin", "main")   # fresh session B
    # stale takeover: B holds a lock whose 'since' is 3 h old; A takes it over; B's late release must not free A's lock
    r["B_acquire"] = daily(B, "lock", "acquire")
    lk = json.load(open(f"{B}/pipeline/lock.json"))
    lk["since"] = (dt.datetime.fromisoformat(lk["since"]) - dt.timedelta(hours=3)).isoformat(timespec="seconds")
    json.dump(lk, open(f"{B}/pipeline/lock.json", "w"))
    sh("git", "-C", B, "commit", "-qam", "age lock (test)"); sh("git", "-C", B, "push", "-q", "origin", "main")
    r["A_takeover_stale"] = daily(A, "lock", "acquire"); r["B_late_release_not_owner"] = daily(B, "lock", "release")
    r["A_still_owner"] = daily(A, "lock", "check"); r["A_final_release"] = daily(A, "lock", "release")
    results["3_lock"] = {k: v if isinstance(v, bool) else v[1].splitlines()[-1] for k, v in r.items()}
    exp = {"A_acquire": 0, "B_acquire_busy": 4, "B_release_not_owner": 7, "A_check": 0, "A_release_dirty_refused": 8, "A_release_ok": 0,
           "B_acquire": 0, "A_takeover_stale": 0, "B_late_release_not_owner": 7, "A_still_owner": 0, "A_final_release": 0}
    bad = {k: r[k] for k, c in exp.items() if r[k][0] != c}
    assert not bad and r["lock_gone_after_release"], bad

try:
    setup(); A, B = f"{TMP}/A", f"{TMP}/B"
    test_metrics(A)
    sh("git", "-C", A, "checkout", "-q", "--", "."); sh("git", "-C", A, "clean", "-qfd")
    test_gate(A)
    sh("git", "-C", A, "checkout", "-q", "--", "."); sh("git", "-C", A, "clean", "-qfd")
    test_lock(A, B)
    print(json.dumps(results, ensure_ascii=False, indent=1)); print("ALL RUN-FIX TESTS PASS")
finally:
    shutil.rmtree(TMP, ignore_errors=True)

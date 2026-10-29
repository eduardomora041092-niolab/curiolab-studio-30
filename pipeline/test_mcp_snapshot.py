"""Offline tests for the MCP-based Buffer snapshot (2026-10-29): validation, pagination, freshness, reuse, links and
the per-run verdict. Run: python3 pipeline/test_mcp_snapshot.py <repo>
Works on a throw-away copy of the repository. The Buffer outputs below are SYNTHETIC fixtures built in memory, shaped
like the real get_account / list_posts / get_post outputs; they are never archived as evidence of the real queue."""
import datetime as dt, json, os, shutil, subprocess, sys, tempfile

SRC = os.path.abspath(sys.argv[1]); TMP = tempfile.mkdtemp(prefix="curiolab_mcp_")
YT, TT, ORG = "6ad73b1a778b240e2f677dbf", "6ad739bd778b240e2f677654", "6ad737f3bb7377f2534a518d"
R = f"{TMP}/repo"; res = {}
shutil.copytree(SRC, R, ignore=shutil.ignore_patterns(".git", "out", "work", "models", "__pycache__"))

def daily(*a):
    r = subprocess.run([sys.executable, f"{R}/pipeline/daily.py", *a], capture_output=True, text=True)
    return r.returncode, (r.stdout + r.stderr).strip()

def node(pid, ch, vid, status, due, sent=None):
    return {"id": pid, "status": status, "dueAt": due, "sentAt": sent, "channelId": ch,
            "channelService": "youtube" if ch == YT else "tiktok", "error": None,
            "assets": [{"video": {"title": f"CurioLab_{vid}.mp4", "durationMs": 26000}}]}

def lst(nodes_, more=False, end="CUR1"):
    return json.dumps({"edges": [{"cursor": n["id"], "node": n} for n in nodes_],
                       "pageInfo": {"hasNextPage": more, "endCursor": end}}) + '{"rateLimit":[{"remaining":1}]}'

def acct(t):
    return json.dumps({"id": "x", "organizations": [{"id": ORG, "limits": {"scheduledPosts": 10}}], "currentTime": t.isoformat()})

def request(purpose):
    rc, out = daily("snapshot-query", purpose); assert rc == 0, out; return json.loads(out)

def fill(q, open_, errs, recent, t=None, extra=None):
    d = q["dir"]; t = t or dt.datetime.now().astimezone()
    open(f"{d}/open.json", "w").write(lst(open_)); open(f"{d}/errors.json", "w").write(lst(errs))
    open(f"{d}/recent.json", "w").write(lst(recent)); open(f"{d}/account.json", "w").write(acct(t))
    for k, v in (extra or {}).items(): open(f"{d}/{k}", "w").write(v)
    return d

try:
    st = json.load(open(f"{R}/pipeline/state.json"))
    live = []
    for vid, v in sorted(st["videos"].items()):   # every live post of the real state appears as scheduled/sent
        for plat, p in v["posts"].items():
            if p.get("status") in ("scheduled", "sending"):
                live.append(node(p["post_id"], YT if plat == "youtube" else TT, vid, "scheduled", "2026-11-30T13:00:00.000Z"))
    rc, out = daily("lock", "acquire")   # no git here: only the run journal matters for this test
    open(f"{R}/pipeline/run_status.json", "w").write(json.dumps({"run_id": "t", "started": "x", "stages": {}}))

    # 1 complete snapshot -> accepted, archived byte for byte with sha256
    q = request("reconcile"); d = fill(q, live, [], live)
    rc, out = daily("queue", d); plan = json.loads(out)
    res["1_accepted"] = (rc, plan["occupied"], plan["snapshots"][0]["source"], sorted(plan["snapshots"][0]["files"]))
    assert rc == 0 and plan["snapshots"][0]["source"] == "mcp" and os.path.isdir(f"{R}/{plan['snapshots'][0]['file']}")
    assert plan["missing_info"] and plan["per_channel_today"][0]["limit"] is None
    # 2 missing file -> refused
    q = request("reconcile"); d = fill(q, live, [], live); os.remove(f"{d}/errors.json")
    rc, out = daily("queue", d); res["2_missing_file"] = out.splitlines()[-1]; assert rc == 5 and "errors.json" in out
    # 3 hasNextPage without next page -> refused naming the exact call; with p2 -> merged
    q = request("reconcile"); d = fill(q, live, [], live[:2])
    open(f"{d}/recent.json", "w").write(lst(live[:2], more=True, end="ENDCUR"))
    rc, out = daily("queue", d); res["3a_partial_page"] = out.splitlines()[-1]; assert rc == 5 and "ENDCUR" in out and "recent.p2.json" in out
    q = request("reconcile"); d = fill(q, live, [], live[:2])
    open(f"{d}/recent.json", "w").write(lst(live[:2], more=True)); open(f"{d}/recent.p2.json", "w").write(lst(live[2:]))
    rc, out = daily("queue", d); res["3b_paginated_ok"] = (rc, json.loads(out)["snapshots"][0]["pages"]); assert rc == 0
    # 4 node that does not match the call's filter (a sent post in the scheduled list) -> refused
    q = request("reconcile"); bad = dict(live[0], status="sent"); d = fill(q, [bad] + live[1:], [], live)
    rc, out = daily("queue", d); res["4_filter_mismatch"] = out.splitlines()[-1]; assert rc == 5 and "filtro" in out
    # 5 freshness: account currentTime long after the request -> refused; reuse for create -> refused
    q = request("reconcile"); d = fill(q, live, [], live, t=dt.datetime.now().astimezone() + dt.timedelta(minutes=15))
    rc, out = daily("queue", d); res["5a_late_calls"] = out.splitlines()[-1]; assert rc == 5 and "min" in out
    q = request("pre-create"); d = fill(q, live, [], live)
    rc, out = daily("queue", d, "--for-create"); assert rc == 0, out
    rc, out = daily("queue", d, "--for-create"); res["5b_reused"] = out.splitlines()[-1]; assert rc == 5 and "ya se usó" in out
    q = request("pre-create"); d = fill(q, live, [], live, t=dt.datetime.now().astimezone() - dt.timedelta(minutes=3))
    rc, out = daily("queue", d, "--for-create"); res["5c_output_older_than_request"] = out.splitlines()[-1]; assert rc == 5 and "anterior" in out
    q = request("pre-create"); d = fill(q, live, [], live, t=dt.datetime.now().astimezone() + dt.timedelta(minutes=1))
    rc, out = daily("queue", d, "--for-create"); res["5d_fresh_ok"] = rc; assert rc == 0, out
    # 6 a dir that no snapshot-query issued -> refused
    os.makedirs(f"{TMP}/rogue"); fill({"dir": f"{TMP}/rogue"}, live, [], live)
    rc, out = daily("queue", f"{TMP}/rogue"); res["6_unissued_dir"] = out.splitlines()[-1]; assert rc == 5
    # 7 sent post without link -> snapshot-links lists the get_post call; link_<id>.json fills the public URL
    v0, p0 = next((v, p) for v, x in sorted(st["videos"].items()) for p, y in x["posts"].items() if y.get("status") == "scheduled")
    pid = st["videos"][v0]["posts"][p0]["post_id"]
    sent = [dict(n, status="sent", sentAt="2026-10-29T13:02:00.000Z") if n["id"] == pid else n for n in live]
    q = request("reconcile"); d = fill(q, [n for n in sent if n["status"] == "scheduled"], [], sent)
    rc, out = daily("snapshot-links", d); need = json.loads(out); res["7a_links_needed"] = [x["post_id"] for x in need]
    assert any(x["post_id"] == pid for x in need)
    open(f"{d}/link_{pid}.json", "w").write(json.dumps({"id": pid, "status": "sent", "externalLink": f"https://example.test/{pid}"}))
    rc, out = daily("queue", d); assert rc == 0, out
    url = json.load(open(f"{R}/pipeline/state.json"))["videos"][v0]["posts"][p0]["url"]; res["7b_link_reconciled"] = url
    assert url == f"https://example.test/{pid}"
    # 8 run verdict: production alone is not a complete run
    open(f"{R}/pipeline/run_status.json", "w").write(json.dumps({"run_id": "t", "started": "x", "stages": {
        "production_031": {"status": "PASS"}, "reconcile": {"status": "BLOCKED", "msg": "sin herramienta"}}}))
    rc, out = daily("cycle"); v1 = json.loads(out)["verdict"]
    open(f"{R}/pipeline/run_status.json", "w").write(json.dumps({"run_id": "t", "started": "x", "stages": {
        "production_031": {"status": "PASS"}, "reconcile": {"status": "PASS"}, "metrics": {"status": "PASS"}, "pre-create": {"status": "PASS"}}}))
    rc, out = daily("cycle"); v2 = json.loads(out)
    for k in ("metrics", "pre-create", "scheduling", "confirm", "reconcile"):
        v2["run"]["required"].setdefault(k, None)
    open(f"{R}/pipeline/run_status.json", "w").write(json.dumps({"run_id": "t", "started": "x", "stages": {
        k: {"status": "PASS"} for k in ("reconcile", "metrics", "pre-create", "scheduling", "confirm")}}))
    rc, out = daily("cycle"); v3 = json.loads(out)["verdict"]
    res["8_run_verdict"] = (v1, v2["verdict"], v2["run"]["not_passed"], v3)
    assert (v1, v2["verdict"], v3) == ("BLOQUEADO", "PARCIAL", "COMPLETO") and v2["run"]["not_passed"] == ["scheduling", "confirm"]
    print(json.dumps(res, ensure_ascii=False, indent=1)); print("ALL MCP SNAPSHOT TESTS PASS")
finally:
    shutil.rmtree(TMP, ignore_errors=True)

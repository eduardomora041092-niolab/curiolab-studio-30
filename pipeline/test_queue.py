"""Offline tests for queue_editorial.plan_queue (no Buffer calls, nothing written). Run: python3 pipeline/test_queue.py ."""
import sys, json, copy, datetime as dt
sys.path.insert(0, sys.argv[1] + "/pipeline")
import daily as D, queue_editorial as Q
YT, TT = D.CHANNELS["youtube"], D.CHANNELS["tiktok"]
def node(pid, ch, vid, status, due, link=None):
    return {"id": pid, "channelId": ch, "status": status, "dueAt": due, "externalLink": link, "error": {"message": "x"} if status == "error" else None,
            "assets": [{"video": {"title": f"CurioLab_{vid}.mp4", "durationMs": 28000}}]}
def snap(recent, open_=None, errs=None, limit=10, atlimit=False):
    open_ = [n for n in recent if n["status"] in ("scheduled", "sending")] if open_ is None else open_
    errs = [n for n in recent if n["status"] == "error"] if errs is None else errs
    e = lambda L: {"pageInfo": {"hasNextPage": False}, "edges": [{"node": n} for n in L]}
    return {"account": {"organizations": [{"limits": {"scheduledPosts": limit}}]},
            "limits": [{"channelId": YT, "isAtLimit": atlimit, "limit": 10, "scheduled": 0, "sent": 0}, {"channelId": TT, "isAtLimit": False, "limit": 25, "scheduled": 0, "sent": 0}],
            "open": e(open_), "errors": e(errs), "recent": e(recent)}
st0 = D.state()
for i in ("010", "011", "012"): st0["videos"][i]["estado"] = "PRODUCED"; [p.update(status="scheduled", url="") for p in st0["videos"][i]["posts"].values()]
for i in sorted(st0["videos"]):
    if i > "012": st0["videos"][i].update(media_url=None, qa=None, posts={})
cal = {r["id"]: r for r in D.load(D.CAL)}
now = dt.datetime(2026, 10, 23, 6, 40, tzinfo=D.TZ)       # next morning run
base = []
for vid, due in (("010", "2026-10-23T13:00:00Z"), ("011", "2026-10-23T17:00:00Z"), ("012", "2026-10-23T22:00:00Z")):
    v = st0["videos"][vid]
    base += [node(v["posts"]["youtube"]["post_id"], YT, vid, "scheduled", due), node(v["posts"]["tiktok"]["post_id"], TT, vid, "scheduled", due)]
def prepared(st, ids=("013", "014", "015")):
    for i in ids:
        st["videos"][i].update({"media_url": f"https://x/CurioLab_{i}.mp4", "qa": {"all_pass": True, "duration_s": 27.0}, "posts": {}})
    return st
res = {}
# 1 morning: 6 occupied, 3 new videos ready -> free 3 -> create 3, wait 3
st = prepared(copy.deepcopy(st0)); p = Q.plan_queue(snap(base), st, cal, now)
res["1_morning_6_occupied"] = (p["occupied"], len(p["create"]), len(p["waiting"]), [(c["id"], c["platform"], c["mode"]) for c in p["create"]])
assert p["occupied"] == 6 and len(p["create"]) == 3 and len(p["waiting"]) == 3
assert all(c["mode"] == "customScheduled" and c["dueAt"].startswith("2026-10-24") for c in p["create"])
# 2 idempotency: rerun with the 3 created posts present -> nothing new to create (queue full at 9)
created = [node(f"new{k}", c["channelId"], c["id"], "scheduled", "2026-10-24T13:00:00Z") for k, c in enumerate(p["create"])]
p2 = Q.plan_queue(snap(base + created), st, cal, now)
res["2_rerun_no_duplicates"] = (p2["occupied"], len(p2["create"]), len(p2["waiting"]))
assert p2["occupied"] == 9 and len(p2["create"]) == 0 and len(p2["waiting"]) == 3
# 3 afternoon: 010/011 sent (with links) -> slots freed -> remaining 3 created, 010/011 reconciled sent
later = [dict(n, status="sent", externalLink=f"https://link/{n['id']}") if n["dueAt"] < "2026-10-23T18:00:00Z" else n for n in base]
now2 = dt.datetime(2026, 10, 23, 13, 40, tzinfo=D.TZ)
p3 = Q.plan_queue(snap(later + created), st, cal, now2)
res["3_afternoon_after_slots"] = (p3["occupied"], len(p3["create"]), len(p3["reconciled"]), st["videos"]["010"]["estado"], st["videos"]["010"]["posts"]["youtube"]["url"])
assert len(p3["create"]) == 3 and st["videos"]["010"]["estado"] == "PUBLISHED" and st["videos"]["011"]["posts"]["tiktok"]["url"].startswith("https://link/")
# 4 open list comes back empty (Buffer filter bug) -> occupied still counted from channel window
st = prepared(copy.deepcopy(st0)); p4 = Q.plan_queue(snap(base, open_=[]), st, cal, now)
res["4_open_list_empty"] = (p4["occupied"], len(p4["create"]))
assert p4["occupied"] == 6 and len(p4["create"]) == 3
# 5 one error -> recreate once; two errors -> blocked
st = prepared(copy.deepcopy(st0), ("013",)); err1 = [node("e1", TT, "013", "error", "2026-10-24T13:00:00Z"), node("ok", YT, "013", "scheduled", "2026-10-24T13:00:00Z")]
p5 = Q.plan_queue(snap(err1), st, cal, now)
st = prepared(copy.deepcopy(st0), ("013",)); err2 = err1 + [node("e2", TT, "013", "error", "2026-10-24T13:00:00Z")]
p5b = Q.plan_queue(snap(err2), st, cal, now)
res["5_error_recreate_once"] = ([(c["id"], c["platform"], c["reason"]) for c in p5["create"]], p5b["blocked"])
assert [(c["id"], c["platform"]) for c in p5["create"]] == [("013", "tiktok")] and p5["create"][0]["reason"] == "recrear tras error"
assert not p5b["create"] and p5b["blocked"]
# 6 duplicate live posts -> warning, nothing created or deleted
st = prepared(copy.deepcopy(st0), ()); dup = base + [node("dup", YT, "010", "scheduled", "2026-10-23T13:00:00Z")]
p6 = Q.plan_queue(snap(dup), st, cal, now)
res["6_duplicate_warning"] = [w for w in p6["warnings"] if w.startswith("DUPLICADO")]
assert res["6_duplicate_warning"] and not p6["create"]
# 7 full queue (9 occupied) -> nothing created, everything waits
st = prepared(copy.deepcopy(st0)); full = base + [node(f"f{k}", YT, "009", "scheduled", "2026-10-22T22:00:00Z") for k in range(3)]
p7 = Q.plan_queue(snap(full), st, cal, now)
res["7_full_queue"] = (p7["occupied"], len(p7["create"]), len(p7["waiting"]))
assert len(p7["create"]) == 0 and len(p7["waiting"]) == 6
# 8 late post warning (scheduled > 45 min after its time)
st = prepared(copy.deepcopy(st0), ()); p8 = Q.plan_queue(snap(base), st, cal, dt.datetime(2026, 10, 23, 10, 0, tzinfo=D.TZ))
res["8_late_warning"] = [w for w in p8["warnings"] if w.startswith("RETRASO")]
assert res["8_late_warning"]
# 9 past slot -> shareNow (never earlier than calendar)
st = prepared(copy.deepcopy(st0), ("013",)); p9 = Q.plan_queue(snap([]), st, cal, dt.datetime(2026, 10, 24, 10, 0, tzinfo=D.TZ))
res["9_past_slot_sharenow"] = [(c["id"], c["platform"], c["mode"]) for c in p9["create"]]
assert all(c["mode"] == "shareNow" for c in p9["create"])
print(json.dumps(res, ensure_ascii=False, indent=1)); print("ALL QUEUE TESTS PASS")

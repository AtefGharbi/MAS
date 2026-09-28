"""Recompute every S2/S3 count reported in Tables XV-XXI of the V20 manuscript from the raw records.
Usage: python reconcile_S2_S3.py <path-to-results-dir>   (contains S2/results.jsonl and S3/results.jsonl)"""
import json, sys, collections as C
import numpy as np
R = sys.argv[1] if len(sys.argv) > 1 else "results"
M = ["M0", "M1", "M2", "M2b", "M3"]; F = ["syn13", "syn34", "syn123"]
load = lambda p: [json.loads(l) for l in open(p) if l.strip()]
def ok(r): return r["status"] == "converged"
s2 = load(f"{R}/S2/results.jsonl"); s3 = load(f"{R}/S3/results.jsonl")
print("== Table XV: reconciliation")
for m in M:
    a = [r for r in s2 if r["method"] == m]; b = [r for r in s3 if r["method"] == m]
    f2 = [r for r in a if not ok(r)]; f3 = [r for r in b if not ok(r)]
    print(m, "S2", len(a), sum(map(ok, a)), len(f2), sum(r["latency_ms"] in (250, 500) for r in f2), sum(r["loss_pct"] == 20 for r in f2),
          "| S3", len(b), sum(map(ok, b)), sum(r["T_PF"] >= 299 for r in f3), sum(r["T_PF"] < 299 for r in f3),
          [sum(r["feeder"] == f for r in f3) for f in F], C.Counter(r["fault"] for r in f3), C.Counter(r["route_available"] for r in f3))
print("== Table XVI: S2 by feeder/method (conv, median T_PF conv, mean C_msg all, max E_V^max conv)")
for f in F:
    for m in M:
        rs = [r for r in s2 if r["feeder"] == f and r["method"] == m]; c = [r for r in rs if ok(r)]
        print(f, m, f"{len(c)}/{len(rs)}", round(np.median([r['T_PF'] for r in c]), 2), round(np.mean([r['C_msg'] for r in rs])), f"{max(r['E_V_max'] for r in c):.1e}")
for m in M:
    rs = [r for r in s2 if r["method"] == m]
    print(m, "false alarms", sum(r["false_alarms"] for r in rs), "reroutes", sum(r["reroutes"] for r in rs))
big = [r for r in s2 if ok(r) and r["method"] != "M0" and r["E_V_max"] > 1e-6]
print("async converged runs with E_V^max>1e-6:", len(big), "latencies:", sorted({r["latency_ms"] for r in big}))
print("== Table XVIII: S3 by method/fault class")
cls = lambda r: "complete" if r["fault"] == "complete_outage" else ("routed_avail" if r["route_available"] else "routed_unavail")
for m in M:
    for c in ("routed_avail", "routed_unavail", "complete"):
        rs = [r for r in s3 if r["method"] == m and cls(r) == c]; cv = [r for r in rs if ok(r)]
        print(m, c, f"{len(cv)}/{len(rs)}", round(np.median([r['T_PF'] for r in cv]), 2), round(np.mean([r['T_PF'] for r in rs]), 2),
              *[sum(r[k] for r in rs) for k in ("restarts", "reroutes", "degraded_entries", "false_alarms")])
print("== Table XIX: S3 by feeder"); [print(f, [sum(ok(r) for r in s3 if r["feeder"] == f and r["method"] == m) for m in M]) for f in F]
co = [r for r in s3 if r["fault"] == "complete_outage" and r["method"] in ("M2b", "M3")]
print("S3 false alarms M2b+M3 total", sum(r["false_alarms"] for r in s3 if r["method"] in ("M2b", "M3")),
      "complete-outage", sum(r["false_alarms"] for r in co), "syn123 complete", sum(r["false_alarms"] for r in co if r["feeder"] == "syn123"),
      "syn123 by duration", {d: sum(r["false_alarms"] for r in co if r["feeder"] == "syn123" and r["duration_s"] == d) for d in sorted({r["duration_s"] for r in co})})
print("== Table XXI: non-converged S3 records")
for r in s3:
    if not ok(r): print(r["method"], r["feeder"], r["fault"], r["duration_s"], r["route_available"], r["seed"], round(r["T_PF"], 2), r["reroutes"], r["trace_id"])

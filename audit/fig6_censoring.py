"""Regenerate Fig. 6 (S3 mean T_PF by duration and route class) with markers on points that include
nonconverged (capped or stalled) trajectories. Usage: python fig6_censoring.py <results-dir> <out.png>"""
import json, sys, numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
R, out = sys.argv[1], sys.argv[2]
rows = [json.loads(l) for l in open(f"{R}/S3/results.jsonl") if l.strip()]
METH = ["M0", "M1", "M2", "M2b", "M3"]; durs = sorted({r["duration_s"] for r in rows})
plt.rcParams.update({"font.family": "serif", "font.size": 9})
fig, axes = plt.subplots(1, 3, figsize=(8.445, 2.77), dpi=200, sharey=True)
for ax, (ra, title) in zip(axes, ((True, "routed faults, route available"), (False, "routed faults, route unavailable"),
                                   (None, "complete outage"))):
    for m in METH:
        ys, cens = [], []
        for d in durs:
            rs = [r for r in rows if r["method"] == m and r["route_available"] == ra and r["duration_s"] == d]
            ys.append(np.mean([r["T_PF"] for r in rs])); cens.append(any(r["status"] != "converged" for r in rs))
        line, = ax.plot(durs, ys, marker="o", ms=3, label=m)
        for d, y, c in zip(durs, ys, cens):
            if c: ax.plot(d, y, marker="x", ms=8, mew=1.4, color="black", zorder=5)
    ax.set_xscale("log"); ax.set_yscale("log"); ax.set_title(title, fontsize=8); ax.set_xlabel("fault duration (s)"); ax.grid(alpha=.3)
axes[0].set_ylabel("mean T_PF (model s), all runs")
h, l = axes[0].get_legend_handles_labels()
h.append(plt.Line2D([], [], marker="x", ls="", color="black", ms=7, mew=1.4)); l.append("includes nonconverged run(s)")
axes[0].legend(h, l, fontsize=6.5, loc="upper left")
fig.subplots_adjust(left=0.075, right=0.99, bottom=0.17, top=0.9, wspace=0.08)
fig.savefig(out, dpi=200)

"""Figure for edge-vs-cloud-cost-model.

Worked arithmetic over three years, with every rate stated on the figure.
The rates are illustrative; the point is that the same four cost lines give
opposite answers for the two shapes of deployment.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

import style
from style import C, INK, INK2, MUTED, GRID, GOOD, WARN, CRIT, save

SLUG = "edge-vs-cloud-cost-model"

YEARS = 3
MONTHS = YEARS * 12

# --- stated assumptions
BOX_COST = 1500          # an edge box with an accelerator, serving up to 8 cameras
CAMS_PER_BOX = 8
EDGE_OPS_SITE_YEAR = 600  # monitoring, updates and the occasional visit
CLOUD_COMPUTE_CAM_MONTH = 18
CLOUD_BANDWIDTH_CAM_MONTH = 12     # one 2 Mbps stream is about 650 GB a month
CLOUD_OPS_SITE_YEAR = 150

SCENARIOS = [
    ("100 shops,\n2 cameras each", 100, 2),
    ("1 port,\n60 cameras", 1, 60),
]


def edge_cost(sites, cams_per_site):
    boxes = sites * int(np.ceil(cams_per_site / CAMS_PER_BOX))
    return {"hardware": boxes * BOX_COST,
            "bandwidth": 0,
            "compute": 0,
            "operations": sites * EDGE_OPS_SITE_YEAR * YEARS}


def cloud_cost(sites, cams_per_site):
    cams = sites * cams_per_site
    return {"hardware": 0,
            "bandwidth": cams * CLOUD_BANDWIDTH_CAM_MONTH * MONTHS,
            "compute": cams * CLOUD_COMPUTE_CAM_MONTH * MONTHS,
            "operations": sites * CLOUD_OPS_SITE_YEAR * YEARS}


LINES = [("hardware", C[0]), ("bandwidth", C[1]), ("compute", C[3]), ("operations", C[2])]

fig, axs = plt.subplots(1, 2, figsize=(12.8, 6.2))

for ax, (title, sites, cams) in zip(axs, SCENARIOS):
    e, c = edge_cost(sites, cams), cloud_cost(sites, cams)
    xs = [0, 1]
    bottoms = [0, 0]
    for name, col in LINES:
        vals = [e[name], c[name]]
        ax.bar(xs, vals, 0.56, bottom=bottoms, color=col)
        for i, v in enumerate(vals):
            if v > max(sum(e.values()), sum(c.values())) * 0.055:
                ax.text(xs[i], bottoms[i] + v / 2, f"{name}\n£{v/1000:,.0f}k",
                        ha="center", va="center", fontsize=10.3, color="white",
                        weight="bold", linespacing=1.25)
        bottoms = [bottoms[0] + vals[0], bottoms[1] + vals[1]]

    tot_e, tot_c = sum(e.values()), sum(c.values())
    top = max(tot_e, tot_c)
    for x, t in zip(xs, [tot_e, tot_c]):
        ax.text(x, t + top * 0.035, f"£{t/1000:,.0f}k", ha="center", fontsize=13.5,
                weight="bold", color=INK)
    winner = "edge" if tot_e < tot_c else "cloud"
    saving = abs(tot_e - tot_c) / max(tot_e, tot_c) * 100
    ax.text(0.5, top * 1.24, f"{winner} is {saving:.0f}% cheaper",
            ha="center", fontsize=13.5, weight="bold", color=GOOD)

    ax.set_xticks(xs, ["edge", "cloud"], fontsize=12.5)
    ax.set_ylim(0, top * 1.34)
    label = title if sites == 1 else f"{title}   ({sites * cams} cameras)"
    ax.set_title(label, fontsize=12.6, loc="left")
    ax.set_ylabel("three-year cost (£)" if ax is axs[0] else "")
    ax.yaxis.set_major_formatter(lambda v, _: f"£{v/1000:,.0f}k")
    ax.grid(axis="x", visible=False)

fig.legend(handles=[Patch(fc=col, label=name) for name, col in LINES],
           loc="upper right", bbox_to_anchor=(0.995, 0.995), fontsize=11, ncol=4,
           frameon=False)

fig.suptitle("The same four cost lines, opposite answers",
             x=0.008, ha="left", fontsize=15.5, weight="bold")
fig.text(0.008, 0.925,
         f"Illustrative rates, stated so you can swap yours in: edge box £{BOX_COST:,} for "
         f"{CAMS_PER_BOX} cameras, edge operations £{EDGE_OPS_SITE_YEAR}/site/year; cloud "
         f"£{CLOUD_COMPUTE_CAM_MONTH}/camera/month compute, £{CLOUD_BANDWIDTH_CAM_MONTH} "
         f"bandwidth, £{CLOUD_OPS_SITE_YEAR}/site/year operations.",
         ha="left", va="top", fontsize=10.9, color=INK2)
fig.tight_layout(rect=[0, 0, 1, 0.875])
save(fig, f"{SLUG}-three-year-cost.png")

for title, sites, cams in SCENARIOS:
    e, c = edge_cost(sites, cams), cloud_cost(sites, cams)
    print(f"{title.replace(chr(10), ' '):28} edge £{sum(e.values()):>8,}   "
          f"cloud £{sum(c.values()):>8,}")

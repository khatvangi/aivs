#!/usr/bin/env python3
"""
make_aivs_schema.py — draw the AIVS record graph schematic for Figure 1
of var_manuscript_cise.md.

Outputs:
  figures/figure_1_aivs_schema.png   (300 dpi raster, for DOCX inline)
  figures/figure_1_aivs_schema.pdf   (vector, for final submission)

This is a diagram (boxes + arrows + labels), not a statistical plot,
so matplotlib is the appropriate tool here (per project CLAUDE.md the
seaborn/plotly rule applies to plt.plot/bar/scatter/hist statistical
calls, not to ax.add_patch/annotate diagram primitives).
"""

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib.path import Path

FIG_W_IN, FIG_H_IN = 10.0, 5.5
DPI = 300

NODE_W, NODE_H = 1.7, 1.05
BOX_STYLE = "round,pad=0.06,rounding_size=0.15"
EDGE_COL = "#3a3a3a"
NODE_EDGE = "#1a1a1a"
NODE_FILL = "#f4f4f4"
ACCENT_FILL = "#e7f0ff"

nodes = {
    # name : (x_center, y_center, subtitle, fill)
    "Source":      (1.0, 3.5, "data, models,\nliterature",         NODE_FILL),
    "Invocation":  (3.5, 3.5, "tool, model, version,\nprompt, response, operator", ACCENT_FILL),
    "Curation":    (6.0, 3.5, "selection,\naccountable author",    NODE_FILL),
    "Deposition":  (8.5, 3.5, "DOI, repo,\nlicense, version",      NODE_FILL),
    "Evaluation":  (3.5, 1.2, "check type, result,\nverifier, evidence URI", ACCENT_FILL),
}

edges_horiz = [
    ("Source",     "Invocation"),
    ("Invocation", "Curation"),
    ("Curation",   "Deposition"),
]
# vertical: Evaluation attaches to Invocation (bidirectional implied; we draw up-arrow)
edges_vert = [
    ("Evaluation", "Invocation"),
]
# iteration self-loop on Invocation (parent_invocation_id)
ITER_LOOP_NODE = "Invocation"

fig, ax = plt.subplots(figsize=(FIG_W_IN, FIG_H_IN))
ax.set_xlim(0, 10)
ax.set_ylim(0, 5)
ax.set_aspect("equal")
ax.axis("off")

# draw nodes
for name, (cx, cy, sub, fill) in nodes.items():
    box = FancyBboxPatch(
        (cx - NODE_W / 2, cy - NODE_H / 2),
        NODE_W, NODE_H,
        boxstyle=BOX_STYLE,
        linewidth=1.4,
        edgecolor=NODE_EDGE,
        facecolor=fill,
    )
    ax.add_patch(box)
    ax.text(cx, cy + 0.20, name,
            ha="center", va="center", fontsize=13, fontweight="bold", color=NODE_EDGE)
    ax.text(cx, cy - 0.25, sub,
            ha="center", va="center", fontsize=8.0, color="#333333")

def draw_arrow(p_from, p_to, rad=0.0, style="-|>", lw=1.4, color=EDGE_COL):
    arrow = FancyArrowPatch(
        p_from, p_to,
        arrowstyle=style,
        mutation_scale=12,
        connectionstyle=f"arc3,rad={rad}",
        linewidth=lw,
        color=color,
        shrinkA=2, shrinkB=2,
    )
    ax.add_patch(arrow)

# horizontal edges
for a, b in edges_horiz:
    xa, ya, *_ = nodes[a]
    xb, yb, *_ = nodes[b]
    draw_arrow((xa + NODE_W/2, ya), (xb - NODE_W/2, yb))

# vertical edge: Evaluation -> Invocation (up arrow)
xa, ya, *_ = nodes["Evaluation"]
xb, yb, *_ = nodes["Invocation"]
draw_arrow((xa, ya + NODE_H/2), (xb, yb - NODE_H/2))
ax.text(xa + 0.18, (ya + yb) / 2, "attaches to",
        ha="left", va="center", fontsize=8.5, color="#444", style="italic")

# self-loop on Invocation: parent_invocation_id (iteration)
xi, yi, *_ = nodes["Invocation"]
loop_arrow = FancyArrowPatch(
    (xi - NODE_W/2 - 0.05, yi + NODE_H/2 - 0.10),
    (xi - NODE_W/2 - 0.05, yi - NODE_H/2 + 0.10),
    arrowstyle="-|>",
    mutation_scale=11,
    connectionstyle="arc3,rad=-0.9",
    linewidth=1.3,
    color=EDGE_COL,
)
ax.add_patch(loop_arrow)
ax.text(xi - NODE_W/2 - 0.45, yi, "parent_invocation_id\n(iteration)",
        ha="right", va="center", fontsize=8.0, color="#444", style="italic")

# small dashed link Curation -> Evaluation to suggest curation may carry verification refs
xc, yc, *_ = nodes["Curation"]
xe, ye, *_ = nodes["Evaluation"]
link = FancyArrowPatch(
    (xc - NODE_W/2 + 0.05, yc - NODE_H/2 + 0.10),
    (xe + NODE_W/2 - 0.05, ye + NODE_H/2 - 0.10),
    arrowstyle="-",
    linestyle=(0, (3, 3)),
    connectionstyle="arc3,rad=0.20",
    linewidth=1.0,
    color="#888",
)
ax.add_patch(link)

# accountable-author footer band
ax.text(5.0, 0.10,
        "Every record carries an accountable-author identifier.",
        ha="center", va="center", fontsize=9.0, color="#222", style="italic")

# stage labels along the top
stage_y = 4.55
ax.text(1.0, stage_y, "Anchor",   ha="center", va="center", fontsize=9.5, color="#666", fontweight="bold")
ax.text(3.5, stage_y, "Generate", ha="center", va="center", fontsize=9.5, color="#666", fontweight="bold")
ax.text(6.0, stage_y, "Curate",   ha="center", va="center", fontsize=9.5, color="#666", fontweight="bold")
ax.text(8.5, stage_y, "Deposit",  ha="center", va="center", fontsize=9.5, color="#666", fontweight="bold")
ax.text(3.5, 2.20, "Evaluate", ha="center", va="center", fontsize=9.5, color="#666", fontweight="bold")

plt.tight_layout()

out_png = "figures/figure_1_aivs_schema.png"
out_pdf = "figures/figure_1_aivs_schema.pdf"
fig.savefig(out_png, dpi=DPI, bbox_inches="tight", facecolor="white")
fig.savefig(out_pdf, bbox_inches="tight", facecolor="white")
print(f"wrote {out_png}")
print(f"wrote {out_pdf}")

#!/usr/bin/env python3
"""
Figure 1 — the AIVS meta-schema kernel.

outputs:
  figures/figure_1_aivs_schema.png   (400 dpi raster, for DOCX inline)
  figures/figure_1_aivs_schema.pdf   (vector, for final submission)

rewritten 2026-09-08 for the CiSE revision. two changes from the previous
version:

  1. it draws the entities the code actually defines. the previous figure
     showed five record types (Source, Invocation, Evaluation, Curation,
     Deposition) that were never implemented. the kernel in
     src/aivs/meta_schema/core.py is Actor, Event, Evidence, Decision, Claim
     and AuditArtifact, with SourceRef, AdapterUsage and SchemaDelta as
     supporting types. every box and every edge label below names a real
     field on a real model.

  2. all routing is orthogonal and every edge label is drawn on an opaque
     patch. reviewer 5 reported overlapping text in the previous version,
     where a curved self-loop crossed the interior of a node and its label
     landed on top of an unrelated box.

note on plotting library: this is a node-link diagram, not a statistical
plot, so it is drawn with matplotlib patches. seaborn and plotly are the
defaults for data figures in this project; neither has a node-link primitive
and neither is used here.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

DPI = 400

# ── palette ──────────────────────────────────────────────────────────────────
INK = "#1a1a1a"
RULE = "#3d3d3d"
CORE_FILL = "#dce7f7"      # the four-node support chain
SUPPORT_FILL = "#f2f2f2"   # supporting types
CONTAINER = "#8a8a8a"
MUTED = "#5a5a5a"

# ── geometry ─────────────────────────────────────────────────────────────────
# one horizontal support chain at CHAIN_Y; supporting types above and below.
# gaps between chain boxes are wide enough to hold an edge label without it
# reaching either neighbour.
BOX_W, BOX_H, GAP = 2.4, 1.6, 1.8
CHAIN_Y = 5.0
RAIL_Y = 6.6
LOWER_Y = 2.5

chain = ["Event", "Evidence", "Decision", "Claim"]
chain_sub = {
    "Event":    "actor, action,\ntarget, content_hash",
    "Evidence": "event_ids,\ndescription,\nconfidence",
    "Decision": "decision_type,\nevidence_ids,\nverification_status",
    "Claim":    "text, location,\nupstream_\ndecision_ids",
}
# left edge of each chain box
chain_x = {n: 0.9 + i * (BOX_W + GAP) for i, n in enumerate(chain)}
cx = {n: chain_x[n] + BOX_W / 2 for n in chain}          # centres

fig, ax = plt.subplots(figsize=(12.2, 6.8))
ax.set_xlim(0, 16.7)
ax.set_ylim(0.10, 9.05)
ax.axis("off")


def box(x, y, w, h, title, sub, fill, title_size=13, sub_size=8.6):
    """rounded node with a bold title and a field list beneath it."""
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.02,rounding_size=0.16",
        linewidth=1.5, edgecolor=INK, facecolor=fill, zorder=2))
    ax.text(x + w / 2, y + h * 0.68, title, ha="center", va="center",
            fontsize=title_size, fontweight="bold", color=INK, zorder=3)
    ax.text(x + w / 2, y + h * 0.28, sub, ha="center", va="center",
            fontsize=sub_size, color=MUTED, linespacing=1.45, zorder=3)


def arrow(x0, y0, x1, y1, style="-|>", color=RULE, ls="-", lw=1.5):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle=style, color=color,
                                linewidth=lw, linestyle=ls,
                                shrinkA=0, shrinkB=0), zorder=1)


def edge_label(x, y, text, size=8.4, style="italic"):
    """label drawn on an opaque patch so it masks the edge instead of
    colliding with it. this is the fix for the reported overlap."""
    ax.text(x, y, text, ha="center", va="center", fontsize=size,
            style=style, color=MUTED, zorder=4,
            bbox=dict(boxstyle="round,pad=0.22", facecolor="white",
                      edgecolor="none"))


# ── container: AuditArtifact ─────────────────────────────────────────────────
ax.add_patch(FancyBboxPatch(
    (0.25, 1.10), 16.2, 7.40,
    boxstyle="round,pad=0.02,rounding_size=0.2",
    linewidth=1.4, edgecolor=CONTAINER, facecolor="none",
    linestyle=(0, (6, 4)), zorder=0))
ax.text(0.55, 8.24, "AuditArtifact", fontsize=11.5, fontweight="bold",
        color=CONTAINER, ha="left", va="center", zorder=1)
ax.text(0.55, 1.45,
        "audit_target · meta_schema_version · vocabulary_version · "
        "capture_tier_achieved · adapters_used · schema_deltas",
        fontsize=8.2, color=CONTAINER, ha="left", va="center", zorder=1)

# ── the support chain ────────────────────────────────────────────────────────
for n in chain:
    box(chain_x[n], CHAIN_Y - BOX_H / 2, BOX_W, BOX_H, n, chain_sub[n], CORE_FILL)

# forward edges = "supports"; the label names the field that encodes the link
for a, b, lab in [("Event", "Evidence", "event_ids"),
                  ("Evidence", "Decision", "evidence_ids"),
                  ("Decision", "Claim", "upstream_\ndecision_ids")]:
    x0 = chain_x[a] + BOX_W
    x1 = chain_x[b]
    arrow(x0 + 0.05, CHAIN_Y, x1 - 0.05, CHAIN_Y)
    edge_label((x0 + x1) / 2, CHAIN_Y + 0.72, lab)

# ── Actor rail (Actor is carried by both Event and Decision) ─────────────────
ACT_W, ACT_H = 2.9, 1.0
ACT_X, ACT_Y = 6.30 - ACT_W / 2, 7.10
box(ACT_X, ACT_Y, ACT_W, ACT_H, "Actor",
    "actor_type, identifier,\nmodel_metadata", SUPPORT_FILL,
    title_size=12, sub_size=8.2)

# orthogonal: drop to rail, run along it, drop into the two nodes that hold it
arrow(6.30, ACT_Y, 6.30, RAIL_Y, style="-")
ax.plot([cx["Event"], cx["Decision"]], [RAIL_Y, RAIL_Y],
        color=RULE, linewidth=1.5, zorder=1)
for n in ("Event", "Decision"):
    arrow(cx[n], RAIL_Y, cx[n], CHAIN_Y + BOX_H / 2 + 0.04)
edge_label(3.90, RAIL_Y, "actor")
edge_label(8.70, RAIL_Y, "actor")

# ── capture provenance, below Event ──────────────────────────────────────────
LOW_W, LOW_H = 3.1, 1.5
box(cx["Event"] - LOW_W / 2, LOWER_Y - LOW_H / 2, LOW_W, LOW_H,
    "SourceRef", "adapter_name, adapter_version,\nraw_location, extracted_at",
    SUPPORT_FILL, title_size=11.5, sub_size=8.0)
arrow(cx["Event"], LOWER_Y + LOW_H / 2 + 0.04,
      cx["Event"], CHAIN_Y - BOX_H / 2 - 0.04)
edge_label(cx["Event"], (LOWER_Y + LOW_H / 2 + CHAIN_Y - BOX_H / 2) / 2,
           "source_ref")

# ── schema growth, below Decision ────────────────────────────────────────────
box(cx["Decision"] - LOW_W / 2, LOWER_Y - LOW_H / 2, LOW_W, LOW_H,
    "SchemaDelta", "proposed_term, proposed_kind,\njustification, status",
    SUPPORT_FILL, title_size=11.5, sub_size=8.0)
arrow(cx["Decision"], CHAIN_Y - BOX_H / 2 - 0.04,
      cx["Decision"], LOWER_Y + LOW_H / 2 + 0.04, ls=(0, (5, 3)))
edge_label(cx["Decision"], (LOWER_Y + LOW_H / 2 + CHAIN_Y - BOX_H / 2) / 2,
           'schema_gap =\n"novel_pattern"')

# ── footer ───────────────────────────────────────────────────────────────────
ax.text(8.35, 0.72,
        "Each entity references the one to its left by id; support flows left to right.",
        ha="center", va="center", fontsize=9.0, style="italic", color=MUTED)
ax.text(8.35, 0.36,
        "Closed at the meta level (these entities and their fields); open at the "
        "vocabulary level (decision_type and action are free strings).",
        ha="center", va="center", fontsize=9.0, style="italic", color=INK)

fig.tight_layout()
out_png = "figures/figure_1_aivs_schema.png"
out_pdf = "figures/figure_1_aivs_schema.pdf"
fig.savefig(out_png, dpi=DPI, bbox_inches="tight", facecolor="white")
fig.savefig(out_pdf, bbox_inches="tight", facecolor="white")
print(f"wrote {out_png}")
print(f"wrote {out_pdf}")

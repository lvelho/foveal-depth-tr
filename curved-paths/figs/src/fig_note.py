"""The figures of the tech note "Real Matching along Curved Paths" (curved-paths/curved.tex), from the records of
visgraf/deep-motion at main 190332a (Code's measurements on the workstation, except the tour's geometry):
  tour_pencils.pdf  the L-tour of demo D5 in plan, with the path N took at each reference (demo5.json), and one
                    reference on the arc with its frames and baselines (drawn from the tour's definition);
  frontier.png      coverage against cells right on the straight path: stage 13a's maps (stage13a.json), stage 12b's
                    confirmed models of N1024 (stage12b.json) and demo D3's model (demo3.json);
  tour_curves.png   coverage and cells right along the tour, demos D2 (demo2.json) and D5 (demo5.json), and the
                    coverage map by sector on the straight path (demo4.json) and the tour (demo5.json).

Drawn in a Claude Science compute cell (Chat sandbox); this file is that cell's code. Its first lines load the
figure-style helpers of the Claude Science plugin; where they are not installed it prints "figure helpers not loaded" and
draws with matplotlib's defaults.
Usage: DM_RUNS=<deep-motion>/docs/runs FIG_OUT=curved-paths/figs python curved-paths/figs/src/fig_note.py
"""
import glob as _glob, os, pathlib
_plugins = os.environ.get("CS_PLUGINS") or (os.environ["CS_WORKDIR"].rpartition("/claude-science-work/")[0] if os.environ.get("CS_WORKDIR") else os.environ.get("HOME", "")) + "/.claude/plugins/synced/*"
try:
    _helper_files = [f for g in ("", "~g*") for f in _glob.glob(_plugins + "/claude-science" + g + "/skills/sci-core-figure-style/kernel.py") if os.path.isfile(f) and os.access(f, os.R_OK) and (_plugins == os.environ.get("CS_PLUGINS") or os.name == "posix" and all(not s.st_mode & (0o22 if s.st_gid else 2) and s.st_uid in (0, os.getuid()) for s in map(os.stat, [f, *list(pathlib.Path(f).parents)[:8]])))]
    exec(pathlib.Path(max(_helper_files, key=os.path.getctime) if len({f.rpartition("/claude-science")[0] for f in _helper_files}) == 1 else "/helpers-not-found").read_text(encoding="utf-8"))
except OSError:
    print("figure helpers not loaded")
    apply_figure_style = lambda **k: None
    set_frame = panel_letter = goodness_arrow = lambda *a, **k: None
    panel_crops = lambda *a, **k: {}
    render_check = lambda *a, **k: dict.fromkeys(("overlaps", "outside", "cut", "small", "on_data"), ())

import json
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

RUNS = pathlib.Path(os.environ.get("DM_RUNS", "../deep-motion/docs/runs"))   # visgraf/deep-motion at main 190332a
OUT = pathlib.Path(os.environ.get("FIG_OUT", "."))
scratch = pathlib.Path(os.environ.get("CS_WORKDIR", ".")).absolute() / ".cache"
scratch.mkdir(parents=True, exist_ok=True)
apply_figure_style(sizes=(9, 8, 7))

# one colour per matcher, as in the diagnosis note
COL = {"perfect": "#0072B2", "B": "#D55E00", "N": "#009E73", "N dark": "#004D38", "grey": "#9A9A9A"}

d5 = json.load(open(RUNS / "dm-issue-35/demo5.json"))
d2 = json.load(open(RUNS / "dm-issue-23/demo2.json"))
d4 = json.load(open(RUNS / "dm-issue-32/demo4.json"))
d3 = json.load(open(RUNS / "dm-issue-29/demo3.json"))
s13 = json.load(open(RUNS / "dm-issue-31/stage13a.json"))
s12b = json.load(open(RUNS / "dm-issue-28/stage12b.json"))


def check(fig, name, final_w=6.2):
    found = render_check(fig, final_width_in=final_w, min_pt=7)
    findings = {k: v for k, v in found.items() if v}
    im = Image.open(name)
    dpi = round(im.info.get("dpi", (0,))[0], 1) or 400
    print(f"{pathlib.Path(name).name}: {round(im.size[0] / dpi, 2)} in wide (target {final_w});",
          f"found {findings}" if findings else "not checked" if () in found.values() else "nothing found")
    return dpi


# ---------------------------------------------------------------- the tour's geometry, in the tour's own frame
# straight 2 m heading +y, then the turn: 0.3 m line, a quarter arc of radius 1 m to the left, 0.3 m line (4.17 m)
R_ARC, S_ARC0 = 1.0, 2.3
S_ARC1 = S_ARC0 + R_ARC * np.pi / 2
S_END = S_ARC1 + 0.3


def pose(s):
    """position (x, y) and heading angle of the tour at arc length s"""
    if s <= S_ARC0:
        return np.array([0.0, s]), np.pi / 2
    if s <= S_ARC1:
        t = (s - S_ARC0) / R_ARC
        return np.array([-R_ARC + R_ARC * np.cos(t), S_ARC0 + R_ARC * np.sin(t)]), np.pi / 2 + t
    p1, _ = pose(S_ARC1)
    return p1 + np.array([-(s - S_ARC1), 0.0]), np.pi


assert abs(S_END - 4.17) < 0.005, S_END
refs = d5["references"]
path_of = {int(k): v["long"] for k, v in d5["n_paths"].items()}

# Methods: tour_pencils.pdf
# 1. The tour of demo D5 is drawn in its own frame from its definition: 2 m straight, then 0.3 m of line, a quarter arc
#    of radius 1 m to the left and 0.3 m of line, looks 1 cm apart.
# 2. References are every 10 looks (s = 0.5 to 3.6 m); each is marked by the path N took on its +/-0.5 m window, as
#    recorded in demo5.json (n_paths).
# 3. Panel b draws, to scale, one reference on the arc (s = 3.0 m) and its ten frames every 0.1 m over +/-0.5 m, with
#    the chord from the reference to each frame: the baseline of that frame's pencil.
fig, (ax, bx) = plt.subplots(1, 2, figsize=(6.2, 3.0), gridspec_kw={"width_ratios": [1.05, 1], "wspace": 0.12})
ss = np.linspace(0, S_END, 800)
P = np.array([pose(s)[0] for s in ss])
ax.plot(P[:, 0], P[:, 1], color="0.25", lw=1.4, zorder=1, solid_capstyle="round")
on_arc = (ss >= S_ARC0) & (ss <= S_ARC1)
ax.plot(P[on_arc, 0], P[on_arc, 1], color="0.25", lw=3.2, alpha=0.35, zorder=1, solid_capstyle="butt")
# one reference's window, on the arc
sw = np.linspace(2.5, 3.5, 100)
W = np.array([pose(s)[0] for s in sw])
ax.plot(W[:, 0], W[:, 1], color=COL["N"], lw=7, alpha=0.22, zorder=0, solid_capstyle="round")
for m in refs:
    p, _ = pose(m / 100)
    filled = path_of[m] == "per-frame"
    ax.scatter(*p, s=18, marker="o", facecolor=COL["N"] if filled else "white", edgecolor=COL["N"], lw=1.0, zorder=3)
ax.scatter(*pose(3.0)[0], s=70, facecolor="none", edgecolor="black", lw=1.0, zorder=4)   # panel b's reference
p0, _ = pose(0.0)
ax.scatter(*p0, s=14, marker="s", color="0.25", zorder=3)
ax.annotate("start", p0, xytext=(8, 0), textcoords="offset points", va="center", fontsize=8)
ax.annotate("the turn's arc,\nradius 1 m", pose(3.3)[0], xytext=(0.20, 3.75), textcoords="data", fontsize=8, ha="left",
            va="center", arrowprops=dict(arrowstyle="-", color="0.4", lw=0.6, shrinkA=2, shrinkB=4))
ax.annotate("one reference's\n±0.5 m window", pose(2.62)[0], xytext=(0.25, 2.25), textcoords="data", fontsize=8,
            ha="left", va="center", color=COL["N dark"],
            arrowprops=dict(arrowstyle="-", color=COL["N dark"], lw=0.6, shrinkA=2, shrinkB=4))
ax.scatter([], [], s=18, facecolor="white", edgecolor=COL["N"], lw=1.0, label="window on one line: N's line path (14)")
ax.scatter([], [], s=18, facecolor=COL["N"], edgecolor=COL["N"], lw=1.0, label="window leaves the line: per-frame path (18)")
ax.legend(loc="lower left", bbox_to_anchor=(-0.02, -0.30), fontsize=8, handletextpad=0.3, borderaxespad=0)
# a 1 m scale bar
ax.plot([-1.3, -0.3], [0.35, 0.35], color="0.25", lw=1.2)
ax.text(-0.8, 0.43, "1 m", ha="center", va="bottom", fontsize=8)
ax.set_aspect("equal")
ax.set_xlim(-1.55, 1.45)
ax.set_ylim(-0.15, 3.95)
ax.axis("off")
ax.set_title("The L-tour of demo D5, in plan", loc="left")
panel_letter(ax, "a", dx=-0.08, dy=1.02)

# panel b: the baselines at one reference on the arc
sr = 3.0
cr, hr = pose(sr)
sk = sr + 0.1 * np.array([k for k in range(-5, 6) if k != 0])
ck = np.array([pose(s)[0] for s in sk])
sa = np.linspace(2.47, 3.58, 200)
A = np.array([pose(s)[0] for s in sa])
bx.plot(A[:, 0], A[:, 1], color="0.25", lw=1.4, zorder=1)
tang = np.array([np.cos(hr), np.sin(hr)])
bx.plot(*np.stack([cr - 0.62 * tang, cr + 0.45 * tang]).T, color="0.45", lw=0.9, ls=(0, (4, 3)), zorder=1)
for s, c in zip(sk, ck):
    bx.plot([cr[0], c[0]], [cr[1], c[1]], color=COL["N"], lw=0.9, alpha=0.9, zorder=2)
bx.scatter(ck[:, 0], ck[:, 1], s=12, color=COL["N"], zorder=3)
bx.scatter(*cr, s=26, color="black", zorder=4)
bx.annotate("", cr + 0.30 * tang, xytext=cr, arrowprops=dict(arrowstyle="-|>", color="black", lw=1.1, mutation_scale=9))
# the largest turn of a baseline, to the frame 0.5 m ahead
ang = np.degrees(np.arctan2(*(ck[-1] - cr)[::-1]) - hr)
bx.text(*(cr + 0.33 * tang + np.array([0.02, 0.045])), "$h$", fontsize=9, ha="left", va="bottom")
bx.annotate("reference $c_r$", cr, xytext=(cr[0] + 0.17, cr[1] - 0.13), fontsize=8, ha="left", va="center",
            arrowprops=dict(arrowstyle="-", color="0.3", lw=0.6, shrinkA=1, shrinkB=4))
bx.annotate("frame $c_k$, 0.5 m ahead", ck[-1], xytext=(ck[-1][0] - 0.10, ck[-1][1] + 0.17), fontsize=8, ha="left",
            va="center", arrowprops=dict(arrowstyle="-", color="0.3", lw=0.6, shrinkA=1, shrinkB=3))
mid = 0.5 * (cr + ck[-1])
bx.annotate(f"its baseline $e_k$:\n{abs(ang):.0f}° off $h$", mid, xytext=(-0.60, 2.70), fontsize=8,
            ha="center", va="center", color=COL["N dark"],
            arrowprops=dict(arrowstyle="-", color=COL["N dark"], lw=0.6, shrinkA=1, shrinkB=2))
bx.text(*(cr - 0.62 * tang + np.array([0.0, -0.06])), "the heading's line", fontsize=8, color="0.35", ha="center",
        va="top")
bx.set_aspect("equal")
bx.set_xlim(-0.82, 0.34)
bx.set_ylim(2.30, 3.46)
bx.axis("off")
bx.set_title("One pencil per frame, about its baseline", loc="left")
panel_letter(bx, "b", dx=-0.08, dy=1.02)
fig.savefig(OUT / "tour_pencils.pdf")
fig.savefig(scratch / "tour_pencils.png")
check(fig, str(scratch / "tour_pencils.png"))
plt.close(fig)
print("baseline turn at 0.5 m on the arc (deg):", round(abs(ang), 2), "= half the arc:", round(np.degrees(0.5 / 2 / R_ARC), 2))

# ---------------------------------------------------------------- the frontier on the straight path
# Methods: frontier.png
# 1. Every point is a map of N's estimates on the Classroom's straight path (12 references), fused into 2 cm cells and
#    judged by stage 9's metric: cells right (within +/-10 % of the true range) against coverage of the surface.
# 2. Grey points are stage 13a's 48 coverage-first maps (6 anchor sources x 2 ray sets x 4 truth-free filters);
#    filled for rays 1-179 deg, open for rays 1-120 deg; outlined, the most covering map at each floor.
# 3. Green lines are stage 12b's errors-first models of N1024 (rays 1-179): cells confirmed by a second reference at
#    least 0, 0.2, 0.5, 0.8 or 1.0 m away, in the same cell or within 2 cm.
# 4. The star is demo D3's model (within 2 cm, 1.0 m, rays 1-120); dotted lines mark the 95, 97 and 98 % floors and the
#    dashed line S2's 99.5 % gate.
fig, ax = plt.subplots(figsize=(6.2, 3.3))
for src, by_rays in s13["sources"].items():
    for rays, by_f in by_rays.items():
        for filt, o in by_f.items():
            ax.scatter(100 * o["right"], 100 * o["coverage"], s=16, lw=0.8, zorder=2,
                       facecolor=COL["grey"] if rays == "1-179" else "white", edgecolor=COL["grey"])
for fl, o in s13["frontier"].items():
    x, y = 100 * o["right"], 100 * o["coverage"]
    ax.scatter(x, y, s=34, facecolor="none", edgecolor="black", lw=1.0, zorder=4)
lab_front = {"0.98": ("most at\n≥ 98 %", (98.75, 28.0)),
             "0.97": ("D4's map (P-D8)", (97.35, 31.5)),
             "0.95": ("most at ≥ 95 %", (94.3, 35.0))}
for fl, (lab, xy) in lab_front.items():
    o = s13["frontier"][fl]
    ax.annotate(lab, (100 * o["right"], 100 * o["coverage"]), xytext=xy, fontsize=8, ha="left", va="center",
                arrowprops=dict(arrowstyle="-", color="black", lw=0.6, shrinkA=1, shrinkB=4))
rules = s12b["bands"]["full"]["N1024"]["rules"]
for rule, ls in (("same cell", "-"), ("within 2 cm", (0, (4, 2)))):
    sp = rules[rule]["spans"]
    keys = sorted(sp, key=float)
    xs = [100 * sp[k]["model"]["right"] for k in keys]
    ys = [100 * sp[k]["model"]["coverage"] for k in keys]
    ax.plot(xs, ys, color=COL["N"], ls=ls, lw=1.2, marker="o", ms=3.5, mfc="white", mew=1.0, zorder=3)
    print(rule, [(k, round(x, 2), round(y, 1)) for k, x, y in zip(keys, xs, ys)])
sc, wc = rules["same cell"]["spans"], rules["within 2 cm"]["spans"]
k0, k1 = sorted(sc, key=float)[0], sorted(sc, key=float)[-1]
ax.annotate("confirmed in the same cell", (100 * sc[k0]["model"]["right"], 100 * sc[k0]["model"]["coverage"]),
            xytext=(96.6, 7.0), fontsize=8, color=COL["N dark"], ha="right", va="center",
            arrowprops=dict(arrowstyle="-", color=COL["N dark"], lw=0.6, shrinkA=1, shrinkB=3))
ax.annotate("confirmed within 2 cm", (100 * wc[k0]["model"]["right"], 100 * wc[k0]["model"]["coverage"]),
            xytext=(96.6, 18.6), fontsize=8, color=COL["N dark"], ha="right", va="center",
            arrowprops=dict(arrowstyle="-", color=COL["N dark"], lw=0.6, shrinkA=1, shrinkB=3))
m3 = d3["end"]["model"]
ax.scatter(100 * m3["right"], 100 * m3["coverage"], marker="*", s=90, color=COL["N dark"], zorder=5)
ax.annotate("D3's\nmodel", (100 * m3["right"], 100 * m3["coverage"]), xytext=(100.42, 11.0), fontsize=8,
            color=COL["N dark"], ha="center", va="center",
            arrowprops=dict(arrowstyle="-", color=COL["N dark"], lw=0.6, shrinkA=1, shrinkB=5))
# every map past 99 % right: its largest coverage (the title's claim)
past99 = [100 * o["coverage"] for by_rays in s13["sources"].values() for by_f in by_rays.values()
          for o in by_f.values() if o["right"] > 0.99]
past99 += [100 * sp["model"]["coverage"] for r in rules.values() for sp in r["spans"].values()
           if sp["model"]["right"] > 0.99] + [100 * m3["coverage"]]
print("largest coverage of any map past 99 % right:", round(max(past99), 2))
for fl in (95, 97, 98):
    ax.axvline(fl, color="0.55", lw=0.7, ls=":", zorder=1)
ax.axvline(99.5, color="0.35", lw=0.8, ls="--", zorder=1)
ax.text(99.5, 37.0, "S2's gate", fontsize=7, ha="center", va="bottom", color="0.3")
for fl in (95, 97, 98):
    ax.text(fl, 37.0, f"{fl} %", fontsize=7, ha="center", va="bottom", color="0.45")
ax.scatter([], [], s=16, facecolor=COL["grey"], edgecolor=COL["grey"], label="coverage-first maps, rays 1–179°")
ax.scatter([], [], s=16, facecolor="white", edgecolor=COL["grey"], label="coverage-first maps, rays 1–120°")
ax.legend(loc="lower left", fontsize=8, handletextpad=0.2)
ax.set_xlim(90.6, 100.95)
ax.set_xticks([92, 94, 96, 98, 100])
ax.set_ylim(-1.0, 37.0)
ax.set_xlabel("fused cells right (%)")
ax.set_ylabel("coverage of the surface (%)")
ax.set_title("Past 99 % right, no map of N covers 9 % of the straight path's surface", loc="left", pad=14)
fig.savefig(OUT / "frontier.png")
check(fig, str(OUT / "frontier.png"))
plt.close(fig)

# ---------------------------------------------------------------- along the tour, and by sector
# Methods: tour_curves.png
# 1. Panels a and b follow demo D2 (perfect matcher; B + H on 128-spp renders) and demo D5 (N's coverage map on the
#    1024-spp renders) look by look along the same 418-look L-tour, both judged by stage 9's metric.
# 2. A reference's cells join the maps once its window is complete, 0.5 m after it; cells right is drawn once a map
#    holds cells.
# 3. Panel c gives the coverage map's fused cells right by stage 9's sector of the angle from the heading (from each
#    cell's dominant reference), on the straight path (demo D4) and on the tour (demo D5), both from S2's gate report.
fig = plt.figure(figsize=(6.2, 4.7))
gs = fig.add_gridspec(2, 2, height_ratios=[1.0, 0.95], hspace=0.62, wspace=0.42)
ax, bx, cx = fig.add_subplot(gs[0, 0]), fig.add_subplot(gs[0, 1]), fig.add_subplot(gs[1, :])
series = [("perfect matcher", d2["progress"], "perfect", COL["perfect"]),
          ("B + H (D2)", d2["progress"], "real", COL["B"]),
          ("N's map (D5)", d5["progress"], "real", COL["N"])]
for axx in (ax, bx):
    axx.axvspan(S_ARC0, S_ARC1, color="0.92", zorder=0, lw=0)
for lab, prog, key, c in series:
    s = np.array([p[0] for p in prog])
    cov = np.array([100 * p[1][key][0] for p in prog])
    rt = np.array([np.nan if p[1][key][1] is None else 100 * p[1][key][1] for p in prog])
    ax.plot(s, cov, color=c, lw=1.3, drawstyle="steps-post")
    bx.plot(s, rt, color=c, lw=1.3, drawstyle="steps-post", label=lab)
    print(lab, "end coverage", round(cov[-1], 2), "end right", round(rt[-1], 3))
bx.legend(loc="center right", bbox_to_anchor=(1.0, 0.5), fontsize=8, handlelength=1.4, borderaxespad=0.2)
ax.text(0.5 * (S_ARC0 + S_ARC1), 46, "arc", fontsize=7, color="0.4", ha="center", va="bottom")
bx.text(0.5 * (S_ARC0 + S_ARC1), 77, "arc", fontsize=7, color="0.4", ha="center", va="center")
ax.set_xlim(0, 4.25)
ax.set_ylim(-2, 100)
ax.set_xlabel("metres along the tour")
ax.set_ylabel("coverage (%)")
ax.set_title("N's map: near B + H's coverage", loc="left")
bx.set_xlim(0, 4.25)
bx.set_ylim(68, 102)
bx.set_xlabel("metres along the tour")
bx.set_ylabel("cells right (%)")
bx.set_title("at 97.7 % right, against 73.6 %", loc="left")
panel_letter(ax, "a", dx=-0.25, dy=1.06)
panel_letter(bx, "b", dx=-0.25, dy=1.06)
# panel c: by sector
names = ["overall", "0-15", "15-60", "60-120", "120-165", "165-180"]
ticks = ["all", "0–15°", "15–60°", "60–120°", "120–165°", "165–180°"]
p4 = d4["end"]["gate"]["parts"]
p5 = d5["validation"]["by_sector"]["parts"]
xs = np.arange(len(names))
v4 = [100 * p4[n]["right"] for n in names]
v5 = [100 * p5[n]["right"] for n in names]
cx.axhline(97, color="0.55", lw=0.7, ls=":", zorder=1)
cx.axhline(99.5, color="0.35", lw=0.8, ls="--", zorder=1)
cx.text(-0.45, 97.08, "97 % floor (P-D8)", fontsize=7, color="0.4", ha="left", va="bottom")
cx.text(-0.45, 99.58, "S2's gate", fontsize=7, color="0.3", ha="left", va="bottom")
for x, a, b in zip(xs, v4, v5):
    cx.plot([x - 0.12, x + 0.12], [a, b], color="0.75", lw=0.8, zorder=2)
cx.scatter(xs - 0.12, v4, s=30, marker="s", facecolor="white", edgecolor=COL["N"], lw=1.2, zorder=3,
           label="the straight path (D4)")
cx.scatter(xs + 0.12, v5, s=30, marker="o", facecolor=COL["N"], edgecolor=COL["N"], lw=1.2, zorder=3,
           label="the L-tour (D5)")
cx.set_xticks(xs, ticks)
cx.set_xlim(-0.5, len(names) - 0.4)
cx.set_ylim(95.1, 100.0)
cx.set_ylabel("fused cells right (%)")
cx.set_xlabel("angle of the cell's ray from the heading")
cx.set_title("N's map by direction: the sides stay under the floor on both paths", loc="left")
cx.legend(loc="lower left", ncol=2, fontsize=8, handletextpad=0.2, borderaxespad=0.3)
panel_letter(cx, "c", dx=-0.11, dy=1.06)
fig.savefig(OUT / "tour_curves.png")
check(fig, str(OUT / "tour_curves.png"))
plt.close(fig)
print("D4 by sector", [round(v, 2) for v in v4])
print("D5 by sector", [round(v, 2) for v in v5])

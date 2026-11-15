"""Figure 1 (geometry), drawn from the formulas only: python figs/src/geometry.py figs/geometry.pdf

(a) The flow on the foveated raster for one step t = 0.099 m toward a fronto-parallel wall at 3 m: every point of the
    wall has the same axial inverse depth zeta = 1/3, so in q = ln tan e every point moves by the same
    d = -ln(1 - t zeta); on the raster (radius rho(e) = E2 ln(1 + e/E2), the Foveated sensor's spacing
    s(e) = s0 (1 + e/E2)), the same d is fewer pixels near the centre. Arrows magnified x40.
(b) d_k(zeta) = -ln(1 - t_k zeta) for the ten frames of the two-sided window (t_k = k x 0.099 m, k = -5..-1, 1..5),
    in native px at 20 deg eccentricity (34 px per unit q there, as noted in foveal-motion's periodic fixture).
"""
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

E2, EMAX = 2.0, 45.0
STEP = 0.0989565
plt.rcParams.update({"font.size": 9, "axes.titlesize": 9, "font.family": "serif"})
fig, ax = plt.subplots(1, 2, figsize=(7.2, 3.3), gridspec_kw={"width_ratios": [1, 1.25]})

rho = lambda e: E2 * np.log1p(e / E2)
R = rho(EMAX)
a = ax[0]
for e in (2, 5, 10, 20, 45):
    th = np.linspace(0, 2 * np.pi, 361)
    a.plot(rho(e) / R * np.cos(th), rho(e) / R * np.sin(th), color="0.75", lw=0.6)
    a.text(rho(e) / R * np.cos(np.radians(62)), rho(e) / R * np.sin(np.radians(62)), f"{e}°", fontsize=7, color="0.45")
zeta, t = 1 / 3.0, STEP
d = -np.log1p(-t * zeta)
for e in (1, 3, 6, 10, 15, 22, 30, 38):
    q = np.log(np.tan(np.radians(e)))
    e2 = np.degrees(np.arctan(np.exp(q + d)))
    for ph in np.radians(np.arange(0, 360, 30) + (15 if e in (3, 10, 22, 38) else 0)):
        r0, r1 = rho(e) / R, rho(e) / R + 40 * (rho(e2) - rho(e)) / R
        a.annotate("", xy=(r1 * np.cos(ph), r1 * np.sin(ph)), xytext=(r0 * np.cos(ph), r0 * np.sin(ph)),
                   arrowprops=dict(arrowstyle="-|>", lw=0.9, color="C3", mutation_scale=5))
a.plot([0], [0], "+", color="k", ms=8)
a.set_aspect("equal")
a.set_xlim(-1.08, 1.08)
a.set_ylim(-1.08, 1.08)
a.axis("off")
a.set_title("(a) one step toward a wall at 3 m:\nthe same $d$ in $q$ everywhere (arrows ×40)")

b = ax[1]
g = 34.0
zz = np.linspace(0, 1.0, 400)
cm = plt.get_cmap("coolwarm")
for k in [k for k in range(-5, 6) if k]:
    tk = k * STEP
    with np.errstate(invalid="ignore", divide="ignore"):
        dk = np.where(tk * zz < 0.98, -np.log1p(-tk * zz), np.nan)
    b.plot(zz, g * dk, color=cm(0.5 + 0.5 * k / 5), lw=1.1 if abs(k) == 5 else 0.7)
b.axhline(0, color="0.6", lw=0.5)
for z_m, lab in ((5.5, "wall 5.5 m"), (2.0, "card 2 m")):
    b.axvline(1 / z_m, color="0.5", ls=":", lw=0.8)
    b.text(1 / z_m + 0.01, -21, lab, fontsize=7, color="0.35", rotation=90, va="bottom")
b.set_xlabel(r"$\zeta$ = 1 / axial depth (1/m)")
b.set_ylabel("displacement at 20° (native px)")
b.set_ylim(-22, 40)
b.set_xlim(0, 1.0)
b.set_title("(b) $d_k(\\zeta) = -\\ln(1 - t_k\\zeta)$ for $t_k = \\pm$0.1 … $\\pm$0.5 m\n(blue: frames behind, red: ahead)")
fig.tight_layout()
fig.savefig(sys.argv[1])
print("wrote", sys.argv[1], "| d for one step at 3 m:", round(d, 5), "in q;", round(g * d, 3), "px at 20 deg")

# VISGRAF documents: foveal motion and depth from motion

A series of VISGRAF Lab documents (technical notes, reports, user manuals and, later, papers) by Luiz Velho, with
Claude, on depth from a moving observer. Each document has its own folder with its own main file, named after the
document (Overleaf is confused by two files of the same name in the hierarchy), and its own `figs/` (`figs/SOURCES.md`
names each figure's origin); in Overleaf, choose which file is the main document. The first note predates this layout
and stays at the root as `main.tex`.

| document | folder | date | software and records |
|---|---|---|---|
| Foveated Vision on a Moving Head: Depth from Forward Motion (M3–M4) | the root: `main.tex`, `figs/` | 15 Nov 2026 | [visgraf/foveal-motion](https://github.com/visgraf/foveal-motion) |
| Möbius Traces: Depth from Motion along Curved Paths | `moebius-traces/mobius.tex` | 19 Nov 2026 | [visgraf/deep-motion](https://github.com/visgraf/deep-motion) |

Build any of them with `pdflatex` on its main file, twice, in its folder (or `latexmk -pdf`). `techrep-ic.sty` is the VISGRAF
technical-report cover; each folder carries a copy. The report numbers on the covers (`\TRNumber`) are placeholders
to confirm.

## The M3–M4 note (root)

It covers experiments M3 (two-frame log-polar matching) and M4 (multi-baseline log-polar matching) of
visgraf/foveal-motion, issues #5 to #16, and is the sequel to
[lvelho/foveal-motion-tr](https://github.com/lvelho/foveal-motion-tr) (M1–M2). Every number comes from
`docs/motion.md` of visgraf/foveal-motion (on `main` at `24d0bdc`, and on `experiment/m5a-depth-edges` at `8c4f4b8`
for Section 7) or from the records it links.

## Möbius Traces (`moebius-traces/`)

The formulation of visgraf/deep-motion (stages 2 to 5, the demo, and the representation comparisons of #11). Every
number comes from `docs/plan.md` of visgraf/deep-motion (on `main` at `c545ab8`) or from the records it links; the
schematic figures were merged to `main` with PR #13 (`a9fbfc0`). The bibliography was written from memory and should be
checked before the note circulates.

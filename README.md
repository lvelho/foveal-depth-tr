# Foveated Vision on a Moving Head: Depth from Forward Motion

VISGRAF Lab technical note (Luiz Velho, with Claude), 15 November 2026. It covers experiments M3 (two-frame log-polar
matching) and M4 (multi-baseline log-polar matching) of [visgraf/foveal-motion](https://github.com/visgraf/foveal-motion),
issues #5 to #16, and is the sequel to [lvelho/foveal-motion-tr](https://github.com/lvelho/foveal-motion-tr) (M1–M2).

- `main.tex`: the note. Build with `pdflatex main.tex` twice (or Overleaf, pdfLaTeX).
- `techrep-ic.sty`: the VISGRAF technical-report cover, as in `lvelho/foveal-motion-tr`.
- `figs/`: figures copied from the records of visgraf/foveal-motion; `figs/SOURCES.md` names each one's origin, and
  `figs/src/geometry.py` draws Figure 1 from the formulas.
- `main.pdf`: the built note.

Every number in the note comes from `docs/motion.md` of visgraf/foveal-motion (on `main` at `24d0bdc`, and on
`experiment/m5a-depth-edges` at `8c4f4b8` for Section 7) or from the records it links. The report number on the cover
(`\TRNumber` in `main.tex`) is a placeholder to confirm.

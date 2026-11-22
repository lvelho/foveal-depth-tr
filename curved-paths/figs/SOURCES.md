# Figure sources

Every figure comes from the records of [visgraf/deep-motion](https://github.com/visgraf/deep-motion) on `main` at
`190332a` (issues #28 to #35). Figures 1 to 3 are drawn by `src/fig_note.py`, the code of a Claude Science cell in the
Chat sandbox, from records that Code measured on the workstation; figure 2's tour is drawn from its definition and
`demo5.json`. Figures 4 and 5 are copied from D5's record, unedited.

| file | figure | origin |
|---|---|---|
| `frontier.png` | 1 | `src/fig_note.py`, from `docs/runs/dm-issue-31/stage13a.json`, `dm-issue-28/stage12b.json` and `dm-issue-29/demo3.json` (Code, workstation) |
| `tour_pencils.pdf` | 2 | `src/fig_note.py`: the L-tour's geometry (0.3 m line, quarter arc of radius 1 m, 0.3 m line after 2 m straight) and N's path per reference from `docs/runs/dm-issue-35/demo5.json` |
| `tour_curves.png` | 3 | `src/fig_note.py`, from `docs/runs/dm-issue-23/demo2.json`, `dm-issue-35/demo5.json` and `dm-issue-32/demo4.json` (Code, workstation) |
| `d5_last_match.png` | 4 | `docs/runs/dm-issue-35/last_match.png` (`deep/demo5.py`; Code, workstation; `a787480`) |
| `classroom_tour_perfect.png`, `classroom_tour_map.png`, `classroom_tour_all.png` | 5 | `docs/runs/dm-issue-35/` (#25's `ply_view.py` in headless Blender; Code, workstation; `a787480`) |

To redraw figures 1 to 3 from a checkout of deep-motion:
`DM_RUNS=<deep-motion>/docs/runs FIG_OUT=curved-paths/figs python curved-paths/figs/src/fig_note.py`
(matplotlib and Pillow; where the Claude Science plugin's figure helpers are not installed, it draws with matplotlib's
defaults).

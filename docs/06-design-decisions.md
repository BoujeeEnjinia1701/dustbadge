---
doc_id: DBG-DEC-001
title: DustBadge design decisions register
project: DustBadge
doc_type: Design decisions register
version: "0.1"
status: Draft
date: '2026-09-30'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-09-30'
    author: Amish Chadha
    change: Register opened with the open decisions from the review note, the decision records and the build plan work
---

# DustBadge design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

All are proposed, awaiting Amish.

| # | Decision needed | Options | Recommendation | Affects in the build | Source |
| --- | --- | --- | --- | --- | --- |
| 1 | Review the design-for-construction changes P1 to P10 (shell screws and tubes, gasket, port seals, screen, stop ribs, module placement, board size, cell ribs, clip screws, light pipe) | Accept; or change any of them | Accept: they keep what the badge does, its size and its cost | The whole build plan | DBG-DDR-003, Table 1 |
| 2 | Cell swelling allowance: 0.7 mm of free depth (about 6 % of the cell's thickness) in the lithium-cell safety case | (a) accept for the prototype, inspect at each charge and retire at the first swelling; (b) deepen the badge 1 mm and add a foam pad (about 1.5 g more, R9 no longer met) | (a), revisited at TRL 4 with the bought cell's datasheet | Safety stops S1 and S7; rear shell depth | DBG-DDR-003, A1 |
| 3 | On and off: the concept has no switch | (a) firmware only: the boost switched off through its enable input, the controller asleep, waking on USB power; (b) a reed switch inside with a magnet outside; (c) a sealed push button (a new opening) | (a): no change to the shell | Wiring (the enable line is already wired) | DBG-DDR-003, A2 |
| 4 | Mass margin for R9: 0.1 g on catalogue masses | (a) accept, weigh the prototype at TRL 4; (b) look for mass now, for example a 1.8 mm rear wall | (a) | First check "mass and size" | DBG-DDR-003, A3; DBG-CAL-001 [J2] |
| 5 | First co-design partner (worker organization, NGO or university hygiene group) | Partner to be named | None given | Not part of the TRL 3 build; needed for field trials | DBG-DDR-001, O1 |
| 6 | How a site silica fraction is obtained where no laboratory is near | Partner laboratory, field infrared method, or other | None given | Not part of the TRL 3 build; needed before silica estimates are shown | DBG-DDR-001, O2 |
| 7 | Clear front window over the sensor, shown in the product renders only | (a) renders only, decide at TRL 4; (b) adopt, adding a sealed joint that bears on R10 | (a) | None now; front shell if adopted | REVIEW 2026-09-26, item 1 |
| 8 | Visible sensor fan in the renders (illustrative; the real sensor encloses its fan) | Keep and caption as illustrative; or remove | Keep, captioned | None | REVIEW 2026-09-26, item 2 |
| 9 | Side grip ribs in the renders stand 0.6 mm proud (65.2 mm wide) | Accept for appearance; or recess them to keep 64 mm | Recess them if adopted | Front shell, if adopted | REVIEW 2026-09-26, item 4 |
| 10 | Lanyard with a breakaway buckle, shown in the renders, has no BOM line | Add an optional line (about $1) at TRL 4; or leave out | Add at TRL 4, within the approved budget | None now | REVIEW 2026-09-26, item 5 |

## To confirm when parts are bought

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | The cell, including its protection board, is no larger than 50 x 34 x 11.5 mm, its lead leaves at one short side, and its plug polarity matches the charger | The cell ribs, the 0.7 mm swelling allowance and the board notch are sized for it | DBG-DDR-003, P8 |
| 2 | The charger module is no larger than 11 x 19 mm with its USB-C on a short edge, and its temperature window is 0 to 45 °C | It must fit beside the sensor with its USB-C in the opening, and the charge stop is part of the safety case | DBG-DDR-003, P6 |
| 3 | The boost module (11.4 x 9 mm or less, with an enable input) and the humidity breakout (10 x 10 mm or less, sensor at one edge) | They are taped into a strip 17 mm wide beside the sensor; the humidity sensor must sit over its vent | DBG-DDR-003, P6 |
| 4 | Where the particle sensor's cable leaves it, and the cable length | The model leaves room above and beside the sensor between the stop ribs; a connector on another face would need the ribs moved | DBG-DDR-003, P5 |
| 5 | The spring clip's base leaf is flat and wide enough for two holes 12 mm apart | The clip is held by two M2 x 8 screws | DBG-DDR-003, P9 |
| 6 | The pilot hole for the M2 thread-forming screws in PETG (1.7 mm assumed), from the screw maker's data | Too large a hole strips; too small cracks the boss | DBG-DDR-003, P1 |

## Decisions made

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-09-25 | TRL 2 review items D1 to D7: SPS30-class sensor, silica shown only as a labeled estimate, US OSHA and MSHA default limits, continuous sampling, worker-owned data, surface quarries and stone fabrication first, downward screened inlet with a yellow shell and clip | Amish: "i accept all your recommendations, go with them across all repos." | DBG-DDR-001, DBG-DDR-002 |
| 2026-09-25 | D8 to D11: 2,000 mAh cell; R3 reference rule (4.2 L/min cyclone over two shifts at low-dust, high-silica sites); sun use rule; R2 restated to 1 mg/m³ with an over-range flag | Amish, same instruction | DBG-DDR-002 |
| 2026-09-26 | Budget set to $91 to cover the priced BOM (O3) | Amish: "i approve all the budget items." | DBG-DDR-002 v0.2 |

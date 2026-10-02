---
doc_id: DBG-DEC-001
title: DustBadge design decisions register
project: DustBadge
doc_type: Design decisions register
version: "0.4"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-09-30'
    author: Amish Chadha
    change: Register opened with the open decisions from the review note, the decision records and the build plan work
  - version: "0.2"
    date: '2026-10-01'
    author: Amish Chadha
    change: Budget treated as a value-engineering target
  - version: "0.3"
    date: '2026-10-01'
    author: Amish Chadha
    change: Dr. Geeti Chadha added as a contributor and the project moved to the BioMedical (healthcare) area (decided by Amish)
  - version: "0.4"
    date: '2026-10-02'
    author: Amish Chadha
    change: 'Amish approved the recommendations for all ten open decisions (2026-10-02); DBG-DDR-003 accepted; moved to decisions made'
---

# DustBadge design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

None. All open decisions were decided on 2026-10-02.

## To confirm when parts are bought

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | The cell, including its protection board, is no larger than 50 x 34 x 11.5 mm, its lead leaves at one short side, and its plug polarity matches the charger | The cell ribs, the 0.7 mm swelling allowance and the board notch are sized for it | DBG-DDR-003, P8 |
| 2 | The charger module is no larger than 11 x 19 mm with its USB-C on a short edge, and its temperature window is 0 to 45 °C | It must fit beside the sensor with its USB-C in the opening, and the charge stop is part of the safety case | DBG-DDR-003, P6 |
| 3 | The boost module (11.4 x 9 mm or less, with an enable input) and the humidity breakout (10 x 10 mm or less, sensor at one edge) | They are taped into a strip 17 mm wide beside the sensor; the humidity sensor must sit over its vent | DBG-DDR-003, P6 |
| 4 | Where the particle sensor's cable leaves it, and the cable length | The model leaves room above and beside the sensor between the stop ribs; a connector on another face would need the ribs moved | DBG-DDR-003, P5 |
| 5 | The spring clip's base leaf is flat and wide enough for two holes 12 mm apart | The clip is held by two M2 x 8 screws | DBG-DDR-003, P9 |
| 6 | The pilot hole for the M2 thread-forming screws in PETG (1.7 mm assumed), from the screw maker's data | Too large a hole strips; too small cracks the boss | DBG-DDR-003, P1 |

## Value engineering

Value-engineering target: USD 91 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 91.00 (USD 0.00 over or under the target, so on the target with no margin). The estimate rests on indicative prices.

Main cost drivers: the optical particle sensor (USD 48.00, 53 % of the cost), the 2,000 mAh LiPo cell (USD 13.00; it added USD 3), the controller and BLE module (USD 10.00) and the carrier board (USD 9.00).

Savings worth trying: confirming prices when parts are bought. A 1,500 mAh cell would save USD 3 but returns R7 (a full shift) to at risk. The optional breakaway lanyard (decided on 2026-10-02 for TRL 4) would take the estimate about USD 1 over the target, and the foam pad and deeper rear shell decided for any worn badge would add a little more.

## Decisions made

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-09-25 | TRL 2 review items D1 to D7: SPS30-class sensor, silica shown only as a labeled estimate, US OSHA and MSHA default limits, continuous sampling, worker-owned data, surface quarries and stone fabrication first, downward screened inlet with a yellow shell and clip | Amish: "i accept all your recommendations, go with them across all repos." | DBG-DDR-001, DBG-DDR-002 |
| 2026-09-25 | D8 to D11: 2,000 mAh cell; R3 reference rule (4.2 L/min cyclone over two shifts at low-dust, high-silica sites); sun use rule; R2 restated to 1 mg/m³ with an over-range flag | Amish, same instruction | DBG-DDR-002 |
| 2026-09-26 | Value-engineering target set to $91 to match the priced BOM (O3) | Amish: "i approve all the budget items." | DBG-DDR-002 v0.2 |
| 2026-10-01 | Dr. Geeti Chadha added as a contributor (CONTRIBUTORS.md, README Credits) and the project moved to the BioMedical (healthcare) area, with soft, non-clinical wording: a research and educational prototype, not a medical device | Amish: "yes add Dr. Geeti Chadha to breathebox and dustbadge and make those both healthcare projects" | `project.yaml`, `CONTRIBUTORS.md`, `README.md`, DBG-PRB-001 v0.7, DBG-PRC-001 v0.8 |
| 2026-10-02 | Design for construction accepted: P1 to P10 as made; the TRL 4 drop test also checks that the boost module, humidity board and motor stay on their foam tape | Amish: "i approve your recommendations for all 555 open decisions." | DBG-DDR-003, Table 1 |
| 2026-10-02 | Cell swelling: the 0.7 mm allowance (a) is accepted only for bench work with nobody wearing the badge; before anyone wears it, (b): the badge is deepened 1 mm with a foam pad behind the cell and R9 is relaxed to 122 g. Return to (a) only if the bought cell's datasheet states swelling under about 6 % | Amish: "i approve your recommendations for all 555 open decisions." | DBG-DDR-003, A1 |
| 2026-10-02 | On and off: firmware only (the boost switched off through its enable input, the controller asleep, waking on USB power), with a firmware low-voltage cutoff set above the cell protection threshold so the cell is never run down to the protection cut-out | Amish: "i approve your recommendations for all 555 open decisions." | DBG-DDR-003, A2 |
| 2026-10-02 | R9 mass margin: accepted, the prototype is weighed at TRL 4; with the deeper shell of the swelling decision the R9 limit is 122 g | Amish: "i approve your recommendations for all 555 open decisions." | DBG-DDR-003, A3; DBG-CAL-001 [J2] |
| 2026-10-02 | First co-design partner: a university industrial hygiene group that already samples respirable crystalline silica, for example one linked to a NIOSH Education and Research Center, working with a stone fabrication shop or surface quarry as the site. This is the first candidate type to approach, not an agreed partner | Amish: "i approve your recommendations for all 555 open decisions." | DBG-DDR-001, O1 |
| 2026-10-02 | Site silica fraction: by default two or three cyclone filter samples per site go to an accredited laboratory (X-ray diffraction, as in NIOSH Method 7500), and no silica estimate is shown until a site fraction exists; field infrared analysis is considered later where a partner has the instrument | Amish: "i approve your recommendations for all 555 open decisions." | DBG-DDR-001, O2 |
| 2026-10-02 | Clear front window: renders only; decided at TRL 4 | Amish: "i approve your recommendations for all 555 open decisions." | `docs/REVIEW.md`, 2026-09-26, item 1 |
| 2026-10-02 | Sensor fan in the renders: kept, with a caption saying it is illustrative | Amish: "i approve your recommendations for all 555 open decisions." | `docs/REVIEW.md`, 2026-09-26, item 2 |
| 2026-10-02 | Side grip ribs: appearance only; if adopted at TRL 4 they are recessed so the badge stays 64 mm wide | Amish: "i approve your recommendations for all 555 open decisions." | `docs/REVIEW.md`, 2026-09-26, item 4 |
| 2026-10-02 | Lanyard: an optional lanyard line is added at TRL 4, specified as breakaway only | Amish: "i approve your recommendations for all 555 open decisions." | `docs/REVIEW.md`, 2026-09-26, item 5 |

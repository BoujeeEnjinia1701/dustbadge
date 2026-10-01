---
doc_id: DBG-DDR-003
title: DustBadge design for construction
project: DustBadge
doc_type: Design decision record
version: "0.2"
status: Draft
date: '2026-10-01'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-30'
  author: Amish Chadha
  change: Changes that make the concept physically buildable, with the reason for each; made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review
- version: "0.2"
  date: '2026-10-01'
  author: Amish Chadha
  change: Budget treated as a value-engineering target
---

# 0003: Design for construction

- **Date:** 2026-09-30
- **Status:** Draft. The changes in Table 1 were made under Amish's 2026-09-30 instruction to make the design physically buildable; they are open for his review. The questions in Table 3 change the safety case or what the product does and are proposed, awaiting Amish.

## Context

On 2026-09-30 Amish asked for every repo to have an illustrated build plan and wrote: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." The DustBadge model of DBG-DDR-002 showed what the badge does and that it fits its envelope, but it was a massing model: the shells had no closure, several parts floated with nothing holding them, the sensor's air path was open to the inside of the badge, and the carrier board's modules were not placed. Checking the model with build123d (overlaps, contacts and clearances between every pair of parts that meet) found the ten problems below.

The changes keep what the badge does: the same 64 x 52 x 30 mm envelope (33 mm with the clip), the same sensor, cell, controller, downward screened inlet, alert motor and LED, the same charger and humidity sensor, and the same parts cost. Nothing here changes the pitch. Every change is in `cad/src/model.py`, which now runs 43 constructability checks (`python cad/src/model.py --check`): parts that must touch do touch with no overlap, and parts that must not touch are apart by at least the stated clearance. All 43 pass.

## Decision

*Table 1. Changes made to the model, the BOM and the calculations.*

| # | Problem in the concept | Change made | Why this way |
| --- | --- | --- | --- |
| P1 | The shells had no fasteners. The three front bosses stopped 0.2 mm short of the carrier board, and nothing stood between the board and the rear shell 14 mm behind it. | Three tubes 4.5 mm across in the rear shell press the board onto the three front bosses (now ending at the board). Three M2 x 20 thread-forming pan-head screws go in from the rear face, heads in 4.2 mm counterbores 1.4 mm deep, through the tubes and the board into 1.7 mm pilot holes in the front bosses. | One screw path closes the badge, clamps the board and squeezes the gasket. The screws match the product renders' rear screws (REVIEW 2026-09-26, item 3) and are within BOM line 11. Screws from the rear keep the hi-vis front face unbroken. |
| P2 | The TPU gasket of BOM line 9 was not modelled and had no room: the rims met face to face. | A flat printed TPU frame the shape of the rim (64 x 52 outside, 2 mm wide), 1 mm thick when squeezed. The rear shell is 1 mm shallower (13 mm) so the badge stays 30 mm deep. | A flat gasket needs no groove in a 2 mm wall and is printed from the TPU already in line 9. |
| P3 | The sensor's inlet and outlet ports hovered 1 mm above the floor slots, so the fan could draw air from inside the badge and recirculate its own exhaust. | Two printed TPU port seals, 16 x 11 mm with a 9 x 6 mm opening: 0.7 mm thick on the inlet (over the screen), 1.0 mm on the outlet. The sensor rests on both. | The fan now draws only outside air through the screened inlet, which the concept assumed. Different thicknesses keep the sensor level over the screen. |
| P4 | The 1.2 mm inlet screen sat "flush in the slot" with nothing holding it, and BOM line 2 gave a 30 x 8 mm piece. | A 16 x 11 mm square of 0.3 mm mesh laid on the inner floor over the inlet slot, held down by the inlet seal. | The seal both clamps and seals the screen; no adhesive in the air path. |
| P5 | Nothing held the sensor upward: 6 mm of space above it, and it needs 194 to 387 N of retention in a drop [DBG-CAL-001, K1]. | Two stop ribs 1.2 mm thick in the front shell, 20 mm left and 2 mm right of centre, 7 mm deep from the front face, their lower edges 0.2 mm above the sensor. With the seals below and the board behind, the sensor is boxed in. | Ribs print with the shell and leave room for the sensor's cable beside them. |
| P6 | The boost and charger modules and the humidity sensor were not placed; the humidity vent opened under the sensor, where only 1 mm of space was left; the USB-C socket was modelled 3.6 mm long where a receptacle is about 7.3 mm. | The charger module (about 11 x 19 mm, with its USB-C on its lower edge, mouth 0.8 mm inside the face) sits on the board's right-hand strip below the controller. The 5 V boost module, the humidity breakout and the vibration motor are stuck with foam tape to the inside of the front face, in front of the controller, on flying leads. The USB-C opening moves from 16 to 18.1 mm right of centre and grows to 9.6 x 3.8 mm; the humidity vent moves from 8 to 18.5 mm right, 3 mm behind the front face, under the breakout. The controller moves 0.2 mm left to clear the side wall. | The only free space in the 12 mm between the front face and the board is the strip to the right of the sensor; two layers use both its depth and its height. |
| P7 | The 56 x 44 mm board's screw holes broke its edges (centres 1 mm from the edge). | Board 59 x 47 mm with its corners cut 1.5 mm at 45° to clear the shells' inside corners; 1.4 mm of board round each hole; a 3 x 4 mm notch in the right edge for the cell lead. | Uses the 0.5 mm left between the board and the walls; the corner cuts keep it clear of the 2 mm inside radius. |
| P8 | The cell could slide 5 mm sideways and 7 mm up and down behind the board; it needs 280 to 559 N of retention in a drop [K1]. | Four locating ribs 1.2 mm thick and 3 mm tall on the inside of the rear wall, 0.2 mm from the cell's sides, top and bottom. The board stops it coming forward. | Holds the cell without glue, so it can be inspected and replaced. |
| P9 | The spring clip had no fixing to the rear shell, and the cell lies 0.5 mm behind the rear wall, so nothing could pass through the wall over it. | Two M2 x 8 thread-forming screws through the clip's base leaf (two 2.2 mm holes 12 mm apart, drilled if the bought clip has none) into two bosses inside the rear shell, 6 mm each side of centre and 21 mm up, above the cell. | The only place above the cell clear of the shell screws; the bosses double as a stop over the cell. |
| P10 | The light pipe was a plain rod with nothing holding it, and no LED behind it: the board is 10 mm back from the front face. | A printed clear PETG pipe: a 4 mm rod with a 6 mm flange that sits on the inside of the front face, standing 1 mm proud outside, and a 3 mm pocket in its inner end for the red LED on leads. | The flange takes the push from outside; the LED sits where the light pipe needs it. |

*Table 2. Knock-on changes.*

| Item | Change | Reason |
| --- | --- | --- |
| Mass | 119.9 g (was 119.8 g); R9 margin 0.1 g (was 0.2 g) [DBG-CAL-001 v0.5, J2]. The gasket and seals are now taken from the model volume in TPU (0.8 g, was an assumed 1.0 g); the rear tubes are 4.5 mm and the stop ribs 1.2 mm to keep the badge under 120 g. | Bosses, ribs and seals added for construction. |
| Cost | Unchanged at an estimated $91.00, within the $91 value-engineering target. Specifications of BOM lines 2, 6, 7, 9, 10 and 11 updated; no price changed. | The gasket and seals use line 9's TPU; the screws, foam tape and the motor driver parts fall within lines 7 and 11. |
| Drawings | DBG-DWG-001 Rev P4; making sketches DBG-DWG-101 to 108 added. | Follows the model. |
| Documents | DBG-CAL-001 v0.5, DBG-PRC-001 v0.7, DBG-REQ-001 v0.7. No requirement changed status. | Follows the model. |
| Run time, heat, breathing zone | Unchanged: the electrical loads, the envelope and the inlet position are the same. | |

*Table 3. Proposed, awaiting Amish.*

| # | Question | Options | Recommendation |
| --- | --- | --- | --- |
| A1 | Cell swelling allowance. The cell has 0.7 mm of free depth (0.2 mm in front, 0.5 mm behind), about 6 % of its 11.5 mm; pouch cells can swell more as they age. This is part of the lithium-cell safety case. | (a) accept for the prototype, inspect the cell at each charge and retire it at the first visible swelling; (b) deepen the badge by 1 mm and add a foam pad behind the cell (about 1.5 g more, so R9 is no longer met). | (a) for the prototype; revisit at TRL 4 with the bought cell's datasheet. |
| A2 | On and off. The concept has no switch, so the sensor runs until the cell's protection cuts out unless firmware turns it off. | (a) firmware only: the controller switches the boost off through its enable input and sleeps, and wakes on USB power; (b) a reed switch inside with a magnet outside (no new opening); (c) a sealed push button (a new opening in the shell). | (a): no change to the shell; the enable line is already wired. |
| A3 | The R9 mass margin is 0.1 g on catalogue masses. | (a) accept, weigh the prototype at TRL 4; (b) look for mass now (for example a 1.8 mm rear wall). | (a). |

## Consequences

- `design_state: constructable` in `project.yaml`. The build plan DBG-BLD-001 shows every component and step in pictures generated from the model (`cad/src/build_plan_media.py`).
- Requirement status is unchanged: one not met (R14, out of scope), two at risk (R3, R11), one not verifiable at TRL 3 (R10), seven met on paper and four met by design (DBG-CAL-001 v0.5).
- R10 (drop and ingress) is still not verifiable at TRL 3, but the sensor and cell now have a load path and the shell joint has a gasket, so the drop and spray tests at TRL 4 have something to test.
- The photoreal renders (`media/render-*.png`), `media/card.png` and `media/social-preview.png` still show the concept: the USB-C opening and humidity vent have moved, the clip screws are new and the gasket is now a flat 1 mm band. They need regenerating on Amish's Mac, where Blender is. `cad/src/product_model.py` still runs against the new model.
- The bought modules, sensor connector, cell and clip are chosen at TRL 4; their sizes must be checked then (DBG-DEC-001, items to confirm).

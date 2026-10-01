---
doc_id: DBG-REQ-001
title: DustBadge requirements
project: DustBadge
doc_type: Requirements
version: "0.6"
status: Draft
date: '2026-09-30'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: First measurable requirements for TRL 2, with status against the concept
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: "TRL 3, status from DBG-CAL-001 for every requirement; R8 restated for the inlet; R6 defaults follow DBG-DDR-001 D3; R11 and R3 now not met, R10 not verifiable at TRL 3"
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: "Recommendations accepted by Amish (DDR-002): R2 restated to 1 mg/m³ with over-range flag, R3 reference rule, R11 sun use rule; statuses from DBG-CAL-001 v0.2 with the 2,000 mAh cell"
- version: "0.5"
  date: '2026-09-26'
  author: Amish Chadha
  change: Budget approved by Amish; R15 target $91, status Not met to Met on paper
- version: "0.6"
  date: '2026-09-30'
  author: Amish Chadha
  change: "Design made constructable (DBG-DDR-003); R9 mass 119.9 g, 0.1 g margin; no status changed"
---

# DustBadge requirements

These are the requirements for the concept, with their status from the TRL 3 calculations in DBG-CAL-001 v0.2. On 2026-09-25 Amish accepted the review recommendations (DBG-DDR-002): R2 is restated to the sensor's 1 mg/m³ range with an over-range flag, R3 keeps ±25 % but requires a larger reference sample at low-dust, high-silica sites, R11 adds a use rule for full sun, and the cell grows to 2,000 mAh. On 2026-09-26 Amish approved a $91 budget to cover the priced BOM (DBG-DDR-002, O3), so R15 is met. On paper one requirement is not met (R14 intrinsic safety, out of scope), two are at risk (R3 accuracy and R11 site conditions), one cannot be verified at TRL 3 (R10), and eleven are met, seven by calculation and four by design.

Table 1. Requirements and concept status.

| ID | Requirement | Target | Status at TRL 3 (DBG-CAL-001) | Verification (TRL 3 or later) |
| --- | --- | --- | --- | --- |
| R1 | Measure the respirable dust fraction | Mass concentration of particles up to 4 µm (PM4), a proxy for the ISO 7708 respirable convention | Met by design. PM4 is a proxy: for quartz, optical PM4 would include grains up to about 6.5 µm aerodynamic, while the sensor under-sees coarse grains (CAL-001, D) | Datasheet review; later comparison with a cyclone sampler |
| R2 | Cover the working range | 0 to 1 mg/m³ respirable dust; minutes above the range flagged, logged at the range limit and counted toward the projection. Restated from 0 to 5 mg/m³ for the first sectors in D6 (DBG-DDR-002 D11) | Met on paper. The RCS limit lies in range only for silica fractions of 5 % or more; above the range the badge reports only that dust was over range (CAL-001, E) | Calculation of expected site ranges; chamber test on CalRig |
| R3 | Accuracy after site calibration | Shift average within ±25 % of a co-located gravimetric sample. Where respirable dust at the action level is below about 100 µg/m³ (low-dust, high-silica sites such as quartz-rich stone), the reference is a 4.2 L/min cyclone over two shifts (DBG-DDR-002 D9) | **At risk.** Met on paper with a factor per task on the same badge: ±21 % (quarry), ±22 % (quartz-rich stone with the D9 reference). Not met with one factor shared across badges per site: ±29 to ±30 % (CAL-001, F). Error terms assumed | Error budget at TRL 3; later co-located field samples |
| R4 | Estimate silica exposure | RCS estimate = calibrated PM4 mass x site silica fraction, always labeled as an estimate; dust shown alone when no fraction is entered | Met by design | Firmware sketch review |
| R5 | Update often enough to catch tasks | 1 s readings, 1 min logged averages, running 8 h time-weighted average (TWA) updated every minute | Met by design; the sensor gives new readings every second | Firmware sketch review |
| R6 | Warn before a limit is reached | Vibration and LED when the projected 8 h RCS TWA exceeds the action level (default 25 µg/m³) and a repeated alert at the limit (default 50 µg/m³); both configurable | Met by design and on paper: five scenarios alert as intended, one early warning after a single heavy cut (CAL-001, G). Defaults per DBG-DDR-001 D3 | Firmware sketch review |
| R7 | Last a full shift | 12 h of continuous sampling per charge | Met on paper with the 2,000 mAh cell (DBG-DDR-002 D8): 17.7 h at the typical 55 mA and 25 °C; 12.8 h at the 65 mA maximum and 0 °C (CAL-001, A) | Power budget calculation |
| R8 | Wearable in the breathing zone | Inlet worn within 30 cm of the nose and mouth; clip or harness loop | Met on paper: inlet 242 mm from the nose and mouth at a collar or upper-strap mount; a mount more than 269 mm below them fails (CAL-001, I) | Massing model |
| R9 | Light and small | Mass 120 g or less; no larger than 75 x 55 x 35 mm | Met on paper: 119.9 g, a 0.1 g margin with the 2,000 mAh cell and the fixings added for construction (DBG-DDR-003); 64 x 52 x 33 mm with the clip (CAL-001, J) | Massing model, then weighing |
| R10 | Survive the site | Electronics splash and dust protected (IP54 target except the sensor air path); inlet facing down; survives a 1.5 m drop onto concrete | Not verifiable at TRL 3: 750 to 1,500 g deceleration on a 1.5 m drop; gasketed joint untested (CAL-001, K) | Design review; later drop and spray tests |
| R11 | Work in site conditions | 0 to 45 °C, 10 to 90 % RH non-condensing; readings flagged when humidity or spray may bias them. Use rule: worn shaded when the ambient is above 40 °C in full sun (DBG-DDR-002 D10) | **At risk.** Under the use rule the shell stays at or below 57.8 °C, 2.2 K under the sensor's 60 °C limit; without it, about 63 °C in full sun at 45 °C. Sensor best performance only to 40 °C and 80 % RH; humidity flag possible with the RH sensor (CAL-001, C) | Literature and datasheet review |
| R12 | Keep a shift log | At least 30 shifts of 1 min records on the badge; export over Bluetooth Low Energy to the worker's phone | Met on paper: 11.5 kB per 12 h shift, about 182 shifts in 2 MB (CAL-001, H) | Storage calculation |
| R13 | Protect the worker's data | Stored on the badge and the worker's phone; shared with an employer only by the worker's choice | Met by design (DBG-DDR-001 D5) | Design review |
| R14 | Safe in hazardous atmospheres | Certified intrinsically safe for gassy mines and explosive atmospheres | **Not met and out of scope** for this prototype; it must be labeled not for such use | Design review |
| R15 | Low cost and buildable | Parts $91 or less (was $90; DBG-DDR-002 O3); no custom PCB required for the first build | Met on paper: $91.00 with the 2,000 mAh cell (CAL-001, L) | Priced BOM |

## Assumptions

- The respirable convention in ISO 7708 has a 50 % cut near 4 µm aerodynamic diameter; PM4 from an optical sensor is used as a proxy.
- A site silica fraction (the quartz share of respirable dust) is available for each site and task from at least one filter sample analyzed by a laboratory or a field infrared method. How it is obtained where no laboratory is near is still open (DBG-DDR-001, O2).
- The wearer follows the sun use rule in R11; the badge cannot enforce it.
- Default limits follow US OSHA and MSHA (50 µg/m³ limit and 25 µg/m³ action level, 8 h TWA), decided by Amish on 2026-09-25 (DBG-DDR-001 D3, DBG-DDR-002). Other jurisdictions can be configured, for example the EU binding limit of 100 µg/m³.
- The calculation assumptions (sensor figures, cell, error terms, thermal coefficients) are listed in DBG-CAL-001, Table 1.
- Shifts are up to 12 h; the projected TWA is normalized to 8 h as the regulations define it.

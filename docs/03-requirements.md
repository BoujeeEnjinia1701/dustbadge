---
doc_id: DBG-REQ-001
title: DustBadge requirements
project: DustBadge
doc_type: Requirements
version: "0.2"
status: Draft
date: '2026-09-25'
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
---

# DustBadge requirements

These are first-pass requirements for the concept. Targets are proposals for review and will be checked by calculation at TRL 3. Two requirements are not met by the concept as drawn (R2 and R14), and several others are unverified; the status column says which.

Table 1. Requirements and concept status.

| ID | Requirement | Target | Status at TRL 2 (estimate) | Verification (TRL 3 or later) |
| --- | --- | --- | --- | --- |
| R1 | Measure the respirable dust fraction | Mass concentration of particles up to 4 µm (PM4), a proxy for the ISO 7708 respirable convention | Met by design with an SPS30-class sensor; optical sizing is not aerodynamic sizing, so the match is approximate | Datasheet review; later comparison with a cyclone sampler |
| R2 | Cover the working range | 0 to 5 mg/m³ respirable dust without saturating | **Not met.** The proposed sensor is specified to 1 mg/m³; readings above are uncalibrated | Calculation of expected site ranges; chamber test on CalRig |
| R3 | Accuracy after site calibration | Shift average within ±25 % of a co-located gravimetric sample | Unverified; NIOSH reports factory-calibrated optical monitors can differ by up to 10 times without a site factor | Error budget at TRL 3; later co-located field samples |
| R4 | Estimate silica exposure | RCS estimate = calibrated PM4 mass x site silica fraction, always labeled as an estimate; dust shown alone when no fraction is entered | Met by design | Firmware sketch review |
| R5 | Update often enough to catch tasks | 1 s readings, 1 min logged averages, running 8 h time-weighted average (TWA) updated every minute | Met by design | Firmware sketch review |
| R6 | Warn before a limit is reached | Vibration and LED when the projected 8 h RCS TWA exceeds the action level (default 25 µg/m³) and a repeated alert at the limit (default 50 µg/m³); both configurable | Met by design | Firmware sketch review |
| R7 | Last a full shift | 12 h of continuous sampling per charge | At risk: about 13 h typical, about 11 h at the sensor's maximum current | Power budget calculation |
| R8 | Wearable in the breathing zone | Worn within 30 cm of the nose and mouth; clip or harness loop | Met: chest mount about 22 cm below the nose in the massing model | Massing model |
| R9 | Light and small | Mass 120 g or less; no larger than 75 x 55 x 35 mm | Met, thin margin on mass: about 110 g, 64 x 52 x 30 mm | Massing model, then weighing |
| R10 | Survive the site | Electronics splash and dust protected (IP54 target except the sensor air path); inlet facing down; survives a 1.5 m drop onto concrete | Unverified | Design review; later drop and spray tests |
| R11 | Work in site conditions | 0 to 45 °C, 10 to 90 % RH non-condensing; readings flagged when humidity or spray may bias them | Unverified; water mist inflates optical readings | Literature and datasheet review |
| R12 | Keep a shift log | At least 30 shifts of 1 min records on the badge; export over Bluetooth Low Energy to the worker's phone | Met: about 12 kB per 12 h shift | Storage calculation |
| R13 | Protect the worker's data | Stored on the badge and the worker's phone; shared with an employer only by the worker's choice | Met by design | Design review |
| R14 | Safe in hazardous atmospheres | Certified intrinsically safe for gassy mines and explosive atmospheres | **Not met and out of scope** for this prototype; it must be labeled not for such use | Design review |
| R15 | Low cost and buildable | Parts $90 or less; no custom PCB required for the first build | Met: about $85 (indicative); a simple carrier board may be hand-wired on perfboard | Priced BOM |

## Assumptions

- The respirable convention in ISO 7708 has a 50 % cut near 4 µm aerodynamic diameter; PM4 from an optical sensor is used as a proxy.
- A site silica fraction (the quartz share of respirable dust) is available for each site and task from at least one filter sample analyzed by a laboratory or a field infrared method.
- Default limits follow US OSHA and MSHA (50 µg/m³ limit and 25 µg/m³ action level, 8 h TWA). Other jurisdictions can be configured, for example the EU binding limit of 100 µg/m³.
- Shifts are up to 12 h; the projected TWA is normalized to 8 h as the regulations define it.

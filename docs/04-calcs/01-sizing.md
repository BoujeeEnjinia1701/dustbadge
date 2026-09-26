---
doc_id: DBG-CAL-001
title: DustBadge sizing calculations
project: DustBadge
doc_type: Calculation
version: "0.1"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: First issue for TRL 3 (power and run time, charging, badge temperature, PM4 against the respirable convention, range, error budget, alert logic, log, breathing zone, mass, drop, cost)
---

# DustBadge sizing calculations

On paper, DustBadge meets nine of its fifteen requirements (five by calculation, four by design), has one at risk, cannot verify one at TRL 3 and misses four. The misses are the working range (R2: the sensor stops at 1 mg/m³ against a 5 mg/m³ target), accuracy after site calibration (R3: about ±34 % for quartz-rich stone at the action level, because an 8 h filter sample collects only 0.037 mg), operation in full sun at 45 °C (R11: the shell reaches about 63 °C, above the sensor's 60 °C limit) and intrinsic safety (R14, out of scope). Run time (R7) is at risk: 13.3 h at the sensor's typical current, but 11.3 h at its maximum current or at 0 °C. The calculations changed two parts of the TRL 2 concept: a humidity and temperature sensor is added to the carrier board so that R11's flag can work at all, and the charger takes a cell thermistor so that the 0 to 45 °C charging rule is enforced. Both add $3, and the parts now cost $88 against the $90 budget. Every number in this note is printed by `docs/04-calcs/sizing.py`; the tag in brackets, for example [A3], is the line of that script's output that carries it.

> **Safety:** These are first-principles estimates for a paper proof of concept. They do not show that a worker's air is safe, and they are not a substitute for co-located filter sampling, chamber checks or electrical safety checks on the lithium cell. See DBG-PRC-001, Safety.

## Scope and method

The note checks every requirement in DBG-REQ-001 v0.3 against the design in DBG-PRC-001 v0.3 and the parametric model `cad/src/model.py`. The script imports the model's `PARAMS`, derived dimensions and mass breakdown, so the envelope, shell volumes, inlet position and cell space used here are the ones in the STEP files and in drawing DBG-DWG-001. It also reads `bom/bom.csv` and `budget_usd` in `project.yaml`. Run it from the repo root with `python docs/04-calcs/sizing.py`.

The design case is a worker in a surface quarry or a stone fabrication shop on a 12 h shift, badge worn at the collar or on an upper harness strap, ambient 0 to 45 °C, 10 to 90 % RH, US OSHA and MSHA limits by default (decision D3 in DBG-DDR-001).

## Assumptions

*Table 1. Main assumptions.*

| Area | Assumption | Basis |
| --- | --- | --- |
| Particle sensor | 45 to 55 mA typical and 65 mA maximum at 4.5 to 5.5 V; 0 to 1,000 µg/m³; PM4 precision ±25 µg/m³ below 100 µg/m³ and ±25 % from 100 to 1,000 µg/m³; drift 1.25 µg/m³ or 1.25 % per year; best performance at 10 to 40 °C and 20 to 80 % RH; operating -10 to 60 °C and 0 to 95 % RH; new readings every second; 26.3 g | [Sensirion SPS30 datasheet, v2.0, June 2023](https://sensirion.com/media/documents/8600FF88/64A3B8D6/Sensirion_PM_Sensors_Datasheet_SPS30.pdf) |
| Electronics | 5 V boost 85 % efficient; controller, BLE and humidity sensor 3 mA from the cell; vibration motor 80 mA at 3 V, 20 alerts of 2 s per shift | Typical module figures; to confirm by measurement at a later TRL |
| Cell | 1,500 mAh, 3.7 V; 80 % usable; 85 % of capacity at 0 °C; charged at 500 mA | Typical LiPo data |
| Badge temperature | Combined surface coefficient 10 W/(m²·K); solar absorptance of yellow PETG 0.45; 1,000 W/m² on the front face; rear face against the wearer treated as adiabatic | Screening values (assumed) |
| Reference sample | Cyclone at 2.5 L/min for 8 h; weighing and blank uncertainty 0.010 mg per filter; gravimetric method ±10 % | Assumed typical values |
| Error terms | Site factor change between days and tasks ±10 % (factor per task) or ±20 % (per site); position and screen ±10 %; humidity below 80 % RH ±5 %; non-linearity after the site factor ±10 %; badge-to-badge after a CalRig check ±10 % | Assumed; each to be measured |
| Silica fractions | 10 % for a typical quarry, 80 % for quartz-rich engineered stone | Assumed for illustration; a site filter sample sets the real value |

## A. Power and run time (R7)

The cell holds 5.55 Wh, of which 4.44 Wh is usable, and 3.77 Wh at 0 °C [A1]. The motor adds only 2.7 mWh per shift [A2]. The sensor's fan and laser dominate.

*Table 2. Run time by sensor current [A3].*

| Sensor current | Power from the cell | Run time at 25 °C | Run time at 0 °C |
| --- | --- | --- | --- |
| 45 mA (typical, low) | 276 mW | 16.1 h | 13.7 h |
| 55 mA (typical, high) | 335 mW | 13.3 h | 11.3 h |
| 65 mA (maximum) | 393 mW | 11.3 h | 9.6 h |

The 12 h target is met at typical current and room temperature and missed at the maximum current or at 0 °C with the upper typical current. Covering the worst case needs about 1,880 mAh [A4], or about 1,600 mAh at 25 °C [A5]. The model leaves 1.5 mm behind the cell, so a cell up to 11.5 mm thick fits without changing the shells [A6]. A larger cell is proposed in `docs/REVIEW.md`, awaiting Amish, because it adds about 8 g (R9) and about $3 (R15).

## B. Charging

At 500 mA (0.33 C) the cell charges in about 3.4 h, 2.4 h at constant current plus about 1 h of taper [B1], so a badge charged after a shift is ready for the next. The charger module now takes the cell's thermistor so that charging stops outside 0 to 45 °C; at TRL 2 this rule was written but nothing enforced it.

## C. Badge temperature (R11)

In shade the electronics warm the badge by 3.3 K. In full sun on the front face the rise is 17.8 K: the shell reaches about 48 °C at 30 °C ambient and about 63 °C at 45 °C ambient [C1]. The sensor's 60 °C operating limit is therefore passed in full sun above about 42 °C ambient, and its 40 °C best-performance limit above about 22 °C ambient [C2]. The sensor draws outside air through its own path, so the air it measures stays near ambient, but its electronics and the cell sit at shell temperature. R11 is not met in full sun at 45 °C. A lighter shell color or a vented sun hood would help; neither is adopted here.

## D. PM4 against the respirable convention (R1)

The ISO 7708 respirable convention passes half of particles at 4.0 µm aerodynamic diameter [D1]. For quartz (2.65 g/cm³), geometric and aerodynamic diameters differ by a factor of about 1.6: a 2.5 µm grain is 4.1 µm aerodynamic and about half respirable, and a 4 µm grain is 6.5 µm aerodynamic and only 12 % respirable [D2]. An optical PM4 channel would therefore over-include coarse quartz if it sized it correctly. In practice the SPS30 calculates PM4 from the distribution of the particles it detects best, which are fine, so it tends to under-see coarse grains. The two errors act in opposite directions and neither is known for site dust [D3]. PM4 remains the closest available output, so R1 is met by design as a proxy, and the site factor must absorb the difference.

## E. Working range (R2)

The sensor covers 0 to 1,000 µg/m³, 20 % of the 5 mg/m³ target span [E1]. What matters for the alert is where the silica limits fall in dust terms.

*Table 3. Respirable dust at the RCS action level and limit, by silica fraction [E2].*

| Silica fraction | Dust at the 25 µg/m³ action level | Dust at the 50 µg/m³ limit | Limit in range |
| --- | --- | --- | --- |
| 2.5 % | 1,000 µg/m³ | 2,000 µg/m³ | No |
| 5 % | 500 µg/m³ | 1,000 µg/m³ | Yes, at the edge |
| 10 % | 250 µg/m³ | 500 µg/m³ | Yes |
| 30 % | 83 µg/m³ | 167 µg/m³ | Yes |
| 80 % | 31 µg/m³ | 62 µg/m³ | Yes |

For dust with 5 % silica or more the limit lies inside the range, and for 2.5 % or more the action level does [E3]. Above the range, readings are not trustworthy, so the firmware logs an over-range minute at the range limit, flags it and counts it toward the projection at no less than that limit, which makes the badge alert rather than go quiet [E4]. R2 is not met: peaks in quarries and artisanal mines can be far above 1 mg/m³, and the badge will report only that they were over range.

## F. Error budget for the shift average (R3)

A site factor from a co-located filter sample is what turns the optical reading into a respirable dust value. The filter sample itself limits the result at low concentrations: 2.5 L/min for 8 h draws 1.20 m³ of air [F1], so at the action level for quartz-rich stone (31 µg/m³ of dust) the filter collects only 0.037 mg, and a 0.010 mg weighing uncertainty is already 27 %.

*Table 4. Combined uncertainty of the shift average at the action level (root sum of squares) [F2, F3].*

| Case | Dust | Filter mass | Same badge, factor per task | Factor shared across badges, per site |
| --- | --- | --- | --- | --- |
| Quartz-rich stone, 80 % silica | 31 µg/m³ | 0.037 mg | ±34 % | ±39 % |
| Quarry, 10 % silica | 250 µg/m³ | 0.300 mg | ±21 % | ±29 % |
| Quartz-rich stone, 4.2 L/min cyclone over 2 shifts | 31 µg/m³ | 0.126 mg | ±22 % | |

The ±25 % target is met only for the quarry case with the reference taken on the same badge for each task, and for quartz-rich stone only with a larger reference sample [F3]. Without any site factor the PM4 precision alone is ±25 µg/m³, 80 % of the dust level at the action level for quartz-rich stone [F4]. R3 is not met on paper for the general case. Every term except the sensor's own figures is assumed and must be measured.

## G. Silica estimate and alert logic (R4, R5, R6)

The sensor gives new readings every second; the firmware logs 1 min means, multiplies calibrated PM4 by the site silica fraction to give the RCS estimate, and projects the 8 h TWA as the dose so far plus the last 60 min mean rate for the rest of the shift. The projection starts once 60 min of data exist; before that the badge alerts only on the dose so far and on peaks. A brief peak alert fires when a 1 min mean exceeds 250 µg/m³ RCS, ten times the action level [G2]. Five scenarios on an 8 h shift test the logic [G1].

*Table 5. Alert behavior in five scenarios (RCS, µg/m³) [G1].*

| Scenario | 8 h TWA | Action-level alert | Limit alert | Peak alerts | Correct? |
| --- | --- | --- | --- | --- | --- |
| S1 steady 30 all shift | 30.0 | Minute 60 | None | 0 | Yes |
| S2 background 10, 2 min dry cut at 1,000 each hour | 43.0 | Minute 60 | None | 8 | Yes |
| S3 background 15, one 1 min truck pass at 110 | 15.2 | None | None | 0 | Yes, no nuisance alert |
| S4 background 5 | 5.0 | None | None | 0 | Yes |
| S5 background 10, one 2 min dry cut at 1,000 | 14.1 | Minute 60 | None | 1 | Early warning; the shift ends below the action level |

The logic warns before the limit in every case where the shift ends above the action level, and it ignores a passing truck. S5 shows the cost of projecting: a single heavy cut in the first hour projects over the action level although the shift ends at 14 µg/m³. That is acceptable for a warning, since the same cut repeated each hour gives S2, but workers should be told what the alert means. R4, R5 and R6 are met by design; R6 is also met on paper for these scenarios.

## H. Shift log (R12)

At 16 bytes per minute a 12 h shift takes 11.5 kB, and 30 shifts take 346 kB, 16 % of the module's 2 MB flash, so the badge holds about 182 shifts [H1]. At a conservative 2 kB/s a shift transfers to a phone in about 6 s [H2]. R12 is met on paper.

## I. Breathing zone (R8)

With the badge worn 210 mm below and 70 mm to the side of the nose and mouth, the inlet is 242 mm from them [I1]. The badge center may sit up to 269 mm below the nose and mouth before the 300 mm limit is passed [I2], so a collar or upper-strap position meets R8 and a low shirt pocket may not. R8 is met on paper for the stated mount.

## J. Size and mass (R9)

The printed shells weigh 16.5 g and 15.1 g from the model volumes; the sensor (26.3 g) and the cell (30 g) are more than half the badge [J1]. The total is 111.8 g, 8.2 g under the 120 g target, and the envelope is 64 x 52 x 33 mm including the clip against 75 x 55 x 35 mm [J2]. A cell 8 g heavier would leave 0.2 g of margin [J3]. R9 is met on paper.

## K. Drop and ingress (R10)

A 1.5 m drop reaches 5.42 m/s with 1.65 J. If the shell corner crushes 1 to 2 mm, the mean deceleration is 750 to 1,500 g, so the sensor needs 194 to 387 N of retention and the cell 221 to 441 N [K1]. The model holds the sensor between the front shell floor and the carrier board, which rests on three screw bosses; whether PETG bosses and a foam-backed cell survive these loads, and whether the gasketed joint reaches IP54 for the electronics, cannot be shown without a test. R10 is not verifiable at TRL 3.

## L. Cost (R15)

The BOM has 12 lines totaling $88.00 against `budget_usd` of $90, a $2.00 margin; the particle sensor is 55 % of the cost [L1]. R15 is met on paper, with little room for the larger cell in section A.

## M. Results against every requirement

*Table 6. Requirement status from this note.*

| ID | Requirement | Value | Target | Status |
| --- | --- | --- | --- | --- |
| R2 | Cover the working range | 0 to 1,000 µg/m³; limit in range for silica fractions of 5 % or more; over-range flagged and counted | 0 to 5 mg/m³ | **Not met** |
| R3 | Accuracy after site calibration | ±34 % (quartz-rich stone), ±21 to ±29 % (quarry); ±22 % with a larger reference sample | ±25 % of a gravimetric shift average | **Not met** on paper (assumed terms) |
| R11 | Work in site conditions | Shell about 63 °C in full sun at 45 °C; sensor best performance only to 40 °C and 80 % RH; humidity flag now possible | 0 to 45 °C, 10 to 90 % RH, readings flagged | **Not met** in full sun above 42 °C |
| R14 | Safe in hazardous atmospheres | Not intrinsically safe | Certified intrinsically safe | **Not met**, out of scope |
| R7 | Last a full shift | 13.3 h typical at 25 °C; 11.3 h at maximum current or at 0 °C | 12 h continuous | **At risk** |
| R10 | Survive the site | 750 to 1,500 g on a 1.5 m drop; IP54 by gasket, untested | IP54 electronics; 1.5 m drop | Not verifiable at TRL 3 |
| R6 | Warn before a limit is reached | Five scenarios behave as intended; one early warning (S5) | Projected TWA alerts at 25 and 50 µg/m³ | Met on paper |
| R8 | Wearable in the breathing zone | Inlet 242 mm from nose and mouth | 300 mm or less | Met on paper |
| R9 | Light and small | 111.8 g; 64 x 52 x 33 mm | 120 g; 75 x 55 x 35 mm | Met on paper |
| R12 | Keep a shift log | 11.5 kB per shift; 182 shifts; 6 s transfer | 30 shifts; BLE export | Met on paper |
| R15 | Low cost and buildable | $88.00; perfboard carrier | $90; no custom PCB | Met on paper |
| R1 | Measure the respirable fraction | PM4 as proxy; size cut offset in both directions (section D) | PM4 as ISO 7708 proxy | Met by design |
| R4 | Estimate silica exposure | Calibrated PM4 x site fraction, labeled | As stated | Met by design |
| R5 | Update often enough | 1 s readings, 1 min log, TWA every minute | As stated | Met by design |
| R13 | Protect the worker's data | Badge and phone only; sharing by the worker | As stated | Met by design |

Counts: 4 not met, 1 at risk, 1 not verifiable at TRL 3, 5 met on paper, 4 met by design.

## Checks against the TRL 2 figures

*Table 7. TRL 2 claims checked.*

| TRL 2 claim (DBG-PRC-001 v0.2) | This note | Action |
| --- | --- | --- |
| About 335 mW from the cell | 335 mW at 55 mA; 393 mW at 65 mA | Stands |
| About 13 h typical, about 11 h worst case | 13.3 h and 11.3 h; also 11.3 h at 0 °C | Precis updated with the cold case |
| Charge about 3.5 h | 3.4 h | Stands |
| Sensor precision ±5 µg/m³ plus 5 % at the action level for quartz-rich stone | That is the PM2.5 figure; PM4 is ±25 µg/m³ below 100 µg/m³ | Precis corrected |
| Log about 12 kB per shift, 30 shifts about 350 kB | 11.5 kB and 346 kB | Stands |
| About 220 mm from badge to nose | Inlet 242 mm from the nose and mouth midpoint | Precis and requirements updated |
| About 110 g | 111.8 g | Precis updated |
| 64 x 52 x 30 mm | 64 x 52 x 30 mm shells, 33 mm with the clip | Precis updated |
| About $85 | $88.00 with the humidity sensor and thermistor charger | Precis, BOM notes and README updated |
| Badge temperature not estimated | About 63 °C shell in full sun at 45 °C | R11 status changed to not met |

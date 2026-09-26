# Review note: DustBadge

## Session 2026-09-25: /populate to a strong TRL 2

### What was done

- `docs/01-problem.md` (DBG-PRB-001 v0.2): problem with cited burden figures, prior work and the gap, users and context, constraints, out of scope, open questions; co-design checklist kept.
- `docs/03-requirements.md` (DBG-REQ-001 v0.2): 15 measurable requirements (R1 to R15) with targets, status against the concept and planned verification; assumptions.
- `docs/02-concept.md` (DBG-PRC-001 v0.2): how it works, numbered components, first-order numbers (power, run time, range, mass, cost), design choices, dependencies on CalRig, safety, open questions.
- `cad/src/concept_media.py`: massing model of the badge (10 numbered parts) with the wearer's upper body as the scale context. The kit's cutaway cuts only across Y, so the script turns the badge 90 degrees and renders a labeled side section through the sensor itself.
- `media/`: `hero.png`, `concept-blueprint.png`, `.pdf` and `.svg`, `exploded.png` with BOM callouts, `cutaway.png`, `flow.png` (data flow), `model.glb` and `viewer.html`. Temporary `_views` folders removed.
- `bom/bom.csv`: 12 lines with indicative prices; lines 1 to 10 match the exploded view. `bom/bom-notes.md` updated.
- `README.md`: hero and links line; concept rationale, burning platform, industry and region tables, trigger, concept, key components and safety expanded with cited sources.
- `docs/pdf/`: branded PDFs of the three controlled documents.

### Key results (estimates, to be checked at TRL 3)

| Quantity | Estimate | Requirement |
| --- | --- | --- |
| Run time, continuous sampling | about 13 h typical, about 11 h worst case | R7 (12 h) at risk |
| Useful range | up to about 1 mg/m³ (sensor specification) | **R2 (5 mg/m³) not met** |
| Respirable dust at the RCS action level | about 250 µg/m³ at 10 % silica; about 30 to 50 µg/m³ for quartz-rich stone | Within range |
| Size and mass | 64 x 52 x 30 mm, about 110 g | R9 met, thin margin on mass |
| Distance to the nose | about 220 mm | R8 met |
| Shift log | about 12 kB per 12 h shift | R12 met |
| Parts cost | about $85 against the $90 budget | R15 met; no budget change proposed |

Requirements not met or unverified:

- **R2 (range) not met:** the SPS30 class is specified to 1 mg/m³; quarry and artisanal mining peaks can be far higher.
- **R14 (intrinsic safety) not met and out of scope:** the badge must not be used in underground coal or explosive atmospheres.
- **R7 (run time) at risk** at the sensor's maximum current.
- **R3 (±25 % accuracy after site calibration), R10 (ingress and drop) and R11 (humidity and spray bias)** are unverified.

`project.yaml` is unchanged: pitch and problem remain accurate. The problem line says results "arrive days later"; NIOSH FAST can give same or next day results, but it is not widely available, so the line was left as is.

### Proposed, awaiting Amish

1. **Particle sensor.** Options: (a) Sensirion SPS30 class with a PM4 output, about $48; (b) Plantower PMS5003, about $15 to $20, no PM4 bin and larger; (c) a wider-range sensor to meet R2, likely over budget. Recommendation: (a), and characterize it above 1 mg/m³ on CalRig at TRL 3.
2. **How silica is shown.** Options: (a) respirable dust always, RCS only as a labeled estimate once a site silica fraction is entered; (b) respirable dust only. Recommendation: (a).
3. **Default limits and alerts.** Options: US OSHA and MSHA values (25 µg/m³ action level, 50 µg/m³ limit) by default, configurable for other jurisdictions such as the EU 100 µg/m³; or a stricter default. Recommendation: US values by default, configurable.
4. **Sampling mode.** Continuous (catches short tasks, about 13 h) or duty-cycled (longer life, misses short peaks). Recommendation: continuous.
5. **Data ownership.** Logs kept by the worker and shared only by consent, with a stated rule that they are not used for discipline. Recommendation: adopt.
6. **First sector and partner.** Surface quarries and stone fabrication first, through a worker organization, NGO or university hygiene group; underground coal and explosive atmospheres excluded. Recommendation: adopt, partner to be chosen by Amish.
7. **Case details.** Downward screened inlet, high-visibility yellow front shell, spring clip with strap loop. Recommendation: adopt for the TRL 3 model.

### Safety concerns

- False reassurance is the main hazard: a low reading from a drifted or uncalibrated sensor could lead a worker to skip a respirator. The documents say plainly that silica is estimated and that the badge does not replace controls, respirators or sampling.
- Not intrinsically safe; must be labeled against use in gassy mines or explosive atmospheres.
- LiPo cell worn on the body in hot, dusty sites: protected and fused cell, no charging while worn, charging between 0 and 45 °C only.
- Exposure logs are sensitive personal data and could be misused by an employer.

### Problems and notes

- `.kit/concept.py` centers its cutaway cutter on the origin, so assemblies placed far from the origin produce an empty cutaway. The badge is modeled at the origin and the wearer placed around it. Worth fixing in the kit.
- The legacy `cad/src/model.py` placeholder is untouched (TRL 3 work).
- Some prevalence figures come from studies of selected groups and should not be read as national rates.

### Recommended next step

Review this note and the media, then decide items 1, 2 and 6. If approved, run `/advance-trl3` to build the error budget for R3, the power budget for R7, the range question for R2 and the parametric model and drawing sheet.

## Session 2026-09-25: TRL 3

On 2026-09-25 Amish asked for this batch to be taken through the usual process with the instruction "you know the drill, nothing gets past TRL 3". He has not reviewed this repo's TRL 2 items one by one, so every item above that carried a recommendation is adopted as recommended for TRL 3 under that instruction and stays open for his review. This session ran `/advance-trl3` on that basis and stopped at TRL 3.

### What was done

- `docs/decisions/0001-trl2-review-decisions.md` (DBG-DDR-001 v0.1, status proposed): items D1 to D7 adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review; O1 and O2 left as "Proposed, awaiting Amish".
- `docs/04-calcs/01-sizing.md` (DBG-CAL-001 v0.1) and `docs/04-calcs/sizing.py`: power and run time, charging, badge temperature in sun, PM4 against the ISO 7708 respirable convention, working range, an error budget for the shift average, alert logic in five scenarios, log size, breathing zone, mass, drop loads and cost, with a status for every requirement. The script imports the model's parameters and mass breakdown and reads the BOM and `project.yaml`; every number in the note is printed by it. Sensor figures were checked against the Sensirion SPS30 datasheet v2.0 (June 2023) with WebFetch.
- `cad/src/model.py`: parametric build123d model (rounded shells with the joint, three screw bosses, inlet and outlet slots, screen, sensor with its ports over the slots, controller, motor, LED light pipe, carrier board with USB-C, cell, clip, plus the wearer interface parameters). Exports `cad/step/` and `cad/stl/` for `dustbadge-assembly`, `front-shell` and `rear-shell`. No part interferences.
- `cad/src/sheets.py` and `cad/drawings/DBG-DWG-001.svg`, `.pdf`, `.png`: general arrangement at Rev P1, 1:1, marked "CONCEPT, NOT FOR FABRICATION" and "PRELIMINARY, NOT FOR FABRICATION". DBG-DWG-001 was free because the concept blueprint is DBG-DWG-010.
- `bom/bom.csv` (12 lines, all priced with a supplier or supplier type, $88.00 against $90) and `bom/bom-notes.md`.
- `cad/src/concept_media.py` now builds from the model; all of `media/` was re-rendered and every image checked. The kit's cutaway cut at the mean part center, which fell on the outlet slot and hid the screen, so the script now cuts on the inlet plane itself (project-side; the kit is unchanged). The exploded view's LED and screen offsets were moved so their callouts no longer sit on the front shell.
- DBG-PRB-001, DBG-PRC-001 and DBG-REQ-001 revised to v0.3; `README.md` (TRL badge, numbers, links, one sun safety line; required sections kept in order) and `project.yaml` (`trl: 3`, `trl_target: 3`, evidence list) updated. PDFs rebuilt in `docs/pdf/`.

Design changes found necessary by the calculations: an SHT4x-class humidity and temperature sensor on the carrier board, because R11 requires a humidity flag and the TRL 2 design had no way to sense humidity; and a charger with a cell thermistor input, because nothing enforced the 0 to 45 °C charging rule. Together they add $3. The TRL 2 precis quoted the PM2.5 precision (±5 µg/m³ plus 5 %) for PM4; the datasheet gives ±25 µg/m³ below 100 µg/m³ for PM4, and the precis is corrected. R8 is restated to apply to the inlet (a clarification, not a relaxed target).

### Requirement status (DBG-CAL-001, Table 6)

4 not met, 1 at risk, 1 not verifiable at TRL 3, 5 met on paper, 4 met by design.

| ID | Status | Key number |
| --- | --- | --- |
| R2 Range | **Not met** | 0 to 1 mg/m³ against 5 mg/m³; the RCS limit is in range only for silica fractions of 5 % or more; over-range minutes flagged and counted |
| R3 Accuracy | **Not met** on paper | ±34 % for quartz-rich stone at the action level (the 8 h filter collects 0.037 mg); ±21 to ±29 % for a quarry at 10 % silica; ±22 % with a 4.2 L/min, two-shift reference. Error terms assumed |
| R11 Site conditions | **Not met** in full sun above about 42 °C | Shell about 63 °C at 45 °C in full sun (sensor limit 60 °C); best performance only to 40 °C and 80 % RH |
| R14 Hazardous atmospheres | **Not met**, out of scope | Must be labeled not for gassy mines or explosive atmospheres |
| R7 Run time | At risk | 13.3 h typical at 25 °C; 11.3 h at the 65 mA maximum or at 0 °C; worst case needs about 1,880 mAh |
| R10 Drop and ingress | Not verifiable at TRL 3 | 750 to 1,500 g on a 1.5 m drop; sensor needs 194 to 387 N of retention |
| R6, R8, R9, R12, R15 | Met on paper | Alert logic correct in five scenarios (one early warning); inlet 242 mm from nose and mouth; 111.8 g, 64 x 52 x 33 mm; 182 shifts in flash; $88.00 of $90 |
| R1, R4, R5, R13 | Met by design | PM4 proxy (its size cut is offset both ways for quartz); labeled RCS estimate; 1 s readings; worker-held data |

### Decisions recorded (DBG-DDR-001)

Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review: D1 SPS30-class sensor; D2 respirable dust always, RCS only as a labeled estimate; D3 US OSHA and MSHA defaults, configurable; D4 continuous sampling; D5 worker-owned data, never used for discipline; D6 surface quarries and stone fabrication first, underground coal and explosive atmospheres excluded; D7 downward screened inlet, yellow front shell, spring clip with strap loop. No budget change, pitch or problem rewording was recommended, so `budget_usd` stays at $90 and the pitch and problem lines are unchanged.

### Still awaiting Amish

1. **O1, first co-design partner.** No recommendation was made.
2. **O2, how a site silica fraction is obtained.** DBG-PRB-001 proposed one filter sample per site and task analyzed by a partner laboratory; it was not in the TRL 2 review list, so it was not adopted.
3. **New, cell size (R7).** Options: (a) keep 1,500 mAh and accept R7 at risk; (b) a 1,900 to 2,000 mAh cell up to 11.5 mm thick, which fits the shells, adds about 8 g (119.8 g, 0.2 g under R9) and about $3 (about $91, $1 over `budget_usd`). Recommendation: (b), with the budget question for Amish. Not applied.
4. **New, R3 accuracy.** Options: (a) keep ±25 % and require a 4.2 L/min cyclone over two shifts for low-dust, high-silica sites (±22 % on paper); (b) relax R3 to ±35 % at dust levels below 100 µg/m³; (c) both. Recommendation: (a). Not applied.
5. **New, sun exposure (R11).** Options: a lighter shell color, a vented sun hood, or a use rule to wear the badge shaded above 40 °C. Recommendation: the use rule now, and a lighter shell tested at a later TRL. Not applied beyond a safety line.
6. **New, range (R2).** Options: accept the 1 mg/m³ range with the over-range flag (adopted in the firmware logic as a fail-safe), or a wider-range sensor, likely over budget. Recommendation: accept with the flag for the first sectors in D6.

### Cross-repo note (CalRig)

The TRL 2 recommendation for D1 said to characterize the SPS30 above 1 mg/m³ on CalRig. CalRig's TRL 2 design (CLR-PRC-001 v0.2, and its own review item 4) uses incense smoke decaying from 300 to 5 µg/m³ and says results will not transfer directly to mineral dust. The two are inconsistent: CalRig can serve DustBadge only for badge-to-badge and drift checks at low levels. Characterization above 1 mg/m³ with mineral dust needs a dust generator or a partner laboratory. The badge (64 x 52 x 33 mm) fits CalRig's 400 x 300 x 300 mm chamber. CalRig was not edited.

### Safety concerns

- False reassurance remains the main hazard. R3 is not met on paper at low dust levels, and the sensor under-sees coarse grains, so a low reading must never be read as safe air. Silica stays a labeled estimate.
- Heat: in full sun above about 42 °C the shell passes the sensor's 60 °C limit and typical LiPo discharge limits. A safety line was added to the precis and README.
- Lithium cell: charging is now blocked outside 0 to 45 °C by the thermistor charger; still never charge while worn.
- Not intrinsically safe; must be labeled against use in gassy mines or explosive atmospheres.
- Exposure logs are health-related personal data (D5).

### Gaps and notes

- Citations: the SPS30 datasheet figures were verified by WebFetch; the other citations were not listed as unchecked and were not re-fetched.
- Every error term in the R3 budget, the thermal coefficients and the drop crush distance are assumptions that only tests can settle.
- The kit's cutaway cuts at the mean part center; this repo now cuts on its own plane in `concept_media.py`. Worth fixing in the kit.
- The flow diagram content is unchanged from TRL 2.
- Existing material beyond TRL 3: `build-log/README.md` (scaffold) is present, untouched and not extended. No test, build or firmware material exists; the alert logic lives only in the calculation script.

### Recommended next step

TRL 4 is on hold by Amish's instruction; this repo stops at TRL 3. Amish's review is needed on D1 to D7 and on items 1 to 6 above, especially the cell size and budget. For the record only, TRL 4 would need: a bench build of the badge; a lab test report (TST, `environment: lab`) of run time at temperature, sensor response to mineral dust against a gravimetric reference including above 1 mg/m³, humidity and spray bias, shell temperature under a solar lamp, and drop and splash; and build log entries. None of this has been started.

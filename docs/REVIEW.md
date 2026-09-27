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

Status update: items 1 to 7 are now "Decided by Amish, 2026-09-25: go with recommendation" (DBG-DDR-002); the partner in item 6 had no recommendation and stays "Proposed, awaiting Amish".

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

Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review (now "Decided by Amish, 2026-09-25: go with recommendation", DBG-DDR-002): D1 SPS30-class sensor; D2 respirable dust always, RCS only as a labeled estimate; D3 US OSHA and MSHA defaults, configurable; D4 continuous sampling; D5 worker-owned data, never used for discipline; D6 surface quarries and stone fabrication first, underground coal and explosive atmospheres excluded; D7 downward screened inlet, yellow front shell, spring clip with strap loop. No budget change, pitch or problem rewording was recommended, so `budget_usd` stays at $90 and the pitch and problem lines are unchanged.

### Still awaiting Amish

Status update: items 3 to 6 are now "Decided by Amish, 2026-09-25: go with recommendation" (DBG-DDR-002, D8 to D11). Items 1 and 2 had no recommendation and stay "Proposed, awaiting Amish"; the budget figure in item 3 is a new open item (O3).

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

## Session 2026-09-25: recommendations accepted

On 2026-09-25 Amish wrote: "i accept all your recommendations, go with them across all repos." Every item with a recommendation is now "Decided by Amish, 2026-09-25: go with recommendation", recorded in `docs/decisions/0002-recommendations-accepted.md` (DBG-DDR-002 v0.1). TRL stays at 3.

### Decisions applied and what changed

- **D1 to D7** (DBG-DDR-001 and the TRL 2 list): SPS30-class sensor, silica as a labeled estimate, US defaults, continuous sampling, worker-owned data, surface quarries and stone fabrication first, downward screened inlet with yellow shell and clip. Wording only; DBG-DDR-001 v0.1 to v0.2.
- **D8, cell size (R7):** option (b). Cell 1,500 mAh, 10 mm, 30 g to 2,000 mAh, 11.5 mm, 38 g in `cad/src/model.py` (STEP and STL re-exported, no interferences). Worst-case run time 9.6 h to 12.8 h; typical 13.3 h to 17.7 h; charge 3.4 h to 4.2 h; mass 111.8 g to 119.8 g; BOM line 8 $10.00 to $13.00, total $88.00 to $91.00 against $90.
- **D9, R3 accuracy:** option (a). ±25 % kept; a 4.2 L/min cyclone over two shifts required at low-dust, high-silica sites. Quartz-rich stone ±34 % to ±22 % (factor per task); shared-factor case ±39 % to ±30 %; quarry unchanged at ±21 to ±29 %.
- **D10, sun (R11):** use rule, wear shaded above 40 °C ambient in full sun. Worst shell temperature 62.8 °C to 57.8 °C, 2.2 K under the 60 °C limit. Added to R11, the precis safety note, the README and the GA notes. The lighter shell test is TRL 4, on hold.
- **D11, range (R2):** accepted. R2 restated from 0 to 5 mg/m³ to 0 to 1 mg/m³ with over-range minutes flagged and counted.
- `budget_usd` unchanged at $90; no pitch or problem rewording was recommended, so `project.yaml` only gains DBG-DDR-002 in `trl_evidence`.
- Documents: DBG-PRB-001 v0.4, DBG-PRC-001 v0.4, DBG-REQ-001 v0.4, DBG-CAL-001 v0.2 (script rerun, every table updated), DBG-DDR-001 v0.2, new DBG-DDR-002 v0.1; DBG-DWG-001 Rev P1 to P2 (cell note and sun rule); `bom/bom.csv` and `bom/bom-notes.md`; media regenerated from the model (key figures updated; the LED's exploded offset moved so its callout clears the front shell); all PDFs rebuilt.
- README: new "What sparked the idea" (MSHA's 2014 coal dust rule and the continuous personal dust monitor, required from February 1, 2016, which gives coal miners in-shift feedback that silica-exposed workers lack), replacing the text about a portfolio review. DBG-PRB-001 had no such attribution.
- Job 2: all generated files re-rendered so they show designmolecule.com; superseded PDFs removed from `docs/pdf/`.

### Requirement status (DBG-CAL-001 v0.2)

2 not met, 2 at risk, 1 not verifiable at TRL 3, 6 met on paper, 4 met by design (was 4, 1, 1, 5, 4).

| ID | Status | Key number |
| --- | --- | --- |
| R14 Hazardous atmospheres | **Not met**, out of scope | Not intrinsically safe |
| R15 Cost | **Not met** (was met) | $91.00 against $90 (O3) |
| R3 Accuracy | At risk (was not met) | ±21 to ±22 % with a factor per task; ±29 to ±30 % with a shared factor |
| R11 Site conditions | At risk (was not met) | Shell at most 57.8 °C under the use rule; relies on the wearer |
| R10 Drop and ingress | Not verifiable at TRL 3 | Cell now needs 280 to 559 N of retention |
| R2, R6, R7, R8, R9, R12 | Met on paper | 1 mg/m³ with flag; five alert scenarios; 12.8 h worst case; 242 mm; 119.8 g (0.2 g margin); 182 shifts |
| R1, R4, R5, R13 | Met by design | Unchanged |

### Still awaiting Amish

1. **O1, first co-design partner.** No recommendation.
2. **O2, how a site silica fraction is obtained where no laboratory is near.** No recommendation.
3. **O3, budget figure for the larger cell.** $91.00 against $90; no recommended figure, so `budget_usd` stays at $90 and R15 is not met. **Decided by Amish, 2026-09-26: budget set to $91** (DBG-DDR-002).

### Cross-repo actions

- **CalRig:** D1's recommendation to characterize the SPS30 above 1 mg/m³ on CalRig cannot be done with CalRig's incense-smoke chamber (5 to 300 µg/m³). CalRig's documents should say it serves DustBadge only for badge-to-badge and drift checks at low levels; mineral dust above 1 mg/m³ needs a dust generator or partner laboratory. CalRig was not edited from this repo.

### Safety

Unchanged hazards (false reassurance, heat, lithium cell, not intrinsically safe, personal data). The sun use rule lowers the heat risk only if the wearer follows it; the badge cannot enforce it. The heavier cell raises the retention load in a drop.

### TRL 4

TRL 4 remains on hold by Amish's instruction. Sensor characterization with mineral dust, the lighter shell under a solar lamp, drop and spray tests, a bench build, buying parts and firmware beyond a sketch are recorded as decided where recommended but not started.

## Session 2026-09-26: budget approved

Amish wrote on 2026-09-26: "i approve all the budget items." Budget set to $91 to cover the priced BOM: decided by Amish, 2026-09-26. This closes O3.

- `project.yaml` `budget_usd` $90 to **$91**. The priced BOM is unchanged at $91.00 (12 lines).
- R15 (cost): target $90 to $91; status **Not met to Met on paper**. Requirement status is now 1 not met (R14, out of scope), 2 at risk (R3, R11), 1 not verifiable at TRL 3 (R10), 7 met on paper, 4 met by design.
- Files changed: `project.yaml`, `README.md`, DBG-PRB-001 v0.5, DBG-PRC-001 v0.5, DBG-REQ-001 v0.5, DBG-CAL-001 v0.3 (`sizing.py` rerun), DBG-DDR-002 v0.2, `bom/bom-notes.md`, `cad/src/concept_media.py` (blueprint key figure); media and PDFs regenerated, temporary `media/_views*` folders deleted.
- Still awaiting Amish: O1 (co-design partner) and O2 (site silica fraction without a nearby laboratory). `trl: 3` and `trl_target: 3` are unchanged; TRL 4 remains on hold.

## Session 2026-09-26: product appearance model and photoreal renders

Amish chose this repo for the first batch of product renders on 2026-09-26. This session adds an appearance model for photoreal renders. It does not change the design, the BOM, the calculations or `cad/src/model.py`.

### What was added

- `cad/src/product_model.py`: `product_parts()` (28 parts: 11 shell, 10 internal, 3 accessory, 4 context), `TITLE` and `RENDER_VIEWS` (hero, exploded and worn). All main dimensions and interfaces come from `PARAMS`, `derived()` and `build_parts()` in `model.py`.
  - Filleted hi-vis yellow front shell (3 mm front perimeter) and dark rear shell (2.5 mm rear perimeter), with 0.6 mm fillets either side of the shell joint and a TPU gasket band showing in the parting line.
  - Ribbed grip texture on both side faces of the front shell.
  - Clear acrylic front window over the particle sensor, showing a sensor fan and a printed label on the sensor face.
  - Lit red alert light pipe (emissive) in a dark bezel; printed status label with three level bars.
  - Three M2 screws in the rear face; stainless inlet screen in the bottom inlet slot.
  - Internals rendered as finished parts: controller module with shield can, vibration motor, carrier board with components, 2,000 mAh pouch cell with label.
  - Stainless spring clip (riveted base leaf, hinge barrel, tongue with the strap-loop slot) inside the `model.py` clip envelope.
  - Accessory: webbing lanyard through the strap loop with a crimp and a teal breakaway buckle.
  - Context for the worn view: curved fabric chest panel with a harness strap, stitching and reflective tape.
- `README.md`: hero image now points to `media/render-hero.png`, with a link to `media/render-exploded.png`. The render files are produced separately.

### Differences from model.py (each Proposed, awaiting Amish)

1. **Front window over the sensor (30 x 24 mm).** `model.py` has a solid front face. The window shows the sensor for the renders but adds a sealing joint that bears on R10 (drop and ingress). Recommendation: keep it in the renders only; decide at TRL 4 whether to adopt it, and if so, add it to BOM line 1 and the drawing.
2. **Visible sensor fan.** An SPS30-class sensor encloses its fan; the recess and fan on the sensor face are illustrative. Recommendation: keep, and describe it as illustrative in any caption that calls out the fan.
3. **Rear screws at the three boss positions.** `model.py` has the bosses but no shell closure fasteners. Recommendation: adopt three M2 screws through the rear shell into the front bosses (BOM line 11 already covers M2 screws).
4. **Side grip ribs stand 0.6 mm proud**, so the rendered width is about 65.2 mm against 64 mm. Recommendation: accept for appearance; if adopted, recess the ribs so the 64 mm envelope holds.
5. **Lanyard and breakaway buckle** have no BOM line. A breakaway is the safer choice near rotating machinery. Recommendation: add an optional BOM line (about $1) at TRL 4, subject to the budget Amish approved.
6. **TPU gasket shown as a visible band.** BOM line 9 lists the gasket; `model.py` does not model it. Recommendation: accept as shown.

### Status

Appearance only: no tolerances, no fabrication detail, no PCB layout. `trl` and `trl_target` stay at 3, and TRL 4 remains on hold.

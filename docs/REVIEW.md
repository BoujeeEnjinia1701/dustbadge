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

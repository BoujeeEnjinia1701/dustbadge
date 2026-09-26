---
doc_id: DBG-DDR-002
title: DustBadge recommendations accepted
project: DustBadge
doc_type: Design decision record
version: "0.2"
status: Draft
date: '2026-09-26'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record the recommendations accepted by Amish on 2026-09-25, what changed in the repo, and the items still open
- version: "0.2"
  date: '2026-09-26'
  author: Amish Chadha
  change: "Budget set to $91 to cover the priced BOM: decided by Amish, 2026-09-26 (O3 closed)"
---

# 0002: Recommendations accepted

- **Date:** 2026-09-25
- **Status:** accepted. Every item below marked "Decided by Amish, 2026-09-25: go with recommendation" is accepted; items without a recommendation remain open, except O3 (budget), decided by Amish on 2026-09-26.

## Context

On 2026-09-25 Amish wrote: "i accept all your recommendations, go with them across all repos." This record lists every item in `docs/REVIEW.md` (TRL 2 and TRL 3 sessions) and in DBG-DDR-001 that carried a recommendation, now decided, and what changed in the repo. Items without a recommendation stay "Proposed, awaiting Amish". Where a recommendation offered several options, the recommended option is the decision. TRL 4 remains on hold by Amish's instruction, and `trl` and `trl_target` stay at 3.

## Options considered

The options for each item are those listed in `docs/REVIEW.md` (sessions 2026-09-25, /populate and TRL 3) and in DBG-DDR-001.

## Decision

*Table 1. Items decided by Amish, 2026-09-25: go with recommendation.*

| # | Item | Decision | What changed in the repo |
| --- | --- | --- | --- |
| D1 | Particle sensor (DDR-001 D1) | Sensirion SPS30 class with a PM4 output, about $48 | Wording only. Its characterization above 1 mg/m³ is test work (TRL 4, on hold), and CalRig cannot do it as designed; listed as a cross-repo action in `docs/REVIEW.md` |
| D2 | How silica is shown (DDR-001 D2) | Respirable dust always; RCS only as a labeled estimate once a site silica fraction is entered | Wording only |
| D3 | Default limits (DDR-001 D3) | US OSHA and MSHA values by default (25 µg/m³ action level, 50 µg/m³ limit), configurable | Wording only (DBG-PRB-001 v0.4, DBG-PRC-001 v0.4, DBG-REQ-001 v0.4) |
| D4 | Sampling mode (DDR-001 D4) | Continuous sampling | Wording only |
| D5 | Data ownership (DDR-001 D5) | Logs kept by the worker, shared only by consent, never used for discipline | Wording only |
| D6 | First sector (DDR-001 D6) | Surface quarries and stone fabrication first; underground coal and explosive atmospheres excluded | Wording only; the partner stays open (O1) |
| D7 | Case details (DDR-001 D7) | Downward screened inlet, high-visibility yellow front shell, spring clip with strap loop | Wording only (already in the model) |
| D8 | Cell size (R7) | Option (b): a larger cell up to 11.5 mm thick; 2,000 mAh chosen to clear the 1,880 mAh worst-case need | `cad/src/model.py`: cell 50 x 34 x 10 mm, 1,500 mAh, 30 g to 50 x 34 x 11.5 mm, 2,000 mAh, 38 g; STEP and STL re-exported; DBG-DWG-001 Rev P1 to P2; BOM line 8 $10.00 to $13.00; media regenerated. DBG-CAL-001 v0.2: worst-case run time 9.6 h to 12.8 h, typical 13.3 h to 17.7 h, R7 at risk to met; mass 111.8 g to 119.8 g (R9 met, 0.2 g margin); charge 3.4 h to 4.2 h; parts $88.00 to $91.00, R15 met to not met by $1 |
| D9 | R3 accuracy | Option (a): keep ±25 % and require a 4.2 L/min cyclone over two shifts for low-dust, high-silica sites | R3 target restated with the reference rule in DBG-REQ-001 v0.4; DBG-CAL-001 v0.2 section F: ±21 % (quarry) and ±22 % (quartz-rich stone) with a factor per task, ±29 to ±30 % with a shared factor; R3 not met to at risk |
| D10 | Sun exposure (R11) | The use rule now (wear the badge shaded when the ambient is above 40 °C in full sun); a lighter shell tested at a later TRL | Use rule added to R11 (DBG-REQ-001 v0.4), the precis safety section, the README and the DBG-DWG-001 notes. DBG-CAL-001 v0.2 [C3]: shell at most 57.8 °C (was up to 62.8 °C), 2.2 K under the sensor's 60 °C limit; R11 not met to at risk. The lighter shell test is TRL 4, on hold |
| D11 | Range (R2) | Accept the 1 mg/m³ range with the over-range flag for the first sectors in D6 | R2 restated from 0 to 5 mg/m³ to 0 to 1 mg/m³ with minutes above the range flagged, logged at the limit and counted (DBG-REQ-001 v0.4); R2 not met to met on paper. The flag was already in the alert logic |

*Table 2. Items still open.*

| # | Item | Status |
| --- | --- | --- |
| O1 | First co-design partner (worker organization, NGO or university hygiene group). No recommendation was made. | Proposed, awaiting Amish |
| O2 | How a site silica fraction is obtained where no laboratory is near. DBG-PRB-001 proposed one filter sample per site and task analyzed by a partner laboratory, but the item was not in the review list and carried no recommendation. | Proposed, awaiting Amish |
| O3 | Budget figure for the larger cell. The parts now cost $91.00 against `budget_usd` of $90. The TRL 3 note left "the budget question for Amish" without a recommended figure, so `budget_usd` stays at $90. | Decided by Amish, 2026-09-26: budget set to $91 (see below) |

### Budget approved, 2026-09-26

On 2026-09-26 Amish wrote: "i approve all the budget items."

- Budget set to $91 to cover the priced BOM: decided by Amish, 2026-09-26. This closes O3. `project.yaml` `budget_usd` 90 to 91; DBG-REQ-001 R15 target $91, status Not met to Met on paper; DBG-CAL-001 v0.3 (`sizing.py` rerun); DBG-PRB-001, DBG-PRC-001, README, `bom/bom-notes.md` and the blueprint key figures updated. The BOM and geometry are unchanged.

## Consequences

- Requirement status (DBG-CAL-001 v0.2): not met 2 (was 4), at risk 2 (was 1), not verifiable at TRL 3 1, met on paper 6 (was 5), met by design 4. Not met: R14 (intrinsic safety, out of scope) and R15 ($91.00 against $90, O3).
- After the 2026-09-26 budget approval (DBG-CAL-001 v0.3): not met 1 (R14), at risk 2, not verifiable at TRL 3 1, met on paper 7, met by design 4.
- `project.yaml`: no change. `budget_usd` stays at $90 (O3), and no pitch or problem rewording was recommended.
- Documents bumped: DBG-PRB-001 v0.4, DBG-PRC-001 v0.4, DBG-REQ-001 v0.4, DBG-CAL-001 v0.2, DBG-DDR-001 v0.2; drawing DBG-DWG-001 Rev P2.
- Cross-repo action: CalRig's smoke chamber (5 to 300 µg/m³) cannot characterize the SPS30 above 1 mg/m³ with mineral dust, so D1's characterization needs a dust generator or partner laboratory; DustBadge uses CalRig only for badge-to-badge and drift checks. Listed in `docs/REVIEW.md`; CalRig is not edited from this repo.
- TRL 4 work (sensor characterization with mineral dust, a lighter shell under a solar lamp, drop and spray tests, a bench build, buying parts, firmware beyond a sketch) remains on hold.

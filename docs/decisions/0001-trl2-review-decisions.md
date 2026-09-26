---
doc_id: DBG-DDR-001
title: DustBadge TRL 2 review decisions
project: DustBadge
doc_type: Design decision record
version: "0.2"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record the TRL 2 review recommendations adopted for TRL 3 work under Amish's 2026-09-25 instruction, and the items that remain open
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: "Recommendations accepted by Amish (DDR-002): D1 to D7 decided; O1 and O2 stay open"
---

# 0001: TRL 2 review decisions

- **Date:** 2026-09-25
- **Status:** items D1 to D7 decided by Amish on 2026-09-25 ("i accept all your recommendations, go with them across all repos"), recorded in DBG-DDR-002; items O1 and O2 remain proposed, awaiting Amish.

## Context

The TRL 2 review note (`docs/REVIEW.md`, session 2026-09-25, /populate) listed seven items as "Proposed, awaiting Amish", each with options and a recommendation. On 2026-09-25 Amish asked for this batch of repos to be taken through the usual process with the instruction "you know the drill, nothing gets past TRL 3". He has not reviewed this repo's items one by one. Every item that carries a recommendation is therefore adopted as recommended for TRL 3 under that instruction and stays open for his review. Items without a recommendation stay "Proposed, awaiting Amish". Later on 2026-09-25 Amish accepted all the recommendations, so D1 to D7 are now decided (DBG-DDR-002).

## Options considered

The options for each item are those listed in `docs/REVIEW.md` (session 2026-09-25, /populate) and in DBG-PRC-001 v0.2, Key design choices.

## Decision

*Table 1. Items adopted for TRL 3, decided by Amish on 2026-09-25 (DBG-DDR-002).*

| # | Item | Adopted recommendation | Status |
| --- | --- | --- | --- |
| D1 | Particle sensor | Option (a): Sensirion SPS30 class with a PM4 output, about $48. The TRL 2 recommendation also said to characterize it above 1 mg/m³ on CalRig; CalRig's own TRL 2 design uses incense smoke decaying from 300 to 5 µg/m³, so it cannot do this as scoped (see Consequences). | Decided by Amish, 2026-09-25: go with recommendation |
| D2 | How silica is shown | Option (a): respirable dust always; RCS only as a labeled estimate once a site silica fraction is entered. | Decided by Amish, 2026-09-25: go with recommendation |
| D3 | Default limits and alerts | US OSHA and MSHA values by default (25 µg/m³ action level, 50 µg/m³ limit, 8 h TWA), configurable for other jurisdictions such as the EU 100 µg/m³. | Decided by Amish, 2026-09-25: go with recommendation |
| D4 | Sampling mode | Continuous sampling all shift, not duty-cycled. | Decided by Amish, 2026-09-25: go with recommendation |
| D5 | Data ownership | Logs kept by the worker and shared only by the worker's consent, with a stated rule that they are not used for discipline. | Decided by Amish, 2026-09-25: go with recommendation |
| D6 | First sector | Surface quarries and stone fabrication first; underground coal and explosive atmospheres excluded. The partner is not chosen (O1). | Decided by Amish, 2026-09-25: go with recommendation |
| D7 | Case details | Downward screened inlet, high-visibility yellow front shell, spring clip with strap loop. Used in the TRL 3 model. | Decided by Amish, 2026-09-25: go with recommendation |

*Table 2. Items that remain open.*

| # | Item | Status |
| --- | --- | --- |
| O1 | First co-design partner (worker organization, NGO or university hygiene group). The TRL 2 note left the choice to Amish and made no recommendation. | Proposed, awaiting Amish |
| O2 | How a site silica fraction is obtained where no laboratory is near. DBG-PRB-001 v0.2 proposed one filter sample per site and task analyzed by a partner laboratory, but the item was not in the review note's list, so it is not adopted here. DBG-CAL-001 section F adds that at low dust levels the sample needs a higher flow or two shifts. | Proposed, awaiting Amish |

New items raised by the TRL 3 calculations (cell size for R7, the R3 reference sample and target, sun exposure for R11, and the R2 range) were listed in `docs/REVIEW.md` as "Proposed, awaiting Amish"; Amish decided them on 2026-09-25 and they are recorded in DBG-DDR-002 (D8 to D11).

## Consequences

- `project.yaml`: only the TRL fields change. No budget, pitch or problem change was recommended, so `budget_usd` stays at $90 and the pitch and problem lines are unchanged.
- DBG-PRB-001, DBG-PRC-001 and DBG-REQ-001 are revised to v0.3. The key design choices in the precis read as adopted for TRL 3; from v0.4 they read as decided by Amish (DBG-DDR-002). R6's default limits now follow D3; R8 is restated as the inlet within 300 mm of the nose and mouth.
- D1 and CalRig: CalRig (CLR-PRC-001 v0.2) is a smoke chamber for 5 to 300 µg/m³ and says its results will not transfer directly to mineral dust. DustBadge therefore uses CalRig only for badge-to-badge and drift checks at low levels. Characterizing the SPS30 above 1 mg/m³ needs a dust generator or a partner laboratory, which is test work beyond TRL 3. This is noted in `docs/REVIEW.md`; CalRig is not edited.
- The TRL 3 calculations (DBG-CAL-001) led to two changes within these decisions: an SHT4x-class humidity and temperature sensor on the carrier board, so the R11 flag can work, and a charger with a cell thermistor input, so charging is blocked outside 0 to 45 °C. They add $3; parts now cost $88.00.
- TRL 4 is on hold by Amish's instruction. Nothing in this record authorizes building or testing.

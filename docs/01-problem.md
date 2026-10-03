---
doc_id: DBG-PRB-001
title: DustBadge problem statement
project: DustBadge
doc_type: Problem statement
version: "0.8"
status: Draft
date: '2026-10-02'
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
  change: Populate to TRL 2 (problem, users, context, constraints, prior work with sources)
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: "TRL 3, record decisions D3 and D6 from DBG-DDR-001 (adopted for TRL 3 pending Amish's review); partner and silica fraction method stay open"
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: "Recommendations accepted by Amish (DDR-002): D3 and D6 decided; low-dust reference rule noted; partner and silica fraction method stay open"
- version: "0.5"
  date: '2026-09-26'
  author: Amish Chadha
  change: Budget approved by Amish; constraint now $91
- version: "0.6"
  date: '2026-10-01'
  author: Amish Chadha
  change: Budget treated as a value-engineering target
- version: "0.7"
  date: '2026-10-01'
  author: Amish Chadha
  change: BioMedical area (DBG-DEC-001 v0.3); constraints state a research and educational prototype, not a medical device
- version: "0.8"
  date: '2026-10-02'
  author: Amish Chadha
  change: 'Estimated cost USD 91.50, USD 0.50 over the value-engineering target (foam pad of the worn version)'
---

# DustBadge problem statement

Respirable crystalline silica (RCS) causes silicosis, which is incurable, yet most exposed workers never learn their own exposure while it can still be changed. Personal sampling with a pump and filter is costly, needs a trained hygienist, and reports a single shift average days later, so a worker cannot tell during the shift that a saw, a dry sweep or a dusty haul road is putting them over the limit.

## The problem

Silicosis killed more than 12,900 people worldwide in 2019, and the burden falls hardest on lower-income regions where protection is weakest ([Chen, Liu and Xie, BMC Pulmonary Medicine, 2022](https://link.springer.com/article/10.1186/s12890-022-02040-9)). In the United States about 2.3 million workers are exposed, and OSHA estimated that its 2016 limit of 50 µg/m³ (8 h average) would prevent more than 600 deaths a year once fully effective ([US Department of Labor, 2016](https://www.dol.gov/newsroom/releases/osha/osha20160324)). An estimated 44 million artisanal and small-scale miners work mostly in developing economies, and a systematic review found a pooled silicosis prevalence of 23.9 % among those studied, with some disease after fewer than 6 years of mining ([Howlett et al., PLOS Global Public Health, 2023](https://journals.plos.org/globalpublichealth/article?id=10.1371%2Fjournal.pgph.0002085)).

Limits exist, but exposure is rarely measured where the work happens. The reference method draws air through a size-selective cyclone onto a filter, which a laboratory analyzes afterward. NIOSH has shortened the wait with its Field Analysis of Silica Tool, which gives results the same or next day using a portable infrared analyzer ([NIOSH, FAST](https://www.cdc.gov/niosh/publications/numbered/2021-118.html)), but that still reports after the shift and needs equipment most small quarries and workshops do not have. Real-time feedback during the shift exists for US underground coal miners through the continuous personal dust monitor ([US Department of Labor, 2016](https://www.dol.gov/newsroom/releases/msha/msha20160801)), a specialized instrument well beyond the budget of an informal quarry.

## Prior work and the gap

- **Continuous personal dust monitors** (for example the Thermo PDM3700 used in US coal mines) give in-shift results for coal mine dust but are costly and not designed for silica fraction estimates in other commodities.
- **Real-time optical monitors.** NIOSH notes that factory-calibrated optical monitors can differ by up to a factor of 10 from gravimetric samples, because the signal depends on particle size, shape and refractive index; a site correction factor from a filter sample is needed ([Cauda, NIOSH Manual of Analytical Methods, 2021](https://www.cdc.gov/niosh/nmam/pdf/chapter-am.pdf)).
- **Low-cost particle sensors in mining.** A calibration study found that a Plantower PMS5003 reached R² of 0.70 to 0.90 against a reference below 3.0 mg/m³ of coal dust, and suggested such sensors could extend personal monitoring to all miners ([Amoah et al., Science of the Total Environment, 2023](https://www.sciencedirect.com/science/article/abs/pii/S0048969722074381)).
- **Sensor modules with a respirable size bin.** The Sensirion SPS30 reports PM4 mass (particles up to 4 µm), close to the respirable convention, over 0 to 1,000 µg/m³ ([Sensirion SPS30 datasheet](https://sensirion.com/media/documents/8600FF88/64A3B8D6/Sensirion_PM_Sensors_Datasheet_SPS30.pdf)).

The gap is an open, low-cost, wearable reference design that estimates respirable dust and silica exposure through the shift, tells the worker when the shift average is heading over a limit, and keeps the worker in control of the data. No optical sensor can identify silica; DustBadge can only estimate it from respirable dust and a site-specific silica fraction, and it must say so.

## Users and context

| User | Need | Context |
| --- | --- | --- |
| Quarry, pit or stone yard worker | Know during the shift when dust is high enough to act (wet the cut, move upwind, fit a respirator, stop) | Surface quarries and open pits, 8 to 12 h shifts, heat, dust, water sprays |
| Stone benchtop fabricator | Warning when cutting, grinding or polishing raises exposure | Small workshops, often without any exposure sampling |
| Construction worker | Feedback when cutting concrete, brick or tile | Building sites, short high-dust tasks |
| Supervisor or safety officer | Which tasks and places drive exposure, with worker consent | Site safety reviews |
| Occupational hygienist, researcher or worker organization | A cheap screening tool between regulatory samples; open data format | Surveys, research, community health programs |

## Constraints

- Garage-buildable prototype, a value-engineering target of $91 USD in parts (`budget_usd`, a hypothetical control target, not a limit; moved from $90 by Amish on 2026-09-26, DBG-DDR-002), with an estimated cost of $91.50 ($0.50 over the target, the foam pad of the worn version), from off-the-shelf modules and 3D-printed parts.
- Small and light enough to wear on the chest within 30 cm of the nose and mouth for a full shift.
- Must work in heat, dust and wet spray without clogging or false alarms dominating.
- Exposure data belongs to the worker. Sharing with an employer is by consent, and the device must not become a tool for discipline.
- Research and educational prototype only. It is not a medical device, is not certified monitoring or personal protective equipment, does not replace regulatory sampling or respirators, and is not certified for explosive atmospheres.

## Out of scope

- Direct measurement of silica content (needs a filter and laboratory or field infrared analysis).
- Regulatory compliance sampling.
- Use in underground coal mines or any atmosphere that may contain flammable gas or combustible dust, which would require an intrinsically safe, certified design.
- Medical diagnosis or health surveillance.

## Open questions

- First sector: surface quarries and stone fabrication first, with underground coal and explosive atmospheres excluded. Decided by Amish, 2026-09-25: go with recommendation (DBG-DDR-001, D6; DBG-DDR-002).
- First co-design partner: a worker organization, NGO or university occupational hygiene group. Proposed, awaiting Amish (DBG-DDR-001, O1).
- Default exposure limits, which differ by country (for example 50 µg/m³ in the US and 100 µg/m³ as the EU binding limit): US values by default, configurable. Decided by Amish, 2026-09-25: go with recommendation (DBG-DDR-001, D3; DBG-DDR-002).
- How a site silica fraction is obtained where no laboratory is near. Proposed: one filter sample per site and task analyzed by a partner laboratory; At low-dust, high-silica sites the reference is now a 4.2 L/min cyclone over two shifts (decided by Amish, 2026-09-25, DBG-DDR-002 D9), but where the sample is analyzed when no laboratory is near remains open. Proposed, awaiting Amish (DBG-DDR-001, O2).

## User research and co-design

This design is for communities the author is not part of, so requirements come from the people who will use it.

- [ ] Identify a local partner organization (Helpful Engineering network, NGO or university)
- [ ] Run co-design sessions with intended users; record who, where and what was learned
- [ ] Validate load, distance, terrain and cost assumptions in the field
- [ ] Revise requirements (REQ) from findings before freezing the design

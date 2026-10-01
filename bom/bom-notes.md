# BOM notes

- Prices are indicative single-unit prices in USD from September 2026 catalog searches and typical distributor listings. They are not quotes.
- Line numbers 1 to 11 match the numbered callouts in `media/exploded.png`; line 12 is software and is not modeled.
- Every line is priced. Total parts cost is $91.00, equal to the $91 `budget_usd` (approved by Amish on 2026-09-26 to cover the priced BOM, DBG-DDR-002; it was $90), as checked by `docs/04-calcs/sizing.py` (DBG-CAL-001 v0.2, section L). The particle sensor is 53 % of the cost; the SPS30 class was decided by Amish on 2026-09-25 (DBG-DDR-001, D1; DBG-DDR-002).
- TRL 3 change: line 7 now includes an SHT4x-class humidity and temperature sensor (R11 flag) and a charger with a cell thermistor input (0 to 45 °C charging), adding $3. Line 8 specifies a cell with a thermistor lead.
- 2026-09-25 change (DBG-DDR-002, D8): line 8 is now a 2,000 mAh cell, 11.5 mm thick, at $13.00 (was 1,500 mAh at $10.00), so R7 is met in the worst case. It takes the total from $88.00 to $91.00. The budget figure for the larger cell (DBG-DDR-002, O3) was decided by Amish on 2026-09-26: `budget_usd` $90 to $91.
- Supplier types are given where no single supplier is needed; the SPS30 and SHT4x are sold by major electronics distributors.
- Not included: the filter sample and laboratory analysis needed to set a site silica fraction, and access to CalRig for chamber checks.
- 2026-09-30 change (DBG-DDR-003, design for construction): specifications of lines 2, 6, 7, 9, 10 and 11 now describe the parts as the build plan uses them (screen size, flanged light pipe, the carrier board's modules, the TPU gasket and port seals, the drilled clip, the five M2 screws and foam tape). No price changed: the gasket and seals are printed from the TPU already in line 9, and the screws and tape fall within line 11. The total stays $91.00.

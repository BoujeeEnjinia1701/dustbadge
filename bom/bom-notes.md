# BOM notes

- Prices are indicative single-unit prices in USD from September 2026 catalog searches and typical distributor listings. They are not quotes.
- Line numbers 1 to 10 match the numbered callouts in `media/exploded.png`. Lines 11 and 12 are not modeled.
- Every line is priced. Total parts cost is $91.00, $1.00 over the $90 `budget_usd`, as checked by `docs/04-calcs/sizing.py` (DBG-CAL-001 v0.2, section L). The particle sensor is 53 % of the cost; the SPS30 class was decided by Amish on 2026-09-25 (DBG-DDR-001, D1; DBG-DDR-002).
- TRL 3 change: line 7 now includes an SHT4x-class humidity and temperature sensor (R11 flag) and a charger with a cell thermistor input (0 to 45 °C charging), adding $3. Line 8 specifies a cell with a thermistor lead.
- 2026-09-25 change (DBG-DDR-002, D8): line 8 is now a 2,000 mAh cell, 11.5 mm thick, at $13.00 (was 1,500 mAh at $10.00), so R7 is met in the worst case. It takes the total from $88.00 to $91.00. The budget figure for the larger cell had no recommendation and is open, awaiting Amish (DBG-DDR-002, O3); `budget_usd` is unchanged at $90.
- Supplier types are given where no single supplier is needed; the SPS30 and SHT4x are sold by major electronics distributors.
- Not included: the filter sample and laboratory analysis needed to set a site silica fraction, and access to CalRig for chamber checks.

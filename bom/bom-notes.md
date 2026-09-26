# BOM notes

- Prices are indicative single-unit prices in USD from September 2026 catalog searches and typical distributor listings. They are not quotes.
- Line numbers 1 to 10 match the numbered callouts in `media/exploded.png`. Lines 11 and 12 are not modeled.
- Every line is priced. Total parts cost is $88.00, within the $90 `budget_usd` with a $2.00 margin, as checked by `docs/04-calcs/sizing.py` (DBG-CAL-001, section L). The particle sensor is 55 % of the cost; the SPS30 class is adopted for TRL 3 (DBG-DDR-001, D1), pending Amish's review.
- TRL 3 change: line 7 now includes an SHT4x-class humidity and temperature sensor (R11 flag) and a charger with a cell thermistor input (0 to 45 °C charging), adding $3. Line 8 specifies a cell with a thermistor lead.
- A larger cell (about 1,900 to 2,000 mAh, up to 11.5 mm thick) would cover R7 in the worst case, at about $3 more, which would take the total to about $91, over the budget. Proposed in `docs/REVIEW.md`, awaiting Amish; not in the BOM.
- Supplier types are given where no single supplier is needed; the SPS30 and SHT4x are sold by major electronics distributors.
- Not included: the filter sample and laboratory analysis needed to set a site silica fraction, and access to CalRig for chamber checks.

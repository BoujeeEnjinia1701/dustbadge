"""DustBadge sizing calculations, DBG-CAL-001 v0.2 (TRL 3, revised for DBG-DDR-002).

Run from the repo root:  python docs/04-calcs/sizing.py
Prints every number quoted in docs/04-calcs/01-sizing.md. Each line carries a tag such as
[A3] that the note cites. Geometry and masses come from cad/src/model.py (PARAMS, derived,
masses), the parts cost from bom/bom.csv and the budget from project.yaml. Sensor figures
are from the Sensirion SPS30 datasheet, version 2.0, June 2023. First-principles estimates
for a paper proof of concept; not a substitute for tests.
"""
import csv
import math
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "cad" / "src"))
from model import PARAMS as P, derived, masses, build_parts  # noqa: E402

D = derived(P)


def tag(t, text):
    print(f"[{t}] {text}")


def phi(x):
    """Standard normal cumulative distribution."""
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


# ------------------------------------------------------------------ assumptions
# Sensor (SPS30 datasheet v2.0)
I_SENS = {"typical low": 0.045, "typical high": 0.055, "maximum": 0.065}   # A at 5 V, measurement mode
V_SENS = 5.0
RANGE_MAX = 1000.0         # ug/m3, mass concentration range
PREC_PM4_ABS = 25.0        # ug/m3, PM4 precision from 0 to 100 ug/m3
PREC_PM4_REL = 0.25        # of reading, PM4 precision from 100 to 1000 ug/m3
DRIFT_REL = 0.0125         # per year, 100 to 1000 ug/m3
DRIFT_ABS = 1.25           # ug/m3 per year, 0 to 100 ug/m3
T_BEST = (10.0, 40.0)      # degC, recommended range for best performance
RH_BEST = (20.0, 80.0)     # % RH
T_OPER_MAX = 60.0          # degC, operating limit
# Electronics
ETA_BOOST = 0.85           # 5 V boost efficiency
P_CTRL = 0.003 * 3.7       # W, nRF52840 with BLE connection events and SHT4x, 3 mA at the cell
ALERTS = 20                # alerts per shift (assumed busy shift)
P_MOTOR = 0.080 * 3.0      # W while vibrating
T_ALERT = 2.0              # s per alert
# Cell
CELL_MAH, CELL_V = P["cell_mah"], 3.7   # 2,000 mAh from the model (DBG-DDR-002 D8; was 1,500 mAh)
USABLE = 0.80              # usable fraction (protection cut-off, ageing allowance)
COLD = 0.85                # capacity factor at 0 degC
SHIFT_H = 12.0
CHARGE_MA = 500.0
# Exposure limits (US OSHA and MSHA defaults, decision D3)
AL, PEL = 25.0, 50.0       # ug/m3 RCS, 8 h TWA

print("DustBadge sizing, DBG-CAL-001 v0.2")
print(f"Geometry from cad/src/model.py: envelope {P['W']:.0f} x {P['D']:.0f} x {P['H']:.0f} mm, sensor {P['sensor']} mm")

# ------------------------------------------------------------------ A. Power and run time (R7)
e_cell = CELL_MAH / 1000 * CELL_V
e_use = e_cell * USABLE
tag("A1", f"Cell energy {e_cell:.2f} Wh nominal; usable {e_use:.2f} Wh at {USABLE:.0%}; {e_use * COLD:.2f} Wh at 0 degC")
e_alert = ALERTS * T_ALERT * P_MOTOR / 3600
tag("A2", f"Alerts: {ALERTS} x {T_ALERT:.0f} s of vibration = {e_alert * 1000:.1f} mWh per shift (negligible)")
run = {}
for name, i in I_SENS.items():
    p_in = i * V_SENS / ETA_BOOST + P_CTRL
    h = (e_use - e_alert) / p_in
    hc = (e_use * COLD - e_alert) / p_in
    run[name] = (p_in, h, hc)
    tag("A3", f"Sensor {name} {i * 1000:.0f} mA: {p_in * 1000:.0f} mW from the cell; run time {h:.1f} h at 25 degC, {hc:.1f} h at 0 degC")
worst_p = run["maximum"][0]
need_wh = worst_p * SHIFT_H + e_alert
need_mah = need_wh / (CELL_V * USABLE * COLD) * 1000
tag("A4", f"12 h at the maximum current and 0 degC needs {need_wh:.2f} Wh usable, a cell of about {need_mah:.0f} mAh")
need_mah_25 = need_wh / (CELL_V * USABLE) * 1000
tag("A5", f"12 h at the maximum current and 25 degC needs about {need_mah_25:.0f} mAh")
space_y = -P["wall"] - (P["cell_y"] + P["cell"][1] / 2)
tag("A6", f"Cell {CELL_MAH:,.0f} mAh, {P['cell'][1]:.1f} mm thick; space behind it to the rear wall {space_y:.1f} mm; "
          f"worst-case need {need_mah:.0f} mAh, margin {CELL_MAH - need_mah:.0f} mAh ({CELL_MAH / need_mah - 1:.0%})")

# ------------------------------------------------------------------ B. Charging
t_cc = 0.8 * CELL_MAH / CHARGE_MA
t_chg = t_cc + 1.0
tag("B1", f"Charge at {CHARGE_MA:.0f} mA ({CHARGE_MA / CELL_MAH:.2f} C): about {t_cc:.1f} h constant current plus about 1 h taper = {t_chg:.1f} h")

# ------------------------------------------------------------------ C. Badge temperature (R11)
A_exp = D["surface_m2"] - D["front_area_m2"]       # rear face against the wearer treated as adiabatic
H_COMB = 10.0             # W/(m2 K), natural convection plus radiation with light air movement (assumed)
ALPHA = 0.45              # solar absorptance of high-visibility yellow PETG (assumed)
G_SUN = 1000.0            # W/m2 normal to the front face
p_el = run["typical high"][0]
q_sun = ALPHA * G_SUN * D["front_area_m2"]
for case, q in (("shade", p_el), ("full sun", p_el + q_sun)):
    dt = q / (H_COMB * A_exp)
    tag("C1", f"{case}: {q:.2f} W into {A_exp * 1e4:.0f} cm2 of exposed surface; rise {dt:.1f} K; "
               f"{30 + dt:.1f} degC at 30 degC ambient, {45 + dt:.1f} degC at 45 degC ambient")
dt_sun = (p_el + q_sun) / (H_COMB * A_exp)
tag("C2", f"Highest ambient in full sun that keeps the shell at or below the sensor's 40 degC best-performance limit: {T_BEST[1] - dt_sun:.1f} degC; "
          f"at or below its {T_OPER_MAX:.0f} degC operating limit: {T_OPER_MAX - dt_sun:.1f} degC")

RULE_T = 40.0             # degC, use rule (DBG-DDR-002 D10): wear shaded when ambient exceeds this in full sun
dt_shade = p_el / (H_COMB * A_exp)
tag("C3", f"Use rule, wear shaded above {RULE_T:.0f} degC ambient in full sun: worst shell {RULE_T + dt_sun:.1f} degC in full sun at {RULE_T:.0f} degC, "
          f"{45 + dt_shade:.1f} degC shaded at 45 degC; both under the {T_OPER_MAX:.0f} degC operating limit (margin {T_OPER_MAX - max(RULE_T + dt_sun, 45 + dt_shade):.1f} K); "
          f"above the {T_BEST[1]:.0f} degC best-performance limit in full sun above {T_BEST[1] - dt_sun:.1f} degC ambient")

# ------------------------------------------------------------------ D. PM4 against the respirable convention (R1)
RHO_Q = 2.65              # g/cm3, quartz


def e_resp(da):
    """ISO 7708 respirable convention as a fraction of total airborne particles."""
    ei = 0.5 * (1 + math.exp(-0.06 * da))
    return ei * (1 - phi(math.log(da / 4.25) / math.log(1.5)))


tag("D1", f"ISO 7708 respirable fraction at 4.0 um aerodynamic: {e_resp(4.0):.2f} (50 % cut near 4 um)")
for dopt in (1.0, 2.5, 4.0, 10.0):
    da = dopt * math.sqrt(RHO_Q)      # spherical quartz; optical diameter taken as the geometric diameter
    tag("D2", f"Quartz sphere {dopt:.1f} um geometric = {da:.1f} um aerodynamic; respirable fraction {e_resp(da):.2f}")
tag("D3", "So an ideal PM4 channel sized optically would include quartz up to 6.5 um aerodynamic, where only about a tenth is respirable,"
          " while the SPS30 infers PM4 from its fine-particle distribution and under-sees coarse grains; the site factor must absorb both")

# ------------------------------------------------------------------ E. Working range (R2)
tag("E1", f"Sensor mass range 0 to {RANGE_MAX:.0f} ug/m3; R2 as restated (DBG-DDR-002 D11) 0 to 1,000 ug/m3 with over-range flag; "
          f"the TRL 2 target of 5,000 ug/m3 was {RANGE_MAX / 5000:.0%} covered")
for f in (0.025, 0.05, 0.10, 0.30, 0.80):
    tag("E2", f"Silica fraction {f:.1%}: respirable dust at the action level {AL / f:,.0f} ug/m3, at the limit {PEL / f:,.0f} ug/m3"
              f" ({'in range' if PEL / f <= RANGE_MAX else 'limit beyond range'})")
tag("E3", f"Lowest silica fraction for which the {PEL:.0f} ug/m3 limit is in range: {PEL / RANGE_MAX:.1%}; for the action level: {AL / RANGE_MAX:.1%}")
tag("E4", "An over-range minute is logged at the range limit and flagged, and it counts toward the projection at no less than that limit (fail-safe)")

# ------------------------------------------------------------------ F. Error budget for the shift average (R3)
Q_SAMP = 2.5              # L/min, cyclone sampler flow (assumed)
T_SAMP = 8 * 60           # min
W_UNC = 0.010             # mg, weighing and blank uncertainty per filter (assumed)
V_SAMP = Q_SAMP * T_SAMP / 1000
tag("F1", f"Reference filter sample: {Q_SAMP} L/min for 8 h = {V_SAMP:.2f} m3 of air")
terms_common = {"gravimetric method": 0.10, "site factor change between days and tasks": 0.20,
                "position on the chest and inlet screen": 0.10, "humidity below 80 % RH": 0.05,
                "sensor non-linearity after the site factor": 0.10}
for label, dust in (("quartz-rich stone, 80 % silica, at the action level", AL / 0.8),
                    ("quarry, 10 % silica, at the action level", AL / 0.1)):
    mass_mg = dust / 1000 * V_SAMP
    u_w = W_UNC / mass_mg
    drift = max(DRIFT_ABS / dust, DRIFT_REL) * 0.25    # 3 months between site factors
    for case, u_unit, u_site in (("same badge co-located, factor per task", 0.0, 0.10),
                                 ("factor shared across badges, per site", 0.10, 0.20)):
        terms = dict(terms_common)
        terms["site factor change between days and tasks"] = u_site
        terms.update({"filter weighing": u_w, "badge-to-badge after a CalRig check": u_unit, "drift over 3 months": drift})
        tot = math.sqrt(sum(v * v for v in terms.values()))
        tag("F2", f"{label}: dust {dust:.0f} ug/m3, filter mass {mass_mg:.3f} mg; {case}: "
                  + ", ".join(f"{k} {v:.0%}" for k, v in terms.items() if v) + f"; combined +/-{tot:.0%} (target 25 %)")
q2, n2 = 4.2, 2
mass2 = (AL / 0.8) / 1000 * q2 * T_SAMP / 1000 * n2
u_w2 = W_UNC / mass2
tot2 = math.sqrt(0.10 ** 2 + 0.10 ** 2 + 0.10 ** 2 + 0.05 ** 2 + 0.10 ** 2 + u_w2 ** 2 + (0.25 * DRIFT_ABS / (AL / 0.8)) ** 2)
tot2s = math.sqrt(tot2 ** 2 - 0.10 ** 2 + 0.20 ** 2 + 0.10 ** 2)
tag("F3", f"Reference rule for low-dust, high-silica sites (DBG-DDR-002 D9): a {q2} L/min cyclone over {n2} shifts collects {mass2:.3f} mg, weighing {u_w2:.0%}; "
          f"combined +/-{tot2:.0%} for the same badge co-located with a factor per task, +/-{tot2s:.0%} with a factor shared across badges per site")
tag("F4", f"Before a site factor the PM4 precision alone is +/-{PREC_PM4_ABS:.0f} ug/m3 below 100 ug/m3: "
          f"{PREC_PM4_ABS / (AL / 0.8):.0%} of the dust level at the action level for 80 % silica stone")

# ------------------------------------------------------------------ G. Alert logic (R4, R5, R6)
SHIFT = 480               # min, 8 h shift for the scenarios
WIN = 60                  # min, rolling window for the projection rate; projection starts once the window is full
PEAK = 10 * AL            # ug/m3 RCS, 1 min mean that triggers the brief peak alert


def simulate(conc):
    dose, first_al, first_pel, peaks = 0.0, None, None, 0
    for t in range(SHIFT):
        dose += conc[t]
        if t + 1 < WIN:
            proj = dose / 480
        else:
            rate = sum(conc[t - WIN + 1:t + 1]) / WIN
            proj = (dose + rate * (SHIFT - t - 1)) / 480
        if proj > AL and first_al is None:
            first_al = t + 1
        if proj > PEL and first_pel is None:
            first_pel = t + 1
        if conc[t] > PEAK and (t == 0 or conc[t - 1] <= PEAK):
            peaks += 1
    return dose / 480, first_al, first_pel, peaks


def scen(base, events):
    c = [base] * SHIFT
    for start, dur, level in events:
        for t in range(start, start + dur):
            c[t] = level
    return c


scenarios = {
    "S1 steady 30 ug/m3 all shift": scen(30, []),
    "S2 background 10, 2 min dry cut at 1,000 every hour": scen(10, [(30 + 60 * k, 2, 1000) for k in range(8)]),
    "S3 background 15, one 1 min truck pass at 110": scen(15, [(60, 1, 110)]),
    "S4 background 5 (well controlled)": scen(5, []),
    "S5 background 10, one 2 min dry cut at 1,000": scen(10, [(30, 2, 1000)]),
}
for name, c in scenarios.items():
    twa, t_al, t_pel, peaks = simulate(c)
    tag("G1", f"{name}: 8 h TWA {twa:.1f} ug/m3 RCS; projected action-level alert "
              f"{'at minute ' + str(t_al) if t_al else 'none'}; limit alert {'at minute ' + str(t_pel) if t_pel else 'none'}; peak alerts {peaks}")
tag("G2", f"Readings every 1 s (sensor), logged as 1 min means; projection rate from a {WIN} min rolling mean; projection from minute {WIN}, before that the dose so far; peak alert when a 1 min mean exceeds {PEAK:.0f} ug/m3 RCS")

# ------------------------------------------------------------------ H. Shift log (R12)
REC = 16                  # bytes: time 4, PM4 2, PM2.5 2, RCS estimate 2, TWA 2, RH 1, T 1, flags 1, spare 1
FLASH = 2 * 1024 * 1024
per_shift = REC * 60 * SHIFT_H
tag("H1", f"Log {REC} B per minute x {SHIFT_H * 60:.0f} min = {per_shift / 1000:.1f} kB per 12 h shift; 30 shifts {30 * per_shift / 1000:.0f} kB "
          f"= {30 * per_shift / FLASH:.0%} of 2 MB flash; capacity {int(FLASH // per_shift)} shifts")
BLE = 2000                # B/s effective, conservative for a phone link
tag("H2", f"Transfer of one shift at {BLE / 1000:.0f} kB/s effective: {per_shift / BLE:.0f} s")

# ------------------------------------------------------------------ I. Breathing zone (R8)
tag("I1", f"Inlet {D['inlet_to_face_mm']:.0f} mm from the nose and mouth midpoint (badge {P['mount_drop']:.0f} mm below, "
          f"{P['mount_lateral']:.0f} mm to the side); target 300 mm")
max_drop = math.sqrt(300 ** 2 - (P["mount_lateral"] + D["inlet_x"]) ** 2 - P["mount_forward"] ** 2) - P["H"] / 2
tag("I2", f"Lowest mount that still meets 300 mm: badge center {max_drop:.0f} mm below the nose and mouth midpoint")

# ------------------------------------------------------------------ J. Size and mass (R9)
m = masses(P)
tot_m = sum(m.values())
ov = D["overall"]
tag("J1", "Mass: " + ", ".join(f"{k} {v:.1f} g" for k, v in m.items()))
tag("J2", f"Total mass {tot_m:.1f} g (target 120 g, margin {120 - tot_m:.1f} g); envelope {ov[0]:.0f} x {ov[2]:.0f} x {ov[1]:.0f} mm "
          f"including the clip (target 75 x 55 x 35 mm)")
tag("J3", f"The {CELL_MAH:,.0f} mAh cell ({P['m_cell']:.0f} g) adds {P['m_cell'] - 30.0:.0f} g over the 1,500 mAh cell of CAL-001 v0.1 (30 g); margin to 120 g {120 - tot_m:.1f} g")

# ------------------------------------------------------------------ K. Drop (R10)
g = 9.81
v = math.sqrt(2 * g * 1.5)
for s_mm in (1.0, 2.0):
    a = v ** 2 / (2 * s_mm / 1000)
    tag("K1", f"1.5 m drop: impact {v:.2f} m/s, {tot_m / 1000 * g * 1.5:.2f} J; with {s_mm:.0f} mm of crush, {a / g:,.0f} g mean deceleration; "
              f"sensor ({P['m_sensor']} g) needs {P['m_sensor'] / 1000 * a:.0f} N of retention, cell {P['m_cell'] / 1000 * a:.0f} N")

# ------------------------------------------------------------------ L. Cost (R15)
rows = list(csv.DictReader((ROOT / "bom" / "bom.csv").open()))
cost = sum(float(r["qty"]) * float(r["unit_cost_usd"]) for r in rows)
budget = float(yaml.safe_load((ROOT / "project.yaml").read_text())["budget_usd"])
sensor_cost = next(float(r["unit_cost_usd"]) for r in rows if r["item"].startswith("3 "))
m_txt = f"margin ${budget - cost:.2f}" if cost <= budget else f"over budget by ${cost - budget:.2f}"
tag("L1", f"BOM {len(rows)} lines, total ${cost:.2f} against budget_usd ${budget:.0f}; {m_txt}; "
          f"particle sensor {sensor_cost / cost:.0%} of the total")

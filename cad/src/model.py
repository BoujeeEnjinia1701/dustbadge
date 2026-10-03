"""DustBadge parametric model (build123d), TRL 3, constructable design.
Revised 2026-09-25 for DBG-DDR-002 (2,000 mAh cell, 11.5 mm thick).
Revised 2026-10-02 for the worn version (DBG-DDR-003, A1, decided 2026-10-02): rear shell 1 mm deeper
(rear face at Y = rear_extra) and a foam pad behind the cell.
Revised 2026-09-30 for DBG-DDR-003 (design for construction): shell screws and rear bosses,
TPU gasket, sensor port seals and stop ribs, screen under the inlet seal, cell locating ribs,
clip screws, the carrier board's modules placed and the light pipe given a flange and an LED.

Run from the repo root:  python cad/src/model.py            exports STEP and STL, prints the checks
                         python cad/src/model.py --check    prints the constructability checks only
Exports STEP and STL into cad/step and cad/stl:
    dustbadge-assembly.step / .stl   the whole badge with its bought-in parts
    front-shell.step / .stl          printed front shell with inlet and outlet slots
    rear-shell.step / .stl           printed rear shell with the clip mount

Axes (badge frame, mm): X across the badge, Z up, Y from the wearer outward is negative.
The rear face (against the wearer) is at Y = 0 and the front face at Y = -depth. The badge
center is on the Z axis at Z = 0, so the kit's cutaway (which cuts near the origin) works.
Bought parts are drawn as envelopes. The same PARAMS feed docs/04-calcs/sizing.py
(DBG-CAL-001), the drawing DBG-DWG-001 (cad/src/sheets.py), the concept media
(cad/src/concept_media.py) and the build plan pictures (cad/src/build_plan_media.py).
"""
import math
import sys
from pathlib import Path

# Top-level parameters (mm unless stated). Edit these, not the geometry below.
PARAMS = {
    # envelope and shells (1 front, 9 rear)
    "W": 64.0, "H": 52.0, "D": 30.0,        # width X, height Z, depth Y (shells only, clip excluded)
    "wall": 2.0,
    "rear_extra": 1.0,                       # rear shell deeper by this much: rear face at Y = rear_extra (worn version)
    "split_y": -14.0,                        # Y of the front shell's rim (the gasket sits on it)
    "gasket_t": 1.0,                         # flat TPU gasket between the rims, squeezed thickness
    "corner_r": 4.0,                         # vertical edge radius
    "boss_d": 5.0,                           # three screw bosses in the front shell, clear of the sensor
    "rear_boss_d": 4.5,                      # matching tubes in the rear shell that press on the board
    "bosses": ((-27.0, 21.0), (27.0, 21.0), (27.0, -21.0)),   # X, Z; the board rests on them
    "boss_end_y": -15.8,                     # front boss ends; the board's front face
    "screw_len": 20.0,                       # M2 x 20 thread-forming screws through the rear shell
    "cbore": (4.2, 1.4),                     # counterbore in the rear face for the screw heads (dia, depth)
    # 3 particle sensor, SPS30 class: 41 x 41 x 12 mm, inlet and outlet on the lower edge
    "sensor": (41.0, 12.0, 41.0),            # X, Y, Z
    "sensor_x": -9.0, "sensor_y": -21.8,     # center; ports face down onto the slots
    "sensor_port": (9.0, 6.0),               # inlet and outlet port size on the sensor edge (X, Y)
    "sensor_port_dx": 10.0,                  # inlet at -dx, outlet at +dx from the sensor center
    "rib_x": (-20.0, 2.0), "rib_t": 1.2, "rib_y1": -21.0,   # two stop ribs above the sensor (front shell)
    # 2 inlet screen under the inlet seal; two slots in the bottom face of the front shell
    "slot": (12.0, 7.0),                     # X, Y of each slot
    "screen": (16.0, 11.0, 0.3),             # mesh square laid on the inner floor over the inlet slot
    "seal": (16.0, 11.0), "seal_t": (0.7, 1.0),   # printed TPU port seals: inlet (on the screen), outlet
    # 4 controller module, 5 motor, 6 LED and light pipe
    "module": (17.5, 4.0, 21.0), "module_pos": (20.8, -17.8, 7.0),
    "motor_d": 10.0, "motor_t": 3.0, "motor_pos": (21.0, -26.5, -6.0),   # stuck to the front face inside
    "led_d": 4.0, "led_pos": (21.0, 20.0),   # X, Z of the light pipe through the front face
    "pipe_flange": (6.0, 1.0), "pipe_len": 7.0, "lamp": (3.0, 5.3),
    # 7 carrier board (perfboard) with the charger, boost and humidity modules
    "pcb": (59.0, 1.6, 47.0), "pcb_y": -15.0, "pcb_chamfer": 1.5,
    "pcb_notch": (3.0, 4.0), "pcb_notch_z": -10.0,       # notch in the right edge for the cell lead
    "charger": (11.0, 4.0, 19.0), "charger_x": 18.1,     # on the board, USB-C on its lower edge
    "usb": (8.9, 3.2, 7.3), "usb_recess": 0.8,           # USB-C receptacle; mouth 0.8 mm inside the face
    "usb_x": 18.1,                                       # USB-C opening in the bottom face (X)
    "boost": (11.4, 3.0, 9.0), "boost_pos": (18.5, 4.0),  # X, Z of its lower left corner region, front face
    "rh": (10.0, 2.0, 10.0), "rh_vent_x": 18.5,          # humidity breakout on the floor; vent under it
    # 8 cell, 2,000 mAh protected LiPo (DBG-DDR-002 D8; was 1,500 mAh, 10 mm thick)
    "cell": (50.0, 11.5, 34.0), "cell_y": -8.25, "cell_mah": 2000.0,
    "cell_rib": (1.2, 4.0),                  # locating ribs on the rear shell: thickness, height
    "pad": (40.0, 1.0, 24.0), "pad_gap": 0.5,   # foam pad behind the cell (X, Y, Z), stuck to the rear wall; clear gap to the cell
    # 10 spring clip with strap loop, on the rear face
    "clip": (22.0, 3.0, 40.0), "clip_z": 4.0,
    "clip_holes": ((-6.0, 21.0), (6.0, 21.0)),   # X, Z of the two M2 x 8 clip screws
    "clip_leaf": 1.0,                         # base leaf thickness; screw heads sit on it
    # wearer interface (for R8): badge center relative to the midpoint of nose and mouth
    "mount_drop": 210.0,                     # below the nose and mouth midpoint (collar or upper strap)
    "mount_lateral": 70.0,                   # to one side of the midline
    "mount_forward": 10.0,                   # inlet forward of the face plane (badge proud of the chest)
    # masses of bought-in parts (g), for R9; shells, gasket and seals from volume
    "m_sensor": 26.3, "m_cell": 38.0, "m_module": 3.0, "m_board": 9.0, "m_motor": 1.0,
    "m_led": 0.5, "m_screen": 0.4, "m_clip": 6.0, "m_hardware": 3.0, "m_pad": 0.2,
    "rho_petg": 1.27, "rho_tpu": 1.21,       # g/cm3
}


def derived(p=PARAMS):
    """Dimensions and figures the calc note and drawing quote, computed from PARAMS."""
    W, H, D = p["W"], p["H"], p["D"]
    sx, sy, sz = p["sensor"]
    inlet_x = p["sensor_x"] - p["sensor_port_dx"]
    outlet_x = p["sensor_x"] + p["sensor_port_dx"]
    # inlet position relative to the nose and mouth midpoint
    inlet_z_rel = -p["mount_drop"] - H / 2
    dist = math.sqrt((p["mount_lateral"] + inlet_x) ** 2 + inlet_z_rel ** 2 + p["mount_forward"] ** 2)
    floor = -H / 2 + p["wall"]                        # inner floor
    s_bot = floor + p["screen"][2] + p["seal_t"][0]   # sensor rests on the inlet seal over the screen
    return {
        "overall": (W, D + p["rear_extra"] + p["clip"][1], H),            # X, Y incl. clip, Z
        "floor": floor,
        "sensor_bottom": s_bot, "sensor_top": s_bot + sz, "sensor_zc": s_bot + sz / 2,
        "inlet_x": inlet_x, "outlet_x": outlet_x,
        "inlet_to_face_mm": dist,
        "front_depth": D + p["split_y"],
        "rear_y0": p["split_y"] + p["gasket_t"],        # rim of the rear shell
        "rear_depth": p["rear_extra"] - (p["split_y"] + p["gasket_t"]),
        "rear_y": p["rear_extra"],                      # rear face
        "cell_back": p["cell_y"] + p["cell"][1] / 2,
        "pad_front": p["rear_extra"] - p["wall"] - p["pad"][1],
        "pcb_front": p["pcb_y"] - p["pcb"][1] / 2, "pcb_back": p["pcb_y"] + p["pcb"][1] / 2,
        "surface_m2": 2 * (W * H + W * D + H * D) * 1e-6,
        "front_area_m2": W * H * 1e-6,
    }


def _b3d():
    import build123d as b
    return b


def box(cx, cy, cz, sx, sy, sz):
    b = _b3d()
    return b.Pos(cx, cy, cz) * b.Box(sx, sy, sz)


def bx(x0, x1, y0, y1, z0, z1):
    return box((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2, abs(x1 - x0), abs(y1 - y0), abs(z1 - z0))


def rounded_box(cx, cy, cz, sx, sy, sz, r):
    """Box with its four edges parallel to Y rounded (the badge outline seen from the front)."""
    b = _b3d()
    shape = b.Box(sx, sy, sz)
    edges = shape.edges().filter_by(b.Axis.Y)
    shape = b.fillet(edges, r)
    return b.Pos(cx, cy, cz) * shape


def ycyl(x, y, z, r, h):
    b = _b3d()
    return b.Pos(x, y, z) * b.Rot(90, 0, 0) * b.Cylinder(r, h)


def ycyl2(x, z, y0, y1, r):
    """Cylinder along Y from y0 to y1."""
    return ycyl(x, (y0 + y1) / 2, z, r, abs(y1 - y0))


def fuse(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


def _seal(cx, cy, z0, t, p):
    ox, oy = p["seal"]
    ix, iy = p["sensor_port"]
    return bx(cx - ox / 2, cx + ox / 2, cy - oy / 2, cy + oy / 2, z0, z0 + t) - \
        bx(cx - ix / 2, cx + ix / 2, cy - iy / 2, cy + iy / 2, z0 - 1, z0 + t + 1)


def _screw(x, z, y_head, length, head=(3.8, 1.3), d=2.0, toward=-1):
    """Pan-head screw along Y. Head underside at y_head; shank runs toward -Y (toward=-1)."""
    hd, hh = head
    h = ycyl2(x, z, y_head, y_head - toward * hh, hd / 2)
    s = ycyl2(x, z, y_head, y_head + toward * length, d / 2)
    return h + s


def build_parts(p=PARAMS):
    """Return an ordered dict: key -> (name, shape, color, bom line)."""
    W, H, D, t = p["W"], p["H"], p["D"], p["wall"]
    sy_ = p["split_y"]
    r = p["corner_r"]
    sx, sdy, sz = p["sensor"]
    d = derived(p)
    fl = d["floor"]
    pf, pb = d["pcb_front"], d["pcb_back"]
    parts = {}

    # 1 front shell: from Y = -D to split, open toward the rear
    fd = D + sy_
    outer = rounded_box(0, (-D + sy_) / 2, 0, W, fd, H, r)
    inner = rounded_box(0, (-D + t + sy_) / 2 + 0.5, 0, W - 2 * t, fd - t + 1, H - 2 * t, max(r - t, 0.5))
    front = outer - inner
    # screw bosses from the inside of the front face back to the board, with screw holes
    by0, by1 = -D + t, p["boss_end_y"]
    for bxx, bz in p["bosses"]:
        front = front + ycyl2(bxx, bz, by0 - 0.01, by1, p["boss_d"] / 2)
    for bxx, bz in p["bosses"]:
        front = front - ycyl2(bxx, bz, by1 + 1, -D + t + 1.0, 1.0)
    # two stop ribs above the sensor, from the front face back 7 mm, 0.2 mm above it
    rt = p["rib_t"]
    for rx in p["rib_x"]:
        front = front + bx(rx - rt / 2, rx + rt / 2, -D + t - 0.01, p["rib_y1"], d["sensor_top"] + 0.2, H / 2 - t + 0.01)
    # bottom slots: sensor inlet (screened) and outlet, USB-C, humidity vent
    slx, sly = p["slot"]
    for xx in (d["inlet_x"], d["outlet_x"]):
        front = front - box(xx, p["sensor_y"], -H / 2, slx, sly, 2 * t + 2)
    ux, uy, uz = p["usb"]
    usb_y = pf - p["charger"][1] / 2
    front = front - box(p["usb_x"], usb_y, -H / 2, ux + 0.7, uy + 0.6, 2 * t + 2)
    rh_y = -D + t + p["rh"][1] / 2
    front = front - box(p["rh_vent_x"], rh_y, -H / 2, 3.0, 2.0, 2 * t + 2)
    # LED light pipe hole in the front face
    lx, lz = p["led_pos"]
    front = front - ycyl(lx, -D + t / 2, lz, p["led_d"] / 2 + 0.2, t + 2)
    parts["front"] = ("Front shell with bottom inlet", front, "#EAB308", 1)

    # 2 inlet screen, laid on the inner floor over the inlet slot
    scx, scy, sct = p["screen"]
    parts["screen"] = ("Inlet dust screen", bx(d["inlet_x"] - scx / 2, d["inlet_x"] + scx / 2, p["sensor_y"] - scy / 2,
                                                p["sensor_y"] + scy / 2, fl, fl + sct), "#374151", 2)
    # port seals (printed TPU, BOM line 9): inlet on the screen, outlet on the floor
    seals = _seal(d["inlet_x"], p["sensor_y"], fl + sct, p["seal_t"][0], p) + \
        _seal(d["outlet_x"], p["sensor_y"], fl, p["seal_t"][1], p)
    parts["seals"] = ("Sensor port seals (TPU)", seals, "#1F2937", 9)

    # 3 particle sensor with its two ports facing down onto the seals
    sensor = box(p["sensor_x"], p["sensor_y"], d["sensor_zc"], sx, sdy, sz)
    parts["sensor"] = ("Optical particle sensor (SPS30 class)", sensor, "#0F766E", 3)

    # 4 controller, 5 motor, 6 light pipe and LED
    mx, my, mz = p["module_pos"]
    parts["module"] = ("Controller and BLE module", box(mx, my, mz, *p["module"]), "#1D4ED8", 4)
    ox, oy, oz = p["motor_pos"]
    parts["motor"] = ("Vibration motor", ycyl(ox, oy, oz, p["motor_d"] / 2, p["motor_t"]), "#6B7280", 5)
    fdia, ft = p["pipe_flange"]
    y_in = -D + t                                       # inner face of the front wall
    pipe = ycyl2(lx, lz, -D - 1.0, y_in, p["led_d"] / 2) + ycyl2(lx, lz, y_in, y_in + ft, fdia / 2) + \
        ycyl2(lx, lz, y_in + ft, -D - 1.0 + p["pipe_len"], p["led_d"] / 2)
    ld, ll = p["lamp"]
    pocket_y0 = -D - 1.0 + p["pipe_len"] - 2.5
    pipe = pipe - ycyl2(lx, lz, pocket_y0, pocket_y0 + 5, ld / 2)
    parts["led"] = ("Alert light pipe", pipe, "#DC2626", 6)
    parts["lamp"] = ("Red LED, 3 mm", ycyl2(lx, lz, pocket_y0, pocket_y0 + ll, ld / 2), "#991B1B", 6)

    # 7 carrier board (perfboard) with screw holes, and its modules
    bx_, by_, bz_ = p["pcb"]
    pcb = box(0, p["pcb_y"], 0, bx_, by_, bz_)
    for hx, hz in p["bosses"]:
        pcb = pcb - ycyl(hx, p["pcb_y"], hz, 1.1, by_ + 1)
    import build123d as b_
    cf = p["pcb_chamfer"]
    for sxx in (-1, 1):                                  # corners cut to clear the shells' inside corners
        for szz in (-1, 1):
            pcb = pcb - b_.Pos(sxx * bx_ / 2, p["pcb_y"], szz * bz_ / 2) * b_.Rot(0, 45, 0) * b_.Box(cf * 2 ** 0.5, by_ + 2, cf * 2 ** 0.5)
    nx, nz = p["pcb_notch"]
    pcb = pcb - bx(bx_ / 2 - nx, bx_ / 2 + 1, p["pcb_y"] - 2, p["pcb_y"] + 2, -nz / 2 + p["pcb_notch_z"], nz / 2 + p["pcb_notch_z"])
    parts["pcb"] = ("Carrier board (perfboard)", pcb, "#15803D", 7)
    cx_, cy_, cz_ = p["charger"]
    ch = bx(p["charger_x"] - cx_ / 2, p["charger_x"] + cx_ / 2, pf - cy_, pf, fl, fl + cz_)
    ch = ch + box(p["usb_x"], usb_y, -H / 2 + p["usb_recess"] + uz / 2, ux, uy, uz)
    parts["charger"] = ("Charger module with USB-C", ch, "#16A34A", 7)
    bsx, bsy, bsz = p["boost"]
    bxc, bz0 = p["boost_pos"]
    parts["boost"] = ("5 V boost module", bx(bxc - bsx / 2, bxc + bsx / 2, y_in, y_in + bsy, bz0, bz0 + bsz), "#22C55E", 7)
    rx_, ry_, rz_ = p["rh"]
    parts["rh"] = ("Humidity sensor breakout", bx(p["rh_vent_x"] - rx_ / 2, p["rh_vent_x"] + rx_ / 2, y_in, y_in + ry_, fl, fl + rz_),
                   "#4ADE80", 7)

    # 8 cell behind the board
    parts["cell"] = (f"LiPo cell, {p['cell_mah']:,.0f} mAh, protected", box(0, p["cell_y"], 0, *p["cell"]), "#C2410C", 8)

    # gasket (BOM line 9): flat frame the shape of the rim
    g0 = sy_
    gout = rounded_box(0, g0 + p["gasket_t"] / 2, 0, W, p["gasket_t"], H, r)
    gin = rounded_box(0, g0 + p["gasket_t"] / 2, 0, W - 2 * t, p["gasket_t"] + 1, H - 2 * t, max(r - t, 0.5))
    parts["gasket"] = ("Gasket (TPU)", gout - gin, "#111827", 9)

    # 9 rear shell: from the gasket to Y = 0, closed at the back, with bosses and ribs
    ry0 = d["rear_y0"]
    Y0 = p["rear_extra"]                               # rear face
    rd = Y0 - ry0
    outer = rounded_box(0, (ry0 + Y0) / 2, 0, W, rd, H, r)
    inner = rounded_box(0, (ry0 + Y0 - t) / 2 - 0.5, 0, W - 2 * t, rd - t + 1, H - 2 * t, max(r - t, 0.5))
    rear = outer - inner
    for hx, hz in p["bosses"]:                         # tubes that press the board onto the front bosses
        rear = rear + ycyl2(hx, hz, Y0 - t + 0.01, pb, p["rear_boss_d"] / 2)
    for hx, hz in p["clip_holes"]:                     # bosses for the clip screws
        rear = rear + ycyl2(hx, hz, Y0 - t + 0.01, Y0 - 7.5, p["boss_d"] / 2)
    cw, chh = p["cell_rib"]
    ccx, ccy, ccz = p["cell"]
    yr0, yr1 = Y0 - t + 0.01, Y0 - t - chh
    for sgn in (-1, 1):                                # cell locating ribs, 0.2 mm off the cell
        x0 = sgn * (ccx / 2 + 0.2)
        rear = rear + bx(x0, x0 + sgn * cw, yr0, yr1, -6, 6)
        z0 = sgn * (ccz / 2 + 0.2)
        rear = rear + bx(-2.5, 2.5, yr0, yr1, z0, z0 + sgn * cw)
    cbd, cbh = p["cbore"]
    for hx, hz in p["bosses"]:
        rear = rear - ycyl2(hx, hz, Y0 + 1, pb - 1, 1.2) - ycyl2(hx, hz, Y0 + 1, Y0 - cbh, cbd / 2)
    for hx, hz in p["clip_holes"]:
        rear = rear - ycyl2(hx, hz, Y0 + 1, Y0 - 7.0, 1.0)
    parts["rear"] = ("Rear shell", rear, "#374151", 9)

    # foam pad (BOM line 13): stuck to the inside of the rear wall behind the cell, clear of it by pad_gap
    pw, pt, ph = p["pad"]
    parts["pad"] = ("Foam pad behind the cell", bx(-pw / 2, pw / 2, Y0 - t - pt, Y0 - t, -ph / 2, ph / 2), "#F59E0B", 13)

    # shell screws: M2 x 20, heads in the counterbores, into the front bosses
    parts["screws"] = ("Shell screws M2 x 20 (3)", fuse([_screw(hx, hz, Y0 - cbh, p["screw_len"]) for hx, hz in p["bosses"]]),
                       "#111827", 11)

    # 10 spring clip with strap loop, and its two screws
    cx_, cy_, cz_ = p["clip"]
    clip = box(0, Y0 + cy_ / 2, p["clip_z"], cx_, cy_, cz_) - box(0, Y0 + cy_ / 2, p["clip_z"] - cz_ / 2 + 7, cx_ - 8, cy_ + 2, 6)
    lf = p["clip_leaf"]
    for hx, hz in p["clip_holes"]:
        clip = clip - ycyl2(hx, hz, Y0 - 1, Y0 + cy_ + 1, 1.1) - ycyl2(hx, hz, Y0 + lf, Y0 + cy_ + 1, 2.2)
    parts["clip"] = ("Spring clip and strap loop", clip, "#9CA3AF", 10)
    parts["clip_screws"] = ("Clip screws M2 x 8 (2)", fuse([_screw(hx, hz, Y0 + lf, 8.0) for hx, hz in p["clip_holes"]]),
                            "#111827", 11)
    return parts


def masses(p=PARAMS, parts=None):
    """Mass breakdown in grams: printed parts from model volume, bought-in parts from PARAMS."""
    parts = parts or build_parts(p)
    rho = p["rho_petg"] / 1000.0                      # g per mm3
    rt = p["rho_tpu"] / 1000.0
    m = {"front shell (PETG)": parts["front"][1].volume * rho,
         "rear shell (PETG)": parts["rear"][1].volume * rho,
         "particle sensor": p["m_sensor"], "cell": p["m_cell"], "controller module": p["m_module"],
         "carrier board and modules": p["m_board"], "motor": p["m_motor"], "LED and light pipe": p["m_led"],
         "screen": p["m_screen"], "foam pad": p["m_pad"], "clip": p["m_clip"], "screws, wire, adhesive": p["m_hardware"],
         "gasket and port seals (TPU)": (parts["gasket"][1].volume + parts["seals"][1].volume) * rt}
    return m


def assembly(p=PARAMS):
    b = _b3d()
    return b.Compound([s for (_, s, _, _) in build_parts(p).values()])


# ------------------------------------------------------------------ constructability checks
def _vol(a, b_):
    try:
        s = a & b_
        return s.volume if s is not None else 0.0
    except Exception:
        return float("nan")


def checks(p=PARAMS):
    """Pairs that must not overlap, and the gap or contact between them (mm). Returns a list of
    (description, overlap volume mm3, gap mm, expectation, ok)."""
    P_ = build_parts(p)
    S = lambda k: P_[k][1]  # noqa: E731
    rows = []

    def chk(desc, a, b_, expect):
        v = _vol(a, b_)
        gp = a.distance_to(b_)
        ok = v < 1e-3 and (gp < 0.05 if expect == "touch" else gp >= expect - 1e-6)
        rows.append((desc, v, gp, expect, ok))

    chk("Screen on the inner floor over the inlet slot", S("screen"), S("front"), "touch")
    chk("Port seals on the screen and floor", S("seals"), S("screen") + S("front"), "touch")
    chk("Sensor resting on the port seals", S("sensor"), S("seals"), "touch")
    chk("Sensor clear of the front shell walls", S("sensor"), S("front"), 0.15)
    chk("Sensor against the carrier board", S("sensor"), S("pcb"), "touch")
    chk("Sensor clear of the screen", S("sensor"), S("screen"), 0.5)
    chk("Carrier board on the front bosses", S("pcb"), S("front"), "touch")
    chk("Rear bosses on the carrier board", S("rear"), S("pcb"), "touch")
    chk("Gasket on the front shell rim", S("gasket"), S("front"), "touch")
    chk("Gasket under the rear shell rim", S("gasket"), S("rear"), "touch")
    chk("Shell screws seated in the rear counterbores", S("screws"), S("rear"), "touch")
    chk("Shell screws clear of the cell", S("screws"), S("cell"), 1.0)
    chk("Shell screws clear of the sensor", S("screws"), S("sensor"), 1.0)
    for k in ("module", "charger"):
        chk(f"{P_[k][0]} on the carrier board", S(k), S("pcb"), "touch")
        chk(f"{P_[k][0]} clear of the sensor", S(k), S("sensor"), 0.5)
        chk(f"{P_[k][0]} clear of the shell screws and bosses", S(k), S("screws") + S("rear"), 0.3)
    chk("Controller module clear of the front shell", S("module"), S("front"), 0.3)
    chk("Charger USB-C in its opening, module on the floor", S("charger"), S("front"), "touch")
    chk("Charger and controller apart", S("charger"), S("module"), 1.0)
    for k in ("motor", "boost", "rh"):
        chk(f"{P_[k][0]} stuck to the front face inside", S(k), S("front"), "touch")
        chk(f"{P_[k][0]} clear of the board's modules", S(k), S("module") + S("charger") + S("pcb"), 3.0)
        chk(f"{P_[k][0]} clear of the sensor", S(k), S("sensor"), 1.0)
    chk("Motor clear of the boost module", S("motor"), S("boost"), 1.0)
    chk("Motor clear of the humidity breakout", S("motor"), S("rh"), 1.0)
    chk("Light pipe flange on the front face", S("led"), S("front"), "touch")
    chk("LED in the light pipe pocket", S("lamp"), S("led"), "touch")
    chk("Light pipe and LED clear of the modules", S("led") + S("lamp"), S("module") + S("boost"), 1.0)
    chk("Cell clear of the carrier board", S("cell"), S("pcb"), 0.15)
    chk("Cell clear of the rear shell (ribs and back)", S("cell"), S("rear"), 0.15)
    chk("Foam pad stuck to the rear wall behind the cell", S("pad"), S("rear"), "touch")
    chk("Foam pad clear of the cell (swelling room 0.5 mm before it presses)", S("pad"), S("cell"), 0.5)
    chk("Foam pad clear of the shell screws and clip screws", S("pad"), S("screws") + S("clip_screws"), 1.0)
    chk("Foam pad clear of the carrier board", S("pad"), S("pcb"), 2.0)
    chk("Cell clear of the clip screws", S("cell"), S("clip_screws"), 1.0)
    chk("Clip on the rear face", S("clip"), S("rear"), "touch")
    chk("Clip screws seated on the clip leaf", S("clip_screws"), S("clip"), "touch")
    chk("Clip screws in their bosses", S("clip_screws"), S("rear"), "touch")
    chk("Front and rear shells apart (gasket between)", S("front"), S("rear"), 0.0)
    return rows


def print_checks(p=PARAMS):
    rows = checks(p)
    bad = 0
    for desc, v, gp, exp, ok in rows:
        e = "touch" if exp == "touch" else f">= {exp:g} mm"
        print(f"  {'ok ' if ok else 'BAD'}  {desc:58s} overlap {v:8.3f} mm3  gap {gp:6.2f} mm  ({e})")
        bad += not ok
    print(f"constructability checks: {len(rows) - bad} of {len(rows)} pass")
    return bad


if __name__ == "__main__":
    if "--check" in sys.argv:
        sys.exit(1 if print_checks() else 0)
    from build123d import Compound, export_step, export_stl
    out = Path(__file__).resolve().parents[1]
    (out / "step").mkdir(exist_ok=True)
    (out / "stl").mkdir(exist_ok=True)
    parts = build_parts()
    groups = {"dustbadge-assembly": Compound([s for (_, s, _, _) in parts.values()]),
              "front-shell": parts["front"][1], "rear-shell": parts["rear"][1]}
    for name, c in groups.items():
        export_step(c, str(out / "step" / f"{name}.step"))
        export_stl(c, str(out / "stl" / f"{name}.stl"), tolerance=0.02, angular_tolerance=0.2)
    bb = groups["dustbadge-assembly"].bounding_box()
    m = masses(PARAMS, parts)
    print(f"assembly bounding box {bb.size.X:.1f} x {bb.size.Y:.1f} x {bb.size.Z:.1f} mm; mass {sum(m.values()):.1f} g")
    print("exported", ", ".join(groups))
    print_checks()

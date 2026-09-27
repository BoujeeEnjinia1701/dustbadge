"""DustBadge product appearance model (build123d), TRL 3.

Finished-product look for photoreal renders: filleted high-visibility front shell and dark rear
shell with a gasket parting line, ribbed side grips, a clear front window over the particle
sensor and its fan, a lit red alert light pipe, a printed status label, rear M2 screws, a
stainless spring clip with a webbing lanyard and breakaway buckle, and a fabric chest panel with
a harness strap for the worn view.
APPEARANCE MODEL ONLY: no tolerances, no fabrication detail. CONCEPT, NOT FOR FABRICATION.
A screening tool, not a compliance instrument.

Every main dimension and interface comes from PARAMS, derived() and build_parts() in model.py.
Axes as model.py: X across the badge, Z up, Y from the wearer outward is negative. The rear face
(against the wearer) is at Y = 0, the front face at Y = -D, and the badge centre is at Z = 0.

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from build123d import (Axis, Box, BuildLine, Compound, Cylinder, FilletPolyline, Plane, Pos,
                       RectangleRounded, Rot, Sphere, extrude, fillet, trace)
from model import PARAMS, derived, build_parts

TITLE = "DustBadge: wearable respirable dust monitor for workers"

RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "internal", "accessory"], "explode": False, "el": 30, "az": -40,
     "note": "Product render from the front right and above (about 30 deg elevation); window over the "
             "particle sensor at left, red alert light at top right, clip and lanyard behind"},
    {"name": "exploded", "groups": ["shell", "internal", "accessory"], "explode": True, "el": 28, "az": -55,
     "note": "Exploded view from the front right and above (about 28 deg elevation): window, front shell, "
             "sensor fan, optical particle sensor, controller, carrier board, cell, rear shell, spring clip "
             "and lanyard"},
    {"name": "worn", "groups": ["shell", "internal", "context"], "explode": False, "el": 14, "az": -32,
     "note": "Worn view from the front right, slightly above (about 14 deg elevation): badge clipped to a "
             "harness strap on a fabric chest panel, inlet facing down"},
]

# Colours (restrained product palette; hi-vis yellow front shell per DBG-DDR-001 D7; kit accent)
C_FRONT = "#E7B416"
C_REAR = "#353A42"
C_GASKET = "#1F2328"
C_ACCENT = "#0F766E"
C_WINDOW = "#DCEBF5"
C_LED = "#FF3B30"
C_LABEL = "#2B2F36"
C_WHITE = "#F4F4F2"
C_STEEL = "#B8BEC6"
C_MESH = "#6B7280"
C_FAN = "#1C1F24"
C_PCB = "#166534"
C_CHIP = "#111827"
C_CAN = "#C9CDD2"
C_POUCH = "#C4C8CD"
C_CELL_LABEL = "#1E3A5F"
C_WEB = "#2F3640"
C_PANEL = "#3B4A5C"
C_STRAP = "#2A2E34"
C_TAPE = "#D5D8DC"
C_STITCH = "#8A94A0"

# Appearance-only detail sizes (mm)
FIL_FRONT = 3.0        # front face perimeter
FIL_REAR = 2.5         # rear face perimeter
FIL_PART = 0.6         # both sides of the shell joint (forms the parting line)
WIN_C = (-9.0, -1.0)   # X, Z of the front window centre (over the sensor)
WIN = (30.0, 24.0)     # window opening, X by Z
WIN_R = 3.0
REAR_SCREWS = PARAMS["bosses"]   # rear screws line up with the three front-shell bosses
FAN_C = (-4.0, 1.0)    # X, Z of the fan recess on the sensor front face
FAN_R = 9.5


def _fillet_try(shape, edges, radii):
    """Fillet `edges` with the first radius that gives a valid solid; else return the input."""
    edges = list(edges)
    if not edges:
        return shape
    for r in radii:
        try:
            out = fillet(edges, r)
            if out.is_valid and out.volume > 0:
                return out
        except Exception:
            pass
    return shape


def _yslab(sx, sz, r, y0, t, x=0.0, z=0.0):
    """Rounded rectangle in the XZ plane (sx by sz, corner r) extruded from y0 toward +Y by t."""
    r = max(min(r, min(sx, sz) / 2 - 0.01), 0.01)
    pl = Plane(origin=(x, y0, z), x_dir=(1, 0, 0), z_dir=(0, 1, 0))
    return extrude(pl * RectangleRounded(sx, sz, r), amount=t)


def _ycyl(x, y0, z, r, t):
    """Cylinder along +Y from y0, length t."""
    return Pos(x, y0 + t / 2, z) * Rot(90, 0, 0) * Cylinder(r, t)


def _xcyl(x0, y, z, r, L):
    return Pos(x0 + L / 2, y, z) * Rot(0, 90, 0) * Cylinder(r, L)


def _outer_loop(shape, at_min_y):
    faces = shape.faces().sort_by(Axis.Y)
    f = faces[0] if at_min_y else faces[-1]
    return f.outer_wire().edges()


def _face_loop_at(shape, y):
    """Outer loop edges of the planar face lying at Y = y."""
    for f in shape.faces():
        bb = f.bounding_box()
        if abs(bb.min.Y - y) < 1e-3 and abs(bb.max.Y - y) < 1e-3:
            return f.outer_wire().edges()
    return []


# ---------------------------------------------------------------- shells
def _front_shell(P, m):
    W, H, D, t = P["W"], P["H"], P["D"], P["wall"]
    f = m["front"][1]
    f = _fillet_try(f, _outer_loop(f, True), [FIL_FRONT, 2.0, 1.2])
    f = _fillet_try(f, _face_loop_at(f, P["split_y"]), [FIL_PART, 0.4])
    # window opening and a shallow seat for the pane
    wx, wz = WIN_C
    f -= _yslab(WIN[0], WIN[1], WIN_R, -D - 1, t + 2, x=wx, z=wz)
    f -= _yslab(WIN[0] + 3.0, WIN[1] + 3.0, WIN_R + 1.5, -D - 1, 1.6, x=wx, z=wz)
    # counterbore around the light pipe for a bezel
    lx, lz = P["led_pos"]
    f -= _ycyl(lx, -D - 1, lz, P["led_d"] / 2 + 1.4, 1.5)
    # ribbed grip texture on both side faces
    for sx in (-1, 1):
        for k in range(7):
            z = -12.0 + 4.0 * k
            rib = Pos(sx * (W / 2 + 0.2), -D + 7.5, z) * Box(0.8, 10.0, 1.2)
            rib = _fillet_try(rib, rib.edges().filter_by(Axis.Y), [0.35, 0.2])
            f += rib
    return f


def _rear_shell(P, m):
    r = m["rear"][1]
    r = _fillet_try(r, _outer_loop(r, False), [FIL_REAR, 1.6, 1.0])
    r = _fillet_try(r, _face_loop_at(r, P["split_y"]), [FIL_PART, 0.4])
    for (x, z) in REAR_SCREWS:
        r -= _ycyl(x, -0.6, z, 2.2, 1.0)          # screw head counterbore in the rear face
        r -= _ycyl(x, -P["wall"] - 1, z, 1.1, P["wall"] + 2)
    return r


def _gasket(P):
    """TPU gasket band seen in the parting-line groove."""
    W, H, r = P["W"], P["H"], P["corner_r"]
    y = P["split_y"]
    outer = _yslab(W - 0.5, H - 0.5, r - 0.25, y - 0.45, 0.9)
    inner = _yslab(W - 2 * P["wall"] + 0.4, H - 2 * P["wall"] + 0.4, r - P["wall"], y - 1, 2)
    return outer - inner


def _window(P):
    D = P["D"]
    wx, wz = WIN_C
    pane = _yslab(WIN[0] + 2.8, WIN[1] + 2.8, WIN_R + 1.4, -D + 0.05, 1.5, x=wx, z=wz)
    pane += _yslab(WIN[0] - 0.2, WIN[1] - 0.2, WIN_R - 0.1, -D + 1.5, P["wall"] - 1.6, x=wx, z=wz)
    return pane


def _status_label(P):
    """Printed status label on the front face below the light pipe: dark plate, three level bars."""
    D = P["D"]
    x, z = 20.5, -8.0
    plate = _yslab(15.0, 20.0, 2.0, -D - 0.15, 0.2, x=x, z=z)
    bars = None
    for k, h in enumerate((3.0, 5.5, 8.0)):
        b = _yslab(2.4, h, 0.4, -D - 0.3, 0.2, x=x - 4.0 + 4.0 * k, z=z - 4.0 + h / 2)
        bars = b if bars is None else bars + b
    ring = _yslab(9.0, 1.2, 0.5, -D - 0.3, 0.2, x=x, z=z + 6.5)
    return plate, bars + ring


def _led(P):
    D = P["D"]
    lx, lz = P["led_pos"]
    r = P["led_d"] / 2
    pipe = _ycyl(lx, -D - 0.6, lz, r, 5.6)
    pipe = _fillet_try(pipe, [pipe.edges().sort_by(Axis.Y)[0]], [1.2, 0.8, 0.5])
    bezel = _ycyl(lx, -D - 0.3, lz, r + 1.3, 1.8) - _ycyl(lx, -D - 1, lz, r + 0.05, 4)
    bezel = _fillet_try(bezel, [bezel.edges().sort_by(Axis.Y)[0]], [0.4, 0.2])
    return pipe, bezel


def _rear_screws(P):
    out = None
    for (x, z) in REAR_SCREWS:
        h = _ycyl(x, -0.6, z, 1.9, 0.6)
        h -= Pos(x, 0, z) * Box(2.4, 0.6, 0.5) + Pos(x, 0, z) * Box(0.5, 0.6, 2.4)
        h += _ycyl(x, -P["wall"] - 4.0, z, 0.8, 3.4)
        out = h if out is None else out + h
    return out


# ---------------------------------------------------------------- internals
def _sensor(P, m):
    s = m["sensor"][1]
    sx, sdy, sz = P["sensor"]
    y_front = P["sensor_y"] - sdy / 2
    s = _fillet_try(s, s.edges().filter_by(Axis.Y), [1.5, 0.8])
    fx, fz = FAN_C
    s -= _ycyl(fx, y_front - 1, fz, FAN_R, 1 + 4.0)
    # small screw holes and a label seat on the face
    for (dx, dz) in ((-17.5, 17.5), (17.5, -17.5)):
        s -= _ycyl(P["sensor_x"] + dx, y_front - 1, dz + (-P["H"] / 2 + P["wall"] + sz / 2 + 1.0), 1.0, 3)
    return s


def _fan(P):
    sdy = P["sensor"][1]
    y_front = P["sensor_y"] - sdy / 2
    fx, fz = FAN_C
    y0 = y_front + 0.6
    hub = _ycyl(fx, y0, fz, 3.2, 3.0)
    hub = _fillet_try(hub, [hub.edges().sort_by(Axis.Y)[0]], [1.0, 0.6])
    fan = hub
    for k in range(9):
        a = 360.0 * k / 9
        blade = Pos(fx, y0 + 1.6, fz) * Rot(0, a, 0) * Pos(0, 0, 5.8) * Rot(0, 0, 30) * Box(2.4, 0.6, 5.6)
        fan += blade
    return fan


def _sensor_label(P):
    sx, sdy, sz = P["sensor"]
    y_front = P["sensor_y"] - sdy / 2
    zc = -P["H"] / 2 + P["wall"] + sz / 2 + 1.0
    return _yslab(10.0, 22.0, 1.0, y_front - 0.15, 0.2, x=P["sensor_x"] - 13.5, z=zc + 2.0)


def _module(P):
    mx, my, mz = P["module_pos"]
    ax, ay, az = P["module"]
    board = Pos(mx, my + ay / 2 - 0.5, mz) * Box(ax, 1.0, az)
    can = Pos(mx, my - 0.5, mz + 2.0) * Box(ax - 3.0, ay - 1.0, az - 8.0)
    can = _fillet_try(can, can.edges().filter_by(Axis.Y), [0.6, 0.3])
    usb = Pos(mx, my - 0.3, mz + az / 2 - 2.5) * Box(9.0, 3.2, 5.0)
    return board, can + usb


def _board(P, m):
    pcb = m["pcb"][1]
    by = P["pcb_y"]
    t = P["pcb"][1]
    chips = None
    for (x, z, sx, sz) in ((-18.0, -12.0, 7.0, 7.0), (-4.0, -16.0, 5.0, 4.0), (6.0, -8.0, 4.0, 4.0),
                           (-20.0, 6.0, 5.0, 3.0), (P["rh_vent_x"], -18.5, 3.0, 3.0)):
        c = Pos(x, by - t / 2 - 0.6, z) * Box(sx, 1.2, sz)
        chips = c if chips is None else chips + c
    return pcb, chips


def _cell(P, m):
    c = m["cell"][1]
    c = _fillet_try(c, c.edges().filter_by(Axis.Y), [2.0, 1.2, 0.6])
    c = _fillet_try(c, c.edges().filter_by(Axis.X), [0.8, 0.4])
    cx, cy, cz = P["cell"]
    label = _yslab(cx - 10.0, cz - 12.0, 1.0, P["cell_y"] - cy / 2 - 0.15, 0.2)
    return c, label


# ---------------------------------------------------------------- clip, lanyard, context
def _clip(P):
    """Stainless spring clip within the model.py clip envelope (22 x 3 x 40 mm at clip_z):
    a riveted base leaf, a hinge barrel and a tongue with the strap-loop slot."""
    cx, cy, cz = P["clip"]
    zc = P["clip_z"]
    z0, z1 = zc - cz / 2, zc + cz / 2
    base = _yslab(cx - 6.0, 26.0, 3.0, 0.0, 1.0, z=z1 - 1.5 - 13.0)
    rivets = None
    for z in (z1 - 8.0, z1 - 20.0):
        rv = _ycyl(0, 1.0, z, 1.6, 0.5)
        rv = _fillet_try(rv, [rv.edges().sort_by(Axis.Y)[-1]], [0.4, 0.2])
        rivets = rv if rivets is None else rivets + rv
    barrel = _xcyl(-cx / 2 + 2.0, 1.5, z1 - 1.5, 1.5, cx - 4.0)
    tongue = _yslab(cx, cz - 2.0, 3.5, 1.9, 1.1, z=(z0 + z1 - 2.0) / 2)
    tongue = _fillet_try(tongue, tongue.edges().filter_by(Axis.X) + tongue.edges().filter_by(Axis.Z), [0.4, 0.2])
    slot_z = z0 + 7.0
    tongue -= _yslab(cx - 8.0, 6.0, 1.5, 1.0, 3.0, z=slot_z)
    for k in range(4):
        tongue -= Pos(0, 3.05, z1 - 10.0 - 2.0 * k) * Box(cx - 8.0, 0.3, 0.6)
    return base + rivets + barrel + tongue


def _lanyard(P):
    """Webbing lanyard looped through the clip slot, a crimp, then lying on the floor in an arc
    around the right side of the badge to a breakaway buckle."""
    cx, cy, cz = P["clip"]
    z0 = P["clip_z"] - cz / 2               # bottom of the clip tongue
    floor = -P["H"] / 2
    w, t = 9.0, 0.8
    top = z0 + 4.0                          # webbing rests on the bar below the slot
    over = Pos(0, 2.35, top + t / 2) * Box(w, 3.9, t)
    rear = Pos(0, 0.4 + t / 2, (top + z0 - 4.0) / 2) * Box(w, t, top - z0 + 4.0)
    front = Pos(0, 4.3 - t / 2, (top + z0 - 4.0) / 2) * Box(w, t, top - z0 + 4.0)
    crimp_z = z0 - 5.0
    crimp = Pos(0, 2.35, crimp_z) * Box(w + 1.6, 5.0, 3.6)
    crimp = _fillet_try(crimp, crimp.edges(), [0.8, 0.5])
    # single strand down to the floor, bending toward +Y
    yb0, yb1 = 1.95, 1.95 + t
    rr = 1.5
    zc_b = floor + t + rr
    down = Pos(0, (yb0 + yb1) / 2, (crimp_z + zc_b) / 2) * Box(w, t, crimp_z - zc_b)
    yc_b = yb1 + rr
    ring = _xcyl(-w / 2, yc_b, zc_b, rr + t, w) - _xcyl(-w / 2 - 1, yc_b, zc_b, rr, w + 2)
    ring = ring & (Pos(0, yc_b - 10, zc_b - 10) * Box(w + 2, 20, 20))
    # flat run on the floor, traced along a filleted plan path
    pts = [(0.0, yc_b - 0.01), (0.0, 20.0), (30.0, 34.0), (58.0, 14.0), (60.0, -16.0), (48.0, -46.0)]
    with BuildLine() as bl:
        FilletPolyline(*pts, radius=12.0)
    band = trace(bl.line, line_width=w)
    run = Pos(0, 0, floor) * extrude(band, amount=t)
    web = over + rear + front + down + ring + run
    # breakaway buckle at the end of the run (teal accent)
    ex, ey = pts[-1]
    ang = math.degrees(math.atan2(ey - pts[-2][1], ex - pts[-2][0]))
    buckle = Pos(ex, ey, floor) * Rot(0, 0, ang) * Pos(6.0, 0, 2.2) * Box(14.0, 12.0, 4.4)
    buckle = _fillet_try(buckle, buckle.edges(), [1.5, 1.0, 0.5])
    buckle -= Pos(ex, ey, floor) * Rot(0, 0, ang) * Pos(8.0, 0, 4.4) * Box(4.0, 8.0, 1.2)
    return web, crimp, buckle


def _chest_panel(P):
    """Fabric chest panel, gently curved like a torso, with a vertical harness strap the clip
    grips, a reflective tape band and stitching (context only)."""
    y_back = P["clip"][1] + 0.05          # strap face sits behind the clip
    R = 320.0
    Hc, z_lo = 170.0, -90.0
    strap_t, panel_t = 1.8, 2.2

    def arc_band(r_in, r_out, half_w, z0, h):
        """Band between radii r_in and r_out about a vertical axis at Y = y_back + R; radius R
        passes through Y = y_back at X = 0, larger radii lie toward -Y (the viewer)."""
        c = Pos(0, y_back + R, z0 + h / 2)
        ring = c * Cylinder(r_out, h) - c * Cylinder(r_in, h + 1)
        return ring & (Pos(0, y_back + 10, z0 + h / 2) * Box(2 * half_w, 60, h))

    strap = arc_band(R - strap_t, R, 21.0, z_lo, Hc)
    panel = arc_band(R - strap_t - panel_t, R - strap_t, 80.0, z_lo, Hc)
    tape = arc_band(R - strap_t, R - strap_t + 0.4, 80.0, -56.0, 14.0) - arc_band(R - 3, R + 1, 21.5, -64.0, 30.0)
    stitch = arc_band(R - 0.1, R + 0.25, 17.6, z_lo + 2, Hc - 4) - arc_band(R - 1, R + 1, 16.9, z_lo, Hc)
    return panel, strap, tape, stitch


def product_parts(P=PARAMS):
    D = derived(P)
    m = build_parts(P)
    out = []

    def add(name, shape, color, material, bom, group, explode):
        out.append({"name": name, "shape": shape, "color": color, "material": material,
                    "bom": bom, "group": group, "explode": tuple(float(v) for v in explode)})

    # ---- shell: shells, gasket, window, light pipe, label, screws, screen, clip
    add("Front shell (hi-vis PETG)", _front_shell(P, m), C_FRONT, "plastic", 1, "shell", (0, -104, 0))
    add("Front window (acrylic)", _window(P), C_WINDOW, "clear", 1, "shell", (0, -128, 0))
    plate, marks = _status_label(P)
    add("Status label", plate, C_LABEL, "painted", 1, "shell", (0, -104, 0))
    add("Status label marks", marks, C_WHITE, "painted", 1, "shell", (0, -104, 0))
    pipe, bezel = _led(P)
    add("Alert LED light pipe (lit)", pipe, C_LED, "emissive", 6, "shell", (0, -120, 0))
    add("Light pipe bezel", bezel, C_LABEL, "plastic", 6, "shell", (0, -113, 0))
    add("Inlet dust screen (stainless mesh)", m["screen"][1], C_MESH, "metal", 2, "shell", (0, -104, -16))
    add("TPU gasket", _gasket(P), C_GASKET, "rubber", 9, "shell", (0, 34, 0))
    add("Rear shell (PETG)", _rear_shell(P, m), C_REAR, "plastic", 9, "shell", (0, 48, 0))
    add("M2 rear screws", _rear_screws(P), C_STEEL, "metal", 11, "shell", (0, 70, 0))
    add("Stainless spring clip", _clip(P), C_STEEL, "metal", 10, "shell", (0, 90, 0))

    # ---- internal: fan, sensor, controller, motor, board, cell
    add("Sensor fan", _fan(P), C_FAN, "plastic", 3, "internal", (0, -60, 38))
    add("Optical particle sensor (SPS30 class)", _sensor(P, m), C_ACCENT, "plastic", 3, "internal", (0, -52, 0))
    add("Sensor label", _sensor_label(P), C_WHITE, "painted", 3, "internal", (0, -52, 0))
    mb, mcan = _module(P)
    add("Controller and BLE module", mb, C_CHIP, "plastic", 4, "internal", (0, -26, 14))
    add("Module shield can and USB-C", mcan, C_CAN, "metal", 4, "internal", (0, -26, 14))
    motor = m["motor"][1]
    motor = _fillet_try(motor, motor.edges(), [0.6, 0.3])
    add("Vibration motor", motor, C_CAN, "metal", 5, "internal", (0, -26, -10))
    pcb, chips = _board(P, m)
    add("Carrier board", pcb, C_PCB, "plastic", 7, "internal", (0, -4, 0))
    add("Carrier board components", chips, C_CHIP, "plastic", 7, "internal", (0, -4, 0))
    cell, clabel = _cell(P, m)
    add("LiPo cell, 2,000 mAh (pouch)", cell, C_POUCH, "metal", 8, "internal", (0, 16, 0))
    add("Cell label", clabel, C_CELL_LABEL, "painted", 8, "internal", (0, 16, 0))

    # ---- accessory: lanyard (no BOM line; appearance only)
    web, crimp, buckle = _lanyard(P)
    add("Webbing lanyard", web, C_WEB, "fabric", None, "accessory", (0, 90, 0))
    add("Lanyard crimp", crimp, C_STEEL, "metal", None, "accessory", (0, 90, 0))
    add("Breakaway buckle", buckle, C_ACCENT, "plastic", None, "accessory", (0, 90, 0))

    # ---- context: fabric chest panel and harness strap (worn view)
    panel, strap, tape, stitch = _chest_panel(P)
    add("Chest panel (workwear fabric)", panel, C_PANEL, "fabric", None, "context", (0, 0, 0))
    add("Harness strap (webbing)", strap, C_STRAP, "fabric", None, "context", (0, 0, 0))
    add("Reflective tape", tape, C_TAPE, "painted", None, "context", (0, 0, 0))
    add("Strap stitching", stitch, C_STITCH, "fabric", None, "context", (0, 0, 0))
    return out


if __name__ == "__main__":
    for p in product_parts():
        s = p["shape"]
        print(f"{p['name']:40s} {p['group']:9s} {p['material']:8s} valid={s.is_valid} vol={s.volume / 1000:7.2f} cm3")

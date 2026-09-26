"""DustBadge parametric model (build123d), TRL 3, massing-plus level of detail.
Revised 2026-09-25 for DBG-DDR-002 (2,000 mAh cell, 11.5 mm thick).

Run from the repo root:  python cad/src/model.py
Exports STEP and STL into cad/step and cad/stl:
    dustbadge-assembly.step / .stl   the whole badge with its bought-in parts
    front-shell.step / .stl          printed front shell with inlet and outlet slots
    rear-shell.step / .stl           printed rear shell with the clip mount

Axes (badge frame, mm): X across the badge, Z up, Y from the wearer outward is negative.
The rear face (against the wearer) is at Y = 0 and the front face at Y = -depth. The badge
center is on the Z axis at Z = 0, so the kit's cutaway (which cuts near the origin) works.
Main dimensions and interfaces only: envelope, shell split, sensor position and its air
path to the downward inlet, electronics stack, cell, clip. Not fabrication detail; not for
fabrication. The same PARAMS feed docs/04-calcs/sizing.py (DBG-CAL-001), the drawing
DBG-DWG-001 (cad/src/sheets.py) and the concept media (cad/src/concept_media.py).
"""
import math
from pathlib import Path

# Top-level parameters (mm unless stated). Edit these, not the geometry below.
PARAMS = {
    # envelope and shells (1 front, 9 rear)
    "W": 64.0, "H": 52.0, "D": 30.0,        # width X, height Z, depth Y (shells only, clip excluded)
    "wall": 2.0,
    "split_y": -14.0,                        # Y of the front and rear shell joint
    "corner_r": 4.0,                         # vertical edge radius
    "boss_d": 5.0,                           # three M2 screw bosses in the front shell, clear of the sensor
    "bosses": ((-27.0, 21.0), (27.0, 21.0), (27.0, -21.0)),   # X, Z; the board rests on them
    "boss_end_y": -16.0,
    # 3 particle sensor, SPS30 class: 41 x 41 x 12 mm, inlet and outlet on the lower edge
    "sensor": (41.0, 12.0, 41.0),            # X, Y, Z
    "sensor_x": -9.0, "sensor_y": -21.8,     # center; bottom edge sits on the inner floor
    "sensor_port": (9.0, 6.0),               # inlet and outlet port size on the sensor edge (X, Y)
    "sensor_port_dx": 10.0,                  # inlet at -dx, outlet at +dx from the sensor center
    # 2 inlet screen and the two slots in the bottom face of the front shell
    "slot": (12.0, 7.0),                     # X, Y of each slot
    "screen_t": 1.2,
    # 4 controller module, 5 motor, 6 LED light pipe
    "module": (17.5, 4.0, 21.0), "module_pos": (21.0, -18.0, 7.0),
    "motor_d": 10.0, "motor_t": 3.0, "motor_pos": (21.0, -18.5, -12.0),
    "led_d": 4.0, "led_pos": (21.0, 20.0),   # X, Z of the light pipe through the front face
    # 7 carrier board (boost, charger with cell thermistor, fuse, USB-C, humidity sensor)
    "pcb": (56.0, 1.6, 44.0), "pcb_y": -15.0,
    "usb": (9.0, 3.2), "usb_x": 16.0,        # USB-C opening in the bottom face (X, Y size)
    "rh_vent_x": 8.0,                        # humidity sensor vent in the bottom face, X position
    # 8 cell, 2,000 mAh protected LiPo (DBG-DDR-002 D8; was 1,500 mAh, 10 mm thick)
    "cell": (50.0, 11.5, 34.0), "cell_y": -8.25, "cell_mah": 2000.0,
    # 10 spring clip with strap loop, on the rear face
    "clip": (22.0, 3.0, 40.0), "clip_z": 4.0,
    # wearer interface (for R8): badge center relative to the midpoint of nose and mouth
    "mount_drop": 210.0,                     # below the nose and mouth midpoint (collar or upper strap)
    "mount_lateral": 70.0,                   # to one side of the midline
    "mount_forward": 10.0,                   # inlet forward of the face plane (badge proud of the chest)
    # masses of bought-in parts (g), for R9; shells from volume
    "m_sensor": 26.3, "m_cell": 38.0, "m_module": 3.0, "m_board": 9.0, "m_motor": 1.0,
    "m_led": 0.5, "m_screen": 0.4, "m_clip": 6.0, "m_hardware": 3.0, "m_gasket": 1.0,
    "rho_petg": 1.27,                        # g/cm3
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
    return {
        "overall": (W, D + p["clip"][1], H),            # X, Y incl. clip, Z
        "sensor_bottom": -H / 2 + p["wall"],
        "inlet_x": inlet_x, "outlet_x": outlet_x,
        "inlet_to_face_mm": dist,
        "front_depth": D + p["split_y"],

        "rear_depth": -p["split_y"],
        "surface_m2": 2 * (W * H + W * D + H * D) * 1e-6,
        "front_area_m2": W * H * 1e-6,
    }


def _b3d():
    import build123d as b
    return b


def box(cx, cy, cz, sx, sy, sz):
    b = _b3d()
    return b.Pos(cx, cy, cz) * b.Box(sx, sy, sz)


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


def build_parts(p=PARAMS):
    """Return an ordered dict: key -> (name, shape, color, bom line)."""
    W, H, D, t = p["W"], p["H"], p["D"], p["wall"]
    sy_ = p["split_y"]
    r = p["corner_r"]
    sx, sdy, sz = p["sensor"]
    parts = {}

    # 1 front shell: from Y = -D to split, open toward the rear
    fd = D + sy_
    outer = rounded_box(0, (-D + sy_) / 2, 0, W, fd, H, r)
    inner = rounded_box(0, (-D + t + sy_) / 2 + 0.5, 0, W - 2 * t, fd - t + 1, H - 2 * t, max(r - t, 0.5))
    front = outer - inner
    # screw bosses from the inside of the front face back to the board
    by0, by1 = -D + t, p["boss_end_y"]
    for bx, bz in p["bosses"]:
        front = front + ycyl(bx, (by0 + by1) / 2, bz, p["boss_d"] / 2, by1 - by0)
    # bottom slots: sensor inlet (screened) and outlet, USB-C, humidity vent
    slx, sly = p["slot"]
    d = derived(p)
    for xx in (d["inlet_x"], d["outlet_x"]):
        front = front - box(xx, p["sensor_y"], -H / 2, slx, sly, 2 * t + 2)
    ux, uy = p["usb"]
    front = front - box(p["usb_x"], p["pcb_y"] - 1.6 - p["pcb"][1] / 2, -H / 2, ux, uy + 0.4, 2 * t + 2)
    front = front - box(p["rh_vent_x"], -20.0, -H / 2, 3.0, 3.0, 2 * t + 2)
    # LED light pipe hole in the front face
    lx, lz = p["led_pos"]
    front = front - ycyl(lx, -D + t / 2, lz, p["led_d"] / 2 + 0.2, t + 2)
    parts["front"] = ("Front shell with bottom inlet", front, "#EAB308", 1)

    # 2 inlet screen, flush in the inlet slot
    parts["screen"] = ("Inlet dust screen", box(d["inlet_x"], p["sensor_y"], -H / 2 + t / 2, slx - 0.6, sly - 0.6, p["screen_t"]),
                       "#374151", 2)

    # 3 particle sensor with its two ports facing down onto the slots
    sz_c = -H / 2 + t + sz / 2 + 1.0
    sensor = box(p["sensor_x"], p["sensor_y"], sz_c, sx, sdy, sz)
    parts["sensor"] = ("Optical particle sensor (SPS30 class)", sensor, "#0F766E", 3)

    # 4 controller, 5 motor, 6 LED light pipe
    mx, my, mz = p["module_pos"]
    parts["module"] = ("Controller and BLE module", box(mx, my, mz, *p["module"]), "#1D4ED8", 4)
    ox, oy, oz = p["motor_pos"]
    parts["motor"] = ("Vibration motor", ycyl(ox, oy, oz, p["motor_d"] / 2, p["motor_t"]), "#6B7280", 5)
    parts["led"] = ("Alert LED light pipe", ycyl(lx, -D + 1.5, lz, p["led_d"] / 2, 5.0), "#DC2626", 6)

    # 7 carrier board with a USB-C socket at its lower edge
    bx_, by_, bz_ = p["pcb"]
    pcb = box(0, p["pcb_y"], 0, bx_, by_, bz_)
    for hx, hz in p["bosses"]:
        pcb = pcb - ycyl(hx, p["pcb_y"], hz, 1.1, by_ + 1)
    pcb = pcb + box(p["usb_x"], p["pcb_y"] - 1.6 - by_ / 2, -H / 2 + t + 1.8, ux - 0.4, 3.2, 3.6)
    parts["pcb"] = ("Carrier board (boost, charger, fuse, RH sensor)", pcb, "#15803D", 7)

    # 8 cell behind the board
    parts["cell"] = (f"LiPo cell, {p['cell_mah']:,.0f} mAh, protected", box(0, p["cell_y"], 0, *p["cell"]), "#C2410C", 8)

    # 9 rear shell: from split to Y = 0, closed at the back
    rd = -sy_
    outer = rounded_box(0, sy_ / 2, 0, W, rd, H, r)
    inner = rounded_box(0, (sy_ - t) / 2 - 0.5, 0, W - 2 * t, rd - t + 1, H - 2 * t, max(r - t, 0.5))
    parts["rear"] = ("Rear shell", outer - inner, "#374151", 9)

    # 10 spring clip with strap loop
    cx_, cy_, cz_ = p["clip"]
    clip = box(0, cy_ / 2, p["clip_z"], cx_, cy_, cz_) - box(0, cy_ / 2, p["clip_z"] - cz_ / 2 + 7, cx_ - 8, cy_ + 2, 6)
    parts["clip"] = ("Spring clip and strap loop", clip, "#9CA3AF", 10)
    return parts


def masses(p=PARAMS, parts=None):
    """Mass breakdown in grams: printed shells from model volume, bought-in parts from PARAMS."""
    parts = parts or build_parts(p)
    rho = p["rho_petg"] / 1000.0                      # g per mm3
    m = {"front shell (PETG)": parts["front"][1].volume * rho,
         "rear shell (PETG)": parts["rear"][1].volume * rho,
         "particle sensor": p["m_sensor"], "cell": p["m_cell"], "controller module": p["m_module"],
         "carrier board and modules": p["m_board"], "motor": p["m_motor"], "LED and light pipe": p["m_led"],
         "screen": p["m_screen"], "clip": p["m_clip"], "screws, wire, adhesive": p["m_hardware"],
         "gasket (TPU)": p["m_gasket"]}
    return m


def assembly(p=PARAMS):
    b = _b3d()
    return b.Compound([s for (_, s, _, _) in build_parts(p).values()])


if __name__ == "__main__":
    from build123d import Compound, export_step, export_stl
    out = Path(__file__).resolve().parents[1]
    (out / "step").mkdir(exist_ok=True)
    (out / "stl").mkdir(exist_ok=True)
    parts = build_parts()
    groups = {"dustbadge-assembly": Compound([s for (_, s, _, _) in parts.values()]),
              "front-shell": parts["front"][1], "rear-shell": parts["rear"][1]}
    for name, c in groups.items():
        export_step(c, str(out / "step" / f"{name}.step"))
        export_stl(c, str(out / "stl" / f"{name}.stl"))
    bb = groups["dustbadge-assembly"].bounding_box()
    m = masses(PARAMS, parts)
    print(f"assembly bounding box {bb.size.X:.1f} x {bb.size.Y:.1f} x {bb.size.Z:.1f} mm; mass {sum(m.values()):.1f} g")
    print("exported", ", ".join(groups))

"""DustBadge concept massing model and media (TRL 2).

Run from the repo root:  python cad/src/concept_media.py
Proportions and main parts only; not for fabrication.

Coordinates in mm. The badge is worn on the upper chest, clipped to a harness
strap or collar, facing the viewer along -Y. Badge local frame: X across the
badge, Z up, the rear face (toward the wearer) at Y = 0 and the front at Y = -30.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".kit"))
from build123d import Box, Cylinder, Sphere, Pos, Rot
from concept import Part, render_all

# Badge envelope (mm)
W, H, D = 64.0, 52.0, 30.0     # width (X), height (Z), depth (Y)
WALL = 2.0
SPLIT = -14.0                  # Y of the front and rear shell joint

# Where the badge sits on the wearer. The badge stays at the origin (the kit's
# cutaway cutter is centered on the origin) and the wearer is placed around it.
BX, BY, BZ = 0.0, 0.0, 0.0
WEAR_X, WEAR_Y, WEAR_Z = 70.0, -3.0, 190.0   # badge center relative to the torso frame


def at(shape):
    """Move a badge-frame shape to its worn position."""
    return Pos(BX, BY, BZ) * shape


def shell(y0, y1, open_side):
    """Hollow half shell between y0 and y1, open toward the joint."""
    depth = y1 - y0
    outer = Pos(0, (y0 + y1) / 2, 0) * Box(W, depth, H)
    if open_side == "rear":   # front shell: closed front face at y0
        inner = Pos(0, (y0 + WALL + y1) / 2 + 0.5, 0) * Box(W - 2 * WALL, depth - WALL + 1, H - 2 * WALL)
    else:                     # rear shell: closed back face at y1
        inner = Pos(0, (y0 + y1 - WALL) / 2 - 0.5, 0) * Box(W - 2 * WALL, depth - WALL + 1, H - 2 * WALL)
    return outer - inner


# 1 Front shell with inlet slot in the bottom face (sensor inlet faces down)
SENS_X = -9.5                                  # sensor center across the badge
front = shell(-D, SPLIT, "rear") - Pos(SENS_X, -22, -H / 2) * Box(30, 8, 6)
# 2 Inlet dust screen, flush in the bottom slot
screen = Pos(SENS_X, -22, -H / 2 + 0.6) * Box(29, 7, 1.2)
# 3 Optical particle sensor, SPS30 class, 41 x 41 x 12 mm, inlet and outlet on its lower edge
sensor = Pos(SENS_X, -21.8, -H / 2 + WALL + 20.5 + 0.3) * Box(41, 12, 41)
# 4 Controller module, nRF52840 class, 21 x 17.5 x 4 mm, beside the sensor
MOD_X = 21.0
module = Pos(MOD_X, -18.0, 9.0) * Box(17.5, 4.0, 21.0)
# 5 Vibration motor, 10 mm coin, below the module
motor = Pos(MOD_X, -18.5, -12.0) * Rot(90, 0, 0) * Cylinder(5.0, 3.0)
# 6 Alert LED light pipe through the front face
led = Pos(MOD_X, -D + 1.5, 20.0) * Rot(90, 0, 0) * Cylinder(2.0, 5.0)
# 7 Carrier board: 5 V boost, charger, fuse, USB-C
pcb = Pos(0, -15.0, 0) * Box(58.0, 1.6, 46.0)
# 8 LiPo cell, 1,500 mAh, 50 x 34 x 10 mm, behind the board
cell = Pos(0, -8.5, 0) * Box(50.0, 10.0, 34.0)
# 9 Rear shell
rear = shell(SPLIT, 0, "front")
# 10 Spring clip and strap loop on the back
clip = Pos(0, 1.5, 4.0) * Box(22.0, 3.0, 40.0)

def ex(t, dz=0.0, dx=0.0):
    """Exploded offset along the badge's front axis, stepped down so parts do not hide each other."""
    return (dx, -t, -0.55 * t + dz)


parts = [
    Part("Front shell with bottom inlet", at(front), "#EAB308", 1, ex(175)),
    Part("Inlet dust screen", at(screen), "#374151", 2, ex(175, -45)),
    Part("Optical particle sensor (SPS30 class)", at(sensor), "#0F766E", 3, ex(105, 0, -12)),
    Part("Controller and BLE module", at(module), "#1D4ED8", 4, ex(105, 20, 22)),
    Part("Vibration motor", at(motor), "#6B7280", 5, ex(105, -15, 22)),
    Part("Alert LED light pipe", at(led), "#DC2626", 6, ex(225, 10)),
    Part("Carrier board (boost, charger, fuse)", at(pcb), "#15803D", 7, ex(50)),
    Part("LiPo cell, 1,500 mAh, protected", at(cell), "#C2410C", 8, ex(0)),
    Part("Rear shell", at(rear), "#374151", 9, ex(-50)),
    Part("Spring clip and strap loop", at(clip), "#9CA3AF", 10, ex(-100)),
]

# Context: upper torso, neck and head of the wearer (grey, not part of the design)
torso = Pos(0, 70, 110) * Box(300, 140, 220)
shoulders = Pos(0, 70, 220) * Rot(0, 90, 0) * Cylinder(70, 380)
joints = Pos(-190, 70, 220) * Sphere(70) + Pos(190, 70, 220) * Sphere(70)
arms = Pos(-190, 70, 70) * Cylinder(52, 300) + Pos(190, 70, 70) * Cylinder(52, 300)
neck = Pos(0, 70, 300) * Cylinder(50, 70)
head = Pos(0, 60, 420) * Sphere(100)
body = torso + shoulders + joints + arms + neck + head
context = [Part("Wearer's upper body", Pos(-WEAR_X, -WEAR_Y, -WEAR_Z) * body, "#C8CDD3")]

render_all(
    parts, project="DustBadge", title="Wearable dust badge concept", dwg_no="DBG-DWG-010",
    key_figures=["Respirable dust (PM4) every 1 s, logged per minute",
                 "RCS estimate = dust x site silica fraction",
                 "Alerts at projected 8 h TWA over action level",
                 "About 13 h per charge, continuous (estimate)",
                 "About 64 x 52 x 30 mm, 110 g (estimate)",
                 "Worn within 30 cm of nose and mouth",
                 "About $85 in parts (indicative)"],
    scale_figure=False, context=context, cut=False,
    flow={"title": "data flow (estimated values)", "unit": "",
          "stages": [("Dust at collar", "PM4, 1 s readings"),
                     ("Site calibration", "gravimetric factor"),
                     ("Silica estimate", "x site quartz fraction"),
                     ("Shift TWA", "8 h, projected"),
                     ("Badge alert", "vibrate + LED"),
                     ("Worker's phone", "BLE shift log")]},
)

# Cutaway: a side section through the sensor, so the stack from front to back and the
# downward-facing inlet show. The kit cuts across Y, so the badge is turned 90 degrees
# about Z first (its depth axis then runs along X, facing the viewer).
from concept import _render, cutaway_parts
shells = (1, 9)   # shell labels would land on the parts inside them, so the note names them
turned = [Part(p.name, Rot(0, 0, -90) * p.shape, p.color, None if p.bom in shells else p.bom) for p in parts]
_render(cutaway_parts(turned), Path("media") / "cutaway.png", azim=-90, elev=12, labels=True,
        title="DustBadge: cutaway, section through the particle sensor",
        note="Front of the badge (worn facing out) on the left. Yellow: front shell (1); dark grey: rear shell (9). "
             "Air enters through the bottom screen (2)")

# Remove temporary view folders left by the renderer
import shutil
for d in (Path("media") / "_views", Path("media") / "_views_fig"):
    shutil.rmtree(d, ignore_errors=True)

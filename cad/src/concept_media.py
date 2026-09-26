"""DustBadge concept media (TRL 3), built from the parametric model in cad/src/model.py.

Run from the repo root:  python cad/src/concept_media.py
Massing-plus detail only; not for fabrication.

Coordinates in mm. The badge is worn on the upper chest, clipped to a harness
strap or collar, facing the viewer along -Y. Badge local frame: X across the
badge, Z up, the rear face (toward the wearer) at Y = 0 and the front at Y = -30.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".kit"))
from build123d import Box, Cylinder, Sphere, Pos, Rot
from concept import Part, render_all

sys.path.insert(0, str(Path(__file__).resolve().parent))
from model import PARAMS, build_parts  # noqa: E402  (TRL 3: media built from the parametric model)

H = PARAMS["H"]
# The badge stays at the origin (the kit's cutaway cutter works near the origin) and the
# wearer is placed around it. Badge center relative to the torso frame used below:
WEAR_X, WEAR_Y, WEAR_Z = 70.0, -3.0, 180.0   # 210 mm below the nose and mouth (about z 390 here)


def ex(t, dz=0.0, dx=0.0):
    """Exploded offset along the badge's front axis, stepped down so parts do not hide each other."""
    return (dx, -t, -0.55 * t + dz)


EXPLODE = {"front": ex(175), "screen": ex(175, -25, -20), "sensor": ex(105, 0, -12), "module": ex(105, 20, 22),
           "motor": ex(105, -15, 22), "led": ex(240, 40, 95), "pcb": ex(50), "cell": ex(0), "rear": ex(-50),
           "clip": ex(-100)}
parts = [Part(name, shape, color, bom, EXPLODE[k]) for k, (name, shape, color, bom) in build_parts().items()]

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
                 "17.7 h per charge typical, 12.8 h worst case (DBG-CAL-001)",
                 "64 x 52 x 30 mm (33 with clip), 120 g (DBG-CAL-001)",
                 "Inlet 242 mm from nose and mouth",
                 "$91 in parts against $90 (indicative prices)"],
    scale_figure=False, context=context, cut=False,
    flow={"title": "data flow (estimated values)", "unit": "",
          "stages": [("Dust at collar", "PM4, 1 s readings"),
                     ("Site calibration", "gravimetric factor"),
                     ("Silica estimate", "x site quartz fraction"),
                     ("Shift TWA", "8 h, projected"),
                     ("Badge alert", "vibrate + LED"),
                     ("Worker's phone", "BLE shift log")]},
)

# Cutaway: a side section through the sensor inlet, so the stack from front to back and the
# screened downward inlet show. The kit's own cutter cuts at the mean part center, which here
# falls on the outlet slot, so this script cuts on the inlet plane itself (project-side; the kit
# is unchanged) and turns the result 90 degrees about Z so the depth axis faces the viewer.
from build123d import Box as _Box, Pos as _Pos
from concept import _render
from model import derived
shells = (1, 9)   # shell labels would land on the parts inside them, so the note names them
x_cut = derived()["inlet_x"]
keep = _Pos(x_cut - 500, 0, 0) * _Box(1000, 1000, 1000)
section = []
for p in parts:
    s_ = p.shape & keep
    if s_.volume > 1e-6:
        section.append(Part(p.name, Rot(0, 0, -90) * s_, p.color, None if p.bom in shells else p.bom))
_render(section, Path("media") / "cutaway.png", azim=-90, elev=12, labels=True,
        title="DustBadge: cutaway, section through the particle sensor inlet",
        note="Front of the badge (worn facing out) on the left. Yellow: front shell (1); dark grey: rear shell (9). "
             "Air enters upward through the bottom screen (2)")

# Remove temporary view folders left by the renderer
import shutil
for d in (Path("media") / "_views", Path("media") / "_views_fig"):
    shutil.rmtree(d, ignore_errors=True)

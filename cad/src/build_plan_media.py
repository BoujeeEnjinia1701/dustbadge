"""DustBadge prototype build plan pictures (DBG-BLD-001, STANDARDS section 18).

Run from the repo root:  python cad/src/build_plan_media.py [overview|sheets|joints|steps|layouts|wiring ...]
With no argument it draws everything. Every picture is drawn from cad/src/model.py
(build_parts), so the pictures and the model never disagree:
    docs/05-build-plan/overview.png        every component pulled apart, numbered in build order
    cad/drawings/DBG-DWG-101 to 108        making sketches for the made and drilled components
    docs/05-build-plan/joint-NN.png        close-ups of the joints that need explaining
    docs/05-build-plan/step-NN.png         one picture per assembly step
    docs/05-build-plan/bottom-face.png     the openings in the bottom face, full size figures
    docs/05-build-plan/wiring.png          block-level wiring with wire sizes (matplotlib)
Uses .kit/build_views.py. The badge is small, so the 3D pictures scale the model up four times
before shading (the kit tessellates to 1 mm); the making sketches use the true size.
BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
import build_views as bv  # noqa: E402
from build_views import Part  # noqa: E402
from model import PARAMS as P, build_parts, derived, bx  # noqa: E402

OUT = ROOT / "docs" / "05-build-plan"
DWG = ROOT / "cad" / "drawings"
DATE = "2026-09-30"
D = derived(P)
C = build_parts(P)
K = 4.0                                   # picture scale factor (see the module note)

COL = {"front": "#EAB308", "led": "#DC2626", "lamp": "#991B1B", "motor": "#6B7280", "boost": "#22C55E",
       "rh": "#0EA5E9", "screen": "#475569", "seals": "#1F2937", "sensor": "#0F766E", "pcb": "#15803D",
       "module": "#1D4ED8", "charger": "#16A34A", "clip": "#0369A1", "clip_screws": "#111827",
       "rear": "#374151", "cell": "#C2410C", "gasket": "#111827", "screws": "#111827"}


def _fuse(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


def big(shape):
    """The shape scaled K times about the model origin (locations included)."""
    import build123d as b
    from OCP.gp import gp_Trsf, gp_Pnt
    from OCP.BRepBuilderAPI import BRepBuilderAPI_Transform
    t = gp_Trsf()
    t.SetScale(gp_Pnt(0, 0, 0), K)
    return b.Shape.cast(BRepBuilderAPI_Transform(shape.wrapped, t, True).Shape())


def part(name, keys, color=None, explode=(0, 0, 0), alpha=1.0, shape=None):
    """A picture part from one or more model parts, scaled for shading; explode in true mm."""
    sh = shape if shape is not None else _fuse([C[k][1] for k in keys])
    return Part(name, big(sh), color or COL[keys[0]], None, tuple(K * v for v in explode), alpha)


def win(sh, x0, x1, y0, y1, z0, z1):
    return sh & bx(x0, x1, y0, y1, z0, z1)


# ----------------------------------------------------------------- overview
ORDER = [  # key in the overview, name, model parts, explode (mm); front half above, rear half below
    ("front", "Front shell", ["front"], (0, -110, 0)),
    ("pipe", "Light pipe and LED", ["led", "lamp"], (0, -100, 50)),
    ("motor", "Vibration motor", ["motor"], (5, -98, 64)),
    ("boost", "5 V boost module", ["boost"], (15, -78, 66)),
    ("rh", "Humidity breakout", ["rh"], (15, -60, 80)),
    ("screen", "Inlet screen", ["screen"], (-10, -78, -28)),
    ("seals", "Port seals (2)", ["seals"], (-10, -55, -30)),
    ("sensor", "Particle sensor", ["sensor"], (-5, -30, 8)),
    ("pcb", "Carrier board (perfboard)", ["pcb"], (0, 5, 0)),
    ("module", "Controller module", ["module"], (55, -5, 22)),
    ("charger", "Charger module with USB-C", ["charger"], (55, -5, -14)),
    ("rear", "Rear shell", ["rear"], (0, -30, -95)),
    ("clip", "Spring clip", ["clip"], (0, 0, -95)),
    ("clip_screws", "Clip screws M2 x 8 (2)", ["clip_screws"], (0, 18, -95)),
    ("cell", "Cell, 2,000 mAh", ["cell"], (0, -62, -95)),
    ("gasket", "Gasket", ["gasket"], (0, -86, -95)),
    ("screws", "Shell screws M2 x 20 (3)", ["screws"], (0, 40, -95)),
]


def overview():
    parts = [part(n, ks, explode=e) for _, n, ks, e in ORDER]
    return bv.overview(parts, OUT / "overview.png", "DustBadge prototype: every component, pulled apart",
                       subtitle="Numbered in build order. Top row: the front half; bottom row: the rear half. Front of the badge to the left",
                       elev=18, azim=-38, size=(11, 7.5), dpi=150, key=True)


# ----------------------------------------------------------------- making sketches
def ghost(name, keys):
    return Part(name, _fuse([C[k][1] for k in keys]), COL[keys[0]], None, (0, 0, 0), 1.0)


def sheets():
    import build123d as b
    base = dict(project="DustBadge", date=DATE)
    out = []
    sx_, sy_, sz_ = P["slot"][0], P["slot"][1], None
    # 101 front shell
    out.append(bv.component_sheet(
        Part("Front shell", C["front"][1], COL["front"]), [ghost("Rear shell", ["rear"]), ghost("Sensor", ["sensor"]), ghost("Board", ["pcb"])],
        dwg_no="DBG-DWG-101", title="DustBadge front shell: making sketch",
        material="PETG, high-visibility yellow, 3D printed, 0.2 mm layers, 4 walls",
        inset_view=(20, -60),
        notes=["Print face down (the front face on the bed); no supports needed.",
               "64 x 52 x 16 mm, walls 2 mm, outside edges round 4 mm.",
               "Bottom face openings (sideways from the centre line, + to the right",
               "  seen from the front; depth from the front face):",
               "  inlet slot 12 x 7 at 19 left, outlet slot 12 x 7 at 1 right,",
               "  both 4.7 to 11.7 back; USB-C 9.6 x 3.8 at 18 right, 12.2 back;",
               "  humidity vent 3 x 2 at 18.5 right, 2 to 4 back.",
               "Light pipe hole 4.4 through the front face, 21 right, 20 above centre.",
               "Three screw bosses 5 dia, 14.2 long from the front face, at 27 left",
               "  and 27 right 21 up, and 27 right 21 down: pilot hole 1.7 mm, 11 deep.",
               "Two stop ribs 1.2 thick above the sensor, 20 left and 2 right,",
               "  7 deep from the front face, their lower edge 0.2 above the sensor.",
               "Check: the sensor drops in under the ribs; the slots are clear."],
        **base))
    # 102 rear shell
    out.append(bv.component_sheet(
        Part("Rear shell", C["rear"][1], COL["rear"]), [ghost("Front shell", ["front"]), ghost("Cell", ["cell"]), ghost("Clip", ["clip"])],
        dwg_no="DBG-DWG-102", title="DustBadge rear shell: making sketch",
        material="PETG, dark grey, 3D printed, 0.2 mm layers, 4 walls",
        inset_view=(20, 120),
        notes=["Print rear face down; no supports needed.",
               "64 x 52 x 13 mm, walls 2 mm, outside edges round 4 mm.",
               "Three tubes 4.5 dia, from the rear wall to 14.2 from the rear face,",
               "  at the same places as the front bosses (seen from the front:",
               "  27 left and 27 right 21 up, 27 right 21 down); hole 2.4 through.",
               "Counterbore each from the rear face 4.2 dia, 1.4 deep (screw heads).",
               "Two clip bosses 5 dia, 5.5 long inside, 6 each side of centre,",
               "  21 up; pilot hole 1.7 mm, 7 deep from the rear face.",
               "Four cell ribs 1.2 thick, 3 tall, 0.2 off the cell: two at the",
               "  sides (12 long), two at top and bottom (5 long).",
               "The rim is 13 from the rear face; the gasket sits on it.",
               "Check: the cell drops between the ribs and lifts out freely."],
        **base))
    # 103 gasket
    g = C["gasket"][1]
    out.append(bv.component_sheet(
        Part("Gasket", g, COL["gasket"]), [ghost("Front shell", ["front"])],
        dwg_no="DBG-DWG-103", title="DustBadge gasket: making sketch", material="TPU 95A, 3D printed, 100 % infill",
        inset_view=(30, 120),
        notes=["A flat frame the shape of the shell rim: outside 64 x 52 with 4 mm",
               "  corners, inside 60 x 48 with 2 mm corners, 2 mm wide.",
               "Print 1.2 mm thick (six 0.2 mm layers) flat on the bed, slowly.",
               "The three shell screws squeeze it to about 1 mm.",
               "Fit: lay it on the front shell rim before the rear shell goes on;",
               "  its inside edge lines up with the inside of the walls.",
               "Check: it lies flat on the rim with no twist or gap."],
        **base))
    # 104 port seals, flipped so the top view shows them as seen from above
    out.append(bv.component_sheet(
        Part("Port seals", C["seals"][1], COL["seals"]), [ghost("Front shell", ["front"]), ghost("Screen", ["screen"])],
        dwg_no="DBG-DWG-104", title="DustBadge sensor port seals (make 2): making sketch", material="TPU 95A, 3D printed, 100 % infill",
        view_shape=b.Pos(0, 0, -D["floor"]) * C["seals"][1], inset_view=(55, 120),
        notes=["Two flat seals, each 16 x 11 mm with a 9 x 6 mm opening in the",
               "  middle that matches the sensor's inlet and outlet.",
               "Inlet seal (left, sits on the screen): 0.7 mm thick.",
               "Outlet seal (right, sits on the floor): 1.0 mm thick.",
               "Print flat, slowly. Mark the inlet seal so they cannot be swapped.",
               "Fit: centre each over its slot on the inner floor, 18 mm apart",
               "  centre to centre; a spot of adhesive holds it while assembling.",
               "The sensor rests on both seals, so they seal its ports to the",
               "  slots and the fan draws only outside air.",
               "Check: the sensor sits level on both seals."],
        **base))
    # 105 light pipe and LED
    out.append(bv.component_sheet(
        Part("Light pipe", C["led"][1], COL["led"]), [ghost("Front shell", ["front"]), ghost("LED", ["lamp"])],
        dwg_no="DBG-DWG-105", title="DustBadge light pipe: making sketch", material="Clear PETG, 3D printed, 100 % infill",
        view_shape=b.Rot(-90, 0, 0) * b.Pos(-P["led_pos"][0], 0, -P["led_pos"][1]) * C["led"][1], inset_view=(20, 120),
        notes=["A 4 mm rod 7 mm long with a 6 mm flange 1 mm thick, 3 mm from",
               "  its outer end; a 3 mm pocket 2.5 deep in its inner end.",
               "Print standing on its outer end, 100 % infill, so light runs along it.",
               "Fit: push it through the 4.4 mm hole from inside the front shell",
               "  until the flange sits on the inner face; it stands 1 mm proud",
               "  outside. A drop of clear adhesive on the flange holds it.",
               "Push the 3 mm red LED into the pocket; a drop of adhesive.",
               "Check: the LED lit by a 3 V coin cell shows clearly outside."],
        **base))
    # 106 inlet screen
    out.append(bv.component_sheet(
        Part("Inlet screen", C["screen"][1], COL["screen"]), [ghost("Front shell", ["front"]), ghost("Seals", ["seals"])],
        dwg_no="DBG-DWG-106", title="DustBadge inlet screen: making sketch", material="Stainless woven mesh, about 1 mm aperture, 0.3 mm wire",
        view_shape=b.Pos(0, 0, -D["floor"]) * C["screen"][1], inset_view=(55, 120),
        notes=["Cut a 16 x 11 mm square of mesh with fine snips.",
               "Flatten it between two steel blocks; file off any loose wire ends.",
               "Fit: lay it on the inner floor, centred over the inlet slot (the",
               "  left slot seen from the front); the inlet seal sits on it and",
               "  holds it down. Nothing else fixes it.",
               "Check: it covers the whole slot with 2 mm to spare all round."],
        **base))
    # 107 carrier board
    out.append(bv.component_sheet(
        Part("Carrier board", C["pcb"][1], COL["pcb"]), [ghost("Front shell", ["front"]), ghost("Sensor", ["sensor"])],
        dwg_no="DBG-DWG-107", title="DustBadge carrier board: making sketch", material="Perfboard, 2.54 mm pitch, 1.6 mm FR4",
        inset_view=(20, 120),
        notes=["Cut perfboard to 59 x 47 mm; file the edges straight and cut",
               "  each corner off 1.5 mm at 45 degrees to clear the shell corners.",
               "Three 2.2 mm holes at the boss positions (seen from the front:",
               "  27 left and 27 right 21 up from the centre, 27 right 21 down).",
               "A notch 3 wide and 4 tall in the right edge, centred 10 below",
               "  the centre, for the cell lead.",
               "Front face (toward the sensor), right-hand strip: controller",
               "  module on headers 12 to 30 right, 3.5 below to 17.5 above",
               "  centre; charger module 12.6 to 23.6 right, from the bottom",
               "  edge up 19 mm, its USB-C 1.2 below the bottom edge.",
               "The sensor's back rests on the left part of the front face.",
               "Check: the board sits flat on the three bosses."],
        **base))
    # 108 spring clip, drilled
    out.append(bv.component_sheet(
        Part("Spring clip", C["clip"][1], COL["clip"]), [ghost("Rear shell", ["rear"]), ghost("Clip screws", ["clip_screws"])],
        dwg_no="DBG-DWG-108", title="DustBadge spring clip: drilling sketch", material="Bought stainless spring clip, about 22 x 40 mm",
        view_shape=b.Pos(0, 0, -P["clip_z"]) * C["clip"][1], inset_view=(20, 120),
        notes=["A bought stainless spring clip with a strap loop, about 22 wide",
               "  and 40 long, base leaf about 1 mm thick.",
               "If its base leaf has no holes, drill two 2.2 mm holes 12 apart",
               "  across the leaf, 3 mm from its top end; open the clip and",
               "  clamp the leaf on wood to drill; deburr.",
               "Fit: base leaf flat on the rear face, centred, top end 2 mm",
               "  below the badge's top edge; two M2 x 8 screws into the bosses.",
               "Check: the screw heads sit flat and the clip still closes."],
        **base))
    return out


# ----------------------------------------------------------------- joints
def joints():
    out = []
    W, H = P["W"], P["H"]
    ix = D["inlet_x"]
    # 01 inlet section: floor slot, screen, seal and sensor port, cut through the inlet
    w = (ix - 30, ix, -32, -12, -H / 2 - 1, -H / 2 + 9)
    out.append(bv.joint([
        part("Front shell floor and inlet slot", None, COL["front"], shape=win(C["front"][1], *w)),
        part("Inlet screen", None, COL["screen"], shape=win(C["screen"][1], *w)),
        part("Inlet seal (0.7 mm)", None, COL["seals"], shape=win(C["seals"][1], *w)),
        part("Sensor, inlet port above the seal", None, COL["sensor"], shape=win(C["sensor"][1], *w) - bx(ix - 4.5, ix + 4.5, P["sensor_y"] - 3, P["sensor_y"] + 3, D["sensor_bottom"] - 1, D["sensor_bottom"] + 3)),
        part("Carrier board", None, COL["pcb"], shape=win(C["pcb"][1], *w))],
        OUT / "joint-02.png", "Joint 2: the inlet, cut through its centre (front of the badge to the left)",
        subtitle="Screen on the floor over the slot, seal on the screen, sensor port on the seal. Air rises straight into the sensor",
        elev=6, azim=-6, size=(8, 5.5)))
    # 02 the stack, cut through a stop rib: front wall, rib, sensor, board, cell, rear wall
    rx = P["rib_x"][0]
    w = (rx - 30, rx, -32, 1, -H / 2 - 1, H / 2 + 1)
    out.append(bv.joint([
        part("Front shell with stop rib", None, COL["front"], shape=win(C["front"][1], *w)),
        part("Particle sensor", None, COL["sensor"], shape=win(C["sensor"][1], *w)),
        part("Port seal", None, COL["seals"], shape=win(C["seals"][1] + C["screen"][1], *w)),
        part("Carrier board", None, COL["pcb"], shape=win(C["pcb"][1], *w)),
        part("Cell", None, COL["cell"], shape=win(C["cell"][1], *w)),
        part("Gasket", None, COL["gasket"], shape=win(C["gasket"][1], *w)),
        part("Rear shell", None, COL["rear"], shape=win(C["rear"][1], *w))],
        OUT / "joint-03.png", "Joint 3: how the sensor and cell are held (cut through the left stop rib)",
        subtitle="Sensor between the seals and the rib, with the board behind it; cell between the board and the rear shell",
        elev=8, azim=-12, size=(8, 6.5)))
    # 03 a shell screw, cut through its axis
    x0, z0 = P["bosses"][1]
    w = (x0 - 3.5, x0, -32, 2, z0 - 9, H / 2 + 1)
    out.append(bv.joint([
        part("Front shell and boss", None, COL["front"], shape=win(C["front"][1], *w)),
        part("Carrier board", None, COL["pcb"], shape=win(C["pcb"][1], *w)),
        part("Gasket", None, COL["gasket"], shape=win(C["gasket"][1], *w)),
        part("Rear shell and tube", None, COL["rear"], shape=win(C["rear"][1], *w)),
        part("M2 x 20 screw", None, "#B45309", shape=win(C["screws"][1], *w))],
        OUT / "joint-05.png", "Joint 5: a shell screw, cut through its centre (top right screw)",
        subtitle="Head in the rear counterbore; the tube presses the board onto the front boss; the gasket is squeezed between the rims",
        elev=10, azim=-15, size=(8, 6)))
    # 04 a clip screw, cut through its axis
    cxh, czh = P["clip_holes"][1]
    w = (cxh - 4, cxh, -12, 4, czh - 7, H / 2 + 1)
    out.append(bv.joint([
        part("Rear shell and clip boss", None, COL["rear"], shape=win(C["rear"][1], *w)),
        part("Spring clip base leaf", None, COL["clip"], shape=win(C["clip"][1], *w)),
        part("M2 x 8 screw", None, "#B45309", shape=win(C["clip_screws"][1], *w)),
        part("Cell (top edge)", None, COL["cell"], shape=win(C["cell"][1], *w))],
        OUT / "joint-06.png", "Joint 6: a clip screw, cut through its centre (wearer's side to the right)",
        subtitle="The screw goes through the clip's base leaf and the rear wall into a boss above the cell",
        elev=8, azim=-10, size=(8, 6)))
    # 05 cell in its ribs, rear shell seen from the open side
    out.append(bv.joint([
        part("Rear shell (inside)", ["rear"]),
        part("Cell", ["cell"]),
        part("Shell screws in their tubes", None, "#B45309", shape=C["screws"][1] & bx(-40, 40, -14.2, 0, -30, 30))],
        OUT / "joint-04.png", "Joint 4: the cell in the rear shell, seen from the open side",
        subtitle="Four ribs keep the cell 0.2 mm from them; the board, fitted next, stops it coming forward",
        elev=20, azim=-75, size=(8, 6)))
    # 06 light pipe, cut through its axis
    lx, lz = P["led_pos"]
    w = (lx - 8, lx, -32, -16, lz - 7, H / 2 + 1)
    out.append(bv.joint([
        part("Front shell", None, COL["front"], shape=win(C["front"][1], *w)),
        part("Light pipe, flange inside", None, COL["led"], shape=win(C["led"][1], *w)),
        part("Red LED in the pocket", None, COL["lamp"], shape=win(C["lamp"][1], *w)),
        part("Controller module", None, COL["module"], shape=win(C["module"][1], *w))],
        OUT / "joint-01.png", "Joint 1: the light pipe, cut through its centre (front to the left)",
        subtitle="The flange sits on the inner face; the pipe stands 1 mm proud outside; the LED is glued in its pocket",
        elev=10, azim=-15, size=(8, 6)))
    return out


# ----------------------------------------------------------------- assembly steps
def steps():
    out = []

    def st(n, done, new, title, sub, **kw):
        out.append(bv.step(done, new, OUT / f"step-{n:02d}.png", f"Step {n}: {title}", subtitle=sub, **kw))

    fs = part("Front shell", ["front"])
    inside = dict(elev=22, azim=140)            # looking into the open front shell from behind
    st(1, [fs], [part("Light pipe", ["led"], explode=(0, 12, 0)), part("Red LED", ["lamp"], explode=(0, 22, 0))],
       "light pipe and LED into the front shell",
       "Shell face down. Pipe through its hole from inside, flange on the inner face, a drop of adhesive; LED into the pocket",
       label_done=False, **inside)
    pipe = part("Light pipe and LED", ["led", "lamp"])
    st(2, [fs, pipe], [part("Vibration motor", ["motor"], explode=(0, 14, 0)), part("5 V boost module", ["boost"], explode=(0, 14, 0)),
                       part("Humidity breakout", ["rh"], explode=(0, 14, 0))],
       "motor, boost module and humidity breakout onto the front face",
       "Each on double-sided foam tape on the inside of the front face, leads already soldered; humidity breakout over its vent",
       label_done=False, **inside)
    l2 = [fs, pipe, part("Front-face parts", ["motor", "boost", "rh"])]
    st(3, l2, [part("Inlet screen", ["screen"], explode=(0, 0, 14)), part("Port seals (inlet on the screen)", ["seals"], explode=(0, 0, 26))],
       "screen and port seals onto the inner floor",
       "Screen over the inlet slot; the thin seal on the screen, the thick one over the outlet slot; a spot of adhesive each",
       label_done=False, elev=40, azim=110)
    l3 = l2 + [part("Screen and seals", ["screen", "seals"])]
    st(4, l3, [part("Particle sensor", ["sensor"], explode=(0, 18, 0))],
       "particle sensor into its pocket",
       "Ports down onto the seals, top under the two stop ribs, front face against the shell; plug in its cable first",
       label_done=False, **inside)
    st(5, [part("Carrier board", ["pcb"])], [part("Controller module", ["module"], explode=(0, -14, 0)),
                                           part("Charger module with USB-C", ["charger"], explode=(0, -14, 0))],
       "build the carrier board",
       "Both modules on header pins on the front face, soldered; then wire the board as the wiring diagram shows",
       label_done=True, elev=18, azim=-60)
    l4 = l3 + [part("Sensor", ["sensor"])]
    st(6, l4, [part("Carrier board with its modules", ["pcb", "module", "charger"], explode=(0, 30, 0))],
       "carrier board onto the front bosses",
       "Solder the front-face leads to it, then lay it on the three bosses, USB-C into its opening, back against the sensor",
       label_done=False, **inside)
    rs = part("Rear shell", ["rear"])
    st(7, [rs], [part("Spring clip", ["clip"], explode=(0, 14, 0)), part("Clip screws M2 x 8", ["clip_screws"], explode=(0, 30, 0))],
       "spring clip onto the rear shell",
       "Base leaf flat on the rear face, centred; two M2 x 8 screws into the bosses, snug (do not strip the plastic)",
       label_done=False, elev=20, azim=60)
    st(8, [rs, part("Clip", ["clip", "clip_screws"])], [part("Cell, 2,000 mAh", ["cell"], explode=(0, -16, 0))],
       "cell into the rear shell",
       "Between the four ribs, lead at the right; plug its lead into the charger module through the board's notch",
       label_done=False, elev=22, azim=-70)
    front_done = l4 + [part("Carrier board", ["pcb", "module", "charger"])]
    st(9, front_done, [part("Gasket", ["gasket"], explode=(0, 14, 0)),
                       part("Rear shell with the cell and clip", ["rear", "cell", "clip", "clip_screws"], explode=(0, 34, 0)),
                       part("Shell screws M2 x 20", ["screws"], explode=(0, 58, 0))],
       "close the badge",
       "Gasket on the front rim; rear shell on; three M2 x 20 screws from the rear face, tightened evenly, snug",
       label_done=False, elev=18, azim=60)
    return out


# ----------------------------------------------------------------- bottom-face layout
def layouts():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle, FancyBboxPatch
    INK, MUT, AC = "#111827", "#4B5563", "#0F766E"
    W, Dp = P["W"], P["D"]
    fd = Dp + P["split_y"]                          # front shell depth, 16 mm
    fig = plt.figure(figsize=(11, 6.4), dpi=150)
    ax = fig.add_axes([0.03, 0.08, 0.94, 0.74]); ax.set_aspect("equal"); ax.set_axis_off()
    # seen from below, front face at the bottom of the page; x to the right as seen from the front,
    # y = depth back from the front face
    ax.add_patch(Rectangle((-W / 2, 0), W, fd, fc="#FEF9C3", ec=INK, lw=1.2))
    ax.add_patch(Rectangle((-W / 2, fd), W, Dp - fd, fc="#E5E7EB", ec=MUT, lw=0.8, ls="--"))
    ax.text(0, fd + (Dp - fd) / 2, "gasket and rear shell (no openings)", ha="center", va="center", fontsize=8, color=MUT)
    ax.text(-W / 2 - 1.5, fd / 2, "front shell\n16 deep", ha="right", va="center", fontsize=8, color=MUT)
    ax.text(-W / 2 - 1.5, -0.5, "front face", ha="right", va="center", fontsize=8, color=MUT)
    ax.plot([0, 0], [-2, Dp + 2], color=MUT, lw=0.6, ls=(0, (8, 3, 2, 3)))
    ops = []
    for xx, name in ((D["inlet_x"], "Inlet slot (screened inside)"), (D["outlet_x"], "Outlet slot")):
        ops.append((name, xx, P["sensor_y"] + Dp, P["slot"][0], P["slot"][1], "below"))
    usb_y = D["pcb_front"] - P["charger"][1] / 2
    ops.append(("USB-C opening", P["usb_x"], usb_y + Dp, P["usb"][0] + 0.7, P["usb"][1] + 0.6, "right"))
    ops.append(("Humidity vent", P["rh_vent_x"], P["wall"] + P["rh"][1] / 2, 3.0, 2.0, "right"))
    for name, xc, yc, w_, h_, where in ops:
        ax.add_patch(Rectangle((xc - w_ / 2, yc - h_ / 2), w_, h_, fc="white", ec=INK, lw=1.1))
        ax.plot([xc, xc], [yc - h_ / 2 - 1.2, yc + h_ / 2 + 1.2], color=MUT, lw=0.4)
        ax.plot([xc - w_ / 2 - 1.2, xc + w_ / 2 + 1.2], [yc, yc], color=MUT, lw=0.4)
        side = f"{abs(xc):g} {'left' if xc < -0.05 else 'right'}"
        txt = f"{name}\n{w_:g} x {h_:g}, centre {side},\n{yc:g} back from the front face"
        if where == "below":
            ax.annotate(txt, xy=(xc, yc - h_ / 2), xytext=(xc, -6), ha="center", va="top", fontsize=7.6, color=INK,
                        linespacing=1.25, arrowprops=dict(arrowstyle="-", color=MUT, lw=0.5))
        else:
            ax.annotate(txt, xy=(xc + w_ / 2, yc), xytext=(W / 2 + 6, yc + (4 if yc > 6 else -4)), ha="left", va="center",
                        fontsize=7.6, color=INK, linespacing=1.25, arrowprops=dict(arrowstyle="-", color=MUT, lw=0.5))
    ax.set_xlim(-W / 2 - 16, W / 2 + 40); ax.set_ylim(-17, Dp + 3)
    fig.text(0.03, 0.965, "Front shell bottom face: the openings", fontsize=13, fontweight="bold", color=INK, va="top")
    fig.text(0.03, 0.915, "Seen from below, front face at the bottom of the page. Sizes in mm; sideways from the centre line (left and right as seen from the front),\n"
             "depth back from the front face. All are printed in, nothing is drilled. The screen and the seals sit on the inside over the two slots.",
             fontsize=8.2, color=MUT, va="top")
    fig.text(0.03, 0.02, "BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT", fontsize=7, color="#B45309")
    fig.text(0.97, 0.02, "github.com/BoujeeEnjinia1701/dustbadge", fontsize=7, color=AC, ha="right", family="monospace")
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / "bottom-face.png", facecolor="white"); plt.close(fig)
    return OUT / "bottom-face.png"


# ----------------------------------------------------------------- wiring
def wiring():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch
    fig = plt.figure(figsize=(12, 7.2), dpi=150)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 120); ax.set_ylim(0, 72); ax.set_axis_off()
    INK, MUT = "#111827", "#4B5563"
    ax.text(2, 70, "DustBadge prototype: block-level wiring", fontsize=13, fontweight="bold", color=INK, va="top")
    ax.text(2, 66.6, "Bought modules on perfboard, wired point to point; no circuit board is laid out. Stranded or solid copper as noted; "
            "every joint soldered and sleeved.", fontsize=8.5, color=MUT, va="top")
    ax.text(2, 1.5, "BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT", fontsize=7, color="#B45309")
    ax.text(118, 1.5, "github.com/BoujeeEnjinia1701/dustbadge", fontsize=7, color="#0F766E", ha="right", family="monospace")
    ax.add_patch(FancyBboxPatch((22, 12), 52, 48, boxstyle="round,pad=0.4", fc="#F0FDF4", ec="#86EFAC", lw=1, ls="--"))
    ax.text(23.5, 59, "On the carrier board", fontsize=8, color=MUT, va="top")
    ax.add_patch(FancyBboxPatch((79, 12), 26, 48, boxstyle="round,pad=0.4", fc="#FEFCE8", ec="#FDE047", lw=1, ls="--"))
    ax.text(80.5, 59, "In the front shell, off the board", fontsize=8, color=MUT, va="top")

    def blk(x, y, w, h, title, sub, color):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.3", fc="white", ec=color, lw=1.8))
        ax.text(x + w / 2, y + h - 1.1, title, ha="center", va="top", fontsize=8.4, fontweight="bold", color=INK)
        ax.text(x + w / 2, y + h - 3.7, sub, ha="center", va="top", fontsize=6.9, color=MUT, linespacing=1.25)

    def wire(pts, color, lw=2.0):
        xs, ys = zip(*pts)
        ax.plot(xs, ys, color=color, lw=lw, solid_capstyle="round", zorder=1)

    def lab(x, y, text, color, ha="left"):
        ax.text(x, y, text, fontsize=7, color=color, ha=ha, va="center", zorder=3,
                bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none"))
    RED, BLU, GRY = "#B91C1C", "#1D4ED8", "#6B7280"
    blk(3, 46, 14, 10, "USB-C charger", "5 V phone charger;\nbadge not worn", "#64748B")
    blk(3, 27, 14, 10, "LiPo cell", "2,000 mAh, protected,\nin the rear shell", "#C2410C")
    blk(25, 46, 16, 10, "Charger module", "500 mA to 4.2 V,\nNTC input, USB-C", "#16A34A")
    blk(25, 28, 16, 9, "Polyfuse", "0.75 A hold, feeds\nevery load", "#7C3AED")
    blk(51, 44, 20, 13, "Controller module", "nRF52840, BLE,\n2 MB flash;\npowered at its BAT pin", "#1D4ED8")
    blk(51, 27, 20, 10, "Motor driver", "small N-MOSFET, diode,\nLED resistor", "#475569")
    blk(82, 49, 16, 7, "Particle sensor", "5 V; I2C or UART", "#0F766E")
    blk(82, 40, 16, 8, "Humidity breakout", "3.3 V, I2C", "#0EA5E9")
    blk(82, 30, 16, 8, "Motor and LED", "front face, light pipe", "#DC2626")
    blk(82, 14, 16, 8, "5 V boost", "enable input", "#22C55E")
    wire([(17, 51), (25, 51)], RED); lab(21, 52.8, "USB-C", RED, "center")
    wire([(17, 32), (21, 32), (21, 48.5), (25, 48.5)], RED); lab(21.6, 42, "cell lead\nand NTC,\n0.2 mm²", RED)
    wire([(33, 46), (33, 37)], RED); lab(33.6, 41.5, "BAT,\n0.2 mm²", RED)
    wire([(41, 32.5), (46, 32.5), (46, 48), (51, 48)], RED); lab(46.6, 41.5, "0.2 mm²", RED)
    wire([(33, 28), (33, 18), (82, 18)], RED); lab(57, 19.6, "battery to the boost, 0.2 mm²", RED, "center")
    wire([(98, 18), (101.5, 18), (101.5, 52.5), (98, 52.5)], RED); lab(102.2, 36, "5 V", RED)
    wire([(71, 52.5), (82, 52.5)], BLU, 1.3); lab(76.5, 54.1, "signals", BLU, "center")
    wire([(71, 46), (82, 44)], BLU, 1.3); lab(76.5, 47.2, "I2C, 3.3 V", BLU, "center")
    wire([(61, 44), (61, 37)], GRY, 1.2); lab(61.6, 40.5, "GPIO", GRY)
    wire([(71, 32), (82, 34)], RED, 1.4); lab(76.5, 30.6, "0.08 mm²", RED, "center")
    ax.text(3, 9.6, "Signal and control wires 0.08 mm² (28 AWG). The controller also switches the boost on and off through its enable "
            "input, wired alongside the boost feed.", fontsize=7.2, color=MUT)
    ax.text(3, 7.0, "Safety: no cell in the shell until the stop points in section 6 of the plan are passed. Never charge while worn, "
            "below 0 °C or above 45 °C.", fontsize=7.6, color="#B45309", fontweight="bold")
    ax.text(3, 4.2, "Red: power. Blue: signal. Grey: sensing and control. All circuits are extra-low voltage: 4.2 V at most on the cell, "
            "5 V from USB and on the sensor rail.", fontsize=7.2, color=MUT)
    out = OUT / "wiring.png"
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, facecolor="white"); plt.close(fig)
    return out


if __name__ == "__main__":
    what = sys.argv[1:] or ["overview", "sheets", "layouts", "joints", "steps", "wiring"]
    fns = {"overview": overview, "sheets": sheets, "layouts": layouts, "joints": joints, "steps": steps, "wiring": wiring}
    for w in what:
        r = fns[w]()
        print(w, "->", r)

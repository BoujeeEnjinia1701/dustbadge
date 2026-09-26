"""DustBadge general arrangement sheet DBG-DWG-001, Rev P1 (TRL 3).

Run from the repo root:  python cad/src/sheets.py
Writes cad/drawings/DBG-DWG-001.svg, .pdf and .png from the parametric model in
cad/src/model.py with .kit/drawing.py. Dimensions come from PARAMS and derived(), so they
follow any parameter change. The concept blueprint in media/ is DBG-DWG-010.
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
from drawing import Sheet, _viewbox, _t, M, TB_Y, INK, MUTED  # noqa: E402
from model import PARAMS as P, assembly, derived, masses  # noqa: E402

DATE = "2026-09-25"


def safe_project_views(part, workdir, line_weight=0.35):
    """Same views as drawing.project_views, but edge by edge, so that a degenerate edge from the
    hidden-line projection is skipped instead of stopping the export."""
    from build123d import ExportSVG, LineType, Unit
    workdir = Path(workdir); workdir.mkdir(parents=True, exist_ok=True)
    bb = part.bounding_box()
    c = bb.center(); d = max(bb.size.X, bb.size.Y, bb.size.Z) * 10
    setups = {"front": ((c.X, c.Y - d, c.Z), (0, 0, 1)), "top": ((c.X, c.Y, c.Z + d), (0, 1, 0)),
              "right": ((c.X + d, c.Y, c.Z), (0, 0, 1)), "iso": ((c.X + d, c.Y - d, c.Z + d * 0.8), (0, 0, 1))}
    out, skipped = {}, 0
    for name, (origin, up) in setups.items():
        visible, hidden = part.project_to_viewport(origin, up, (c.X, c.Y, c.Z))
        ex = ExportSVG(unit=Unit.MM, line_weight=line_weight)
        ex.add_layer("Visible", line_color=0x111827)
        ex.add_layer("Hidden", line_color=0x6B7280, line_type=LineType.ISO_DASH, line_weight=line_weight / 2)
        for layer, edges in (("Visible", visible), ("Hidden", hidden if name != "iso" else [])):
            for e in edges:
                try:
                    ex.add_shape(e, layer=layer)
                except (AssertionError, ValueError, ZeroDivisionError):
                    skipped += 1
        p = workdir / f"{name}.svg"
        ex.write(str(p))
        out[name] = p
    print(f"projected views; skipped {skipped} degenerate edges")
    return out


def ortho_cells(sheet, views, names=("front", "top", "right")):
    """Repeat Sheet.add_ortho's layout arithmetic to find where each view lands (x, y, w, h)."""
    ax, ay, aw, ah = M + 10, M + 16, 245, TB_Y - M - 20
    gap, lab = 14, 12
    dims = {n: _viewbox(Path(views[n]).read_text())[2:] for n in names}
    fw, fh = dims["front"]; tw, th = dims["top"]; rw, rh = dims["right"]
    k = sheet.scale
    ax += (aw - (k * (max(fw, tw) + rw) + gap)) / 2
    ay += (ah - (k * (th + max(fh, rh)) + gap + 2 * lab)) / 2
    colw = k * max(fw, tw)
    front_y = ay + k * th + lab + gap
    row_h = k * max(fh, rh)
    return {"top": (ax, ay, colw, k * th), "front": (ax, front_y, colw, row_h),
            "right": (ax + colw + gap, front_y, k * rw, row_h)}


def dim_h(x1, x2, y, text):
    a = 1.4
    return [f'<line x1="{x1:.2f}" y1="{y:.2f}" x2="{x2:.2f}" y2="{y:.2f}" stroke="{INK}" stroke-width="0.18"/>',
            f'<path d="M{x1:.2f} {y:.2f} l{a} -0.5 l0 1 Z" fill="{INK}"/>',
            f'<path d="M{x2:.2f} {y:.2f} l{-a} -0.5 l0 1 Z" fill="{INK}"/>',
            _t((x1 + x2) / 2, y - 1.0, text, 2.3, 400, INK, "middle", mono=True)]


def dim_v(x, y1, y2, text, side=-1):
    a = 1.4
    cx, cy = x + side * 1.0, (y1 + y2) / 2
    return [f'<line x1="{x:.2f}" y1="{y1:.2f}" x2="{x:.2f}" y2="{y2:.2f}" stroke="{INK}" stroke-width="0.18"/>',
            f'<path d="M{x:.2f} {y1:.2f} l-0.5 {a} l1 0 Z" fill="{INK}"/>',
            f'<path d="M{x:.2f} {y2:.2f} l-0.5 {-a} l1 0 Z" fill="{INK}"/>',
            f'<g transform="rotate(-90 {cx:.2f} {cy:.2f})">{_t(cx, cy, text, 2.3, 400, INK, "middle", mono=True)}</g>']


def ext(x1, y1, x2, y2):
    return f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{MUTED}" stroke-width="0.13"/>'


def leader(x1, y1, x2, y2, text, anchor="start"):
    return [f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{MUTED}" stroke-width="0.15"/>',
            f'<circle cx="{x1:.2f}" cy="{y1:.2f}" r="0.5" fill="{INK}"/>',
            _t(x2 + (1 if anchor == "start" else -1), y2 + 0.8, text, 2.1, 400, INK, anchor)]


def main():
    D = derived(P)
    work = ROOT / "cad" / "drawings" / "_views"
    asm = assembly()
    views = safe_project_views(asm, work)
    bb = asm.bounding_box()
    s = Sheet(project="DustBadge", title="General arrangement", dwg_no="DBG-DWG-001", rev="P1",
              author="Amish Chadha", date=DATE, scale=None, theme="technical",
              material="PETG shells; bought-in parts per bom/bom.csv. PRELIMINARY, NOT FOR FABRICATION",
              revisions=[("P1", "Preliminary GA for TRL 3 (from cad/src/model.py)", DATE, "AC")])
    s.add_ortho(views)
    k = s.scale
    c = ortho_cells(s, views)
    L = []
    W, H, Dp = P["W"], P["H"], P["D"]

    # front view (from -Y): X to the right, Z up
    x, y, w, h = c["front"]
    X = lambda mx: x + (mx - bb.min.X) * k
    Z = lambda mz: y + h - (mz - bb.min.Z) * k
    yb = Z(H / 2) - 8
    L += [ext(X(-W / 2), Z(H / 2) - 1, X(-W / 2), yb - 1), ext(X(W / 2), Z(H / 2) - 1, X(W / 2), yb - 1)]
    L += dim_h(X(-W / 2), X(W / 2), yb, f"{W:.0f}")
    xl = X(-W / 2) - 8
    L += [ext(X(-W / 2) - 1, Z(H / 2), xl - 1, Z(H / 2)), ext(X(-W / 2) - 1, Z(-H / 2), xl - 1, Z(-H / 2))]
    L += dim_v(xl, Z(H / 2), Z(-H / 2), f"{H:.0f}")
    lx, lz = P["led_pos"]
    L += leader(X(lx), Z(lz), X(-W / 2) - 16, Z(H / 2) + 8, "6 ALERT LED LIGHT PIPE", "end")
    L += leader(X(P["motor_pos"][0]), Z(P["motor_pos"][2]), X(-W / 2) - 16, Z(-H / 2) + 4, "5 MOTOR (HIDDEN)", "end")
    L += leader(X(P["sensor_x"]), Z(0), X(-W / 2) - 16, Z(H / 2) - 4, "3 SENSOR 41 x 41 x 12 (HIDDEN)", "end")

    # top view (from +Z): X to the right, Y up the sheet; shows the bottom-face openings as hidden lines
    x, y, w, h = c["top"]
    Xt = lambda mx: x + (mx - bb.min.X) * k
    Yt = lambda my: y + h - (my - bb.min.Y) * k
    ya = Yt(bb.max.Y) - 5
    for xx, lab in ((D["inlet_x"], "INLET"), (D["outlet_x"], "OUTLET")):
        L.append(_t(Xt(xx), ya, lab, 1.9, 600, INK, "middle"))
    L += dim_h(Xt(D["inlet_x"]), Xt(D["outlet_x"]), ya - 4, f"{D['outlet_x'] - D['inlet_x']:.0f}")
    L.append(_t(Xt(bb.max.X) + 3, Yt(bb.min.Y) - 1, "FRONT FACE (-Y), WORN FACING OUT", 1.9, 400, MUTED))

    # right view (from +X): -Y to the left? looking along -X, +Y appears to the right
    x, y, w, h = c["right"]
    Yr = lambda my: x + (my - bb.min.Y) * k
    Zr = lambda mz: y + h - (mz - bb.min.Z) * k
    yd = Zr(H / 2) - 6
    L += [ext(Yr(-Dp), Zr(H / 2) - 1, Yr(-Dp), yd - 1), ext(Yr(0), Zr(H / 2) - 1, Yr(0), yd - 1)]
    L += dim_h(Yr(-Dp), Yr(0), yd, f"{Dp:.0f}")
    yd2 = Zr(H / 2) - 14
    L += [ext(Yr(bb.min.Y), Zr(H / 2) - 1, Yr(bb.min.Y), yd2 - 1), ext(Yr(bb.max.Y), Zr(H / 2) - 1, Yr(bb.max.Y), yd2 - 1)]
    L += dim_h(Yr(bb.min.Y), Yr(bb.max.Y), yd2, f"{bb.size.Y:.0f} OVERALL")
    L += leader(Yr(P["split_y"]), Zr(H / 2 - 6), Yr(bb.max.Y) + 6, Zr(H / 2) - 4, "SHELL JOINT, GASKET")
    L += leader(Yr(P["clip"][1] / 2), Zr(P["clip_z"]), Yr(bb.max.Y) + 6, Zr(P["clip_z"]), "10 CLIP")
    L += leader(Yr(P["sensor_y"]), Zr(-H / 2), Yr(P["sensor_y"]) - 4, Zr(-H / 2) + 14, "AIR IN (DOWN)", "end")

    s._layers += L
    s.add_svg(views["iso"], 276, 32, 140, 100, label="Isometric view", sublabel="Not to scale")
    m = sum(masses(P).values())
    s.add_notes("Main dimensions and interfaces (mm)", [
        f"Shells {W:.0f} x {H:.0f} x {Dp:.0f}; {bb.size.Y:.0f} deep with clip; wall {P['wall']:.0f}; joint {-P['split_y']:.0f} from rear",
        f"Sensor SPS30 class {P['sensor'][0]:.0f} x {P['sensor'][2]:.0f} x {P['sensor'][1]:.0f}, ports down onto two slots",
        f"Slots {P['slot'][0]:.0f} x {P['slot'][1]:.0f}: inlet (screened) at X {D['inlet_x']:.0f}, outlet at X {D['outlet_x']:.0f}",
        f"USB-C opening at X {P['usb_x']:.0f}; humidity vent at X {P['rh_vent_x']:.0f}; all in the bottom face",
        f"Cell {P['cell'][0]:.0f} x {P['cell'][2]:.0f} x {P['cell'][1]:.0f}, 1,500 mAh; up to 11.5 thick fits",
        f"Three M2 bosses; carrier board {P['pcb'][0]:.0f} x {P['pcb'][2]:.0f} rests on them",
        f"Mass {m:.0f} g (DBG-CAL-001); inlet {D['inlet_to_face_mm']:.0f} from nose and mouth when worn",
        "Not intrinsically safe; not for gassy mines or explosive atmospheres",
        "Third-angle; front view from -Y; origin at the badge center, rear face Y = 0",
    ], x=276, y=158, width=146)
    out = s.save(ROOT / "cad" / "drawings" / "DBG-DWG-001")
    shutil.rmtree(work, ignore_errors=True)
    print(f"wrote {out} and .pdf, .png at scale {k:g}:1" if k >= 1 else f"wrote {out} at 1:{1 / k:g}")


if __name__ == "__main__":
    main()

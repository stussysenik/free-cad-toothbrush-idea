#!/usr/bin/env python3
"""
Sonicare-to-Philips One Adapter
Build a SINGLE visible solid. No boolean chain madness.
"""
import sys, os, math
sys.path.insert(0, '/Applications/FreeCAD.app/Contents/Resources/lib')

import FreeCAD
import Part

OUTPUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'SonicareAdapter.FCStd')

# ─── PARAMETERS (mm) ─── adjust these with caliper measurements ───
# Philips One handle top (conical)
HANDLE_CONE_BASE_DIA = 16.0   # diameter at base of the conical top
HANDLE_CONE_TIP_DIA  = 8.0    # diameter at the tip where shaft starts
HANDLE_CONE_HEIGHT   = 8.0    # height of the conical section

# Metal drive shaft
SHAFT_DIA            = 3.0    # shaft diameter
SHAFT_CLEARANCE      = 0.5    # extra clearance around shaft

# Sonicare brush head connector (the funnel/trumpet stem)
HEAD_INNER_DIA_BOT   = 9.0    # inner diameter at bottom of head stem
HEAD_INNER_DIA_TOP   = 15.0   # inner diameter at top of head stem (flared)
HEAD_STEM_HEIGHT     = 25.0   # height of the head's connector stem

# Adapter design
ADAPTER_COLLAR_DIA   = 13.5   # outer diameter of collar (head slides over this)
ADAPTER_COLLAR_H     = 15.0   # collar height (sits inside head stem)
ADAPTER_GRIP_H       = 8.0    # how far adapter wraps over handle cone
ADAPTER_WALL_MIN     = 2.0    # minimum wall thickness
SNAP_LIP_DIA         = 14.2   # snap lip OD (slightly larger than collar)
SNAP_LIP_H           = 1.5    # snap lip height
PRINT_TOL            = 0.2    # FDM tolerance

# ─── BUILD ───────────────────────────────────────────────────────

doc = FreeCAD.newDocument("SonicareAdapter")

# === SPREADSHEET (for documentation & future parametric use) ===
sheet = doc.addObject('Spreadsheet::Sheet', 'Params')
params = [
    ('handle_cone_base_dia', HANDLE_CONE_BASE_DIA, 'Philips One cone base diameter'),
    ('handle_cone_tip_dia',  HANDLE_CONE_TIP_DIA,  'Philips One cone tip diameter'),
    ('handle_cone_height',   HANDLE_CONE_HEIGHT,    'Philips One cone height'),
    ('shaft_dia',            SHAFT_DIA,             'Metal shaft diameter'),
    ('shaft_clearance',      SHAFT_CLEARANCE,       'Clearance around shaft'),
    ('adapter_collar_dia',   ADAPTER_COLLAR_DIA,    'Adapter collar outer diameter'),
    ('adapter_collar_h',     ADAPTER_COLLAR_H,      'Adapter collar height'),
    ('adapter_grip_h',       ADAPTER_GRIP_H,        'Grip depth over handle cone'),
    ('adapter_wall_min',     ADAPTER_WALL_MIN,       'Minimum wall thickness'),
    ('snap_lip_dia',         SNAP_LIP_DIA,          'Snap lip outer diameter'),
    ('snap_lip_h',           SNAP_LIP_H,            'Snap lip height'),
    ('print_tol',            PRINT_TOL,             'FDM print tolerance'),
]
sheet.set('A1', 'Parameter')
sheet.set('B1', 'Value (mm)')
sheet.set('C1', 'Description')
for i, (name, val, desc) in enumerate(params, start=2):
    sheet.set(f'A{i}', name)
    sheet.set(f'B{i}', str(val))
    sheet.set(f'C{i}', desc)
    sheet.setAlias(f'B{i}', name)
sheet.recompute()

# === GEOMETRY (built as raw shapes, assigned to ONE feature) ===

collar_r = ADAPTER_COLLAR_DIA / 2
collar_h = ADAPTER_COLLAR_H
grip_h   = ADAPTER_GRIP_H
total_h  = grip_h + collar_h
shaft_r  = (SHAFT_DIA + SHAFT_CLEARANCE + PRINT_TOL) / 2
snap_r   = SNAP_LIP_DIA / 2
snap_h   = SNAP_LIP_H

# Grip section: matches the Philips One conical top
# Outer = cylinder at collar diameter extending down
# Inner = cone matching the handle cone (inverted, wider at bottom)
grip_cone_r_bot = (HANDLE_CONE_BASE_DIA / 2) + PRINT_TOL  # wider (base of handle cone)
grip_cone_r_top = (HANDLE_CONE_TIP_DIA / 2) + PRINT_TOL   # narrower (tip of handle cone)

# OUTER SHAPE: collar cylinder + grip skirt
# The collar is a straight cylinder
outer_collar = Part.makeCylinder(collar_r, collar_h,
                                 FreeCAD.Vector(0, 0, grip_h))

# The grip section outer - slightly larger than the handle cone
grip_outer_r_bot = max(grip_cone_r_bot + ADAPTER_WALL_MIN, collar_r)
grip_outer_r_top = collar_r

# If grip is wider than collar at bottom, make a cone; otherwise cylinder
if abs(grip_outer_r_bot - grip_outer_r_top) > 0.1:
    outer_grip = Part.makeCone(grip_outer_r_bot, grip_outer_r_top, grip_h,
                                FreeCAD.Vector(0, 0, 0))
else:
    outer_grip = Part.makeCylinder(collar_r, grip_h)

outer = outer_grip.fuse(outer_collar)

# INNER CAVITY: conical bore matching handle cone shape
# The cone is wider at z=0 (handle base) and narrower at z=grip_h (handle tip)
inner_cone = Part.makeCone(grip_cone_r_bot, grip_cone_r_top, grip_h,
                            FreeCAD.Vector(0, 0, 0))

# SHAFT HOLE: straight bore through entire part
shaft_hole = Part.makeCylinder(shaft_r, total_h + 2,
                                FreeCAD.Vector(0, 0, -1))

# SNAP LIP: small ring at top of collar
snap_ring = Part.makeCylinder(snap_r, snap_h,
                               FreeCAD.Vector(0, 0, total_h - snap_h))
# Bore out the inside of snap ring so it's just a ring
snap_bore = Part.makeCylinder(collar_r - 0.01, snap_h + 1,
                               FreeCAD.Vector(0, 0, total_h - snap_h - 0.5))
snap_final = snap_ring.cut(snap_bore)

# FLEX SLITS: 4 slits for press-fit flex
slit_w = 1.5
slit_depth = grip_h * 0.75
slit_len = grip_outer_r_bot * 2 + 4

slit1 = Part.makeBox(slit_w, slit_len, slit_depth,
                      FreeCAD.Vector(-slit_w/2, -slit_len/2, 0))
slit2 = Part.makeBox(slit_len, slit_w, slit_depth,
                      FreeCAD.Vector(-slit_len/2, -slit_w/2, 0))

# COMBINE
adapter = outer.fuse(snap_final)
adapter = adapter.cut(inner_cone)
adapter = adapter.cut(shaft_hole)
adapter = adapter.cut(slit1)
adapter = adapter.cut(slit2)

# Clean up the shape
adapter = adapter.removeSplitter()

# === CREATE SINGLE FEATURE ===
feat = doc.addObject("Part::Feature", "SonicareAdapter")
feat.Shape = adapter

doc.recompute()

# === SAVE WITH GUI DATA ===
doc.saveAs(OUTPUT)

# Now inject GuiDocument.xml for proper visibility
FreeCAD.closeDocument(doc.Name)

import zipfile, shutil
TEMP = OUTPUT + '.tmp'
gui_xml = '''<?xml version='1.0' encoding='utf-8'?>
<Document SchemaVersion="1">
    <ViewProviderData Count="2">
        <ViewProvider name="SonicareAdapter" expanded="0">
            <Properties Count="2">
                <Property name="Visibility" type="App::PropertyBool" status="1">
                    <Bool value="true"/>
                </Property>
                <Property name="Selectable" type="App::PropertyBool">
                    <Bool value="true"/>
                </Property>
            </Properties>
        </ViewProvider>
        <ViewProvider name="Params" expanded="0">
            <Properties Count="1">
                <Property name="Visibility" type="App::PropertyBool" status="1">
                    <Bool value="true"/>
                </Property>
            </Properties>
        </ViewProvider>
    </ViewProviderData>
</Document>'''

with zipfile.ZipFile(OUTPUT, 'r') as zin:
    with zipfile.ZipFile(TEMP, 'w') as zout:
        for item in zin.infolist():
            zout.writestr(item, zin.read(item.filename))
        zout.writestr('GuiDocument.xml', gui_xml.encode('utf-8'))
shutil.move(TEMP, OUTPUT)

# Print summary
bb = adapter.BoundBox
print(f"\n=== SonicareAdapter ===")
print(f"File: {OUTPUT}")
print(f"Size: {bb.XLength:.1f} x {bb.YLength:.1f} x {bb.ZLength:.1f} mm")
print(f"Volume: {adapter.Volume:.1f} mm³")
print(f"Total height: {total_h:.1f} mm (grip {grip_h} + collar {collar_h})")
print(f"Collar OD: {ADAPTER_COLLAR_DIA} mm")
print(f"Grip cone bore: {HANDLE_CONE_BASE_DIA}mm -> {HANDLE_CONE_TIP_DIA}mm")
print(f"\nDouble-click the .FCStd file to open!")

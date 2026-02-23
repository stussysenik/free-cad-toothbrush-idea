# Technical Documentation

## Python Script Details

### generate_adapter.py

The main parametric build script. Creates the adapter using FreeCAD's Part workbench API:

1. **Outer shape:** Fuses a grip cone (matching Philips One handle taper) with a collar cylinder
2. **Inner cavity:** Cuts a conical bore matching the handle geometry (with print tolerance)
3. **Shaft hole:** Cuts a through-bore for the drive shaft (3mm + clearance)
4. **Snap lip:** Adds a retention ring at the collar top
5. **Flex slits:** Cuts two perpendicular slots extending 75% down the grip depth

All 12 parameters are defined as constants at the top of the file. The script also:
- Creates a FreeCAD Spreadsheet object with all parameters
- Injects `GuiDocument.xml` into the FCStd ZIP for GUI visibility
- Prints a build summary with dimensions and volume

### export_stl.py

Opens the FCStd file, recomputes, and exports the `SonicareAdapter` shape to binary STL. Reports bounding box dimensions (X, Y, Z), volume (mm³), and surface area (mm²).

### fix_visibility.py

Diagnostic tool that iterates all objects in the FCStd, checks if each has a valid Shape, and reports bounding boxes. Used when objects aren't visible in FreeCAD GUI.

### fix_fcstd.py

Workaround for headless FreeCAD not generating GUI data. Manually creates `GuiDocument.xml` with ViewProvider entries for each object:
- `SonicareAdapter` → visible, teal color (0x4CB0BFFF)
- All construction objects → hidden, gray

Injects the XML directly into the FCStd ZIP archive.

## FreeCAD Workflow

### Headless (CLI)

```bash
# Generate model from parameters
freecadcmd generate_adapter.py

# Export to STL
freecadcmd export_stl.py

# Debug visibility issues
freecadcmd fix_visibility.py
```

### GUI (Interactive)

1. Open FreeCAD → File → Open → `SonicareAdapter.FCStd`
2. Or run `build_adapter.FCMacro` to rebuild from scratch
3. The macro sets teal material, adjusts camera, prints summary
4. Export via File → Export → STL

## Parametric Design

All dimensions flow from 12 constants in `generate_adapter.py`. To modify the adapter:

1. Change parameter values (e.g., `ADAPTER_COLLAR_DIA = 14.0`)
2. Run `freecadcmd generate_adapter.py`
3. Run `freecadcmd export_stl.py`
4. Slice and print the new STL

The boolean operation chain: outer cone + collar → fuse → cut inner bore → cut shaft hole → add snap lip → cut flex slits → `removeSplitter()` for clean geometry.

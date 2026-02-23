# Sonicare-to-Philips One Toothbrush Adapter

A parametric 3D-printable adapter that lets you use Sonicare brush heads on a Philips One electric toothbrush handle. Designed in FreeCAD with Python scripting for fully reproducible geometry.

## The Problem

Sonicare brush heads don't fit on the Philips One handle — the connector geometries are different. This adapter bridges them with a press-fit mechanical coupling.

## Design Overview

The adapter consists of:
- **Grip section** (8mm) — conical bore that wraps over the Philips One handle tip
- **Collar section** (15mm) — straight cylinder where the Sonicare head slides on
- **Snap lip** (1.5mm) — retention ring preventing the head from sliding off
- **Shaft hole** (3mm) — central bore for the metal drive shaft to pass through
- **Flex slits** — two perpendicular 1.5mm cuts allowing press-fit flexibility

## Key Parameters

| Parameter | Value | Description |
|-----------|-------|-------------|
| Handle cone base | 16.0 mm | Philips One handle widest diameter |
| Handle cone tip | 8.0 mm | Philips One handle narrowest diameter |
| Adapter collar OD | 13.5 mm | Outer diameter of Sonicare connection |
| Snap lip OD | 14.2 mm | Retention ring outer diameter |
| Wall minimum | 2.0 mm | Minimum structural wall thickness |
| Print tolerance | 0.2 mm | FDM printing clearance buffer |

## How to Generate

### Headless (recommended)
```bash
freecadcmd generate_adapter.py
freecadcmd export_stl.py
```

### FreeCAD GUI
1. Open FreeCAD
2. Macro → Execute Macro → select `build_adapter.FCMacro`
3. File → Export → save as STL

## Printing

- **Material:** PLA or PETG
- **Layer height:** 0.15–0.2mm recommended
- **Infill:** 100% (small part, structural)
- **Supports:** Not needed (simple geometry)
- **Estimated volume:** ~1000 mm³

## Project Structure

```
free-cad-toothbrush-idea/
├── generate_adapter.py      # Main parametric build script (headless)
├── build_adapter.FCMacro    # FreeCAD GUI macro (interactive)
├── export_stl.py            # Export model to STL for printing
├── fix_visibility.py        # Debug shape validity in FCStd
├── fix_fcstd.py             # Inject GUI data into FCStd archive
├── SonicareAdapter.FCStd    # FreeCAD project file
├── SonicareAdapter.stl      # Ready-to-print mesh (1.4 MB)
├── openspec/                # Spec-driven development config
└── nvim-portable/           # Portable Neovim configuration
```

## Scripts

| Script | Purpose |
|--------|---------|
| `generate_adapter.py` | Build the complete adapter model from parameters |
| `export_stl.py` | Export to STL with bounding box and volume stats |
| `fix_visibility.py` | Check and report shape validity of all objects |
| `fix_fcstd.py` | Inject GuiDocument.xml for correct visibility in FreeCAD |
| `build_adapter.FCMacro` | Interactive builder for FreeCAD GUI |

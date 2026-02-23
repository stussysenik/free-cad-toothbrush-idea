"""Export the adapter to STL and print dimensions."""
import sys
import os
sys.path.insert(0, '/Applications/FreeCAD.app/Contents/Resources/lib')
import FreeCAD

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
fcstd = os.path.join(OUTPUT_DIR, 'SonicareAdapter.FCStd')
stl_out = os.path.join(OUTPUT_DIR, 'SonicareAdapter.stl')

doc = FreeCAD.openDocument(fcstd)
doc.recompute()

adapter = doc.getObject("SonicareAdapter")
if adapter and hasattr(adapter, 'Shape') and not adapter.Shape.isNull():
    shape = adapter.Shape
    shape.exportStl(stl_out)
    print(f"STL exported: {stl_out}")
    bb = shape.BoundBox
    print("\nBounding box:")
    print(f"  X: {bb.XLength:.1f} mm (width)")
    print(f"  Y: {bb.YLength:.1f} mm (depth)")
    print(f"  Z: {bb.ZLength:.1f} mm (height)")
    print(f"Volume: {shape.Volume:.1f} mm^3")
    print(f"Surface area: {shape.Area:.1f} mm^2")
else:
    print("ERROR: SonicareAdapter shape not found or is null")
    for obj in doc.Objects:
        has_shape = hasattr(obj, 'Shape') and not obj.Shape.isNull() if hasattr(obj, 'Shape') else False
        print(f"  {obj.Name} ({obj.TypeId}) shape_ok={has_shape}")

FreeCAD.closeDocument(doc.Name)

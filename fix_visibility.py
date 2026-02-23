"""Fix visibility — make SonicareAdapter visible and fit view."""
import sys, os
sys.path.insert(0, '/Applications/FreeCAD.app/Contents/Resources/lib')
import FreeCAD

fcstd = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'SonicareAdapter.FCStd')
doc = FreeCAD.openDocument(fcstd)
doc.recompute()

# Check all objects and their shapes
for obj in doc.Objects:
    has_shape = hasattr(obj, 'Shape')
    is_null = obj.Shape.isNull() if has_shape else True
    is_valid = obj.Shape.isValid() if has_shape and not is_null else False
    print(f"  {obj.Name:20s}  type={obj.TypeId:25s}  hasShape={has_shape}  null={is_null}  valid={is_valid}")

adapter = doc.getObject("SonicareAdapter")
if adapter:
    print(f"\nAdapter shape null: {adapter.Shape.isNull()}")
    print(f"Adapter shape valid: {adapter.Shape.isValid()}")
    if not adapter.Shape.isNull():
        bb = adapter.Shape.BoundBox
        print(f"BoundBox: {bb.XMin:.1f},{bb.YMin:.1f},{bb.ZMin:.1f} -> {bb.XMax:.1f},{bb.YMax:.1f},{bb.ZMax:.1f}")

FreeCAD.closeDocument(doc.Name)

"""
Inject GuiDocument.xml into the .FCStd to control visibility and colors.
Headless freecadcmd doesn't create GUI data — we add it manually.
"""
import zipfile
import os
import shutil

FCSTD = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'SonicareAdapter.FCStd')
TEMP = FCSTD + '.tmp'

# All Part objects in the model (from Document.xml)
ALL_OBJECTS = [
    'Grip', 'Shoulder', 'Collar', 'GripPlusShoulder', 'OuterBody',
    'HandleBore', 'ShaftBore', 'AllBores', 'BodyWithBores',
    'LipOuter', 'LipInner', 'LipRing', 'BodyWithLip',
    'SlitY', 'SlitX', 'AfterSlitY', 'SonicareAdapter'
]
VISIBLE = {'SonicareAdapter'}

def make_viewprovider(name, visible):
    vis = 'true' if visible else 'false'
    # Teal-ish color for the adapter, gray for hidden
    if name == 'SonicareAdapter':
        diffuse = '1283702527'  # 0x4CB0BFFF — teal
        transparency = '0'
    else:
        diffuse = '3435973887'  # gray
        transparency = '0'

    return f'''    <ViewProvider name="{name}" expanded="0">
        <Properties Count="3">
            <Property name="Visibility" type="App::PropertyBool" status="1">
                <Bool value="{vis}"/>
            </Property>
            <Property name="ShapeAppearance" type="App::PropertyMaterialList">
                <MaterialList file=""/>
            </Property>
            <Property name="Selectable" type="App::PropertyBool">
                <Bool value="true"/>
            </Property>
        </Properties>
    </ViewProvider>'''

# Build GuiDocument.xml
gui_xml = '''<?xml version='1.0' encoding='utf-8'?>
<Document SchemaVersion="1" >
    <ViewProviderData Count="{count}">
{providers}
    </ViewProviderData>
    <Camera settings=""/>
</Document>'''.format(
    count=len(ALL_OBJECTS) + 1,  # +1 for Params
    providers='\n'.join(
        make_viewprovider(name, name in VISIBLE)
        for name in ALL_OBJECTS
    ) + '\n' + '''    <ViewProvider name="Params" expanded="0">
        <Properties Count="1">
            <Property name="Visibility" type="App::PropertyBool" status="1">
                <Bool value="true"/>
            </Property>
        </Properties>
    </ViewProvider>'''
)

# Inject into the FCStd ZIP
with zipfile.ZipFile(FCSTD, 'r') as zin:
    with zipfile.ZipFile(TEMP, 'w') as zout:
        for item in zin.infolist():
            zout.writestr(item, zin.read(item.filename))
        # Add GuiDocument.xml
        zout.writestr('GuiDocument.xml', gui_xml.encode('utf-8'))

shutil.move(TEMP, FCSTD)
print("Injected GuiDocument.xml with visibility flags")
print(f"  Visible: {VISIBLE}")
print(f"  Hidden: {set(ALL_OBJECTS) - VISIBLE}")
print(f"\nNow close and re-open SonicareAdapter.FCStd in FreeCAD")
print(f"Then press 'V' then 'F' to fit the view to the object")

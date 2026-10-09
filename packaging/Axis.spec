# PyInstaller build definition for the portable Axis folder.
from pathlib import Path

project_root = Path(SPECPATH).parent
hiddenimports = [
    "fontTools.designspaceLib",
    "fontTools.subset",
    "fontTools.ttLib",
    "fontTools.varLib",
]

a = Analysis(
    [str(project_root / "app" / "main.py")],
    pathex=[str(project_root)],
    binaries=[],
    datas=[(str(project_root / "reference" / "LOGO.svg"), "reference")],
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="Axis",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    name="Axis",
)

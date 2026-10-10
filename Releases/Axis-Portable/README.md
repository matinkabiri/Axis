# Axis

Axis is a Windows-first desktop tool for turning compatible font masters into variable fonts.

The first prototype focuses on the visual workflow: adding font files or folders, reviewing source rows, resolving compatibility, and adding future axis columns. Weight is the only active axis in the first release.

## Run the prototype

```powershell
python -m pip install -r requirements.txt
python -m app.main
```

This prototype currently uses representative rows so the UI states can be reviewed before the font engine is connected.

## Build the portable Windows package

On Windows with internet access, run:

```powershell
.\packaging\build-portable.ps1
```

The result is `dist\Axis-Portable.zip`. Extract it and run `Axis.exe`; no Python installation is needed on the target machine.

## Repository layout

- `app/ui` - desktop interface
- `app/core` - font inspection and variable-font generation services
- `reference` - supplied Illustrator/PDF artwork
- `docs` - product and technical notes

# Axis

Axis is a Windows-first desktop application for turning compatible font masters into variable fonts. The first alpha focuses on the Weight axis and a clear, artist-oriented workflow.

## Alpha download

| Package | Platform | CPU | Type |
|---|---|---|---|
| `Axis-0.1.0-alpha.1-windows-x64-portable.zip` | Windows 10/11 | x64 / AMD64 | Portable folder, no installer |

Extract the complete ZIP, then run `Axis.exe`. Keep the `_internal` folder beside the executable; it contains the bundled Qt runtime.

This alpha is an early preview. The interface, font inspection, compatibility reporting, and packaging are present, while the complete production export workflow is still under development.

## Run from source

```powershell
python -m pip install -r requirements.txt
python -m app.main
```

## Build the portable Windows package

On Windows with internet access:

```powershell
.\packaging\build-portable.ps1
```

The build produces a self-contained `dist\Axis-Portable` folder and a ZIP archive. The current build targets Windows x64 / AMD64. Windows ARM64 is not supported by this alpha.

## Repository layout

- `app/ui` - desktop interface
- `app/core` - font inspection, compatibility, trimming, and variable-font services
- `reference` - supplied Illustrator and PDF artwork
- `docs` - product and release notes
- `packaging` - Windows portable build configuration
- `tests` - automated tests

## Font licensing

Do not commit commercial or licensed source fonts to this repository. Users should select their own font files locally through Axis.

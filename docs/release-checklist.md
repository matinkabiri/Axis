# Release checklist

## 0.1.0-alpha.1

- Platform: Windows 10/11
- Architecture: x64 / AMD64
- Distribution: portable ZIP; no installer
- Runtime: bundled PySide6 and Python runtime
- Source fonts: not included
- Status: early alpha; not production-ready

## Before publishing a release

- Build from a clean checkout.
- Start `Axis.exe` on a clean Windows x64 machine.
- Extract the ZIP to a path without administrator permissions.
- Add a licensed test font collection.
- Confirm the app opens without a console window.
- Confirm the release asset name includes version, platform, and architecture.
- Attach the SHA-256 checksum to the release notes.

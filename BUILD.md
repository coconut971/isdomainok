# Build Guide - okitsok

This document explains how to build standalone binaries for okitsok.

## Prerequisites

```bash
pip install pyinstaller
```

## Build for your platform

```bash
pyinstaller okitsok.spec
```

The binary will be generated in the `dist/` folder.

## Results by platform

- **Windows**: `dist/okitsok.exe` (~10-15 MB)
- **macOS**: `dist/okitsok` (~10-15 MB)
- **Linux**: `dist/okitsok` (~10-15 MB)

## Test the binary

```bash
# Windows
.\dist\okitsok.exe google

# macOS / Linux
./dist/okitsok google
```

## Multi-platform builds

PyInstaller generates native binaries for the platform it runs on.

To create binaries for multiple platforms:

1. **Windows**: Run the build on Windows
2. **macOS**: Run the build on macOS
3. **Linux**: Run the build on Linux

Or use CI/CD solutions like GitHub Actions.

## Notes

- The binary includes Python and all dependencies (dnspython)
- No Python installation required on target machine
- The binary can be distributed as-is
- Approximate size: 10-15 MB (compressed with UPX)

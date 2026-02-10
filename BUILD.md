# Build Instructions for DeltaForce-ESP

This document explains how to build the project into compiled formats.

## Prerequisites

Install build tools:
```bash
pip install cython
pip install pyinstaller
pip install wheel
```

## Option 1: Build Cython Extensions (.pyd DLLs)

Compile Python modules to native extensions (Windows DLLs):

```bash
python setup.py build_ext --inplace
```

This creates:
- `memory_reader_compiled.pyd` - Compiled memory reader module (DLL)
- `esp_compiled.pyd` - Compiled ESP calculator module (DLL)
- `overlay_compiled.pyd` - Compiled overlay renderer module (DLL)

These .pyd files are Windows DLLs that can be imported directly:
```python
import memory_reader_compiled
import esp_compiled
import overlay_compiled
```

## Option 2: Build Standalone Executable

Create a single executable with all dependencies bundled:

```bash
python build_executable.py
```

This creates:
- `dist/DeltaForce-ESP.exe` - Standalone executable
- All Python DLLs and dependencies are bundled inside

### Run the executable:
```bash
dist\DeltaForce-ESP.exe
```

## Option 3: Build Wheel Package

Create a distributable wheel package:

```bash
python setup.py bdist_wheel
```

This creates:
- `dist/DeltaForce_ESP-1.0.0-*.whl` - Installable wheel package

Install with:
```bash
pip install dist/DeltaForce_ESP-1.0.0-*.whl
```

## Build Directory Structure

After building, you'll have:

```
DeltaForce-ESP/
├── build/                    # Build artifacts (can be deleted)
├── dist/                     # Distribution files
│   ├── DeltaForce-ESP.exe   # Standalone executable
│   └── *.whl                # Wheel package (if built)
├── *.pyd                     # Compiled Python extensions (DLLs)
├── *.c                       # Generated C files (from Cython)
└── DeltaForce-ESP.spec      # PyInstaller spec file
```

## Clean Build Files

To clean up build artifacts:

```bash
# Windows
rmdir /s /q build dist
del *.pyd *.c *.spec

# Linux/Mac
rm -rf build dist *.pyd *.c *.spec
```

## Notes

1. **Cython Extensions (.pyd)**:
   - These are Windows DLLs that Python can import
   - Compiled to native machine code
   - Faster execution than interpreted Python
   - Platform-specific (must rebuild for each OS)

2. **PyInstaller Executable**:
   - Single file that includes Python interpreter
   - All dependencies bundled as DLLs inside
   - Can run on systems without Python installed
   - Larger file size (~50-100MB)

3. **Performance**:
   - Cython extensions: ~2-10x faster
   - PyInstaller: Same speed as Python, but easier distribution

## Troubleshooting

**Issue**: "Microsoft Visual C++ required"
- **Solution**: Install Visual Studio Build Tools

**Issue**: "Cannot find OpenGL DLLs"
- **Solution**: Ensure OpenGL drivers are installed on target system

**Issue**: "Failed to execute script"
- **Solution**: Run from command line to see error messages

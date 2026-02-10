"""
PyInstaller Build Script
Creates a standalone executable with all dependencies bundled

Usage:
    python build_executable.py

Output:
    - dist/DeltaForce-ESP.exe (standalone executable)
    - All dependencies bundled as DLLs in the dist folder
"""

import PyInstaller.__main__
import os
import sys

def build_executable():
    """Build standalone executable using PyInstaller"""
    
    print("=" * 70)
    print("Building DeltaForce-ESP Executable")
    print("=" * 70)
    print()
    
    # PyInstaller arguments
    args = [
        'main.py',                           # Entry point
        '--name=DeltaForce-ESP',             # Output name
        '--onefile',                         # Single executable file
        '--windowed',                        # No console window (for GUI apps)
        '--icon=NONE',                       # No icon (can add later)
        '--add-data=config.json;.',          # Include config file
        '--hidden-import=OpenGL',            # Ensure OpenGL is included
        '--hidden-import=OpenGL.GL',
        '--hidden-import=OpenGL.GLU',
        '--hidden-import=pygame',
        '--hidden-import=numpy',
        '--hidden-import=pymem',
        '--hidden-import=PIL',
        '--collect-all=OpenGL',              # Collect all OpenGL files
        '--collect-all=pygame',              # Collect all pygame files
        '--clean',                           # Clean cache
        '--noconfirm',                       # Overwrite without asking
    ]
    
    print("PyInstaller arguments:")
    for arg in args:
        print(f"  {arg}")
    print()
    
    # Run PyInstaller
    try:
        PyInstaller.__main__.run(args)
        print()
        print("=" * 70)
        print("Build completed successfully!")
        print("=" * 70)
        print()
        print("Output files:")
        print("  - dist/DeltaForce-ESP.exe    (Standalone executable)")
        print("  - build/                     (Build artifacts)")
        print("  - DeltaForce-ESP.spec        (Build specification)")
        print()
        print("All dependencies are bundled as DLLs inside the executable.")
        print()
        
    except Exception as e:
        print()
        print("=" * 70)
        print(f"Build failed: {e}")
        print("=" * 70)
        sys.exit(1)

if __name__ == "__main__":
    build_executable()

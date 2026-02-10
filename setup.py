# setup.py - Build script for creating compiled extensions and executables
"""
Build script for Delta Force ESP Overlay

This script provides multiple build options:
1. Build Python extensions (.pyd/.dll) using Cython
2. Create standalone executable using PyInstaller
3. Create distribution package

Usage:
    python setup.py build_ext --inplace    # Build Cython extensions
    python build_executable.py             # Create standalone .exe
"""

from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy as np

# Define extensions to compile
extensions = [
    Extension(
        "memory_reader_compiled",
        ["memory_reader.py"],
        include_dirs=[np.get_include()],
    ),
    Extension(
        "esp_compiled",
        ["esp.py"],
        include_dirs=[np.get_include()],
    ),
    Extension(
        "overlay_compiled",
        ["overlay.py"],
        include_dirs=[np.get_include()],
    ),
]

setup(
    name="DeltaForce-ESP",
    version="1.0.0",
    description="Educational ESP Overlay System for Delta Force 2025",
    author="Educational Project",
    ext_modules=cythonize(
        extensions,
        compiler_directives={
            'language_level': "3",
            'embedsignature': True,
        }
    ),
    install_requires=[
        'PyOpenGL==3.1.7',
        'PyOpenGL-accelerate==3.1.7',
        'pygame==2.5.2',
        'pymem==1.13.1',
        'numpy==1.26.3',
        'Pillow==10.3.0',
    ],
)

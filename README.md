# Delta Force 2025 ESP Overlay + DLL Injector - Educational Project

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Educational](https://img.shields.io/badge/purpose-educational-green.svg)]()

## ⚠️ EDUCATIONAL DISCLAIMER

**THIS PROJECT IS FOR EDUCATIONAL PURPOSES ONLY**

This software is designed as a school project to demonstrate and teach:
- **Graphics Programming**: OpenGL rendering, overlay techniques, transparency
- **Memory Management**: Process memory reading, pointer arithmetic
- **3D Mathematics**: World-to-screen projection, coordinate transformations
- **Software Architecture**: Clean code structure, design patterns, modularity
- **Process Injection**: DLL injection techniques, Windows API programming

**DO NOT:**
- Use this in online multiplayer games
- Violate any game's terms of service
- Use for competitive advantage
- Distribute for malicious purposes

**Legal Notice**: Using such tools in online games may result in account bans and legal consequences. This is intended solely for learning in controlled, offline environments.

---

## 📋 Project Overview

A comprehensive educational toolkit for Delta Force 2025, featuring:

1. **ESP (Extra Sensory Perception) Overlay System**: Transparent overlay with real-time graphics
2. **DLL Injector**: Process injection tool demonstrating Windows API techniques

Both components showcase advanced programming concepts including graphics rendering, memory manipulation, and system-level programming.

## 🎯 Learning Objectives

### Graphics Programming
- Understanding the OpenGL rendering pipeline
- Implementing transparent overlay windows
- Working with 2D/3D transformations
- Alpha blending and transparency effects

### Memory Management
- Process enumeration and attachment
- Reading process memory safely
- Understanding pointer chains and offsets
- Handling memory read errors gracefully

### Process Injection (NEW)
- Windows API programming
- DLL injection techniques
- Process privilege management
- Security implications and detection

### Mathematics
- 3D vector mathematics
- Matrix transformations (view matrices)
- Perspective projection
- Distance calculations in 3D space

### Software Engineering
- Clean code architecture
- Separation of concerns
- Configuration management
- Error handling and logging

## 🏗️ Project Structure

```
DeltaForce-ESP/
├── main.py              # ESP overlay entry point
├── memory_reader.py     # Memory reading and process handling
├── overlay.py           # OpenGL overlay window and rendering
├── esp.py              # ESP logic and coordinate transformations
├── injector.py         # DLL injection module (NEW)
├── injector_gui.py     # DLL injector GUI (NEW)
├── config.json         # Configuration file
├── requirements.txt    # Python dependencies
├── setup.py            # Build configuration
├── build_executable.py # Executable builder
├── .gitignore         # Git ignore rules
├── README.md          # This file
├── BUILD.md           # Build instructions
└── INJECTOR.md        # DLL injector documentation (NEW)
```

## 🚀 Getting Started

### Prerequisites

- **Python 3.8 or higher**
- **Windows OS** (for memory reading functionality)
- **OpenGL support** (most modern systems have this)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/TheRUN/DeltaForce-ESP.git
   cd DeltaForce-ESP
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   # or
   source venv/bin/activate  # On Linux/Mac
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

```bash
python main.py
```

**Note**: The application runs in demonstration mode, showing example ESP rendering without actually attaching to a game process.

### Building Compiled Versions

You can compile the Python code into DLLs or create a standalone executable:

#### Option 1: Build as DLL Extensions (.pyd files)
```bash
# Install build tools
pip install cython wheel

# Build Cython extensions (Windows DLLs)
python setup.py build_ext --inplace
```

This creates compiled `.pyd` files (Windows DLLs):
- `memory_reader_compiled.pyd`
- `esp_compiled.pyd`
- `overlay_compiled.pyd`

#### Option 2: Build Standalone Executable
```bash
# Install PyInstaller
pip install pyinstaller

# Build executable with bundled DLLs
python build_executable.py
```

This creates `dist/DeltaForce-ESP.exe` - a standalone executable with all dependencies bundled as DLLs inside.

**See [BUILD.md](BUILD.md) for detailed build instructions.**

## 🎮 Features

### ESP Overlay System

#### Core Features

1. **Memory Reading Module** (`memory_reader.py`)
   - Process enumeration and discovery
   - Safe memory reading with error handling
   - Player entity data parsing
   - View matrix extraction

2. **OpenGL Overlay** (`overlay.py`)
   - Transparent window overlay
   - 2D and 3D rendering primitives
   - Text rendering
   - Health bar visualization
   - Optimized rendering pipeline

3. **ESP Calculator** (`esp.py`)
   - World-to-screen coordinate conversion
   - 2D/3D bounding box calculations
   - Distance calculations
   - Color interpolation
   - Angle calculations

4. **Main Application** (`main.py`)
   - Configuration management
   - Main render loop
   - Input handling (hotkeys)
   - FPS management
   - Status UI

#### Hotkeys

- **F1** - Toggle ESP on/off
- **F2** - Toggle bounding boxes
- **F3** - Toggle distance indicators
- **F10** - Exit application
- **ESC** - Exit application

#### Visual Elements

- **Bounding Boxes**: 2D boxes around player positions
- **Distance Indicators**: Show distance in meters
- **Health Bars**: Visual health status (optional)
- **Color Coding**: Different colors for teammates vs enemies
- **Status UI**: FPS counter and feature toggles

### DLL Injector (NEW)

A comprehensive DLL injection tool for educational purposes.

#### Features

1. **DLL Injection Module** (`injector.py`)
   - LoadLibrary injection method
   - Process privilege elevation (SeDebugPrivilege)
   - DLL validation
   - Comprehensive error handling
   - Educational comments explaining each step

2. **Injector GUI** (`injector_gui.py`)
   - User-friendly graphical interface
   - Process selection from running processes
   - DLL file browser
   - Injection method selector
   - Real-time log output
   - Built with tkinter

#### Injection Methods

- **LoadLibrary**: Classic injection using CreateRemoteThread
- **Manual Mapping**: Advanced technique (placeholder for future implementation)

#### How to Use

**Run GUI:**
```bash
python injector_gui.py
```

**Steps:**
1. Select target process from the list
2. Browse and select your DLL file
3. Choose injection method
4. Click "Inject DLL"

**Programmatic Usage:**
```python
from injector import DLLInjector, InjectionMethod

injector = DLLInjector()
success, msg = injector.inject_dll(
    process_id=1234,
    dll_path="C:/path/to/your.dll",
    method=InjectionMethod.LOAD_LIBRARY
)
```

**See [INJECTOR.md](INJECTOR.md) for complete documentation.**

## ⚙️ Configuration

Edit `config.json` to customize the overlay:

```json
{
  "window": {
    "width": 1920,
    "height": 1080,
    "fps": 60
  },
  "esp": {
    "enabled": true,
    "box_enabled": true,
    "distance_enabled": true,
    "max_distance": 500.0
  },
  "colors": {
    "enemy": [255, 0, 0, 200],
    "teammate": [0, 255, 0, 200],
    "box_thickness": 2.0
  }
}
```

## 📚 Educational Resources

### Graphics Programming
- [LearnOpenGL](https://learnopengl.com/) - Comprehensive OpenGL tutorials
- [OpenGL Tutorial](http://www.opengl-tutorial.org/) - Step-by-step OpenGL guide
- [PyOpenGL Documentation](http://pyopengl.sourceforge.net/documentation/index.html)

### Memory Reading
- [Windows API Documentation](https://docs.microsoft.com/en-us/windows/win32/api/)
- [Understanding Memory Management](https://docs.microsoft.com/en-us/windows/win32/memory/about-memory-management)
- [Process and Thread Functions](https://docs.microsoft.com/en-us/windows/win32/procthread/)

### Mathematics
- [3D Math Primer for Graphics](https://gamemath.com/)
- [Mathematics for 3D Game Programming](https://www.3dgep.com/3d-math-primer/)
- [Essential Mathematics for Games](https://www.essentialmath.com/)

### Game Development
- [Game Programming Patterns](https://gameprogrammingpatterns.com/)
- [Game Engine Architecture](https://www.gameenginebook.com/)

## 🔧 Technical Details

### World-to-Screen Projection

The core of ESP rendering is converting 3D world coordinates to 2D screen coordinates:

```python
# Transformation pipeline:
World Space → View Space → Clip Space → NDC → Screen Space
```

1. **World Space**: 3D coordinates in the game world
2. **View Space**: Coordinates relative to the camera
3. **Clip Space**: After applying projection matrix
4. **NDC** (Normalized Device Coordinates): Range [-1, 1]
5. **Screen Space**: Final pixel coordinates

### Memory Reading Concepts

```
Game Process Memory Layout:
┌─────────────────────┐
│  Module Base        │ ← Base address of game executable
├─────────────────────┤
│  Static Addresses   │ ← Game variables
├─────────────────────┤
│  Player List        │ ← Array/linked list of players
│    ├─ Player 1      │
│    ├─ Player 2      │
│    └─ ...           │
├─────────────────────┤
│  View Matrix        │ ← Camera transformation matrix
└─────────────────────┘
```

### Rendering Pipeline

```
1. Clear screen (transparent background)
2. Read game data from memory
3. For each player:
   a. Calculate world-to-screen position
   b. Calculate bounding box
   c. Render box if on screen
   d. Render distance text
   e. Render health bar
4. Render UI elements (FPS, status)
5. Swap buffers (display frame)
```

## 🛠️ Development

### Code Style
- Follow PEP 8 style guidelines
- Use type hints for function parameters
- Write descriptive docstrings
- Add educational comments explaining concepts

### Testing
Currently, this is a demonstration project. For production use, you would add:
- Unit tests for mathematical functions
- Integration tests for memory reading
- Performance benchmarks
- Mock game process for testing

### Contributing
This is an educational project. Feel free to:
- Fork and experiment
- Add new features for learning
- Improve documentation
- Share your learning experience

## 📝 Code Examples

### Basic World-to-Screen Conversion

```python
from esp import ESPCalculator

# Initialize calculator
esp = ESPCalculator(screen_width=1920, screen_height=1080)

# World position of a player
player_pos = (100.0, 200.0, 50.0)  # (x, y, z)

# View matrix from game (4x4 matrix, 16 elements)
view_matrix = [...] # Read from game memory

# Convert to screen coordinates
screen_pos = esp.world_to_screen(player_pos, view_matrix)

if screen_pos:
    x, y = screen_pos
    print(f"Player is at screen position: ({x}, {y})")
```

### Drawing ESP Elements

```python
from overlay import Overlay

# Create overlay window
overlay = Overlay(width=1920, height=1080)

# Draw a bounding box
overlay.draw_box(
    x=100, y=100,
    width=50, height=100,
    color=(255, 0, 0, 200),  # Red with alpha
    thickness=2.0
)

# Draw distance text
overlay.draw_text("25m", x=120, y=80, color=(255, 255, 255, 255))

# Update display
overlay.update()
```

## 🐛 Troubleshooting

### Common Issues

**Issue**: "Failed to initialize overlay window"
- **Solution**: Ensure your system supports OpenGL. Update graphics drivers.

**Issue**: "Process not found"
- **Solution**: The demo mode doesn't require the actual game. Check `memory_reader.py` for mock data.

**Issue**: Low FPS
- **Solution**: Reduce overlay resolution in `config.json` or decrease rendering complexity.

**Issue**: Import errors
- **Solution**: Ensure all dependencies are installed: `pip install -r requirements.txt`

## 📄 License

MIT License - See LICENSE file for details.

This project is for educational purposes only. Using memory reading tools in online games may violate terms of service and result in bans.

## 🙏 Acknowledgments

- **PyOpenGL** - Python OpenGL bindings
- **Pygame** - Window management and event handling
- **NumPy** - Mathematical operations
- **OpenGL Community** - Tutorials and documentation

## 📧 Contact

For educational questions or collaboration:
- GitHub: [TheRUN/DeltaForce-ESP](https://github.com/TheRUN/DeltaForce-ESP)
- Issues: [Report issues](https://github.com/TheRUN/DeltaForce-ESP/issues)

---

**Remember**: Use this knowledge responsibly and ethically. The goal is education, not exploitation.

Happy Learning! 🎓
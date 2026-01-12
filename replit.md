# Photo Monitor and Print Application

## Overview
A Windows desktop application that automatically monitors a folder for new photos, applies a template overlay, and sends them to a printer. Includes both command-line and GUI versions, plus build scripts for creating a Windows installer.

## Project Architecture

### Directory Structure
```
├── main.py                 # Command-line application & service class
├── gui_app.py              # Graphical user interface version
├── config.ini              # Configuration file
├── create_sample_template.py  # Script to generate sample template
├── build_exe.py            # PyInstaller build script
├── installer.iss           # Inno Setup installer script
├── README_WINDOWS.txt      # Windows installation guide
├── src/
│   ├── __init__.py
│   ├── folder_watcher.py   # File system monitoring
│   ├── image_processor.py  # Template overlay processing
│   └── printer.py          # Windows printer integration
├── templates/              # Template images folder
├── watch_folder/           # Monitored folder for new photos
└── processed/              # Output folder for processed images
```

### Key Components
1. **PhotoMonitorService**: Core service with start/stop capability and status callbacks
2. **PhotoMonitorGUI**: Tkinter-based graphical interface
3. **FolderWatcher**: Uses watchdog library to monitor folder for new image files
4. **ImageProcessor**: Uses Pillow to apply PNG template overlay to photos
5. **Printer**: Windows printing via pywin32, falls back to simulation on other platforms

### Configuration (config.ini)
- `watch_folder`: Folder to monitor for new photos
- `template_path`: Path to PNG template overlay (should have transparency)
- `output_folder`: Where processed images are saved
- `print_enabled`: Enable/disable automatic printing
- `printer_name`: Target printer name or "default"
- `copies`: Number of copies to print
- `position`: Template overlay position (center, top-left, etc.)
- `opacity`: Template opacity (0-100)

## How to Run

### GUI Version
```
python gui_app.py
```

### Command-Line Version
```
python main.py
```

### Building Windows Installer
1. Install PyInstaller: `pip install pyinstaller`
2. Run: `python build_exe.py`
3. Install Inno Setup and compile `installer.iss`

## Recent Changes
- Initial project creation (January 2026)
- Added GUI interface with Tkinter
- Added PyInstaller and Inno Setup build scripts
- Refactored to service-based architecture for GUI support

## User Preferences
- Windows target platform
- Support for common image formats
- Automatic printing workflow
- Simple GUI for non-technical users

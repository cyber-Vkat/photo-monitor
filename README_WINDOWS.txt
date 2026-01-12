===============================================
  PHOTO MONITOR - Windows Installation Guide
===============================================

This application monitors a folder for new photos, applies a
template overlay, and automatically prints them.


QUICK INSTALLATION (Using Installer)
====================================

1. Download and install Python 3.11+ from python.org
   - Check "Add Python to PATH" during installation

2. Open Command Prompt and run:
   pip install Pillow watchdog pywin32 pyinstaller

3. In the project folder, run:
   python build_exe.py

4. Install Inno Setup from https://jrsoftware.org/isinfo.php

5. Open installer.iss with Inno Setup and click Build

6. Run the installer from installer_output/PhotoMonitor_Setup.exe


MANUAL INSTALLATION (Without Installer)
=======================================

1. Install Python 3.11+ from python.org
   - Check "Add Python to PATH" during installation

2. Extract all project files to a folder (e.g., C:\PhotoMonitor)

3. Open Command Prompt and navigate to the folder:
   cd C:\PhotoMonitor

4. Install required libraries:
   pip install Pillow watchdog pywin32

5. Run the GUI application:
   python gui_app.py

   Or run the command-line version:
   python main.py


USING THE APPLICATION
=====================

GUI Version (gui_app.py):
- Set the Watch Folder (where you'll drop photos)
- Set the Template (your overlay image - PNG with transparency)
- Set the Output Folder (where processed images are saved)
- Select your printer
- Click "Start Monitoring"
- Drop photos into the Watch Folder - they'll be processed and printed!

Command-Line Version (main.py):
- Edit config.ini to configure settings
- Run: python main.py
- Drop photos into watch_folder/


CONFIGURATION OPTIONS
====================

Edit config.ini to customize:

[Settings]
watch_folder = watch_folder          # Folder to monitor
template_path = templates/overlay_template.png  # Template image
output_folder = processed            # Where to save processed images
print_enabled = true                 # Enable/disable printing
supported_formats = .jpg,.jpeg,.png,.bmp,.gif,.tiff

[Printing]
printer_name = default               # Printer name or "default"
copies = 1                           # Number of copies

[Template]
position = center                    # center, top-left, top-right, etc.
opacity = 100                        # 0-100


TEMPLATE TIPS
=============

- Use PNG format with transparency for overlays
- The template will be resized to match each photo
- Design your template at high resolution (e.g., 1920x1080)
- Transparent areas will show the original photo


TROUBLESHOOTING
===============

"pywin32 not found"
- Run: pip install pywin32

"No printers found"
- Make sure you have a printer installed in Windows
- Try refreshing the printer list in the GUI

Photos not detected:
- Check that the file format is supported
- Wait a moment - there's a short delay to ensure files are fully copied

Prints not working:
- Check printer connection and status
- Try setting a specific printer name instead of "default"


SUPPORT
=======

For issues, check that:
1. Python 3.11+ is installed
2. All dependencies are installed
3. The watch folder exists and is accessible
4. Your template file exists and is a valid image

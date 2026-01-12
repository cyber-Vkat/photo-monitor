"""
Build script to create Windows executable using PyInstaller.

Instructions:
1. Install PyInstaller: pip install pyinstaller
2. Run this script: python build_exe.py
3. The executable will be in the 'dist' folder
"""

import subprocess
import sys
import os


def build():
    print("Building Photo Monitor executable...")
    print("=" * 50)
    
    pyinstaller_args = [
        'pyinstaller',
        '--name=PhotoMonitor',
        '--onefile',
        '--windowed',
        '--add-data=config.ini;.',
        '--add-data=templates;templates',
        '--hidden-import=PIL',
        '--hidden-import=PIL.Image',
        '--hidden-import=PIL.ImageDraw',
        '--hidden-import=PIL.ImageFont',
        '--hidden-import=PIL.ImageWin',
        '--hidden-import=watchdog',
        '--hidden-import=watchdog.observers',
        '--hidden-import=watchdog.events',
        '--hidden-import=win32print',
        '--hidden-import=win32ui',
        '--hidden-import=win32con',
        '--hidden-import=configparser',
        'gui_app.py'
    ]
    
    if os.path.exists('icon.ico'):
        pyinstaller_args.insert(-1, '--icon=icon.ico')
    
    try:
        subprocess.run(pyinstaller_args, check=True)
        print("\n" + "=" * 50)
        print("Build successful!")
        print("Executable location: dist/PhotoMonitor.exe")
        print("=" * 50)
        print("\nTo create installer:")
        print("1. Install Inno Setup from https://jrsoftware.org/isinfo.php")
        print("2. Open installer.iss with Inno Setup")
        print("3. Click Build > Compile")
    except subprocess.CalledProcessError as e:
        print(f"Build failed: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print("PyInstaller not found. Install it with: pip install pyinstaller")
        sys.exit(1)


if __name__ == '__main__':
    build()

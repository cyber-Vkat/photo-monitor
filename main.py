import os
import sys
import time
import configparser
from datetime import datetime

from src.folder_watcher import FolderWatcher
from src.image_processor import ImageProcessor
from src.printer import Printer


class PhotoMonitorService:
    def __init__(self, config_path='config.ini', status_callback=None):
        self.config_path = config_path
        self.status_callback = status_callback
        self.config = None
        self.watcher = None
        self.processor = None
        self.printer = None
        self.print_enabled = True
        self.output_folder = 'processed'
        self.is_running = False
        
        self.load_config()

    def log(self, message):
        if self.status_callback:
            self.status_callback(message)
        else:
            print(message)

    def load_config(self):
        config = configparser.ConfigParser()
        
        if os.path.exists(self.config_path):
            config.read(self.config_path)
            self.log(f"Configuration loaded from: {self.config_path}")
        else:
            config['Settings'] = {
                'watch_folder': 'watch_folder',
                'template_path': 'templates/overlay_template.png',
                'output_folder': 'processed',
                'print_enabled': 'true',
                'supported_formats': '.jpg,.jpeg,.png,.bmp,.gif,.tiff'
            }
            config['Printing'] = {
                'printer_name': 'default',
                'copies': '1'
            }
            config['Template'] = {
                'position': 'center',
                'opacity': '100'
            }
            self.save_config(config)
        
        self.config = config
        return config

    def save_config(self, config=None):
        if config is None:
            config = self.config
        with open(self.config_path, 'w') as f:
            config.write(f)
        self.log(f"Configuration saved to: {self.config_path}")

    def update_setting(self, section, key, value):
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, key, str(value))
        self.save_config()

    def get_setting(self, section, key, fallback=''):
        return self.config.get(section, key, fallback=fallback)

    def setup_directories(self):
        watch_folder = self.config.get('Settings', 'watch_folder')
        output_folder = self.config.get('Settings', 'output_folder')
        template_folder = os.path.dirname(self.config.get('Settings', 'template_path'))
        
        for folder in [watch_folder, output_folder, template_folder]:
            if folder and not os.path.exists(folder):
                os.makedirs(folder)
                self.log(f"Created directory: {folder}")

    def initialize_components(self):
        template_path = self.config.get('Settings', 'template_path')
        position = self.config.get('Template', 'position')
        opacity = self.config.getint('Template', 'opacity')
        
        self.processor = ImageProcessor(template_path, position, opacity)
        
        printer_name = self.config.get('Printing', 'printer_name')
        copies = self.config.getint('Printing', 'copies')
        self.printer = Printer(printer_name, copies)
        
        self.print_enabled = self.config.getboolean('Settings', 'print_enabled')
        self.output_folder = self.config.get('Settings', 'output_folder')
        
        supported_formats = self.config.get('Settings', 'supported_formats').split(',')
        watch_folder = self.config.get('Settings', 'watch_folder')
        
        self.watcher = FolderWatcher(
            watch_folder,
            supported_formats,
            self._on_new_photo
        )

    def _on_new_photo(self, photo_path):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = os.path.basename(photo_path)
        name, ext = os.path.splitext(filename)
        output_filename = f"{name}_{timestamp}{ext}"
        output_path = os.path.join(self.output_folder, output_filename)
        
        self.log(f"Processing: {filename}")
        processed_path = self.processor.apply_overlay(photo_path, output_path)
        
        if not processed_path:
            self.log(f"Failed to process: {filename}")
            return False
        
        self.log(f"Saved to: {output_path}")
        
        if self.print_enabled:
            self.log(f"Sending to printer...")
            self.printer.print_image(processed_path)
            self.log(f"Print job sent for: {filename}")
        
        return True

    def start(self):
        if self.is_running:
            self.log("Already running")
            return
        
        self.setup_directories()
        self.initialize_components()
        
        self.log("=" * 50)
        self.log("Photo Monitor Started")
        self.log("=" * 50)
        self.log(f"Watch folder: {self.config.get('Settings', 'watch_folder')}")
        self.log(f"Template: {self.config.get('Settings', 'template_path')}")
        self.log(f"Printing: {'Enabled' if self.print_enabled else 'Disabled'}")
        self.log("Waiting for new photos...")
        
        self.watcher.start()
        self.is_running = True

    def stop(self):
        if not self.is_running:
            return
        
        if self.watcher:
            self.watcher.stop()
        
        self.is_running = False
        self.log("Photo Monitor Stopped")

    def get_available_printers(self):
        temp_printer = Printer()
        return temp_printer.get_available_printers()


class PhotoMonitorApp:
    def __init__(self, config_path='config.ini'):
        self.service = PhotoMonitorService(config_path)

    def run(self):
        print("=" * 60)
        print("  Photo Monitor and Print Application")
        print("=" * 60)
        print(f"Watch folder: {self.service.get_setting('Settings', 'watch_folder')}")
        print(f"Template: {self.service.get_setting('Settings', 'template_path')}")
        print(f"Output folder: {self.service.get_setting('Settings', 'output_folder')}")
        print("=" * 60)
        print("Waiting for new photos... (Press Ctrl+C to stop)")
        print()
        
        self.service.start()
        
        try:
            while self.service.is_running:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nShutting down...")
            self.service.stop()
            print("Application stopped.")


def main():
    if len(sys.argv) > 1:
        config_path = sys.argv[1]
    else:
        config_path = 'config.ini'
    
    app = PhotoMonitorApp(config_path)
    app.run()


if __name__ == '__main__':
    main()

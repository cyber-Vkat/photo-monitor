import os
import sys
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime

from main import PhotoMonitorService


class PhotoMonitorGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Photo Monitor & Print")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        self.log_text = None
        self.monitor_thread = None
        
        self._create_widgets()
        
        self.service = PhotoMonitorService(status_callback=self.log_message)
        self._load_settings()
        self._refresh_printers()
        
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    def _create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        settings_frame = ttk.LabelFrame(main_frame, text="Settings", padding="10")
        settings_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(settings_frame, text="Watch Folder:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.watch_folder_var = tk.StringVar()
        watch_entry = ttk.Entry(settings_frame, textvariable=self.watch_folder_var, width=40)
        watch_entry.grid(row=0, column=1, padx=5, pady=2)
        ttk.Button(settings_frame, text="Browse", command=self._browse_watch_folder).grid(row=0, column=2, pady=2)
        
        ttk.Label(settings_frame, text="Template:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.template_var = tk.StringVar()
        template_entry = ttk.Entry(settings_frame, textvariable=self.template_var, width=40)
        template_entry.grid(row=1, column=1, padx=5, pady=2)
        ttk.Button(settings_frame, text="Browse", command=self._browse_template).grid(row=1, column=2, pady=2)
        
        ttk.Label(settings_frame, text="Output Folder:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.output_folder_var = tk.StringVar()
        output_entry = ttk.Entry(settings_frame, textvariable=self.output_folder_var, width=40)
        output_entry.grid(row=2, column=1, padx=5, pady=2)
        ttk.Button(settings_frame, text="Browse", command=self._browse_output_folder).grid(row=2, column=2, pady=2)
        
        ttk.Label(settings_frame, text="Printer:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.printer_var = tk.StringVar()
        self.printer_combo = ttk.Combobox(settings_frame, textvariable=self.printer_var, width=37)
        self.printer_combo.grid(row=3, column=1, padx=5, pady=2)
        ttk.Button(settings_frame, text="Refresh", command=self._refresh_printers).grid(row=3, column=2, pady=2)
        
        options_frame = ttk.Frame(settings_frame)
        options_frame.grid(row=4, column=0, columnspan=3, pady=10)
        
        self.print_enabled_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Enable Printing", variable=self.print_enabled_var).pack(side=tk.LEFT, padx=10)
        
        ttk.Label(options_frame, text="Copies:").pack(side=tk.LEFT, padx=(20, 5))
        self.copies_var = tk.StringVar(value="1")
        copies_spin = ttk.Spinbox(options_frame, from_=1, to=10, width=5, textvariable=self.copies_var)
        copies_spin.pack(side=tk.LEFT)
        
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=10)
        
        self.start_btn = ttk.Button(control_frame, text="Start Monitoring", command=self._start_monitoring)
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_btn = ttk.Button(control_frame, text="Stop Monitoring", command=self._stop_monitoring, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(control_frame, text="Save Settings", command=self._save_settings).pack(side=tk.LEFT, padx=5)
        
        self.status_var = tk.StringVar(value="Stopped")
        self.status_label = ttk.Label(control_frame, textvariable=self.status_var, foreground="red")
        self.status_label.pack(side=tk.RIGHT, padx=10)
        ttk.Label(control_frame, text="Status:").pack(side=tk.RIGHT)
        
        log_frame = ttk.LabelFrame(main_frame, text="Activity Log", padding="5")
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        self.log_text = tk.Text(log_frame, height=12, state=tk.DISABLED, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def _load_settings(self):
        self.watch_folder_var.set(self.service.get_setting('Settings', 'watch_folder', 'watch_folder'))
        self.template_var.set(self.service.get_setting('Settings', 'template_path', 'templates/overlay_template.png'))
        self.output_folder_var.set(self.service.get_setting('Settings', 'output_folder', 'processed'))
        self.printer_var.set(self.service.get_setting('Printing', 'printer_name', 'default'))
        self.copies_var.set(self.service.get_setting('Printing', 'copies', '1'))
        self.print_enabled_var.set(self.service.get_setting('Settings', 'print_enabled', 'true').lower() == 'true')

    def _save_settings(self):
        self.service.update_setting('Settings', 'watch_folder', self.watch_folder_var.get())
        self.service.update_setting('Settings', 'template_path', self.template_var.get())
        self.service.update_setting('Settings', 'output_folder', self.output_folder_var.get())
        self.service.update_setting('Settings', 'print_enabled', str(self.print_enabled_var.get()).lower())
        self.service.update_setting('Printing', 'printer_name', self.printer_var.get())
        self.service.update_setting('Printing', 'copies', self.copies_var.get())
        self.log_message("Settings saved")

    def _browse_watch_folder(self):
        folder = filedialog.askdirectory(title="Select Watch Folder")
        if folder:
            self.watch_folder_var.set(folder)

    def _browse_template(self):
        file = filedialog.askopenfilename(
            title="Select Template Image",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
        )
        if file:
            self.template_var.set(file)

    def _browse_output_folder(self):
        folder = filedialog.askdirectory(title="Select Output Folder")
        if folder:
            self.output_folder_var.set(folder)

    def _refresh_printers(self):
        printers = self.service.get_available_printers()
        printers = ['default'] + printers
        self.printer_combo['values'] = printers
        if not self.printer_var.get():
            self.printer_var.set('default')

    def _start_monitoring(self):
        self._save_settings()
        self.service.load_config()
        
        self.monitor_thread = threading.Thread(target=self.service.start, daemon=True)
        self.monitor_thread.start()
        
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.status_var.set("Running")
        self.status_label.config(foreground="green")

    def _stop_monitoring(self):
        self.service.stop()
        
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.status_var.set("Stopped")
        self.status_label.config(foreground="red")

    def log_message(self, message):
        if self.log_text is None:
            print(message)
            return
        
        timestamp = datetime.now().strftime('%H:%M:%S')
        full_message = f"[{timestamp}] {message}\n"
        
        def update_log():
            self.log_text.config(state=tk.NORMAL)
            self.log_text.insert(tk.END, full_message)
            self.log_text.see(tk.END)
            self.log_text.config(state=tk.DISABLED)
        
        if threading.current_thread() is threading.main_thread():
            update_log()
        else:
            self.root.after(0, update_log)

    def _on_close(self):
        if self.service.is_running:
            if messagebox.askyesno("Confirm Exit", "Monitoring is still running. Stop and exit?"):
                self.service.stop()
                self.root.destroy()
        else:
            self.root.destroy()

    def run(self):
        self.log_message("Application started")
        self.log_message("Configure settings and click 'Start Monitoring'")
        self.root.mainloop()


def main():
    app = PhotoMonitorGUI()
    app.run()


if __name__ == '__main__':
    main()

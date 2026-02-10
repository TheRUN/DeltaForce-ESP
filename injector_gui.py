"""
DLL Injector GUI - Educational Tool
User-friendly interface for DLL injection demonstration

EDUCATIONAL DISCLAIMER:
This is an educational tool for learning about process injection.
Do NOT use for malicious purposes or to violate terms of service.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import logging
from typing import Optional
import psutil
import os
import sys
from datetime import datetime

# Import our injector module
from injector import DLLInjector, InjectionMethod


class InjectorGUI:
    """GUI application for DLL injection"""
    
    def __init__(self, root):
        """Initialize the GUI"""
        self.root = root
        self.root.title("DLL Injector - Educational Tool")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Set up logging to GUI
        self.setup_logging()
        
        # Initialize injector
        self.injector = DLLInjector()
        
        # Selected process and DLL
        self.selected_process_id: Optional[int] = None
        self.selected_dll_path: Optional[str] = None
        
        # Create GUI
        self.create_widgets()
        
        # Load processes
        self.refresh_processes()
        
        self.logger.info("DLL Injector GUI initialized")
    
    def setup_logging(self):
        """Set up logging configuration"""
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
    
    def create_widgets(self):
        """Create all GUI widgets"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        main_frame.rowconfigure(4, weight=1)
        
        # Disclaimer label
        disclaimer_frame = ttk.LabelFrame(main_frame, text="⚠️ Educational Disclaimer", padding="5")
        disclaimer_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        disclaimer_text = tk.Text(disclaimer_frame, height=3, wrap=tk.WORD, 
                                 bg='#fff3cd', fg='#856404', font=('Arial', 9))
        disclaimer_text.insert('1.0', 
            "This tool is for EDUCATIONAL PURPOSES ONLY. It demonstrates process injection "
            "techniques used in debugging and security research. Do NOT use for malicious "
            "purposes or to violate any terms of service.")
        disclaimer_text.config(state='disabled')
        disclaimer_text.pack(fill=tk.BOTH, expand=True)
        
        # Process selection frame
        process_frame = ttk.LabelFrame(main_frame, text="1. Select Target Process", padding="10")
        process_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        process_frame.columnconfigure(0, weight=1)
        
        # Process list
        process_list_frame = ttk.Frame(process_frame)
        process_list_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        process_list_frame.columnconfigure(0, weight=1)
        process_list_frame.rowconfigure(0, weight=1)
        
        # Scrollbar for process list
        scrollbar = ttk.Scrollbar(process_list_frame)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        self.process_listbox = tk.Listbox(process_list_frame, height=8,
                                          yscrollcommand=scrollbar.set)
        self.process_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.config(command=self.process_listbox.yview)
        
        self.process_listbox.bind('<<ListboxSelect>>', self.on_process_select)
        
        # Refresh button
        refresh_btn = ttk.Button(process_frame, text="🔄 Refresh Processes", 
                                command=self.refresh_processes)
        refresh_btn.grid(row=1, column=0, pady=(5, 0))
        
        # DLL selection frame
        dll_frame = ttk.LabelFrame(main_frame, text="2. Select DLL File", padding="10")
        dll_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        dll_frame.columnconfigure(0, weight=1)
        
        dll_path_frame = ttk.Frame(dll_frame)
        dll_path_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))
        dll_path_frame.columnconfigure(0, weight=1)
        
        self.dll_path_var = tk.StringVar(value="No DLL selected")
        dll_path_label = ttk.Label(dll_path_frame, textvariable=self.dll_path_var,
                                   foreground='gray')
        dll_path_label.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        
        browse_btn = ttk.Button(dll_path_frame, text="Browse...", 
                               command=self.browse_dll)
        browse_btn.grid(row=0, column=1)
        
        # Injection options frame
        options_frame = ttk.LabelFrame(main_frame, text="3. Injection Options", padding="10")
        options_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Method selection
        ttk.Label(options_frame, text="Injection Method:").grid(row=0, column=0, sticky=tk.W)
        self.method_var = tk.StringVar(value=InjectionMethod.LOAD_LIBRARY.value)
        method_combo = ttk.Combobox(options_frame, textvariable=self.method_var,
                                    values=[m.value for m in InjectionMethod],
                                    state='readonly', width=20)
        method_combo.grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        
        # Inject button
        inject_btn_frame = ttk.Frame(main_frame)
        inject_btn_frame.grid(row=4, column=0, pady=(0, 10))
        
        self.inject_btn = ttk.Button(inject_btn_frame, text="💉 Inject DLL", 
                                     command=self.inject_dll, style='Accent.TButton')
        self.inject_btn.pack()
        
        # Log output frame
        log_frame = ttk.LabelFrame(main_frame, text="Log Output", padding="10")
        log_frame.grid(row=5, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=10, 
                                                  wrap=tk.WORD, state='disabled')
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Add log handler
        text_handler = TextHandler(self.log_text)
        text_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s',
                                                    datefmt='%H:%M:%S'))
        logging.getLogger().addHandler(text_handler)
    
    def refresh_processes(self):
        """Refresh the process list"""
        self.process_listbox.delete(0, tk.END)
        self.log("Refreshing process list...")
        
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    pid = proc.info['pid']
                    name = proc.info['name']
                    processes.append((pid, name))
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            # Sort by name
            processes.sort(key=lambda x: x[1].lower())
            
            # Add to listbox
            for pid, name in processes:
                self.process_listbox.insert(tk.END, f"{name} (PID: {pid})")
            
            self.log(f"Found {len(processes)} processes")
            
        except Exception as e:
            self.log(f"Error refreshing processes: {e}", level='error')
    
    def on_process_select(self, event):
        """Handle process selection"""
        selection = self.process_listbox.curselection()
        if selection:
            text = self.process_listbox.get(selection[0])
            # Extract PID from text (format: "name (PID: 1234)")
            try:
                pid_str = text.split("PID: ")[1].rstrip(")")
                self.selected_process_id = int(pid_str)
                self.log(f"Selected process PID: {self.selected_process_id}")
            except Exception as e:
                self.log(f"Error parsing PID: {e}", level='error')
    
    def browse_dll(self):
        """Browse for DLL file"""
        filename = filedialog.askopenfilename(
            title="Select DLL file",
            filetypes=[("DLL files", "*.dll"), ("All files", "*.*")]
        )
        
        if filename:
            self.selected_dll_path = filename
            self.dll_path_var.set(os.path.basename(filename))
            self.log(f"Selected DLL: {filename}")
            
            # Validate DLL
            valid, message = self.injector.validate_dll(filename)
            if valid:
                self.log("DLL validation: PASSED", level='info')
            else:
                self.log(f"DLL validation: FAILED - {message}", level='warning')
    
    def inject_dll(self):
        """Perform DLL injection"""
        # Validate inputs
        if not self.selected_process_id:
            messagebox.showerror("Error", "Please select a target process")
            return
        
        if not self.selected_dll_path:
            messagebox.showerror("Error", "Please select a DLL file")
            return
        
        # Confirm injection
        result = messagebox.askyesno(
            "Confirm Injection",
            f"Inject DLL into process {self.selected_process_id}?\n\n"
            f"DLL: {os.path.basename(self.selected_dll_path)}\n"
            f"Method: {self.method_var.get()}\n\n"
            "This is for educational purposes only!",
            icon='warning'
        )
        
        if not result:
            return
        
        # Disable inject button during injection
        self.inject_btn.config(state='disabled')
        self.root.update()
        
        try:
            self.log("=" * 60)
            self.log("Starting DLL injection...")
            self.log(f"Target PID: {self.selected_process_id}")
            self.log(f"DLL: {self.selected_dll_path}")
            self.log(f"Method: {self.method_var.get()}")
            
            # Get injection method
            method = InjectionMethod(self.method_var.get())
            
            # Perform injection
            success, message = self.injector.inject_dll(
                self.selected_process_id,
                self.selected_dll_path,
                method
            )
            
            if success:
                self.log(f"SUCCESS: {message}", level='info')
                messagebox.showinfo("Success", f"DLL injected successfully!\n\n{message}")
            else:
                self.log(f"FAILED: {message}", level='error')
                messagebox.showerror("Injection Failed", message)
            
            self.log("=" * 60)
            
        except Exception as e:
            self.log(f"Exception during injection: {e}", level='error')
            messagebox.showerror("Error", f"Injection error: {str(e)}")
        
        finally:
            # Re-enable inject button
            self.inject_btn.config(state='normal')
    
    def log(self, message: str, level: str = 'info'):
        """Add message to log"""
        if level == 'info':
            self.logger.info(message)
        elif level == 'warning':
            self.logger.warning(message)
        elif level == 'error':
            self.logger.error(message)
        else:
            self.logger.info(message)


class TextHandler(logging.Handler):
    """Logging handler that writes to a tkinter Text widget"""
    
    def __init__(self, text_widget):
        logging.Handler.__init__(self)
        self.text_widget = text_widget
    
    def emit(self, record):
        msg = self.format(record)
        
        def append():
            self.text_widget.config(state='normal')
            self.text_widget.insert(tk.END, msg + '\n')
            self.text_widget.see(tk.END)
            self.text_widget.config(state='disabled')
        
        # Thread-safe update
        self.text_widget.after(0, append)


def main():
    """Main entry point for GUI"""
    # Check if running on Windows
    if sys.platform != 'win32':
        print("ERROR: This injector only works on Windows")
        return 1
    
    # Create and run GUI
    root = tk.Tk()
    
    # Set style
    style = ttk.Style()
    style.theme_use('clam')
    
    app = InjectorGUI(root)
    root.mainloop()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

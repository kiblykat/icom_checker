import os
import subprocess
import shutil
import time
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class FlashToolGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Flash Tool")
        self.root.geometry("700x700")
        
        # Constants
        self.FPKX = 0
        self.WHUD = 1
        
        # Store paths
        self.main_directory = os.getcwd()
        self.build_folder_AC = tk.StringVar()
        self.build_folder_GC = tk.StringVar()
        self.project_type = tk.IntVar(value=self.WHUD)  # Default to WHUD
        
        self.create_gui()
        
    def create_gui(self):
        # Create main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Build Folder Selection
        ttk.Label(main_frame, text="AC Build Folder:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.build_folder_AC, width=40).grid(row=0, column=1, padx=5)
        ttk.Button(main_frame, text="Browse", command=lambda: self.browse_folder('AC')).grid(row=0, column=2)
        
        ttk.Label(main_frame, text="GC Build Folder:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.build_folder_GC, width=40).grid(row=1, column=1, padx=5)
        ttk.Button(main_frame, text="Browse", command=lambda: self.browse_folder('GC')).grid(row=1, column=2)
        
        # Project Type Selection
        project_frame = ttk.LabelFrame(main_frame, text="Project Type", padding="5")
        project_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        ttk.Radiobutton(project_frame, text="FPKX", variable=self.project_type, value=self.FPKX).grid(row=0, column=0, padx=20)
        ttk.Radiobutton(project_frame, text="WHUD", variable=self.project_type, value=self.WHUD).grid(row=0, column=1, padx=20)
        
        # Progress Area
        self.progress_text = tk.Text(main_frame, height=30, width=80)
        self.progress_text.grid(row=3, column=0, columnspan=3, pady=10)
        
        # Start Button
        ttk.Button(main_frame, text="Start Process", command=self.start_process).grid(row=4, column=0, columnspan=3, pady=10)
        
    def browse_folder(self, folder_type):
        folder_path = filedialog.askdirectory(initialdir=self.main_directory)
        if folder_path:
            relative_path = os.path.relpath(folder_path, self.main_directory)
            if folder_type == 'AC':
                self.build_folder_AC.set(relative_path.upper())
            else:
                self.build_folder_GC.set(relative_path.upper())
    
    def log_progress(self, message):
        self.progress_text.insert(tk.END, f"{time.strftime('%X')} {message}\n")
        self.progress_text.see(tk.END)
        self.root.update()
    
    def validate_paths(self):
        ac_path = os.path.join(self.main_directory, self.build_folder_AC.get())
        gc_path = os.path.join(self.main_directory, self.build_folder_GC.get())
        
        if not os.path.exists(ac_path):
            messagebox.showerror("Error", "AC build folder not found!")
            return False
        if not os.path.exists(gc_path):
            messagebox.showerror("Error", "GC build folder not found!")
            return False
        return True
    
    def run_command(self, command, working_dir, wait=True, input_text=None):
        try:
            os.chdir(working_dir)
            if wait:
                if input_text:
                    process = subprocess.Popen(command, stderr=subprocess.PIPE, stdin=subprocess.PIPE, text=True)
                    process.communicate(input=input_text)
                    self.log_progress(f"Completed: {command}")
                else:
                    subprocess.run(command, stderr=subprocess.PIPE, stdin=subprocess.PIPE, text=True)
                    self.log_progress(f"Completed: {command}")
            else:
                process = subprocess.Popen(command, stderr=subprocess.PIPE, stdin=subprocess.PIPE, text=True)
                self.log_progress(f"Started: {command}")
                time.sleep(0.5)
            return True
        except Exception as e:
            self.log_progress(f"Error executing {command}: {str(e)}")
            return False
    
    def process_whud(self):
        # AC Generation
        ac_gen_path = os.path.join(self.main_directory, self.build_folder_AC.get(), "prv/tool/_GEN")
        self.run_command(["__changeRSA_PubKey.bat"], ac_gen_path)
        self.run_command(["__Gen_ALL.bat"], ac_gen_path)
        
        # GC Generation
        gc_gen_path = os.path.join(self.main_directory, self.build_folder_GC.get(), "prv/tool/_GEN")
        self.run_command(["__changeRSA_PubKey.bat"], gc_gen_path)
        self.run_command(["__Gen_ALL.bat"], gc_gen_path)
        
        # Open flash tools in sequence
        gc_out_path = os.path.join(self.main_directory, self.build_folder_GC.get(), "pkg/fls/tool/mapscrpt/out")
        ac_out_path = os.path.join(self.main_directory, self.build_folder_AC.get(), "pkg/fls/tool/mapscrpt/out")
        
        # GC Loader
        if os.path.exists(os.path.join(gc_out_path, "HUDW_MQB2020_Q3_GC_Loader.prg")):
            self.run_command(["cmd", "/c", "HUDW_MQB2020_Q3_GC_Loader.prg"], gc_out_path, False)
        else:
            self.run_command(["cmd", "/c", "HUDW_MQB2020_Q3_GC_Loader_ETH.prg"], gc_out_path, False)
        
        # AC Loader
        if os.path.exists(os.path.join(ac_out_path, "HUDW_MQB2020_Q3_AC_Loader.prg")):
            self.run_command(["cmd", "/c", "HUDW_MQB2020_Q3_AC_Loader.prg"], ac_out_path, False)
        else:
            self.run_command(["cmd", "/c", "HUDW_MQB2020_Q3_AC_Loader_ETH.prg"], ac_out_path, False)
        
        # Additional tools
        self.run_command(["cmd", "/c", "BACKUP_IDL.prg"], ac_out_path, False)
        self.run_command(["cmd", "/c", "FormatEEProm.prg"], ac_out_path, False)
        self.run_command(["cmd", "/c", "HUDW_MQB2020_Q3_GC_All.prg"], gc_out_path, False)
        self.run_command(["cmd", "/c", "HUDW_MQB2020_Q3_AC_All.prg"], ac_out_path, False)
        self.run_command(["cmd", "/c", "HUDW_MQB2020_AU380PA_C5_LL_ds.prg"], ac_out_path, False)
    
    def process_fpkx(self):
        # AC Processing
        ac_core_path = os.path.join(self.main_directory, self.build_folder_AC.get(), "tool/integration/tool/deliver/core")
        self.run_command(["get_sym.bat"], ac_core_path, False)
        self.run_command(["get_prg.bat"], ac_core_path, True, "ALL\n ")
        
        # GC Processing
        gc_core_path = os.path.join(self.main_directory, self.build_folder_GC.get(), "tool/integration/tool/deliver/core")
        self.run_command(["get_sym.bat"], gc_core_path, False)
        self.run_command(["get_prg.bat"], gc_core_path, True, "ALL\n ")
    
    def start_process(self):
        if not self.validate_paths():
            return
        
        self.progress_text.delete(1.0, tk.END)
        self.log_progress("Starting process...")
        
        try:
            if self.project_type.get() == self.WHUD:
                self.process_whud()
            else:
                self.process_fpkx()
            
            self.log_progress("Process completed successfully!")
        except Exception as e:
            self.log_progress(f"Error during process: {str(e)}")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FlashToolGUI(root)
    root.mainloop()
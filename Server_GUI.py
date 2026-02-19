import subprocess
import signal
import os
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk
import json
import requests


bash_path = r"C:\Program Files\Git\bin\bash.exe"
script_dir = ".\AasxServerBlazor.v0.3.1.343-aasV3-alpha-latest\AasxServerBlazor"
script_name = "00startForDemo.sh"

shell_folder = ".\JSON_files\JSON_Shells"
submodel_folder = ".\JSON_files\JSON_Submodels"

PORT = "5001"
SERVER_BASE = f"http://localhost:{PORT}"  # your server base URL
SUBMODEL_ENDPOINT = f"{SERVER_BASE}/submodels"
SHELL_ENDPOINT = f"{SERVER_BASE}/shells"

class ServerGUI:
    def __init__(self, root):
        self.root = root
        self.process = None  # shared subprocess

        #============================Basic Server Buttons==========================

        # Start button
        self.start_btn = tk.Button(root,text="Start Server",width=18,command=self.start_server)
        self.start_btn.place(x=50, y=40, width=120, height=40)

        # Stop button
        self.stop_btn = tk.Button(root,text="Stop Server",width=18,command=self.stop_server)
        self.stop_btn.place(x=50, y=80, width=120, height=40)

        # Reset button
        self.reset_btn = tk.Button(root,text="Reset Server",width=18,command=self.reset_server)
        self.reset_btn.place(x=50, y=120, width=120, height=40)

        #Post Shell Button
        self.post_shell_btn = tk.Button(root, text="Post Shell", width=18, command=self.post_shell)
        self.post_shell_btn.place(x=200, y=40, width=120, height=40)

        #Post Submodel Button
        self.post_submodel_btn = tk.Button(root, text="Post Submodel", width=18, command=self.post_submodel)
        self.post_submodel_btn.place(x=200, y=80, width=120, height=40)

        #============================File Dropboxes================================

        # --- Shell files dropdown ---
        self.shell_file_var = tk.StringVar(master=root)
        self.shell_files = ["Nothing Selected"] + [f for f in os.listdir(shell_folder) if f.endswith(".json")]
        self.shell_dropdown = ttk.Combobox(root,textvariable=self.shell_file_var,values=self.shell_files,state="readonly")
        self.shell_dropdown.place(x=320, y=40, width=300, height=40)
        self.shell_dropdown.current(0)

        # --- Submodel files dropdown ---
        self.submodel_file_var = tk.StringVar(master=root)
        self.submodel_files = ["Nothing Selected"] + [f for f in os.listdir(submodel_folder) if f.endswith(".json")]
        self.submodel_dropdown = ttk.Combobox(root,textvariable=self.submodel_file_var,values=self.submodel_files,state="readonly")
        self.submodel_dropdown.place(x=320, y=80, width=300, height=40)
        self.submodel_dropdown.current(0)

        #============================Misc============================================

        # --- Hook the window close event ---
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.terminal_output = ScrolledText(root, state='disabled', width=120, height=20)
        self.terminal_output.place(x=50, y=180, width=400, height=200)

    #=======================================GUI Functions================================0

    def start_server(self):
        if self.process and self.process.poll() is None:
            self.append_terminal("Server already running")
            return
        self.append_terminal("Starting Server...")
        self.process = subprocess.Popen(
            [bash_path, "-lc", f"./{script_name}"],
            cwd=script_dir,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
        )
        self.append_terminal("Server Started")

    def stop_server(self):
        if not self.process or self.process.poll() is not None:
            self.append_terminal("Server is not running")
            return

        self.append_terminal("Stopping server...")
        self.process.send_signal(signal.CTRL_C_EVENT)

        try:
            self.process.wait(timeout=1)
            self.append_terminal("Server stopped cleanly")
        except subprocess.TimeoutExpired:
            self.append_terminal("Graceful stop failed — forcing shutdown")
            self.process.kill()
            self.process.wait()
            self.append_terminal("Server force stopped")

        self.process = None

    def reset_server(self):
        self.append_terminal("Resetting server...")
        self.stop_server()
        self.start_server()
        self.append_terminal("Server Reset")

    def on_close(self):
        if self.process and self.process.poll() is None:
            self.append_terminal("Closing GUI, stopping server first...")
            self.stop_server()
        self.root.destroy()
    
    def post_shell(self):
        selected_file = self.shell_file_var.get()
        if selected_file == "Nothing Selected":
            self.append_terminal("No shell file selected")
            return
        full_path = os.path.join(shell_folder, selected_file)
        with open(full_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        response = requests.post(SHELL_ENDPOINT, json=data, headers={"Content-Type": "application/json"})
        self.append_terminal(f"Shell POST ({selected_file}): {response.status_code}")

    def post_submodel(self):
        selected_file = self.submodel_file_var.get()
        if selected_file == "Nothing Selected":
            self.append_terminal("No submodel file selected")
            return
        full_path = os.path.join(submodel_folder, selected_file)
        with open(full_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        response = requests.post(SUBMODEL_ENDPOINT, json=data, headers={"Content-Type": "application/json"})
        self.append_terminal(f"Submodel POST ({selected_file}): {response.status_code}")

    def append_terminal(self, text):
        self.terminal_output.configure(state='normal')
        self.terminal_output.insert(tk.END, text + "\n")
        self.terminal_output.see(tk.END)  # scroll to the end
        self.terminal_output.configure(state='disabled')

root = tk.Tk()
root.title("AAS Server Controller")
root.geometry("1000x500")        # width x height
root.resizable(False, False)
app = ServerGUI(root)
root.mainloop()












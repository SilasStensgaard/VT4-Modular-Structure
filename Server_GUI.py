import subprocess
import time
import signal
import tkinter as tk

def start_server():
    print("start")

def stop_server():
    print("stop")

def reset_server():
    print("Reset")

root = tk.Tk()
root.title("AAS Server Controller")

root.geometry("1000x500")        # width x height


root.resizable(False, False)

start_btn = tk.Button(root, text="Start Server", width=18,command=start_server)
stop_btn = tk.Button(root, text="Stop Server", width=18, command=stop_server)
reset_btn = tk.Button(root,text="Reset Server", width=18, command=reset_server)

start_btn.place(x=50, y=40, width=120, height=40)
stop_btn.place(x=50, y=80, width=120, height=40)
reset_btn.place(x=50, y=120, width=120, height=40)


root.mainloop()











#bash_path = r"C:\Program Files\Git\bin\bash.exe"
#script_dir = r"C:\Users\silas\Desktop\Manufacturing_Technology_4\Software\VT4-Modular-Structure\AasxServerBlazor.v0.3.1.343-aasV3-alpha-latest\AasxServerBlazor"
#script_name = "00startForDemo.sh"
#
#process = subprocess.Popen(
#    [bash_path, "-lc", f"./{script_name}"],
#    cwd=script_dir,
#    creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
#)
#
#print("Server started")
#time.sleep(10)
#
#print("Stopping server...")
#process.send_signal(signal.CTRL_C_EVENT)
#
#try:
#    #It could wait forever, the server shuts down fast but it still waits
#    process.wait(timeout=3)   # wait up to 3 sec for clean shutdown
#    print("Server stopped cleanly")
#except subprocess.TimeoutExpired:
#    print("Graceful stop failed — forcing shutdown")
#    process.kill()
#    process.wait()
#    print("Server force stopped")

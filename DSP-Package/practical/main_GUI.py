import tkinter as tk
import importlib.util

def open_and_execute_file(file_path):
    spec = importlib.util.spec_from_file_location("module_name", file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

def open_file_and_execute_code(file_path):
    open_and_execute_file(file_path)

root = tk.Tk()
root.geometry("700x500")
root.configure(bg="#EBE3D5")
root.title("Main GUI for DSP Practical Tasks")


# For the Filter button
def open_filter_file():
    open_file_and_execute_code("filters.py")

button2 = tk.Button(root, text="Filters", command=open_filter_file)
button2.configure(font=("Arial", 12, "bold"), bg="#EBE3D5", fg="#053B50")
button2.place(relx=0.4, rely=0.2, anchor=tk.CENTER)

root.mainloop()
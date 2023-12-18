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
root.configure(bg="purple")
root.title("Main GUI for DSP Project")

# For the DFT button
def open_DFT_file():
    open_file_and_execute_code("DFT.py")

button1 = tk.Button(root, text="DFT", command=open_DFT_file)
button1.configure(font=("Arial", 12), bg="blue", fg="white")
button1.place(relx=0.3, rely=0.1, anchor=tk.CENTER)

# For the IDFT button
def open_IDFT_file():
    open_file_and_execute_code("IDFT.py")

button2 = tk.Button(root, text="IDFT", command=open_IDFT_file)
button2.configure(font=("Arial", 12), bg="blue", fg="white")
button2.place(relx=0.6, rely=0.1, anchor=tk.CENTER)

# For the "DCT" button (replace "YourFile.py" with the actual file path)
def open_DCT_file():
   open_file_and_execute_code("DCT.py")

button3 = tk.Button(root, text="DCT", command=open_DCT_file)
button3.configure(font=("Arial", 12), bg="blue", fg="white")
button3.place(relx=0.3, rely=0.25, anchor=tk.CENTER)


def open_Moving_Average():
   open_file_and_execute_code("movingAverage.py")

button4 = tk.Button(root, text="Smoothing", command=open_Moving_Average)
button4.configure(font=("Arial", 12), bg="blue", fg="white")
button4.place(relx=0.6, rely=0.25, anchor=tk.CENTER)


def open_Sharpen():
   open_file_and_execute_code("sharpen.py")

button5 = tk.Button(root, text="Sharpen", command=open_Sharpen)
button5.configure(font=("Arial", 12), bg="blue", fg="white")
button5.place(relx=0.3, rely=0.35, anchor=tk.CENTER)

def Delay_Advance():
   open_file_and_execute_code("delay_advance.py")

button6 = tk.Button(root, text="Shifting", command=Delay_Advance)
button6.configure(font=("Arial", 12), bg="blue", fg="white")
button6.place(relx=0.6, rely=0.35, anchor=tk.CENTER)


def convolution():
   open_file_and_execute_code("convolution.py")

button7 = tk.Button(root, text="Convolution", command=convolution)
button7.configure(font=("Arial", 12), bg="blue", fg="white")
button7.place(relx=0.3, rely=0.45, anchor=tk.CENTER)


def correlation():
   open_file_and_execute_code("correlation.py")

button8 = tk.Button(root, text="Correlation", command=correlation)
button8.configure(font=("Arial", 12), bg="blue", fg="white")
button8.place(relx=0.6, rely=0.45, anchor=tk.CENTER)


def template_matching():
   open_file_and_execute_code("template_matching.py")

button9 = tk.Button(root, text="Template Matching", command=template_matching)
button9.configure(font=("Arial", 12), bg="blue", fg="white")
button9.place(relx=0.3, rely=0.55, anchor=tk.CENTER)

def fast_correlation():
   open_file_and_execute_code("fastCorrelation.py")

button10 = tk.Button(root, text="Fast Correlation", command=fast_correlation)
button10.configure(font=("Arial", 12), bg="blue", fg="white")
button10.place(relx=0.6, rely=0.55, anchor=tk.CENTER)

def fast_convolution():
   open_file_and_execute_code("fastConvolution.py")

button11 = tk.Button(root, text="Fast Convolution", command=fast_convolution)
button11.configure(font=("Arial", 12), bg="blue", fg="white")
button11.place(relx=0.3, rely=0.65, anchor=tk.CENTER)
root.mainloop()

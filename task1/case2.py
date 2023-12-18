from tkinter import *
from tkinter import messagebox, Tk
from tkinter import ttk
import matplotlib.pyplot as plt
import numpy as np

def  get_data():

    selected_option = combo_box.get()
    amplitude_val=float(amplitude_input.get())
    phaseShift_val=float(phaseShift_input.get())
    Analog_freq_val=float(Analog_freq_input.get())
    sampling_freq_val=float(sampling_freq_input.get())

    if(sampling_freq_val<(2*Analog_freq_val)):
        messagebox.showinfo("Alert","The sampling frequency must be more than 2xAnalog frequancy")
    else:
        plot_data(selected_option, amplitude_val, phaseShift_val, Analog_freq_val, sampling_freq_val)



def plot_data(selected_option, amplitude_val, phaseShift_val, Analog_freq_val, sampling_freq_val):
        #phaseShift_val=phaseShift_val*(np.pi)
        t = np.linspace(0, 1, num=1000)
        n = np.arange(0, 50)
        if selected_option == "sin":
            analogSignal = amplitude_val * np.sin(2 * np.pi * Analog_freq_val * t + phaseShift_val)
            discreteSignal = amplitude_val * np.sin((2 * np.pi * Analog_freq_val * n / sampling_freq_val) + phaseShift_val)
            print("Discrete signal values 'sin' \n ",discreteSignal)
        elif selected_option == "cos":
            analogSignal = amplitude_val * np.cos(2 * np.pi * Analog_freq_val * t + phaseShift_val)
            discreteSignal = amplitude_val * np.cos((2 * np.pi * Analog_freq_val * n / sampling_freq_val) + phaseShift_val)
            print("Discrete signal values 'cos' \n ",discreteSignal)


        # Plot the analog signal
        plt.figure(figsize=(14,7))
        plt.subplot(2, 1, 1)
        plt.plot(t, analogSignal, label="Analog Signal")
        plt.xlabel("Time (s)")
        plt.ylabel("Amplitude")
        plt.title("Analog Signal")
        plt.grid(True)

        # Plot the discrete signal
        plt.subplot(2, 1, 2)
        plt.stem(n, discreteSignal, label="Discrete Signal")
        plt.xlabel("Sampel")
        plt.ylabel("Amplitude")
        plt.title("Discrete Signal")
        plt.legend()
        plt.grid(True)

        plt.tight_layout()
        plt.show()




#############gui##########
root = Tk()
root.geometry("1000x500")
root.configure(bg="light blue")
root.title("Case 2-Task 1")
signal_type_label=Label(root,text="Choose signal type",fg="red",font="bold",bg="light blue")
signal_type_label.grid(row=1, column=0)

signal_type_options=["sin","cos"]
combo_box = ttk.Combobox(root, values=signal_type_options)
combo_box.grid(row=1, column=1)


amplitude_label=Label(root,text="Amplitude",fg="red",font=("bold"),bg="light blue")
amplitude_label.grid(row=2, column=0)

amplitude_input = Entry(root, font=(15), fg="gray")
amplitude_input.grid(row=2, column=1)


phaseShift_label=Label(root,text="Phase shift ",fg="red",font=("bold"),bg="light blue")
phaseShift_label.grid(row=3, column=0)

phaseShift_input = Entry(root, font=(15), fg="gray")
phaseShift_input.grid(row=3, column=1)


Analog_freq_label=Label(root,text="Analog Frequancy ",fg="red",font=("bold"),bg="light blue")
Analog_freq_label.grid(row=4, column=0)

Analog_freq_input = Entry(root, font=(15), fg="gray")
Analog_freq_input.grid(row=4, column=1)

sampling_freq_label=Label(root,text="Sampling Frequancy ",fg="red",font=("bold"),bg="light blue")
sampling_freq_label.grid(row=5, column=0)

sampling_freq_input = Entry(root, font=(15), fg="gray")
sampling_freq_input.grid(row=5, column=1)


calc_btn = Button(root, text="View Signal", width="10", height="1", font="20", bg="black", fg="white", command=get_data)
calc_btn.grid(row=6, column=1)


root.mainloop()
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import *
import numpy as np
import matplotlib.pyplot as plt

# Enable interactive plotting
plt.ion()

x_values1 = []
y_values1 = []
x_values2 = []
y_values2 = []

def DFT(signal):
    N = len(signal)
    X = np.zeros(N, dtype=complex)
    for k in range(N):
        X[k] = 0
        for n in range(N):
            X[k] += signal[n] * np.exp(-2j * np.pi * k * n / N)

    return X

def IDFT(X):
    N = len(X)
    signal = np.zeros(N, dtype=complex)

    for n in range(N):
        signal[n] = 0
        for k in range(N):
            angle = 2 * np.pi * n * k / N
            real_part = np.cos(angle)
            imaginary_part = np.sin(angle)
            signal[n] += (X[k].real * real_part) - (X[k].imag * imaginary_part)

        signal[n] /= N

    return signal





def open_file1():
    file_path = filedialog.askopenfilename()

    if file_path:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            if len(lines) >= 3:
                array_size = int(lines[2].strip())

                for line in lines[3:]:
                    values = line.strip().split()
                    if len(values) >= 2:
                        x_value = float(values[0])
                        y_value = float(values[1])
                        x_values1.append(x_value)
                        y_values1.append(y_value)

def open_file2():
    file_path = filedialog.askopenfilename()

    if file_path:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            if len(lines) >= 3:
                array_size = int(lines[2].strip())

                for line in lines[3:]:
                    values = line.strip().split()
                    if len(values) >= 2:
                        x_value = float(values[0])
                        y_value = float(values[1])
                        x_values2.append(x_value)
                        y_values2.append(y_value)



# def fast_convolution(y_values1, y_values2):
#     # Apply zero-padding to make both arrays the same length
#     max_len = max(len(y_values1), len(y_values2))
#     y_values1_padded = np.pad(y_values1, (0, max_len - len(y_values1)))
#     y_values2_padded = np.pad(y_values2, (0, max_len - len(y_values2)))
#
#     # Perform FFT on both arrays
#     y_values1_freq = np.fft.fft(y_values1_padded)
#     y_values2_freq = np.fft.fft(y_values2_padded)
#
#     # Multiply the arrays in the frequency domain
#     result_freq_domain = y_values1_freq * y_values2_freq
#
#     # Apply Inverse Fast Fourier Transform (IFFT) to obtain the convolution result in the time domain
#     result_time_domain = np.fft.ifft(result_freq_domain)
#
#     # Use np.real to get the real part of the result
#     result_time_domain_real = np.real(result_time_domain)
#
#     return result_time_domain_real

# Rest of your code remains the same...




def perform_FC():
    len1 = len(y_values1)
    len2 = len(y_values2)

    extended_len = len1 + len2 - 1
    y_values1_padded = np.pad(y_values1, (0, extended_len - len1))
    y_values2_padded = np.pad(y_values2, (0, extended_len - len2))

    Y1 = DFT(y_values1_padded)
    Y2 = DFT(y_values2_padded)

    result_freq_domain = Y1 * Y2

    result_time_domain = IDFT(result_freq_domain)

    start_index = int(min(x_values1))
    x_values_result = np.arange(start_index, start_index + extended_len)

    print(x_values_result, result_time_domain.real)

    return x_values_result, result_time_domain.real






root = tk.Tk()
root.geometry("500x400")
root.configure(bg="beige")
root.title("Fast Convolution")
sampling_frequency_label = tk.Label(root, text="Enter the sampling frequency (Hz):")
sampling_frequency_label.configure(font=("Arial", 12), bg="beige")
sampling_frequency_label.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

sampling_frequency_entry = tk.Entry(root)
sampling_frequency_entry.configure(font=("Arial", 12))
sampling_frequency_entry.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
upload_button_s1 = tk.Button(root, text="Upload SIGNAL - 1", command=open_file1)
upload_button_s1.configure(font=("Arial", 12), bg="black", fg="white")
upload_button_s1.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

upload_button_s2 = tk.Button(root, text="Upload SIGNAL - 2", command=open_file2)
upload_button_s2.configure(font=("Arial", 12), bg="black", fg="white")
upload_button_s2.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

convolution_button = tk.Button(root, text="Perform Fast Convolution", command=perform_FC)
convolution_button.configure(font=("Arial", 12), bg="black", fg="white")
convolution_button.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

root.mainloop()
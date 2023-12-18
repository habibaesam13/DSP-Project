import tkinter as tk
from tkinter import filedialog
import numpy as np
import matplotlib.pyplot as plt

indices = result = []
x_values1 = []
y_values1 = []
x_values2 = []
y_values2 = []


def apply_test(indices, samples):
    expected_indices = [-2, -1, 0, 1, 2, 3, 4, 5, 6]
    expected_samples = [1, 1, -1, 0, 0, 3, 3, 2, 1]

    if len(expected_samples) != len(samples) or len(expected_indices) != len(indices):
        print("Conv Test case failed, your signal has a different length from the expected one")
        return

    for i in range(len(indices)):
        if indices[i] != expected_indices[i]:
            print("Conv Test case failed, your signal has different indices from the expected one")
            return

    for i in range(len(expected_samples)):
        if abs(samples[i] - expected_samples[i]) < 0.01:
            continue
        else:
            print("Conv Test case failed, your signal has different values from the expected one")
            return

    print("Conv Test case passed successfully")


def convolution(x_values1, y_values1, x_values2, y_values2):
    len1 = len(y_values1)
    len2 = len(y_values2)

    start_index = int(min(x_values1) + min(x_values2))
    end_index = int(max(x_values1) + max(x_values2))

    indices = list(range(start_index, end_index + 1))

    for n in range(len1 + len2 - 1):
        sum_val = 0
        for m in range(min(n, len1 - 1) + 1):
            if 0 <= n - m < len2:
                sum_val += y_values1[m] * y_values2[n - m]
        result.append(sum_val)

    return indices, result


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


def perform_conv():
    indices, result = convolution(x_values1, y_values1, x_values2, y_values2)
    apply_test(indices, result)
    print(indices, "\nresults", result)
    plot_convolution(x_values1, y_values1, x_values2, y_values2, indices, result)


def plot_convolution(x_values1, y_values1, x_values2, y_values2, indices, result):
    plt.figure(figsize=(12, 8))

    plt.subplot(3, 1, 1)
    plt.plot(x_values1, y_values1, 'bo-', label='Signal 1')
    plt.title('Signal 1')
    plt.legend()

    plt.subplot(3, 1, 2)
    plt.plot(x_values2, y_values2, 'go-', label='Signal 2')
    plt.title('Signal 2')
    plt.legend()

    plt.subplot(3, 1, 3)
    plt.stem(indices, result, 'ro-', label='Convolution Result')
    plt.title('Convolution Result')
    plt.legend()

    plt.xlabel('Index')
    plt.ylabel('Amplitude')

    plt.tight_layout()
    plt.show()


##################### GUI ######################


root = tk.Tk()
root.geometry("500x400")
root.configure(bg="beige")
root.title("Convolution Of Two Signals")

upload_button_s1 = tk.Button(root, text="Upload SIGNAL - 1", command=open_file1)
upload_button_s1.configure(font=("Arial", 12), bg="black", fg="white")
upload_button_s1.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

upload_button_s2 = tk.Button(root, text="Upload SIGNAL - 2", command=open_file2)
upload_button_s2.configure(font=("Arial", 12), bg="black", fg="white")
upload_button_s2.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

convolution_button = tk.Button(root, text="Perform Convolution", command=perform_conv)
convolution_button.configure(font=("Arial", 12), bg="black", fg="white")
convolution_button.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

root.mainloop()

import tkinter as tk
from tkinter import filedialog
import numpy as np
import matplotlib.pyplot as plt
from comparesignal2 import SignalSamplesAreEqual

# def simple_moving_average(data, window_size):
#     cumsum = [0] * (len(data) - window_size + 1)
#     cumsum[0] = sum(data[:window_size])
#
#     for i in range(1, len(cumsum)):
#         cumsum[i] = cumsum[i - 1] - data[i - 1] + data[i + window_size - 1]
#
#     return [cumsum[i] / window_size for i in range(len(cumsum))]


def simple_moving_average(data, window_size):
    moving_averages = []

    for i in range(len(data) - window_size + 1):
        window_sum = sum(data[i:i + window_size])
        moving_average = window_sum / window_size
        moving_averages.append(moving_average)

    return moving_averages

def open_file():
    WSize = int(windowSize_entry.get())
    file_path = filedialog.askopenfilename()

    if file_path:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            if len(lines) >= 3:
                array_size = int(lines[2].strip())
                x_values = []  # Initialize the x_values array
                y_values = []  # Initialize the y_values array

                for line in lines[3:]:  # Iterate from the fourth line
                    values = line.strip().split()
                    if len(values) >= 2:  # Ensure there are at least 2 values on the line
                        x_value = float(values[0])  # Convert to float
                        y_value = float(values[1])  # Convert to float
                        x_values.append(x_value)  # Append the first value to x_values
                        y_values.append(y_value)  # Append the second value to y_values

                # Apply Simple Moving Average
                ResMA = simple_moving_average(y_values, WSize)

                # Plot original and smoothed data
                plt.figure(figsize=(8, 6))

                # Plot original data
                plt.subplot(2, 1, 1)
                plt.plot(x_values, y_values, label='Original Data')
                plt.title('Original Data')

                # Plot data after applying moving average
                plt.subplot(2, 1, 2)
                plt.plot(x_values[WSize-1:], ResMA, label=f'Moving Average (Window Size={WSize})')
                plt.title('Data After Applying Moving Average')

                # Add labels and legend
                plt.xlabel('X Values')
                plt.ylabel('Y Values')
                plt.legend()

                # Show the plots
                plt.tight_layout()
                plt.show()

                # SignalSamplesAreEqual("input_output_files/MovAvgTest2.txt", ResMA)

# GUI
root = tk.Tk()
root.geometry("500x400")
root.configure(bg="beige")
root.title("Smoothing Signal - Moving Average")

windowSizeLable = tk.Label(root, text="Window Size", bg="beige", fg="black")
windowSizeLable.place(relx=0.5, rely=0.2, anchor=tk.CENTER)
windowSize_entry = tk.Entry(root)
windowSize_entry.configure(font=("Arial", 12))
windowSize_entry.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

upload_button_s1 = tk.Button(root, text="Upload SIGNAL", command=open_file)
upload_button_s1.configure(font=("Arial", 12), bg="black", fg="white")
upload_button_s1.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

root.mainloop()

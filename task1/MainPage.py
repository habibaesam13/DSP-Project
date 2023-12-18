from tkinter import *
import matplotlib.pyplot as plt
import numpy as np

def plot_data():
    # Get the text from the Entry widget
    y_values = sampels.get().split(',')  # Split input by comma
    x_values = np.arange(len(y_values))  # Create an array of x-values from 0 to len(y_values) - 1

    # Convert the input values to float
    x_values = list(map(float, x_values))
    y_values = list(map(float, y_values))

    # Create a figure with two subplots side by side
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

    # Plot the digital signal in the first subplot with vertical lines connecting x and y
    for x, y in zip(x_values, y_values):
        ax1.vlines(x, 0, y, color='blue', linestyle='-', linewidth=2)

    ax1.set_xlabel('Time')
    ax1.set_ylabel('Sample Value')
    ax1.set_title('Digital Signal')

    # Plot the analog signal in the second subplot
    ax2.plot(x_values, y_values,color="blue")
    ax2.set_xlabel('Time')
    ax2.set_ylabel('Value')
    ax2.set_title('Analog Signal')

    plt.tight_layout()  # Ensure proper spacing between subplots
    plt.show()


                           ########## GUI ###########
root = Tk()
root.geometry("1000x500")
root.configure(bg="light blue")
root.title("Home")

sampels_label = Label(text="Enter The Samples", font=20)
sampels_label.grid(row=4, column=0)

sampels = Entry(root, font=("Helvetica", 15), fg="gray")
sampels.grid(row=4, column=1)

calc_btn = Button(root, text="View Signal", width="10", height="1", font="20", bg="black", fg="white", command=plot_data)
calc_btn.grid(row=6, column=1)

root.mainloop()

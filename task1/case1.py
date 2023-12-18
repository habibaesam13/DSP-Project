from tkinter import *
import matplotlib.pyplot as plt
from tkinter import filedialog

def open_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            if len(lines) >= 3:
                array_size = int(lines[2].strip())
                my_array = [None] * array_size  # Initialize the main array
                x_values = []  # Initialize the x_values array
                y_values = []  # Initialize the y_values array

                for line in lines[3:]:  # Iterate from the fourth line
                    values = line.strip().split()
                    if len(values) >= 2:  # Ensure there are at least 2 values on the line
                        x_value = values[0]
                        y_value = values[1]
                        x_values.append(x_value)  # Append the first value to x_values
                        y_values.append(y_value)  # Append the second value to y_values
                plot_data(x_values,y_values)
                


def plot_data(x_values, y_values):
    x_values = list(map(float, x_values))
    y_values = list(map(float, y_values))


    # Create a figure with two subplots side by side
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    # Plot the digital signal in the first subplot with vertical lines connecting x and y
    for x, y in zip(x_values, y_values):
         #ax1.scatter(x_values, y_values, color='blue', marker='o', s=50)
         ax1.stem(x_values, y_values)

    ax1.set_xlabel('Sample')
    ax1.set_ylabel('Amplitude')
    ax1.set_title('Digital Signal')

    # Plot the analog signal in the second subplot
    ax2.plot(x_values, y_values, color="blue")
    ax2.set_xlabel('Time')
    ax2.set_ylabel('Amplitude')
    ax2.set_title('Analog Signal ')

    plt.tight_layout()  # Ensure proper spacing between subplots
    plt.show()






            #############GUI################
root = Tk()
root.geometry("400x400")
root.configure(bg="light blue")
root.title("Case 1-Task 1")

upload_button = Button(root, text="Upload File", command=open_file)
upload_button.pack(pady=10)


root.mainloop()
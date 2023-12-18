from tkinter import *
from tkinter import messagebox, Tk
import matplotlib.pyplot as plt
from tkinter import ttk
from tkinter import filedialog
          ##########glogal var ########


selected_operation = ""
x_values=[]
y_values=[]


           ################## open file function #################
def open_file():
    file_path = filedialog.askopenfilename()
    global array_size
    if file_path:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            if len(lines) >= 3:
                array_size = int(lines[2].strip())
                my_array = [None] * array_size  # Initialize the main array
                   # Initialize the y_values array

                for line in lines[3:]:  # Iterate from the fourth line
                    values = line.strip().split()
                    if len(values) >= 2:  # Ensure there are at least 2 values on the line
                        x_value = int(values[0])  # Convert to a float
                        y_value = int(values[1])  # Convert to a float
                        x_values.append(x_value)  # Append the first value to x_values
                        y_values.append(y_value)  # Append the second value to y_values
    plot_result(x_values, y_values)



def normalize(normalized_entry1_val, normalized_entry2_val, x_values, y_values):
    if not y_values:
        return None  # Handle the case where y_values is empty or None

    min_value = int(normalized_entry1_val)
    max_value = int(normalized_entry2_val)

    # Calculate the scaling factor
    scale_factor = (max_value - min_value) / (max(y_values) - min(y_values))

    # Normalize the signal values to the new range
    normalized_data_y = [(value - min(y_values)) * scale_factor + min_value for value in y_values]
    print("Normalize Values is\n",normalized_data_y)
    plot_result(x_values,normalized_data_y)





def perform_operation():
    normalized_entry1_val=normalized_entry1.get()
    normalized_entry2_val=normalized_entry2.get()
    # Now you can use file1_data_x, file1_data_y, file2_data_x, file2_data_y, and selected_operation
    normalize(normalized_entry1_val,normalized_entry2_val,x_values, y_values)




def plot_result(x1, y1):
    plt.figure(figsize=(12, 12))
    plt.plot(x1, y1, label="Signal")
    plt.xlabel("X Values")
    plt.ylabel("Y Values")
    plt.title("Signal Plot")
    plt.legend()
    plt.show()





    #####################gui##################




root = Tk()
root.geometry("400x400")
root.configure(bg="black")
root.title("task 2-operations on one signal")

upload_button_s1 = Button(root, text="Upload SIGNAL ", command= open_file)

upload_button_s1.configure(font=("Arial", 12), bg="black", fg="white")

upload_button_s1.place(relx=.5,rely=0.2,anchor=CENTER)


normalized_entry_label1=Label(root,text="Min Scale to signal",bg="black",fg="white")
normalized_entry_label1.place(relx=0.35,rely=0.25)
normalized_entry1 = Entry(root,text="")  # Create an Entry widget
normalized_entry1.place(relx=0.33, rely=0.3)  # Adjust the position as needed

normalized_entry_label2=Label(root,text="Max Scale to signal",bg="black",fg="white")
normalized_entry_label2.place(relx=0.35,rely=0.35)
normalized_entry2 = Entry(root,text="")  # Create an Entry widget
normalized_entry2.place(relx=0.33, rely=0.4)  # Adjust the position as needed

calc_btn = Button(root, text="View Normalized Signal", width="25", height="1", font="20", bg="black", fg="white", command=perform_operation)
calc_btn.place(relx=0.15,rely=0.6)

root.mainloop()
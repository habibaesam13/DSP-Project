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







         ######################  operations on signals #################


def multi (x_values,y_values ,val):
    result_data_y = []

    # Loop through the data points and add the corresponding y values
    for i in range(len(x_values)):  # Iterate through the x_values
        result_data_y.append(y_values[i] * int(val))   # Update y_values in place

    print("Mulitplication Result",result_data_y,"\n\n")
    plot_result(x_values, result_data_y)





def shifting( x_values,y_values, val):
    result_y_axis=[]
    for i in range(len(x_values)):
        result_y_axis.append(x_values[i]+int(val))
    print("Shifting Result", result_y_axis, "\n\n")
    plot_result(y_values, result_y_axis)




   ########################## apply opperations with condition #################

def perform_operation():
    # Now you can use file1_data_x, file1_data_y, file2_data_x, file2_data_y, and selected_operation
    selected_operation=combo_box.get()
    val = multi_entry.get()

    if selected_operation == "MULTI":
        val = multi_entry.get()
        multi(x_values, y_values,val)
    elif selected_operation == "SHIFTING(x-axis)":
        val = multi_entry.get()
        shifting(x_values, y_values,val)



             ###########function plot res ###############
def plot_result(x1, y1):
    plt.figure(figsize=(12, 12))
    plt.plot(x1, y1, label="Signal 1")
    plt.xlabel("X Values")
    plt.ylabel("Y Values")
    plt.title("Signal Plot")
    plt.legend()
    plt.show()

############gui#########

root = Tk()
root.geometry("400x400")
root.configure(bg="black")
root.title("task 2-operations on one signal")

upload_button_s1 = Button(root, text="Upload SIGNAL ", command= open_file)

upload_button_s1.configure(font=("Arial", 12), bg="black", fg="white")

upload_button_s1.place(relx=.5,rely=0.2,anchor=CENTER)


choose_operation_label=Label(root,text="Operation on Signals",bg="black",fg="white")
choose_operation_label.place(relx=0.34,rely=.25)

signals_operations=["MULTI","SHIFTING(x-axis)","Accumulation"]
style = ttk.Style()
style.configure("TCombobox", background="black", foreground="darkred")
combo_box =ttk.Combobox(root, values=signals_operations,style="TCombobox")
combo_box.set("Select an option")  # Set the default text
combo_box.place(relx=0.31,rely=0.31)
multi_entry_label=Label(root,text="Scale to signal",bg="black",fg="white")
multi_entry_label.place(relx=0.37,rely=0.38)
multi_entry = Entry(root,text="")  # Create an Entry widget
multi_entry.place(relx=0.33, rely=0.435)  # Adjust the position as needed

calc_btn = Button(root, text="View Signal", width="10", height="1", font="20", bg="black", fg="white", command=perform_operation)
calc_btn.place(relx=0.35,rely=0.52)

root.mainloop()
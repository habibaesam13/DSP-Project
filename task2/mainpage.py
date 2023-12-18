from tkinter import *
from tkinter import messagebox, Tk
import matplotlib.pyplot as plt
from tkinter import ttk
from tkinter import filedialog
          ##########glogal var ########
file1_data_x = []
file1_data_y = []
file2_data_x = []
file2_data_y = []
selected_operation = ""
file1_size=""
file2_size=""
result_data_y_f1=[]
result_data_y_f2=[]



           ################## open file function #################
def open_file(file_num):
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
                        x_value = int(values[0])  # Convert to a float
                        y_value = int(values[1])  # Convert to a float
                        x_values.append(x_value)  # Append the first value to x_values
                        y_values.append(y_value)  # Append the second value to y_values

                if file_num == 1:
                    global file1_data_x, file1_data_y
                    file1_size=array_size
                    file1_data_x = x_values
                    file1_data_y = y_values
                elif file_num == 2:
                    file2_size=array_size
                    global file2_data_x, file2_data_y
                    file2_data_x = x_values
                    file2_data_y = y_values


        ############### function for validation #################
def check_files_size(file1_size,file2_size=""):
    if (file1_size==file2_size):
        return

    elif(file1_size>file2_size):
        for i in range(file2_size + 1, file1_size + 1):
            file2_data_x.append(i)
            file2_data_y.append(0)

    elif(file2_size>file1_size):
        for i in range(file1_size + 1, file2_size + 1):
            file1_data_x.append(i)
            file1_data_y.append(0)


         ######################  operations on signals #################
def add(file1_data_x ,file1_data_y ,file2_data_x ,file2_data_y):
    check_files_size(file1_size,file2_size)
    result_data_y = []

    # Loop through the data points and add the corresponding y values
    for i in range(len(file1_data_y)):
        result_y = file1_data_y[i] + file2_data_y[i]
        result_data_y.append(result_y)
    plot_result(file1_data_x, result_data_y)


def sub (file1_data_x ,file1_data_y ,file2_data_x ,file2_data_y):
    check_files_size(file1_size,file2_size)
    result_data_y = []

    # Loop through the data points and add the corresponding y values
    for i in range(len(file1_data_y)):
        result_y = file1_data_y[i] - file2_data_y[i]
        result_data_y.append(result_y)
    plot_result(file1_data_x, result_data_y)


   ########################## apply opperations with condition #################

def perform_operation():
    # Now you can use file1_data_x, file1_data_y, file2_data_x, file2_data_y, and selected_operation
    selected_operation=combo_box.get()
    if selected_operation == "ADD":
        add(file1_data_x, file1_data_y, file2_data_x, file2_data_y)
    elif selected_operation == "SUB":
        sub(file1_data_x, file1_data_y, file2_data_x, file2_data_y)




             ###########function plot res ###############
def plot_result(x1, y1, x2=None, y2=None):
    plt.figure(figsize=(8, 6))
    plt.plot(x1, y1, label="Signal 1")
    if x2 and y2:
        plt.plot(x2, y2, label="Signal 2")
    plt.xlabel("X Values")
    plt.ylabel("Y Values")
    plt.title("Signal Plot")
    plt.legend()
    plt.show()

############gui#########

root = Tk()
root.geometry("400x400")
root.configure(bg="black")
root.title("task 2")

upload_button_s1 = Button(root, text="Upload SIGNAL 1", command=lambda: open_file(1))
upload_button_s2 = Button(root, text="Upload SIGNAL 2", command=lambda: open_file(2))

upload_button_s1.configure(font=("Arial", 12), bg="black", fg="white")
upload_button_s2.configure(font=("Arial", 12), bg="black", fg="white")
upload_button_s1.place(relx=.5,rely=0.1,anchor=CENTER)
upload_button_s2.place(relx=.5,rely=0.2,anchor=CENTER)

choose_operation_label=Label(root,text="Operation on Signals",bg="black",fg="white")
choose_operation_label.place(relx=0.34,rely=.25)

signals_operations=["ADD","SUB"]
style = ttk.Style()
style.configure("TCombobox", background="black", foreground="darkred")
combo_box =ttk.Combobox(root, values=signals_operations,style="TCombobox")
combo_box.set("Select an option")  # Set the default text
combo_box.place(relx=0.31,rely=0.31)

calc_btn = Button(root, text="View Signal", width="10", height="1", font="20", bg="black", fg="white", command=perform_operation)
calc_btn.place(relx=0.33,rely=0.39)

root.mainloop()
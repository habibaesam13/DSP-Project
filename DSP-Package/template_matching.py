import tkinter as tk
import os
from tkinter import filedialog
import numpy as np
import matplotlib.pyplot as plt

def open_folder(title):
    folder_path = filedialog.askdirectory(title=f"Select {title} Folder")
    return folder_path

def open_test_file():
    global test_file_content
    test_file_content = process_file(filedialog.askopenfilename(title="Select Test Signal File"))
    print("Test File Content:", test_file_content)

def open_class1_folder():
    global class1_content
    class1_content = process_folder(open_folder("Class 1"))
    print("Class 1 Folder Content:", class1_content)

def open_class2_folder():
    global class2_content
    class2_content = process_folder(open_folder("Class 2"))
    print("Class 2 Folder Content:", class2_content)

def process_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        return np.array(content.split(), dtype=float)

def process_folder(folder_path):
    files_contents = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            content = process_file(file_path)
            files_contents.append(content)

    aggregated_samples = aggregate_samples(files_contents)
    return aggregated_samples

def aggregate_samples(files_contents):
    max_samples = max(len(content) for content in files_contents)
    aggregated_samples = np.zeros(max_samples)

    for content in files_contents:
        aggregated_samples[:len(content)] += content

    aggregated_samples /= len(files_contents)
    return aggregated_samples

def calculate_correlation(test_file_content, folder_content):
    correlation = np.corrcoef(test_file_content, folder_content)[0, 1]
    return correlation

def plot_arrays():
    plt.figure(figsize=(10, 6))

    plt.subplot(3, 1, 1)
    plt.plot(test_file_content, label='Test File')
    plt.title('Test File Array')
    plt.legend()

    plt.subplot(3, 1, 2)
    plt.plot(class1_content, label='Class 1')
    plt.title('Class 1 Array')
    plt.legend()

    plt.subplot(3, 1, 3)
    plt.plot(class2_content, label='Class 2')
    plt.title('Class 2 Array')
    plt.legend()

    plt.tight_layout()
    plt.show()

def decide_correlation():
    correlation_class1 = calculate_correlation(test_file_content, class1_content)
    correlation_class2 = calculate_correlation(test_file_content, class2_content)

    print(f"Correlation with Class 1: {correlation_class1}")
    print(f"Correlation with Class 2: {correlation_class2}")

    if correlation_class1 > correlation_class2:
        result_label.config(text="The test file is highly correlated with Class 1.")
    else:
        result_label.config(text="The test file is highly correlated with Class 2.")

    plot_arrays()

myframe = tk.Tk()
myframe.geometry("500x400")
myframe.title("Template Matching for Signal Classification")
myframe.configure(bg="beige")

test_button = tk.Button(myframe, text="Open Test File", command=open_test_file, bg="blue", fg="white")
test_button.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

class1_button = tk.Button(myframe, text="Open Class 1 Folder", command=open_class1_folder, bg="blue", fg="white")
class1_button.place(relx=0.3, rely=0.4, anchor=tk.CENTER)

class2_button = tk.Button(myframe, text="Open Class 2 Folder", command=open_class2_folder, bg="blue", fg="white")
class2_button.place(relx=0.7, rely=0.4, anchor=tk.CENTER)

result_label = tk.Label(myframe, text="", bg="beige", font=("Helvetica", 12))
result_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

calculate_button = tk.Button(myframe, text="Calculate Correlation", command=decide_correlation, bg="green", fg="white")
calculate_button.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

myframe.mainloop()

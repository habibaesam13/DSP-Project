import numpy as np
import tkinter as tk
from tkinter import ttk, filedialog, simpledialog  # Import simpledialog
from PIL import Image, ImageTk

results_before = []  # Define results_before outside the if block

def calculate_idft(X):
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

def browse_file_and_process():
    selected_operation = combo_box.get()
    file_path = filedialog.askopenfilename()

    if selected_operation == "convert to  time domain":
        if file_path:
            try:
                X = []

                with open(file_path, 'r') as file:
                    lines = file.readlines()
                    for line in lines[3:]:
                        values = line.strip().replace(",",
                                                      " ").split()  # Replace commas with spaces and split
                        if len(values) == 2:
                            amplitude_str = values[0].replace("f",
                                                              "")  # Remove 'f' suffix
                            phase_str = values[1].replace("f", "")  # Remove 'f' suffix
                            amplitude = float(amplitude_str)
                            phase = float(phase_str)
                            complex_value = amplitude * (
                                    np.cos(phase) + 1j * np.sin(phase))
                            X.append(complex_value)

                signal = calculate_idft(X)
                N = len(signal)
                sampling_frequency = 1

                results = [{"Value": signal[n].real} for n in range(N)]

                display_results(results)

            except Exception as e:
                print(f"Error: {e}")
    elif selected_operation == "change component":
        if file_path:
            try:
                X = []

                with open(file_path, 'r') as file:
                    lines = file.readlines()
                    for line in lines[3:]:
                        values = line.strip().replace(",",
                                                      " ").split()  # Replace commas with spaces and split
                        if len(values) == 2:
                            amplitude_str = values[0].replace("f",
                                                              "")  # Remove 'f' suffix
                            phase_str = values[1].replace("f", "")  # Remove 'f' suffix
                            amplitude = float(amplitude_str)
                            phase = float(phase_str)
                            complex_value = amplitude * (
                                    np.cos(phase) + 1j * np.sin(phase))
                            X.append(complex_value)

                component_index = simpledialog.askinteger("Component Index",
                                                          "Enter the index of the component to change:")
                new_amplitude = simpledialog.askfloat("New Amplitude", "Enter the new amplitude value:")
                new_phase = simpledialog.askfloat("New Phase", "Enter the new phase value (in radians):")

                if component_index is not None and new_amplitude is not None and new_phase is not None:
                    if component_index >= 0 and component_index < len(X):
                        X[component_index] = new_amplitude * (np.cos(new_phase) + 1j * np.sin(new_phase))

                        #  Calculate the time domain signal before modification
                        # signal_before = calculate_idft(X.copy())  # Make a copy of X for before modification
                        #
                        #
                        #
                        # # Display the results before modification
                        # display_results(results, "Before")

                        # Calculate the time domain signal after modification
                        signal_after = calculate_idft(X)  # Calculate with modified X

                        N = len(signal_after)
                        results_after = [{"Value": signal_after[n].real} for n in range(N)]

                        # Display the results after modification
                        display_results(results_after, "After")

                    else:
                        print("Component index is out of range.")
                else:
                    print("Invalid input for component modification.")

            except Exception as e:
                print(f"Error: {e}")

def display_results(results, label=""):
    if results:
        x_n = "{" + ", ".join([f"{result['Value']:.4f}" for result in results]) + "}"
        print(f'x(n) {label}  = {x_n}')

# Create the main window
window = tk.Tk()
window.geometry("500x400")
window.configure(bg="beige")
window.title("Time Domain Analysis")

choose_operation_label = tk.Label(window, text="Operation on Signals", bg="beige", fg="black")
choose_operation_label.place(relx=0.34, rely=0.2)

signals_operations = ["convert to  time domain", "change component"]
style = ttk.Style()
style.configure("TCombobox", background="black", foreground="darkred")
combo_box = ttk.Combobox(window, values=signals_operations, style="TCombobox")
combo_box.place(relx=0.34, rely=0.3)

# Create and place the button
browse_and_process_button = tk.Button(window, text="Apply Operation", command=browse_file_and_process)
browse_and_process_button.configure(font=("Arial", 12), bg="black", fg="white")
browse_and_process_button.place(relx=0.47, rely=0.45, anchor=tk.CENTER)

# Start the GUI main loop
window.mainloop()

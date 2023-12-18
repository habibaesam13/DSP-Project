import tkinter as tk
from tkinter import messagebox, filedialog
import numpy as np
import matplotlib.pyplot as plt
import math
from practical.Practical_task1.CompareSignal import Compare_Signals
# from scipy import signal
# Declare global variables

Hd = []
signal_after_filtering = []
x_values = []
y_values = []
convRes = []
def test_signal_after_resampling(M,L,indexes,result):
     if M !=0 and L==0:
         print(f"\nTEST SIGNAL WITH DOWN SAMPLING ONLY WITH M={M} AND L= {L}\n")
         Compare_Signals("D:\python\DSP-Tasks\DSP-Package\practical\Practical_task1\Sampling test cases\Testcase 1\Sampling_Down.txt",
                         indexes,result)
     elif L !=0 and M ==0 :
         print(f"\nTEST SIGNAL WITH UP SAMPLING ONLY WITH M={M} AND L= {L}\n")
         Compare_Signals(
             "D:\python\DSP-Tasks\DSP-Package\practical\Practical_task1\Sampling test cases\Testcase 2\Sampling_Up.txt",
             indexes, result)
     elif L >0 and M >0 :
         print(f"\nTEST SIGNAL WITH UP SAMPLING AND dOWN WITH M={M} AND L= {L}\n")
         Compare_Signals(
             "D:\python\DSP-Tasks\DSP-Package\practical\Practical_task1\Sampling test cases\Testcase 3\Sampling_Up_Down.txt",
             indexes, result)

def convolution(x_values, y_values, x_values2, y_values2):
    len1 = len(y_values)
    len2 = len(y_values2)

    start_index = int(min(x_values) + min(x_values2))
    end_index = int(max(x_values) + max(x_values2))

    indices = list(range(start_index, end_index + 1))

    for n in range(len1 + len2 - 1):
        sum_val = 0
        for m in range(min(n, len1 - 1) + 1):
            if 0 <= n - m < len2:
                sum_val += y_values[m] * y_values2[n - m]
        convRes.append(round(sum_val, 10))

    return indices, convRes


def apply_window(Hd, windowName, N):
    positiveindices = []
    multi_res = []
    if windowName == "Rectangular":
        # Return indices and values symmetrically
        indices = list(range(-int(N / 2), int(N / 2) + 1))
        return indices, Hd + Hd[::-1]
    elif windowName == "Hanning":
        for i in range(int(N / 2) + 1):
            positiveindices.append(0.5 + 0.5 * math.cos(2 * math.pi * i / N))
    elif windowName == "Hamming":
        for i in range(int(N / 2) + 1):
            positiveindices.append(0.54 + 0.46 * math.cos(2 * math.pi * i / N))
    elif windowName == "Blackman":
        for i in range(int(N / 2) + 1):
            component1 = 0.42
            component2 = 0.5 * math.cos(2 * math.pi * i / (N - 1))
            component3 = 0.08 * math.cos(4 * math.pi * i / (N - 1))

            positiveindices.append(component1 + component2 + component3)
    else:
        raise ValueError("Unsupported windowName")

    # Multiply corresponding Hd and window values
    for value1, value2 in zip(Hd, positiveindices):
        multi_res.append(round(value1 * value2, 10))

    # Iterate over negative indices and append to the list
    for i in range(-1, -len(multi_res) - 1, -1):
        value = multi_res[i]
        signal_after_filtering.append(value)

    # Iterate over positive indices and append to the list
    for i in range(1, len(multi_res)):
        value = multi_res[i]
        signal_after_filtering.append(value)

    # Return the indices and symmetric values
    indices = list(range(-int(N / 2), int(N / 2) + 1))

    return indices, signal_after_filtering


def lowPassFilter():
    global fs_original
    fs_original = float(sampling_frequency_entry.get())
    stop_attenuation = float(stop_attenuation_entry.get())
    transition_width = float(transition_band_entry.get())
    cutoff = float(CutoffFrequency_entry.get())
    cutoff /= fs_original
    transition_width /= fs_original

    window_stopBandAttenuation = [
        (21, 0.9, "Rectangular"),
        (44, 3.1, "Hanning"),
        (53, 3.3, "Hamming"),
        (74, 5.5, "Blackman"),
    ]
    for tup in window_stopBandAttenuation:
        first_value = tup[0]
        if first_value >= stop_attenuation:
            windowName = tup[2]
            N = round(tup[1] / transition_width)
            if N % 2 == 0:
                N += 1
            break
    cutoff += 0.5 * transition_width
    Hd.append(2 * cutoff)
    for i in range(1, int(N / 2) + 1):
        Hd.append(
            2 * cutoff * (math.sin(i * 2 * math.pi * cutoff) / (i * 2 * math.pi * cutoff)))
    indices, signal_after_filtering = apply_window(Hd, windowName, N)
    return indices, signal_after_filtering

def downSampling(M,L,X=x_values,Y=y_values):
   if L ==0:
     convIndx,convRes=convolution(X,Y,filteredIndicies,FilteredSignal)
     nyquist = 0.5 * fs_original
     # avoid Aliasing
     if fs_original / M < nyquist:
         messagebox.showinfo("Alert", "Can Not Apply Resampling cause Aliasing Will Accrue")
         return
     else:
         min_index = min(convIndx)
         downsampled_result = []
         downsampled_indices = []

         for i in range(0, len(convRes), M):
             downsampled_result.append(convRes[i])
             downsampled_indices.append(min_index)
             min_index += 1
             if i >= len(convRes):
                 break
     test_signal_after_resampling(M, L, downsampled_indices, downsampled_result)
     plot_three_figures(x_values, y_values, convIndx, convRes, downsampled_indices, downsampled_result,
                        "Filtered Signal", "Down Sampling Signal")

   else:
       nyquist = 0.5 * fs_original
       # avoid Aliasing
       if fs_original / M < nyquist:
           messagebox.showinfo("Alert", "Can Not Apply Resampling cause Aliasing Will Accrue")
           return
       else:
           min_index = min(X)
           downsampled_result = []
           downsampled_indices = []

           for i in range(0, len(Y), M):
               downsampled_result.append(Y[i])
               downsampled_indices.append(min_index)
               min_index += 1
               if i >= len(Y):
                   break

       return downsampled_indices,downsampled_result

def upSampling(M, L):
    upsampled_result = []
    upsampled_indices = []
    # Iterate through the data
    for i in range(len(x_values) - 1):
        # Append the current element
        upsampled_result.append(y_values[i])

        # Add L-1 zeros between the current and next element
        for j in range(1, L):
            upsampled_result.append(0)

    # Append the last element of the original data
    upsampled_result.append(y_values[-1])
    for i in range(len(upsampled_result)):
        upsampled_indices.append(i)

    lastIndx, lastVal = convolution(upsampled_indices, upsampled_result, filteredIndicies, FilteredSignal)
    if M == 0:
        test_signal_after_resampling(M, L, lastIndx, lastVal)
        plot_three_figures(x_values, y_values, upsampled_indices, upsampled_result, lastIndx, lastVal,
                           "Up Sampling Signal", "Filtered Signal")
    else :
     return lastIndx, lastVal


def upandDown(M,L):
    lastindx,lastval=[],[]
    upInd, UpRes = upSampling(M, L)
    lastindx,lastval=downSampling(M, L, upInd, UpRes)
    test_signal_after_resampling(M,L,lastindx,lastval)
    plot_three_figures(x_values, y_values, upInd, UpRes, lastindx,lastval, "Up Sampling Signal",
                       "Down Sampling (FINAL RES)")

def Resampling():
    global filteredIndicies, FilteredSignal
    filteredIndicies, FilteredSignal = lowPassFilter()
    M = int(DownSamplingFactor_entry.get())
    L = int(UpSamplingFactor_entry.get())
    if M==0 and L==0:
        return
    elif M != 0 and L == 0:
       # filter then down sampling by M-1
       downSampling(M,L)
    elif L !=0 and M == 0:
        upSampling(M,L)
    elif L != 0 and M != 0 :
        upandDown(M,L)


def plot_three_figures(x_original, y_original, indices_filtered, filtered_values, indices_downsampled,
                       downsampled_values,
                       title_2, title_3):
    # Create a new figure
    plt.figure(figsize=(10, 6))

    # Plot original signal
    plt.subplot(3, 1, 1)
    plt.plot(x_original, y_original, label="Original Signal")
    plt.title("Original Signal")
    plt.xlabel("Index")
    plt.ylabel("Amplitude")
    plt.legend()

    # Plot filtered values
    plt.subplot(3, 1, 2)

    # Ensure lengths match for stem plot
    min_len = min(len(indices_filtered), len(filtered_values))
    plt.stem(indices_filtered[:min_len], filtered_values[:min_len], label=title_2, basefmt="C1-")

    plt.title(title_2)
    plt.xlabel("Index")
    plt.ylabel("Amplitude")
    plt.legend()

    # Plot downsampled values
    plt.subplot(3, 1, 3)
    plt.stem(indices_downsampled, downsampled_values, label=title_3, basefmt="C2-")
    plt.title(title_3)
    plt.xlabel("Index")
    plt.ylabel("Amplitude")
    plt.legend()

    # Adjust layout to prevent overlapping
    plt.tight_layout()

    # Show the plot
    plt.show()


def open_file():
    global x_values, y_values
    file_path = filedialog.askopenfilename()

    if file_path:
        with open(file_path, "r") as file:
            lines = file.readlines()
            if len(lines) >= 3:
                array_size = int(lines[2].strip())

                for line in lines[3:]:
                    values = line.strip().split()
                    if len(values) >= 2:
                        x_value = float(values[0])
                        y_value = float(values[1])
                        x_values.append(x_value)
                        y_values.append(y_value)

    Resampling()


#####################################GUI##################################################
root = tk.Tk()
root.geometry("900x600")
root.configure(bg="#EBE3D5")
root.title("RESAMPLING")

# Down sampling Factor(M) Entry and Label
DownSamplingFactor_label = tk.Label(root, text="Down Sampling Factor:")
DownSamplingFactor_label.configure(font=("Arial", 12, "bold"), fg="#053B50", bg="#EBE3D5")
DownSamplingFactor_label.place(relx=0.25, rely=0.18, anchor=tk.CENTER)
DownSamplingFactor_entry = tk.Entry(root)
DownSamplingFactor_entry.configure(font=("Arial", 12, "bold"))
DownSamplingFactor_entry.place(relx=0.6, rely=0.18, anchor=tk.CENTER)

# Up Sampling Factor Entry and Label
UpSamplingFactor_label = tk.Label(root, text="Up Sampling Factor:")
UpSamplingFactor_label.configure(font=("Arial", 12, "bold"), fg="#053B50", bg="#EBE3D5")
UpSamplingFactor_label.place(relx=0.24, rely=0.26, anchor=tk.CENTER)
UpSamplingFactor_entry = tk.Entry(root)
UpSamplingFactor_entry.configure(font=("Arial", 12, "bold"))
UpSamplingFactor_entry.place(relx=0.6, rely=0.26, anchor=tk.CENTER)

# Filter Specifications
filterSpecification_label = tk.Label(root, text="Filter Specifications")
filterSpecification_label.configure(font=("Arial", 14, "bold"), fg="#053B50", bg="#EBE3D5")
filterSpecification_label.place(relx=0.45, rely=0.4, anchor=tk.CENTER)

# Sampling Frequency Entry and Label
sampling_frequency_label = tk.Label(root, text="Sampling Frequency(HZ):")
sampling_frequency_label.configure(font=("Arial", 12, "bold"), fg="#053B50", bg="#EBE3D5")
sampling_frequency_label.place(relx=0.26, rely=0.48, anchor=tk.CENTER)
sampling_frequency_entry = tk.Entry(root)
sampling_frequency_entry.configure(font=("Arial", 12, "bold"))
sampling_frequency_entry.place(relx=0.6, rely=0.48, anchor=tk.CENTER)

# Stop Attenuation Entry and Label
stop_attenuation_label = tk.Label(root, text="Stop Attenuation:")
stop_attenuation_label.configure(font=("Arial", 12, "bold"), fg="#053B50", bg="#EBE3D5")
stop_attenuation_label.place(relx=0.225, rely=0.55, anchor=tk.CENTER)
stop_attenuation_entry = tk.Entry(root)
stop_attenuation_entry.configure(font=("Arial", 12, "bold"))
stop_attenuation_entry.place(relx=0.6, rely=0.55, anchor=tk.CENTER)

# Transition Band Entry and Label
transition_band_label = tk.Label(root, text="Transition Band:")
transition_band_label.configure(font=("Arial", 12, "bold"), fg="#053B50", bg="#EBE3D5")
transition_band_label.place(relx=0.22, rely=0.62, anchor=tk.CENTER)
transition_band_entry = tk.Entry(root)
transition_band_entry.configure(font=("Arial", 12, "bold"))
transition_band_entry.place(relx=0.6, rely=0.62, anchor=tk.CENTER)

# Cutoff frequency Entry and Label
CutoffFrequency_label = tk.Label(root, text="Cutoff Frequency:")
CutoffFrequency_label.configure(font=("Arial", 12, "bold"), fg="#053B50", bg="#EBE3D5")
CutoffFrequency_label.place(relx=0.22, rely=0.68, anchor=tk.CENTER)
CutoffFrequency_entry = tk.Entry(root)
CutoffFrequency_entry.configure(font=("Arial", 12, "bold"))
CutoffFrequency_entry.place(relx=0.6, rely=0.68, anchor=tk.CENTER)

# Create and place the buttons
browse_and_button = tk.Button(root, text="Upload Signal", command=open_file)
browse_and_button.configure(font=("Arial", 12, "bold"), bg="#EBE3D5", fg="#053B50")
browse_and_button.place(relx=0.45, rely=0.79, anchor=tk.CENTER)



root.mainloop()

import tkinter as tk
from tkinter import messagebox, filedialog
import numpy as np
import matplotlib.pyplot as plt
import math
import os
Filter_type = None

Hd = []
signal_after_filtering = []

               ############## READ FOLDERS AND FILES CONTENT ###############
def open_test_file1():
    global test_file1_content
    test_file1_content = process_file(filedialog.askopenfilename(title="Select Test Signal File"))
    print("Test File Content:", test_file1_content)
def open_test_file2():
    global test_file2_content
    test_file2_content = process_file(filedialog.askopenfilename(title="Select Test Signal File"))
    print("Test File Content:", test_file2_content)
def open_folder(title):
    folder_path = filedialog.askdirectory(title=f"Select {title} Folder")
    return folder_path

def open_test_file():
    global test_file_content
    test_file_content = process_file(filedialog.askopenfilename(title="Select Test Signal File"))
    print("Test File Content:", test_file_content)

def open_class1_folder():
    global class1_content
    arr1_class1, arr2_class1, arr3_class1 = [], [], []
    arr4_class1, arr5_class1, arr6_class1 = [], [], []
    global Class1_arrCollection
    Class1_arrCollection = [arr1_class1, arr2_class1, arr3_class1, arr4_class1, arr5_class1, arr6_class1]
    class1_content = process_folder(open_folder("Class 1"))
    for file_info, arrIndx in zip(class1_content, Class1_arrCollection):
        file_name = file_info['file_name']
        content_array = file_info['content_array']
        # print(f"Class 1 File Name: {file_name}, Content Array: {content_array}")
        for value in content_array:
            arrIndx.append(value)  # Use arrIndx directly here, as it represents the array


def open_class2_folder():
    arr1_class2, arr2_class2, arr3_class2 = [], [], []
    arr4_class2, arr5_class2, arr6_class2 = [], [], []
    global Class2_arrCollection
    Class2_arrCollection = [arr1_class2, arr2_class2, arr3_class2, arr4_class2, arr5_class2, arr6_class2]
    global class2_content
    class2_content = process_folder(open_folder("Class 2"))
    for file_info, arrIndx in zip(class2_content, Class2_arrCollection):
        file_name = file_info['file_name']
        content_array = file_info['content_array']
        # print(f"Class 2 File Name: {file_name}, Content Array: {content_array}")
        for value in content_array:
            arrIndx.append(value)  # Use arrIndx directly here, as it represents the array



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
            files_contents.append({
                'file_name': filename,
                'content_array': content
            })
    return files_contents


    ############ Apply Convolution ################
def convolution(x_values, y_values, x_values2, y_values2):
    len1 = len(y_values)
    len2 = len(y_values2)
    convRes=[]
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

    ########### APPLY FILTER BASED ON ITS TYPE ##############
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

def ApplyFilter(Fs,fType="lowPass")  :
    ###  fs , f1 ,f2 ,transition band, stop band att
    if not( stop_attenuation_entry.get() and transition_band_entry.get() and Mini_frequency_entry.get() and Max_frequency_entry.get() ):
        return
    # to specify window
    stopAtt = float(stop_attenuation_entry.get())
    transBand = float(transition_band_entry.get())
    Mini_frequency = float(Mini_frequency_entry.get())
    Max_frequency = float(Max_frequency_entry.get())
     # normalization
    transBand /= Fs
    Mini_frequency /= Fs
    Max_frequency /= Fs
    # know window
    window_stopBandAttenuation = [
        (21, 0.9, "Rectangular"),
        (44, 3.1, "Hanning"),
        (53, 3.3, "Hamming"),
        (74, 5.5, "Blackman"),
    ]
    for tup in window_stopBandAttenuation:
        first_value = tup[0]
        if first_value >= stopAtt:
            windowName = tup[2]
            N = round(tup[1] / transBand )
            if N % 2 == 0:
                N += 1
            break
    # get Hd
    if fType=="lowPass":
        Cuttoff = int(CutoffFrequency_entry.get())
        Cuttoff += 0.5 * transBand
        Hd.append(2 *Cuttoff)
        for i in range(1, int(N / 2) + 1):
            Hd.append(
                2 * Cuttoff * (math.sin(i * 2 * math.pi * Cuttoff) / (i * 2 * math.pi * Cuttoff)))
        indices, signal_after_filtering = apply_window(Hd, windowName, N)
    elif Filter_type == "bandPass":
        # high pass     low pass
        Mini_frequency -= (0.5 * transBand)
        Max_frequency += (0.5 * transBand)
        Hd.append(2 * (Max_frequency  - Mini_frequency))
        for i in range(1, int(N / 2) + 1):
            inserted_val = 2 * Max_frequency  * (math.sin(i * 2 * math.pi * Max_frequency ) / (i * 2 * math.pi * Max_frequency ))
            inserted_val += -2 * Mini_frequency * (math.sin(i * 2 * math.pi * Mini_frequency) / (i * 2 * math.pi * Mini_frequency))
            Hd.append(inserted_val)
        indices, signal_after_filtering = apply_window(Hd, windowName, N)
    elif Filter_type == "bandReject":
        # low pass      high pass
        Mini_frequency += (0.5 * transBand)
        Max_frequency -= (0.5 * transBand)
        Hd.append(1 - 2 * (Max_frequency - Mini_frequency))
        for i in range(1, int(N / 2) + 1):
            inserted_val = 2 * Mini_frequency * (math.sin(i * 2 * math.pi * Mini_frequency) / (i * 2 * math.pi * Mini_frequency))
            inserted_val += -2 * Max_frequency * (math.sin(i * 2 * math.pi * Max_frequency) / (i * 2 * math.pi * Max_frequency))
            Hd.append(inserted_val)
        indices, signal_after_filtering = apply_window(Hd, windowName, N)

    return indices, signal_after_filtering
      ############################ DOWN SAMPLING THE SIGNAL #####################################3


def downSampling(M, indx, Class1_val, Class2_val=""):
    M = int(1 / M)
    arr1_class1, arr2_class1, arr3_class1 = [], [], []
    arr4_class1, arr5_class1, arr6_class1 = [], [], []
    arr1_class2, arr2_class2, arr3_class2 = [], [], []
    arr4_class2, arr5_class2, arr6_class2 = [], [], []

    Class1_downSampled_val = [arr1_class1, arr2_class1, arr3_class1, arr4_class1, arr5_class1, arr6_class1]
    Class2_downSampled_val = [arr1_class2, arr2_class2, arr3_class2, arr4_class2, arr5_class2, arr6_class2]

    Class1_afterdown_indx = []
    first_iteration = True
    minIndx = min(indx)

    for indexArr1, indexArr2, newArrC1, newArrC2 in zip(Class1_val, Class2_val,
                                                        Class1_downSampled_val, Class2_downSampled_val):
        # Reset Class1_afterdown_indx for each iteration of the loop
        current_Class1_afterdown_indx = []
        for i in range(0, len(indexArr1), M):
            newArrC1.append(indexArr1[i])

        for j in range(0, len(indexArr2), M):
            newArrC2.append(indexArr2[j])
            current_Class1_afterdown_indx.append(minIndx)
            minIndx += 1
        # Append the current indices to the overall list
        if first_iteration:
            Class1_afterdown_indx.extend(current_Class1_afterdown_indx)
            first_iteration = False

    return Class1_afterdown_indx, Class1_downSampled_val, Class2_downSampled_val




def upsampling(L, indx, Class1_val, Class2_val):
    L = int(L)
    first_iteration = True
    arr1_class1, arr2_class1, arr3_class1 = [], [], []
    arr4_class1, arr5_class1, arr6_class1 = [], [], []
    arr1_class2, arr2_class2, arr3_class2 = [], [], []
    arr4_class2, arr5_class2, arr6_class2 = [], [], []

    Class1_upSampled_val = [arr1_class1, arr2_class1, arr3_class1, arr4_class1, arr5_class1, arr6_class1]
    Class2_upSampled_val = [arr1_class2, arr2_class2, arr3_class2, arr4_class2, arr5_class2, arr6_class2]

    Class1_afterup_indx = []

    minIndx = min(indx)

    for indexArr1, indexArr2, newArrC1, newArrC2 in zip(Class1_val, Class2_val,
                                                        Class1_upSampled_val, Class2_upSampled_val):
        current_Class1_afterup_indx = []
        current_Class2_afterup_indx = []

        # Upsample each array based on the provided logic
        for i in range(len(indexArr1) - 1):
            # Append the current element
            newArrC1.append(indexArr1[i])
            # Add L-1 zeros between the current and next element
            for j in range(1, L):
                newArrC1.append(0)

        # Append the last element of the original data
        newArrC1.append(indexArr1[-1])

        # Create corresponding upsampled indices for Class1
        for i in range(len(newArrC1)+1):
            current_Class1_afterup_indx.append(minIndx)
            minIndx += 1
        if first_iteration:
        # Append the current indices to the overall list for Class1
         Class1_afterup_indx.extend(current_Class1_afterup_indx)
         first_iteration=False

        # Reset minIndx for Class2
        minIndx = min(indx)

        # Upsample each array in Class2
        for i in range(len(indexArr2) - 1):
            newArrC2.append(indexArr2[i])
            for j in range(1, L):
                newArrC2.append(0)

        newArrC2.append(indexArr2[-1])

        # Create corresponding upsampled indices for Class2
        for i in range(len(newArrC2)):
            current_Class2_afterup_indx.append(minIndx)
            minIndx += 1
        # Append the current indices to the overall list for Class2
    print(len(indx))
    for arr in Class1_upSampled_val:
        print(len(arr),"\n")
    print("\n\n",Class1_afterup_indx)
    return Class1_afterup_indx, Class1_upSampled_val, Class2_upSampled_val


################## remove DC #############################
def remove_dc_component(y_values):
    print("remove_dc_component function is called")
    mean_value = np.mean(y_values)
    y_values = [val - mean_value for val in y_values]
   # print(dc_inputs, "\n", dc_outputs)
    return y_values

###### NORMALIZE SIGNAL ###########
def normalize( y_values):
    if not y_values:
        return None  # Handle the case where y_values is empty or None
    min_value = int(-1)
    max_value = int(1)
    # Calculate the scaling factor
    scale_factor = (max_value - min_value) / (max(y_values) - min(y_values))
    # Normalize the signal values to the new range
    normalized_data_y = [(value - min(y_values)) * scale_factor + min_value for value in y_values]
    return normalized_data_y
######## Auto Correlation ###############
def auto_correlation(x1, x2):
    N = len(x1)
    cross_corr_result = []

    for n in range(N):
        cross_corr_value = 1/N * sum(x1[j] * x2[(j + n) % N] for j in range(N))
        cross_corr_result.append(cross_corr_value)


    return cross_corr_result[0]

#### dct #######
def dct1d(x):
    N = len(x)
    y = np.zeros(N)

    for k in range(N):
        sum_val = 0.0
        for n in range(N):
            sum_val += np.sqrt(2/N) * x[n] * np.cos(np.pi / (4 * N) * (2 * n - 1) * (2 * k - 1))
        y[k] = sum_val


    return y
##### template matching ######
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

def decide_correlation(class1_content,class2_content):
    # class1 with2 test files
    correlation_class11 = calculate_correlation(test_file1_content, class1_content)
    correlation_class12 = calculate_correlation(test_file2_content, class1_content)
    # class 2 with 2 test files
    correlation_class21 = calculate_correlation(test_file1_content, class2_content)
    correlation_class22 = calculate_correlation(test_file2_content, class2_content)
    print(f"Correlation with Class 1: {correlation_class11}")
    print(f"Correlation with Class 1: {correlation_class12}")
    print(f"Correlation with Class 2: {correlation_class21}")
    print(f"Correlation with Class 2: {correlation_class22}")

    if correlation_class11 > correlation_class21:
        print("The test 1 file  is highly correlated with Class A.")
    else:
        print("The test 1 file  is highly correlated with Class B.")
    if  correlation_class12 > correlation_class22:
        print("The test 2 file  is highly correlated with Class A.")
    else:
        print("The test 2 file  is highly correlated with Class B.")

    ############ CALL ALL FUNCTIONS AT RUN TIME ###############
def Apply_Process():
    isSampled=False
    first_iteration=True

    eachSegInd = []
    arr1_class1, arr2_class1, arr3_class1 = [], [], []
    arr4_class1, arr5_class1, arr6_class1 = [], [], []
    arr1_class2, arr2_class2, arr3_class2 = [], [], []
    arr4_class2, arr5_class2, arr6_class2 = [], [], []
    Class1_afterFiltringResam_val = [arr1_class1, arr2_class1, arr3_class1, arr4_class1, arr5_class1, arr6_class1]
    Class2_afterFiltringResam_val = [arr1_class2, arr2_class2, arr3_class2, arr4_class2, arr5_class2, arr6_class2]
    Class1_afterFiltring_val = [arr1_class1, arr2_class1, arr3_class1, arr4_class1, arr5_class1, arr6_class1]
    Class2_afterFiltring_val = [arr1_class2, arr2_class2, arr3_class2, arr4_class2, arr5_class2, arr6_class2]
    filterWindowIndx, filterWindowValues = [], []
    Class1_afterFiltring_indx= []
    ##### STEP 1 FILTER ALL SEGMENTS
    for i in range(2500):
        eachSegInd.append(i)
    if not Filter_type:
        messagebox.showinfo("Alert", "Choose Filter Type")
        # Handle the case where Filter_type is not selected
    else:
        ## for band filter
        if not (sampling_frequency_entry.get()):
            # Handle the case where sampling frequency is not provided
            return
        else:
            Fs = float(sampling_frequency_entry.get())

            filterWindowIndx, filterWindowValues = ApplyFilter(Fs)
            
            for indexArr1, indexArr2, newArrC1, newArrC2 in zip(Class1_arrCollection, Class2_arrCollection,
                                                                Class1_afterFiltring_val, Class2_afterFiltring_val):
                # Perform convolution for Class1
                indices1, convRes1 = convolution(eachSegInd, indexArr1, filterWindowIndx, filterWindowValues)
                newArrC1.extend(convRes1)

                # Perform convolution for Class2
                indices2, convRes2 = convolution(eachSegInd, indexArr2, filterWindowIndx, filterWindowValues)
                newArrC2.extend(convRes2)

            # Fill Class1_afterFiltring_indx and Class2_afterFiltring_indx only once
            Class1_afterFiltring_indx.extend(indices1)
            print("\nBAND PASS FILTER IS DONE !!!!!!\n")
            # for i, arr in enumerate(Class1_afterFiltring_val):
            #     for j in Class1_afterFiltring_indx:
            #         filename = f"class1_segment_{i}_BandPass.txt"
            #         with open(filename, 'a') as file:  # Use 'a' for append mode or 'w' for write mode
            #             file.write(f"{j} {arr[j]}\n")
            # for i, arr in enumerate(Class2_afterFiltring_val):
            #     for j in Class1_afterFiltring_indx:
            #         filename = f"class2_segment_{i}_BandPass.txt"
            #         with open(filename, 'a') as file:  # Use 'a' for append mode or 'w' for write mode
            #             file.write(f"{j} {arr[j]}\n")

            ### STEP 2 RESAMPLE ALL SEGMENTS
             ## for resampling i will check if it < 0.5*fs then reject else make down sampling

            if not NewFs_entry.get():
                return
            else:
                NewFs = float(NewFs_entry.get())
                if NewFs>= 0.5*Fs:
                    isSampled=True
                    filterWindowIndx, filterWindowValues = ApplyFilter(Fs, "lowPass")
                    factor = NewFs / Fs
                    print("factor is:",factor,"\n")
                    if NewFs<Fs and 1/factor >1 :
                        # down sampling the filtered segments
                        for indexArr1, indexArr2, newArrC1, newArrC2 in zip(Class1_afterFiltring_val,Class2_afterFiltring_val,
                                                                            Class1_afterFiltringResam_val,Class2_afterFiltringResam_val):
                            # Perform convolution for Class1
                            indices1, convRes1 = convolution(Class1_afterFiltring_indx, indexArr1, filterWindowIndx,
                                                             filterWindowValues)
                            newArrC1.extend(convRes1)

                            # Perform convolution for Class2
                            indices2, convRes2 = convolution(Class1_afterFiltring_indx, indexArr2, filterWindowIndx,
                                                             filterWindowValues)
                            newArrC2.extend(convRes2)

                        # Fill Class1_afterFiltring_indx and Class2_afterFiltring_indx only once
                        Class1_afterFiltring_indx.extend(indices1)
                        Class1_afterFiltring_indx, Class1_afterFiltringResam_val, Class2_afterFiltringResam_val=downSampling(factor,Class1_afterFiltring_indx,  Class1_afterFiltring_val, Class2_afterFiltring_val)
                        print(f"\nDOWN RESAMPLING WITH M = {int(1/factor)} IS DONE !!!!!!\n")
                        # for i, arr in enumerate(Class1_afterFiltringResam_val):
                        #     for j in Class1_afterFiltring_indx:
                        #         filename = f"class1_segment_{i}_BandPass and down.txt"
                        #         with open(filename, 'a') as file:  # Use 'a' for append mode or 'w' for write mode
                        #             file.write(f"{j} {arr[j]}\n")
                        # for i, arr in enumerate(Class2_afterFiltringResam_val):
                        #     for j in Class1_afterFiltring_indx:
                        #         filename = f"class2_segment_{i}_BandPass and down.txt"
                        #         with open(filename, 'a') as file:  # Use 'a' for append mode or 'w' for write mode
                        #             file.write(f"{j} {arr[j]}\n")

                    elif  NewFs>Fs and factor>1:
                         # up sample then filter segments
                        Class1_afterFiltring_indx,Class1_afterFiltring_val, Class2_afterFiltring_val= upsampling(factor,Class1_afterFiltring_indx,Class1_afterFiltring_val, Class2_afterFiltring_val)
                        for indexArr1, indexArr2, newArrC1, newArrC2 in zip(Class1_afterFiltring_val,Class2_afterFiltring_val,
                                                                            Class1_afterFiltringResam_val,Class2_afterFiltringResam_val):
                            # Perform convolution for Class1
                            indices1, convRes1 = convolution(Class1_afterFiltring_indx, indexArr1, filterWindowIndx,
                                                             filterWindowValues)
                            newArrC1.extend(convRes1)

                            # Perform convolution for Class2
                            indices2, convRes2 = convolution(Class1_afterFiltring_indx, indexArr2, filterWindowIndx,
                                                             filterWindowValues)
                            newArrC2.extend(convRes2)
                        # Fill Class1_afterFiltring_indx and Class2_afterFiltring_indx only once
                        Class1_afterFiltring_indx.extend(indices1)
                        print(f"\nUP RESAMPLING WITH L = {int(factor)} IS DONE !!!!!!\n")
                        # for i, arr in enumerate(Class1_afterFiltringResam_val):
                        #    for j in Class1_afterFiltring_indx:
                        #          filename = f"class1_segment_{i}_BandPass and up sample.txt"
                        #          with open(filename, 'a') as file:  # Use 'a' for append mode or 'w' for write mode
                        #              file.write(f"{j} {arr[j]}\n")
                        # for i, arr in enumerate(Class2_afterFiltringResam_val):
                        #      for j in Class1_afterFiltring_indx:
                        #          filename = f"class2_segment_{i}_BandPass and up sample.txt"
                        #          with open(filename, 'a') as file:  # Use 'a' for append mode or 'w' for write mode
                        #              file.write(f"{j} {arr[j]}\n")



                else:
                    messagebox.showinfo("Alert", "We can Not resample with Fs small than NYQUIST")
        ###remove dc component from each segment
        if not(isSampled):
            for indexArr1, indexArr2, newArrC1, newArrC2 in zip(Class1_afterFiltring_val, Class2_afterFiltring_val,
                                                                Class1_afterFiltringResam_val, Class2_afterFiltringResam_val):
                newArrC1=remove_dc_component(indexArr1)
                newArrC2=remove_dc_component(indexArr2)
            Class1_afterFiltring_val=Class1_afterFiltringResam_val
            Class2_afterFiltring_val=Class2_afterFiltringResam_val

        else:
            Class1_afterFiltring_val = Class1_afterFiltringResam_val
            Class2_afterFiltring_val = Class2_afterFiltringResam_val
        print("\nREMOVE DC COMPONENT IS DONE !!!!!\n")
        ####Normalize all ######
        for indexArr1, indexArr2, newArrC1, newArrC2 in zip(Class1_afterFiltring_val, Class2_afterFiltring_val,
                                                            Class1_afterFiltringResam_val,Class2_afterFiltringResam_val):
            newArrC1 = normalize(indexArr1)
            newArrC2 = normalize(indexArr2)
        Class1_afterFiltring_val = Class1_afterFiltringResam_val
        Class2_afterFiltring_val = Class2_afterFiltringResam_val
        # i = 1
        # for index, arr in enumerate(Class1_afterFiltring_val):
        #     for j in Class1_afterFiltring_indx:
        #         filename = f"class1_segment_{i}_normalized.txt"
        #         with open(filename, 'a') as file:
        #             file.write(f"{j} {arr[index]}\n")
        #     i += 1
        #
        # i = 1
        # for index, arr in enumerate(Class2_afterFiltring_val):
        #     for j in Class1_afterFiltring_indx:
        #         filename = f"class2_segment_{i}_normalized.txt"
        #         with open(filename, 'a') as file:
        #             file.write(f"{j} {arr[index]}\n")
        #     i += 1
        print("\nNORMALIZATION IS DONE !!!!!\n")
        ### auto correlation ######
        for indexArr1, indexArr2, newArrC1, newArrC2 in zip(Class1_afterFiltring_val, Class2_afterFiltring_val,
                                                            Class1_afterFiltringResam_val,Class2_afterFiltringResam_val):
            newArrC1 = auto_correlation(indexArr1,indexArr1)
            newArrC2 = auto_correlation(indexArr2,indexArr2)
        Class1_afterFiltring_val = Class1_afterFiltringResam_val
        Class2_afterFiltring_val = Class2_afterFiltringResam_val
        print("\nAUTO CORRELATION IS DONE !!!!!\n")
        ######compute DCT #########
        for indexArr1, indexArr2, newArrC1, newArrC2 in zip(Class1_afterFiltring_val, Class2_afterFiltring_val,
                                                            Class1_afterFiltringResam_val,Class2_afterFiltringResam_val):
            newArrC1 = dct1d(indexArr1)
            newArrC2 = dct1d(indexArr2)
        Class1_afterFiltring_val = Class1_afterFiltringResam_val
        Class2_afterFiltring_val = Class2_afterFiltringResam_val
        print("\nDCT IS DONE !!!!!\n")
        #### for tempalte matching ###
        Class1,Class2=[],[]
        Class1=aggregate_samples(Class1_afterFiltring_val)
        Class2=aggregate_samples(Class2_afterFiltring_val)
        Class1_list = Class1.tolist()
        newClass1 = Class1_list[:2500]
        Class2_list = Class2.tolist()
        newClass2 = Class2_list[:2500]
        print(Class1,"\n\n\n\n")
        print(Class2, "\n\n\n\n")
        decide_correlation(newClass1,newClass2)
                ################# GUI ####################
def on_checkbox_clicked():
    global Filter_type
    if bandPass_var.get():
        Filter_type = "bandPass"

    if bandReject_var.get():
        Filter_type = "bandReject"



myframe = tk.Tk()
myframe.geometry("900x600")
myframe.title("ECG Signal Processing")
myframe.configure(bg="#EBE3D5")

# Sampling Frequency Entry and Label
sampling_frequency_label = tk.Label(myframe, text="Sampling Frequency(HZ):")
sampling_frequency_label.configure(font=("Arial", 12, "bold"), fg="#053B50", bg="#EBE3D5")
sampling_frequency_label.place(relx=0.194, rely=0.1, anchor=tk.CENTER)
sampling_frequency_entry = tk.Entry(myframe)
sampling_frequency_entry.configure(font=("Arial", 12, "bold"))
sampling_frequency_entry.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

# Stop Attenuation Entry and Label
stop_attenuation_label = tk.Label(myframe, text="Stop Attenuation:")
stop_attenuation_label.configure(font=("Arial", 12, "bold"), fg="#053B50", bg="#EBE3D5")
stop_attenuation_label.place(relx=0.16, rely=0.2, anchor=tk.CENTER)
stop_attenuation_entry = tk.Entry(myframe)
stop_attenuation_entry.configure(font=("Arial", 12, "bold"))
stop_attenuation_entry.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

# Transition Band Entry and Label
transition_band_label = tk.Label(myframe, text="Transition Band:")
transition_band_label.configure(font=("Arial", 12, "bold"), fg="#053B50", bg="#EBE3D5")
transition_band_label.place(relx=0.16, rely=0.3, anchor=tk.CENTER)
transition_band_entry = tk.Entry(myframe)
transition_band_entry.configure(font=("Arial", 12, "bold"))
transition_band_entry.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

# Mini Frequency Entry and Label
Mini_frequency_label = tk.Label(myframe, text="Mini Frequency(HZ):")
Mini_frequency_label.configure(font=("Arial", 12, "bold"), fg="#053B50", bg="#EBE3D5")
Mini_frequency_label.place(relx=0.175, rely=0.4, anchor=tk.CENTER)
Mini_frequency_entry = tk.Entry(myframe)
Mini_frequency_entry.configure(font=("Arial", 12, "bold"))
Mini_frequency_entry.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

# Max Frequency Entry and Label
Max_frequency_label = tk.Label(myframe, text="Max Frequency(HZ):")
Max_frequency_label.configure(font=("Arial", 12, "bold"), fg="#053B50", bg="#EBE3D5")
Max_frequency_label.place(relx=0.175, rely=0.5, anchor=tk.CENTER)
Max_frequency_entry = tk.Entry(myframe)
Max_frequency_entry.configure(font=("Arial", 12, "bold"))
Max_frequency_entry.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# NewFs Frequency Entry and Label
NewFs_label = tk.Label(myframe, text="New Frequency(HZ):")
NewFs_label.configure(font=("Arial", 12, "bold"), fg="#053B50", bg="#EBE3D5")
NewFs_label.place(relx=0.175, rely=0.6, anchor=tk.CENTER)
NewFs_entry = tk.Entry(myframe)
NewFs_entry.configure(font=("Arial", 12, "bold"))
NewFs_entry.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

# Cutoff frequency Entry and Label
CutoffFrequency_label = tk.Label(myframe, text="Cutoff Frequency:")
CutoffFrequency_label.configure(font=("Arial", 12, "bold"), fg="#053B50", bg="#EBE3D5")
CutoffFrequency_label.place(relx=0.17, rely=0.7, anchor=tk.CENTER)
CutoffFrequency_entry = tk.Entry(myframe)
CutoffFrequency_entry.configure(font=("Arial", 12, "bold"))
CutoffFrequency_entry.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

# choose filter type
bandPass_var = tk.BooleanVar()
bandReject_var = tk.BooleanVar()
bandPass_checkbox = tk.Checkbutton(
    myframe, text="BAND PASS FILTER", variable=bandPass_var, command=on_checkbox_clicked
)
bandReject_checkbox = tk.Checkbutton(
   myframe, text="BAND REJECT FILTER", variable=bandReject_var, command=on_checkbox_clicked
)

bandPass_checkbox.configure(font=("Arial", 11, "bold"), fg="#053B50", bg="#EBE3D5")
bandPass_checkbox.place(relx=0.055, rely=0.8)
bandReject_checkbox.configure(font=("Arial", 11, "bold"), fg="#053B50", bg="#EBE3D5")
bandReject_checkbox.place(relx=0.4, rely=0.8)

# Class A
class1_button = tk.Button(myframe, text="Open Class A Folder", command=open_class1_folder, font=("Arial", 12, "bold"), bg="#EBE3D5", fg="#053B50")
class1_button.place(relx=0.2, rely=0.9, anchor=tk.CENTER)
# Class B
class2_button = tk.Button(myframe, text="Open Class B Folder", command=open_class2_folder, font=("Arial", 12, "bold"), bg="#EBE3D5", fg="#053B50")
class2_button.place(relx=0.5, rely=0.9, anchor=tk.CENTER)
test1_button = tk.Button(myframe, text="Open test 1 file", command=open_test_file1, font=("Arial", 12, "bold"), bg="#EBE3D5", fg="#053B50")
test1_button.place(relx=0.75, rely=0.3, anchor=tk.CENTER)
test2_button = tk.Button(myframe, text="Open test 2 file", command=open_test_file2, font=("Arial", 12, "bold"), bg="#EBE3D5", fg="#053B50")
test2_button.place(relx=0.75, rely=0.5, anchor=tk.CENTER)
# Run Processes
calculate_button = tk.Button(myframe, text="Process Signals", command=Apply_Process, font=("Arial", 12, "bold"), bg="#EBE3D5", fg="#053B50")
calculate_button.place(relx=0.8, rely=0.9, anchor=tk.CENTER)

myframe.mainloop()

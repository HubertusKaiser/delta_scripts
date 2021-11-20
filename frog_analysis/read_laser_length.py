import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os


def read_folders(local_path):
    shirp_list = ()
    for i in os.listdir(local_path):
        shirp_list = np.append(shirp_list,i)
    return shirp_list



def get_names(local_path,arg_folderlist):
    write_file = open("temporal_plus_i.txt", "w+")
    for i in arg_folderlist:
        frog_error=temporal=spectral=timebandwidthproduct=timebandwidthproduct_err=()
        opened_folder_names=()
        print(i,"i")
        opened_folder_names=os.listdir(local_path+i)
        for j in opened_folder_names:
            open_file_names=os.listdir(local_path+i+str("/")+j)
            for string in open_file_names:
                if substring in string:
                    datContent = [i.strip().split() for i in open(local_path + i + str("/") + j + str("/") + string)]
                    frog_error=np.append(float(datContent[1][3].replace(",",".")),frog_error)
                    temporal=np.append(float(datContent[2][2].replace(",",".")), temporal)
                    spectral=np.append(float(datContent[3][2].replace(",",".")), spectral)
                    timebandwidthproduct=np.append(float(datContent[4][3].replace(",",".")),timebandwidthproduct)
                    timebandwidthproduct_err=np.append(float(datContent[5][3].replace(",",".")),timebandwidthproduct_err)
        write_file.write(i+str(",")+str(np.sum(temporal)/len(temporal))+str(",")+str(np.std(temporal))+"\n")
    
    return datContent

local_path="C:/Users/Hubertus/Documents/GitHub/optics/frog_analysis/Frogmessungen_17.09.2021v2/chirp_series/"
substring="_Frog.dat"

shirps = read_folders(local_path=local_path)
everything_from_data=get_names(local_path=local_path, arg_folderlist=shirps)


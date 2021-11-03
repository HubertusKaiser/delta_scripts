# -*- coding: utf-8 -*-
"""
Created on Tue Sep  7 15:49:52 2021

@author: arjun
"""

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os
from scipy.optimize import curve_fit

def gaussian(x,amp,mean,std):
    return (amp/np.sqrt(2*np.pi)/std)*np.exp(-(x - mean)**2/(2*std**2))

#Changing the working directory
os.chdir(r'C:\Users\NewUser\OneDrive - Technische Universität Dortmund\DELTA\CHG_Spectra_measurements\2021-10-28-chg\400nm\grating1')
pwd=os.getcwd()
#print(pwd)

N_sample= 700#len(os.listdir(pwd+'/28.395')) #Total No.of spectra taken
im_i=list(range(1,N_sample+1))
columns = 3
rows = 3
I=np.linspace(1,max(im_i),len(im_i))
r56=(0.2e-3 *I**2)+ (46e-3* I) +2.59 #e-3

###This section is to fit the central peak to the central wavelength and calibrate the wavelength axis
m=3.66466753e-02 #slope of pixel to wavelength relation
wl_0= 400 #central wavelength in nm
im = Image.open('28.395/andor_X300.tif') #open the file with the optimal spectra
pix=np.array(im)[100] 
pix=pix-np.mean(pix[-10:])
pix=pix/max(pix)
lim=[0,512]
ydata=pix[lim[0]:lim[1]]
xdata=np.array(list(range(lim[0],lim[1])))
pars, cov = curve_fit(f=gaussian,xdata=xdata,ydata=ydata,p0=[1,600,50])
x = np.linspace(0,512, 1024)
y = gaussian(x,pars[0],pars[1],pars[2])
plt.plot(x, y)
plt.plot(xdata, ydata)
spec=m*(xdata-pars[1])+wl_0


dir_list=os.listdir(pwd)[:9] #selecting folders with spectra data
fig=plt.figure()
fig.suptitle("Spectra for different compressor settings")
fig_i=1
bg_all=[]
for dirct in dir_list:
    fname=dirct[-7:]
    print("Reading Folder "+fname)
    os.chdir(pwd+"/"+dirct)
    heatmap,heatmap_norm=[],[]
    bg=[]
    for i in im_i:
        im = Image.open('andor_X'+str(i)+'.tif')
        imarray=np.array(im) 
        bg.append(np.mean(imarray[-10:,-10:]))
        imarray=imarray-np.mean(imarray[-10:,-10:]) #Subtracting background 
        imsum=np.sum(imarray,axis=0) #[130:380] #Summing only the illuminated rows of pixels
        imsum_norm=imsum/max(imsum)
        heatmap.append(imsum)
        heatmap_norm.append(imsum_norm)
    np.save(pwd+"\\Processed\\"+fname+"_normalized",heatmap_norm)
    #np.save(pwd+"\\Processed\\"+fname,heatmap)
    fig.add_subplot(rows, columns, fig_i)
    plt.contourf(spec,r56,heatmap,levels=100)

    if fig_i%columns==1:
        plt.ylabel('R56  ($\mu m$)')
    if fig_i/columns>rows-1:
        plt.xlabel('Wavelength (nm)')
    
    plt.title(fname,loc='right',fontsize=9)
    
    fig_i+=1
    bg_all.append(bg)
plt.show()

os.chdir(pwd)
fig=plt.figure()
fig.suptitle("Spectra for different compressor settings (Normalized)")
fig_i=1
for dirct in dir_list:
    fname=dirct[-7:]
    imarray=np.load("Processed\\"+fname+"_normalized.npy")
    fig.add_subplot(rows, columns, fig_i)
    plt.contourf(spec,r56,imarray,levels=100)
    
    if fig_i%columns==1:
        plt.ylabel('R56  ($\mu m$)')
    if fig_i/columns>rows-1:
        plt.xlabel('Wavelength (nm)')
    
    plt.title(fname,loc='right',fontsize=9)
    fig_i+=1
    
os.chdir(dname)
    

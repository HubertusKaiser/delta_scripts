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

### Multiple plots
#Changing the working directory to the source directory
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
data_dir="mod_rad_timescan_300A"  #Name of the directory that contains the spectra
os.chdir(dname+"/"+data_dir)
pwd=os.getcwd()
#print(pwd)
timescan= True

def gaussian(x,amp,mean,std):
    return (amp/np.sqrt(2*np.pi)/std)*np.exp(-(x - mean)**2/(2*std**2))


N_sample= len(os.listdir()) #Total No.of spectra taken
sample_rate= 2 #No.of spectra taken per second
im_i=list(range(1,N_sample+1))
I=np.linspace(1,max(im_i),len(im_i))
r56=(0.2e-3 *I**2)+ (46e-3* I) +2.59 #e-3

###To set the prominent peak to 400 nm and calibrate the wavelength scale
m=3.66466753e-02  #slope of pixel to wavelength relation
im = Image.open('andor_X300.tif')
pix=np.array(im)[100]
pix=pix-np.mean(pix[-10:])
pix=pix/max(pix)
lim=[0,1024]
ydata=pix[lim[0]:lim[1]]
xdata=np.array(list(range(lim[0],lim[1])))
pars, cov = curve_fit(f=gaussian,xdata=xdata,ydata=ydata,p0=[1,600,50])
x = np.linspace(0,1024, 1024)
y = gaussian(x,pars[0],pars[1],pars[2])
plt.plot(x, y)
plt.plot(pix)
spec=m*(xdata-pars[1])+400


fig=plt.figure()

heatmap,heatmap_norm=[],[]
for i in im_i:
    im = Image.open('andor_X'+str(i)+'.tif')
    imarray=np.array(im)
    imarray=imarray-np.mean(imarray[-10:,-10:]) #Subtracting background 
    imsum=np.sum(imarray,axis=0) #Summing only the illuminated rows of pixels
    imsum_norm=imsum/max(imsum)
    heatmap.append(imsum)
    heatmap_norm.append(imsum_norm)
    
    np.save("../Processed/mod_rad_timescan_normalized",heatmap)
    np.save("../Processed/mod_rad_timescan",heatmap)

if timescan:
    plt.contourf(spec,I/sample_rate,heatmap,levels=100)
    plt.ylabel('Time (s)')
    plt.xlabel('Wavelength (nm)')
    plt.figure()
    plt.contourf(spec,I/sample_rate,heatmap_norm,levels=100)
    plt.ylabel('Time (s)')
else:
    plt.contourf(spec,r56,heatmap,levels=100)
    plt.ylabel('R56  ($\mu m$)')
    plt.xlabel('Wavelength (nm)')
    plt.figure()
    plt.contourf(spec,r56,heatmap_norm,levels=100)
    plt.ylabel('R56  ($\mu m$)')
plt.xlabel('Wavelength (nm)')


os.chdir(dname)
   

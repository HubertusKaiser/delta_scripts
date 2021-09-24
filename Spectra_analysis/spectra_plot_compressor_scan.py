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

#Changing the working directory to the source directory
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
pwd=os.getcwd()
#print(pwd)

N_sample= len(os.listdir(pwd+'/28.397')) #Total No.of spectra taken
im_i=list(range(1,N_sample+1))
columns = 3
rows = 3
I=np.linspace(1,max(im_i),len(im_i))
r56=(0.2e-3 *I**2)+ (46e-3* I) +2.59 #e-3


m=3.66466753e-02 #slope of pixel to wavelength relation
im = Image.open('28.397/andor_X300.tif')
pix=np.array(im)[100]
pix=pix-np.mean(pix[-10:])
pix=pix/max(pix)
lim=[0,1024]
ydata=pix[lim[0]:lim[1]]
xdata=np.array(list(range(lim[0],lim[1])))
pars, cov = curve_fit(f=gaussian,xdata=xdata,ydata=ydata,p0=[1,600,50])
x = np.linspace(0,1024, 1024)
y = gaussian(x,pars[0],pars[1],pars[2])
#plt.plot(x, y)
spec=m*(xdata-pars[1])+400


dir_list=os.listdir(pwd)[:9] #selecting folders with spectra data
fig=plt.figure()
fig_i=1

for dirct in dir_list:
    fname=dirct[-7:]
    print("Reading Folder "+fname)
    os.chdir(pwd+"/"+dirct)
    heatmap,heatmap_norm=[],[]
    
    for i in im_i:
        im = Image.open('andor_X'+str(i)+'.tif')
        imarray=np.array(im)
        imarray=imarray-np.mean(imarray[-10:,-10:]) #Subtracting background 
        imsum=np.sum(imarray,axis=0) #Summing only the illuminated rows of pixels
        imsum_norm=imsum/max(imsum)
        heatmap.append(imsum)
        heatmap_norm.append(imsum_norm)
    np.save(pwd+"\\Processed\\"+fname+"_normalized",heatmap_norm)
    np.save(pwd+"\\Processed\\"+fname,heatmap)
    fig.add_subplot(rows, columns, fig_i)
    plt.contourf(spec,r56,heatmap_norm,levels=100)

    if fig_i%columns==1:
        plt.ylabel('R56  ($\mu m$)')
    if fig_i/columns>rows-1:
        plt.xlabel('Wavelength (nm)')
    
    plt.title(fname,loc='right',fontsize=9)
    
    fig_i+=1


os.chdir(dname)
    

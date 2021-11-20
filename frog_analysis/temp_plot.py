import numpy as np
import matplotlib.pyplot as plt

data=np.genfromtxt("temporal_plus_i.txt", delimiter=",")
x=data[:,0]
y=data[:,1]
err=data[:,2]

plt.errorbar(x,y,yerr=err,fmt=".g",elinewidth=1,capsize=7,markersize=10)
plt.ylabel("pluse length (fs)")
plt.xlabel("compressor length (mm)")
plt.grid()
plt.xticks(rotation=-45)
plt.savefig("tempvschirp.pdf")
plt.legend()
plt.show()

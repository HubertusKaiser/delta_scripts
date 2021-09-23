import numpy as np
import matplotlib.pyplot as plt

data=np.genfromtxt("temporal_plus_i.txt", delimiter=",")
y=data[:,0]
x=data[:,1]

plt.plot(x,y, ".g", label="pulse length")
plt.ylabel("pluse length")
plt.xlabel("grating_dist")
plt.grid()
plt.xticks(rotation=-45)
plt.savefig("tempvschirp.pdf")
plt.legend()
plt.show()
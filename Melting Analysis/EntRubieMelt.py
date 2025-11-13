import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from matplotlib.gridspec import GridSpec
import gc

#USER INPUTS_________________________________________________________________

gamma =            #Impactor to target mass ratio (needed for naming plots and accessing files)
angle =            #Impact angle (needed for naming (needed for naming plots)
time =             #Time you are analyzing the melting at
ncores =           #Number of cores used in the simulation
path =             #Path to data files
outputpath =       #Output file path for the plots
r0 = 1e6           #Unit of length for the spatial axes (default is 1e6 m)
axesscale = 9      #Length of each axis in units of r0 (default is 9 r0)

#USER INPUTS_________________________________________________________________

secondstime=time*100
meltedparticles=[]
xmlist=[]
ymlist=[]
xlist=[]
ylist=[]
otherxlist=[]
otherylist=[]

masslist=[]
x=[]
y=[]
z=[]

entcounter=0
rubiecounter=0

print()
with open(f"{path}changes{gamma}.txt","r") as file:
    mantcounter=0
    for line in file:
        elements=line.split()
        ID=elements[0]
        tag=int(elements[1])
        mass=float(elements[2])
        xx=float(elements[3])/r0
        yy=float(elements[4])/r0
        zz=float(elements[5])/r0
        entchange=float(elements[13])

        if tag == 0:

            mantcounter=mantcounter+1

            if mantcounter % 100000 == 0:
                print(f"Mantle Particle Number: {mantcounter}")

            if entchange >= 500:
            
                entcounter=entcounter+1

                if -0.4 < zz < 0.4:

                    xmlist.append(xx)
                    ymlist.append(yy)

            else:

                if -0.4 < zz < 0.4:

                    xlist.append(xx)
                    ylist.append(yy)

        else:

            if -0.4 < zz < 0.4:

                otherxlist.append(xx)
                otherylist.append(yy)

        if tag == 1:

            x.append(xx)
            y.append(yy)
            z.append(zz)
            masslist.append(mass)

x=np.array(x)
y=np.array(y)
z=np.array(z)
masslist=np.array(masslist)

xcm=(np.sum(x*masslist))/np.sum(masslist)
ycm=(np.sum(y*masslist))/np.sum(masslist)
zcm=(np.sum(z*masslist))/np.sum(masslist)       

xlist=np.array(xlist)-xcm
ylist=np.array(ylist)-ycm
xmlist=np.array(xmlist)-xcm
ymlist=np.array(ymlist)-ycm
otherxlist=np.array(otherxlist)-xcm
otherylist=np.array(otherylist)-ycm

fig,ax=plt.subplots(figsize=(8,6))
gs=GridSpec(1,2,width_ratios=[20,0.5],figure=fig)
norm=plt.Normalize(0, 500)
scatter=ax.scatter(xlist, ylist, c='blue', s=1.7, marker='.')
scatter2=ax.scatter(xmlist,ymlist,c='red',s=1.7,marker='.')
ax.set_aspect('equal')

ax.set_xlabel("x (1e6 m)")
ax.set_ylabel("y (1e6 m)")

ticks=np.linspace(-axesscale,axesscale,9)

ax.set_xticks(ticks)
ax.set_yticks(ticks)

ax.set_xlim(-axesscale,axesscale)
ax.set_ylim(-axesscale,axesscale)

ax.set_title(f"Visualization of Entropy Melting, t={time*100} s,\n"+ 
            fr"$\gamma={gamma}$, ${angle}^o$",
            multialignment='center')

print(f"\nOutputted EntropyMelt.png\n")
plt.savefig(f"{outputpath}EntropyMelt.png",dpi=300)
plt.close(fig)
#plt.show()

xtmlist=[]
ytmlist=[]
xtlist=[]
ytlist=[]
otherxlist=[]
otherylist=[]

for i in range(ncores):
    print(f"results.{time:05d}_{ncores:05d}_{i:05d}.dat")
    with open(f"{path}results.{time:05d}_{ncores:05d}_{i:05d}.dat","r") as file:
        file.readline()
        file.readline()
        for line in file:
            elements=line.split()
            ID = int(elements[0])
            tag = int(elements[1])
            mass = float(elements[2])
            xx = float(elements[3])/r0 
            yy = float(elements[4])/r0
            zz = float(elements[5])/r0
            density=float(elements[9])
            energy=float(elements[10])
            pressure=float(elements[11])
            entropy = float(elements[13])
            temperature = float(elements[14])

            if pressure*1e-9 < 24.0: #Rubie et al., (2015) melt model
                Tmelt = (1874.0 + 55.43 * pressure * 1e-9 - 1.74 * (pressure * 1e-9)**2.0  + 0.0193 * (pressure * 1e-9)**3.0) 
    
            else:    
                Tmelt = (1249.0 + 58.28 * pressure * 1e-9 - 0.395 * (pressure * 1e-9)**2.0  + 0.011 * (pressure * 1e-9)**3.0) 

            if tag == 0:
                
                if temperature > Tmelt:

                    rubiecounter=rubiecounter+1

                if -0.4 < zz < 0.4:

                    if temperature > Tmelt:

                        xtmlist.append(xx-xcm)
                        ytmlist.append(yy-ycm)
                        
                    else:

                        xtlist.append(xx-xcm)
                        ytlist.append(yy-ycm)

            else:

                if -0.4 < zz < 0.4:

                    otherxlist.append(xx-xcm)
                    otherylist.append(yy-ycm)

fig,ax=plt.subplots(figsize=(8,6))
gs=GridSpec(1,2,width_ratios=[20,0.5],figure=fig)
norm=plt.Normalize(0, 500)
scatter=ax.scatter(xlist, ylist, c='blue', s=1.7, marker='.')
scatter2=ax.scatter(xtmlist,ytmlist,c='red',s=1.7,marker='.')
ax.set_aspect('equal')

ax.set_xlabel("x (1e6 m)")
ax.set_ylabel("y (1e6 m)")

ticks=np.linspace(-axesscale,axesscale,9)

ax.set_xticks(ticks)
ax.set_yticks(ticks)

ax.set_xlim(-axesscale,axesscale)
ax.set_ylim(-axesscale,axesscale)

ax.set_title(f"Visualization of Rubie Model Melting, t={time*100} s,\n"+ 
            fr"$\gamma={gamma}$, ${angle}^o$",
            multialignment='center')

print(f"\nOutputted RubieMelt.png\n")
plt.savefig(f"{outputpath}RubieMelt.png",dpi=300)
plt.close(fig)

print(f"The total number of mantle particles is: {mantcounter}")
print(f"The total number of melted mantle particles (Rubie Model) is: {rubiecounter} ")
print(f"The total number of melted mantle particles (Entropy Model) is: {entcounter}\n")






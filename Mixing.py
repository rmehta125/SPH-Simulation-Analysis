import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import numpy as np

#USER INPUTS ---------------------------------------------

path = r"/home/theia/roshanm125/FinalMeltScalingCollisions/Collisions/0.03/90Deg/"
outputpath =r"/home/theia/roshanm125/FinalMeltScalingCollisions/Collisions/0.03/90Deg/"
ncores = 100
outputnumber1 = 370
outputnumber2 = 370
axesdim = 15
axesscale = 1e6
particlesize = 1

tarcorecolor = "gray"
impcorecolor = "crimson"


#---------------------------------------------------------

f=open(f"{outputpath}InEarthMant.txt",'w')

for j in range(outputnumber1,outputnumber2+1):

    xlist=[]
    ylist=[]
    zlist=[]

    xtarmant=[]
    ytarmant=[]
    ztarmant=[]

    xtarcore=[]
    ytarcore=[]
    ztarcore=[]

    ximpmant=[]
    yimpmant=[]
    zimpmant=[]

    ximpcore=[]
    yimpcore=[]
    zimpcore=[]

    specialx=[]
    specialy=[]
    specialz=[]

    for i in range(ncores):

        filename=f"{path}/results.{j:05d}_{ncores:05d}_{i:05d}.dat"

        with open (filename, "r") as file:
            timevalue=float(file.readline().strip())
            file.readline()
        
            for line in file:
                elements=line.split()
                tag=int(elements[1])
                xx = float(elements[3])/axesscale
                yy = float(elements[4])/axesscale
                zz = float(elements[5])/axesscale

                if tag == 1:

                    xtarcore.append(xx)
                    ytarcore.append(yy)
                    ztarcore.append(zz) 

    xcm=np.mean(np.array(xtarcore))
    ycm=np.mean(np.array(ytarcore))
    zcm=np.mean(np.array(ztarcore))

    xtarcore=[]
    ytarcore=[]
    ztarcore=[]

    for i in range(ncores):

        filename=f"{path}/results.{j:05d}_{ncores:05d}_{i:05d}.dat"

        with open (filename, "r") as file:
            timevalue=float(file.readline().strip())
            file.readline()
        
            for line in file:
                elements=line.split()
                tag=int(elements[1])
                xx = (float(elements[3])/axesscale)-xcm
                yy = (float(elements[4])/axesscale)-ycm
                zz = (float(elements[5])/axesscale)-zcm

                if tag == 1:

                    xtarcore.append(xx)
                    ytarcore.append(yy)
                    ztarcore.append(zz)

                if tag == 2:

                    ximpmant.append(xx)
                    yimpmant.append(yy)
                    zimpmant.append(zz)

                if tag == 3:

                    if 3.45 < np.sqrt((xx)**2+(yy)**2+(zz)**2)<7.5:

                        specialx.append(xx)
                        specialy.append(yy)
                        specialz.append(zz)

                    else:

                        ximpcore.append(xx)
                        yimpcore.append(yy)
                        zimpcore.append(zz)

    fig,ax=plt.subplots(figsize=(7,6))

    ax.scatter(specialx,specialy,c='blue',marker='.',s=particlesize)       
    ax.scatter(xtarcore,ytarcore,c=tarcorecolor,marker='.',s=particlesize)
    ax.scatter(ximpcore,yimpcore,c=impcorecolor,marker='.',s=particlesize)

    ax.set_xlabel(f"x ({axesscale:.0e} m)")
    ax.set_ylabel(f"y ({axesscale:.0e} m)")

    ticks=np.linspace(-axesdim/2,axesdim/2,5)
    ax.set_xticks(ticks)
    ax.set_yticks(ticks)

    ax.set_xlim(-axesdim/2,axesdim/2)
    ax.set_ylim(-axesdim/2,axesdim/2)

    title = ax.set_title(f"Projection Visualization at t={timevalue:.2e} s")

    pos = ax.get_position()
    title.set_position([0.5, 1.02])
    ax.set_aspect('equal')

    plt.savefig(f"{outputpath}/snap_{j:05d}.png", dpi=300)
    print(f"Outputted snap_{j:05d}.png")

    print(f"The number of core particles in the mantle is: {len(specialx)}")
    print(f"The total number of impactor core particles is: {len(specialx)+len(ximpcore)}")
    print()
    f.write("{} {}\n".format(j,len(specialx)/(len(specialx)+len(ximpcore))))
    plt.close()
f.close()








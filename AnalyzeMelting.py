import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from matplotlib.gridspec import GridSpec
from collections import namedtuple
import gc

#USER INPUTS_________________________________________________________________

gamma=0.3
angle=45
outputnumber=1200
ncores=150
path=r"C:\Users\nakaj\OneDrive\Desktop\2025Work\MeltScalingCollisions\FinalCollisions\0.3\60Deg\\"
outputpath=path
axesdim=18
cutoff='No'

#____________________________________________________________________________

r0=1e6

def melting():  #Determines which particles are melted

    print("\nAnalyzing melting...\n")

    xmlist=[]
    ymlist=[]
    xlist=[]
    ylist=[]
    melted=0
    total=0

    with open(f'{path}/SortedData.txt','r') as file:

        timevalue=float(file.readline())
        num=float(file.readline())
        radius=float(file.readline())
        mass=float(file.readline())
        cms=file.readline().split()
        xcm,ycm,zcm=float(cms[0]),float(cms[1]),float(cms[2])

        k=0
        percent=0

        for line in file:

            elements=line.split()
            tag=int(elements[1])
            fate=int(elements[15])

            if tag == 0 or tag == 2:

                if fate != 2:

                    xx=((float(elements[3]))-xcm)/r0
                    yy=((float(elements[4]))-ycm)/r0
                    zz=((float(elements[5]))-zcm)/r0
                    pressure=float(elements[11])
                    temperature = float(elements[14])

                    total=total+1

                    if pressure*1e-9 < 24.0: #Melting criteria from Rubie et al., (2015)

                        Tmelt=(1874.0 + 55.43 * pressure*1e-9 - 1.74 * (pressure*1e-9)**2.0  + 0.0193 * (pressure*1e-9)**3.0) 
            
                    else:    

                        Tmelt=(1249.0 + 58.28 * pressure*1e-9 - 0.395 * (pressure*1e-9)**2.0  + 0.011 * (pressure*1e-9)**3.0) 

                    if temperature > Tmelt:

                        melted=melted+1

                    if -0.4 < zz < 0.4:

                        if temperature > Tmelt:

                            xmlist.append(xx)
                            ymlist.append(yy)
                            
                        else:

                            xlist.append(xx)
                            ylist.append(yy)

            if k%((num-1)//10) == 0:

                print(f"    {percent}% complete")

                percent=percent+10

            k=k+1

    meltfrac=round((melted/total)*100,2)

    print(f"\n    The total number of melted mantle particles is: {melted} ")
    print(f"    The total number of mantle particles is: {total}")
    print(f"    The melt mass fraction is: {meltfrac}%\n")

    return xlist,ylist,xmlist,ymlist,meltfrac,timevalue



def plotting(xlist,ylist,xmlist,ymlist,meltfrac,timevalue): #Generates a plot of the melting distribution

    print("Plotting the mantle melt...\n")

    plt.figure(figsize=(8,6))
    plt.scatter(xlist, ylist, c='blue', s=1.7, marker='.')
    plt.scatter(xmlist,ymlist,c='red',s=1.7,marker='.')
    plt.gca().set_aspect('equal', adjustable='box')
    plt.xlabel("x (1e6 m)")
    plt.ylabel("y (1e6 m)")
    ticks=np.linspace(-axesdim,axesdim,9)
    plt.xticks(ticks)
    plt.yticks(ticks)
    plt.xlim(-axesdim,axesdim)
    plt.ylim(-axesdim,axesdim)
    hour=round((((timevalue)//10)*10)/3600,2)
    plt.title(f"Visualization of Melting, t={hour} hrs,\n"+ 
                fr"$\gamma={gamma}$, ${angle}^o$",
                multialignment='center')
    plt.text(0.98, 0.02, f"Melting %: {meltfrac}", transform=plt.gca().transAxes, ha='right', va='bottom', fontsize=10, 
             bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))
    plt.savefig(f"{outputpath}/Melting_{outputnumber}.png",dpi=300)
    plt.close()

    print(f"    Outputted Melting_{outputnumber}.png\n")



def main():

    xlist,ylist,xmlist,ymlist,meltfrac,timevalue=melting()
    plotting(xlist,ylist,xmlist,ymlist,meltfrac,timevalue)



main()

import matplotlib.pyplot as plt
import numpy as np
from collections import namedtuple

#USER INPUTS_________________________________________________________________

type = "Body"       #Type of file, type "Collision" for collision files or "Body" for body files
path=r"c:\Users\nakaj\OneDrive\Desktop\2025Work\MeltScalingCollisions\Impactors\0.01\\"     #Path to data files
ncores=25       #Number of cores used in the simulation
time=10     #Time you are analyzing the radii/escape velocity at

#____________________________________________________________________________

if type == "Collision":

    implist=[]
    tarlist=[]
    impmasslist=[]
    tarmasslist=[]

    xi=[]
    yi=[]
    zi=[]
    massi=[]
    xt=[]
    yt=[]
    zt=[]
    masst=[]

    print("\nFinding Centers of Mass...\n")
    for i in range(ncores):
        file = f"{path}results.{time:05d}_{ncores:05d}_{i:05d}"+".dat"
        with open(file, "r") as file:
            file.readline()
            file.readline()
            for line in file:
                elements=line.split()
                ID = int(elements[0])
                tag = int(elements[1])
                mass = float(elements[2])
                xx = float(elements[3]) 
                yy = float(elements[4])
                zz = float(elements[5])

                if tag == 1 or tag == 0:
                    xt.append(xx)
                    yt.append(yy)
                    zt.append(zz)
                    masst.append(mass)

                if tag == 3 or tag == 2:
                    xi.append(xx)
                    yi.append(yy)
                    zi.append(zz)
                    massi.append(mass)

    xi,yi,zi,massi=np.array(xi),np.array(yi),np.array(zi),np.array(massi)
    xcmi=np.sum(xi*massi)/np.sum(massi)
    ycmi=np.sum(yi*massi)/np.sum(massi)
    zcmi=np.sum(zi*massi)/np.sum(massi)

    xt,yt,zt,masst=np.array(xt),np.array(yt),np.array(zt),np.array(masst)
    xcmt=np.sum(xt*masst)/np.sum(masst)
    ycmt=np.sum(yt*masst)/np.sum(masst)
    zcmt=np.sum(zt*masst)/np.sum(masst)

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
                xx = float(elements[3]) 
                yy = float(elements[4])
                zz = float(elements[5])
                if tag == 2 or tag == 3:
                    r=np.sqrt((xx-xcmi)**2+(yy-ycmi)**2+(zz-zcmi)**2)
                    implist.append(r)
                    impmasslist.append(mass)
                if tag == 0 or tag ==1:
                    r=np.sqrt((xx-xcmt)**2+(yy-ycmt)**2+(zz-zcmt)**2)
                    tarlist.append(r)
                    tarmasslist.append(mass)

    tarradiusmax=max(tarlist)
    impradiusmax=max(implist)
    tarmass=np.sum(tarmasslist)
    impmass=np.sum(impmasslist)
    impmasslist,tarmasslist=np.array(impmasslist),np.array(tarmasslist)
    escapevelocity=np.sqrt((2*6.67*10**(-11)*(impmass+tarmass)/(tarradiusmax+impradiusmax)))

    print(f"\nThe impactor radius (m) is: {impradiusmax}")
    print(f"The target radius (m) is {tarradiusmax}")
    print(f"The escape velocity (m/s) is {escapevelocity}\n")

if type == "Body":

    bodylist=[]
    masslist=[]

    print()
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
                xx = float(elements[3]) 
                yy = float(elements[4])
                zz = float(elements[5])
                bodylist.append(np.sqrt(xx**2+yy**2+zz**2))

    radius=max(bodylist)

    print(f"\nThe body radius (m) is: {radius}\n")
        


        

            





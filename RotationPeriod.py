import matplotlib.pyplot as plt
import numpy as np
from collections import namedtuple

#USER INPUTS_________________________________________________________________

path =        #Path to data files
ncores =      #Number of cores used in the simulation
time =        #Time you are analyzing the rotation period at

#____________________________________________________________________________

xcore=[]
ycore=[]
zcore=[]
vxcore=[]
vycore=[]
vzcore=[]
masslist=[]

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
            vx = float(elements[6])
            vy = float(elements[7])
            vz = float(elements[8])

            if tag == 1:
                xcore.append(xx)
                ycore.append(yy)
                zcore.append(zz)
                vxcore.append(vx)
                vycore.append(vy)
                vzcore.append(vz)
                masslist.append(mass)

xcore,ycore,zcore,mass=np.array(xcore),np.array(ycore),np.array(zcore),np.array(masslist)
vxcore,vycore,vzcore=np.array(vxcore),np.array(vycore),np.array(vzcore)

xcm=np.sum(xcore*masslist)/np.sum(masslist)
ycm=np.sum(ycore*masslist)/np.sum(masslist)
zcm=np.sum(zcore*masslist)/np.sum(masslist)

vxcm=np.sum(vxcore*masslist)/np.sum(masslist)
vycm=np.sum(vycore*masslist)/np.sum(masslist)
vzcm=np.sum(vzcore*masslist)/np.sum(masslist)

print("CENTER OF MASS (positions):", xcm, ycm, zcm)
print("CENTER OF MASS (velocities):", vxcm, vycm, vzcm)
print()

Lnet=np.array([0,0,0])
I=0

for i in range(ncores):
    file = f"{path}results.{time:05d}_{ncores:05d}_{i:05d}"+".dat"
    print(f"results.{time:05d}_{ncores:05d}_{i:05d}"+".dat")
    with open(f"{path}results.{time:05d}_{ncores:05d}_{i:05d}.dat","r") as file:
        file.readline()
        file.readline()
        for line in file:
            elements=line.split()
            ID = int(elements[0])
            tag = int(elements[1])
            mass = float(elements[2])
            xx = float(elements[3])-xcm 
            yy = float(elements[4])-ycm
            zz = float(elements[5])-zcm
            vx = float(elements[6])-vxcm
            vy = float(elements[7])-vycm
            vz = float(elements[8])-vzcm
            v = np.array([vx,vy,vz])
            r = np.array([xx,yy,zz])
            if np.linalg.norm(r)<=6400*10**3:
                L = mass*np.cross(r,v)
                I = I+mass*(xx**2+yy**2)
                Lnet=Lnet+L

omegaz=np.linalg.norm(Lnet)/I
periodz=(2*np.pi)/omegaz
print(f"\nThe rotation period is: {periodz/3600} hours\n")



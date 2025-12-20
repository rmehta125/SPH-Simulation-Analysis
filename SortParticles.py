import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from matplotlib.gridspec import GridSpec
from collections import namedtuple
import gc

#USER INPUTS_________________________________________________________________

outputnumber=1200
ncores=150
path=r"C:\Users\nakaj\OneDrive\Desktop\2025Work\MeltScalingCollisions\FinalCollisions\0.3\60Deg\\"
outputpath=path
xlim=20
percentile=99
iterations=10

#____________________________________________________________________________

r0=1e6
G=6.67*10**(-11)

def center_of_mass():

    x=[]
    y=[]
    z=[]
    xtotal=[]
    ytotal=[]
    ztotal=[]
    xiron=[]
    yiron=[]
    ziron=[]
    xsili=[]
    ysili=[]
    zsili=[]
    masslist=[]
    radiuslist=[]

    print("\nPlotting particle distributions...\n")

    for i in range(ncores):

        with open(f'{path}results.{outputnumber:05d}_{ncores:05d}_{i:05d}.dat','r') as file:

            file.readline()
            file.readline()

            for line in file:

                elements=line.split()
                ID=elements[0]
                tag=int(elements[1])
                mass=float(elements[2])
                xx=float(elements[3])/r0
                yy=float(elements[4])/r0
                zz=float(elements[5])/r0

                xtotal.append(xx)
                ytotal.append(yy)
                ztotal.append(zz)
                radiuslist.append(np.sqrt(xx**2+yy**2+zz**2))

                if tag == 1:

                    x.append(xx)
                    y.append(yy)
                    z.append(zz)
                    masslist.append(mass)
                
                if tag == 0 or tag == 2:

                    xsili.append(xx)
                    ysili.append(yy)
                    zsili.append(zz)

                if tag == 1 or tag == 3:

                    xiron.append(xx)
                    yiron.append(yy)
                    ziron.append(zz)

    # Compute the center of mass:

    x=np.array(x)
    y=np.array(y)
    z=np.array(z)
    masslist=np.array(masslist)

    xcm=(np.sum(x*masslist))/np.sum(masslist)
    ycm=(np.sum(y*masslist))/np.sum(masslist)
    zcm=(np.sum(z*masslist))/np.sum(masslist)  
    cms=[xcm,ycm,zcm]     

    xtotal=np.array(xtotal)-xcm
    ytotal=np.array(ytotal)-ycm
    ztotal=np.array(ztotal)-zcm
    totals=[xtotal,ytotal,ztotal]

    xiron=np.array(xiron)-xcm
    yiron=np.array(yiron)-ycm
    ziron=np.array(ziron)-zcm
    irons=[xiron,yiron,ziron]

    xsili=np.array(xsili)-xcm
    ysili=np.array(ysili)-ycm
    zsili=np.array(zsili)-zcm
    silis=[xsili,ysili,zsili]

    return cms,totals,irons,silis 



def plotdist(totals, irons, silis,xlim):

    # Plot particle distributions and determine initial guesses:

    xtotal,ytotal,ztotal=totals[0],totals[1],totals[2]
    xiron,yiron,ziron=irons[0],irons[1],irons[2]
    xsili,ysili,zsili=silis[0],silis[1],silis[2]

    radiuslist=np.sqrt(xtotal**2+ytotal**2+ztotal**2)
    ironlist=np.sqrt(xiron**2+yiron**2+ziron**2)
    sililist=np.sqrt(xsili**2+ysili**2+zsili**2)

    if xlim=='max':

        xlim=max(radiuslist)

    plt.figure(figsize=(8,5))
    plt.hist(x=sililist,bins=500,range=(0,xlim),color='blue',alpha=0.4,label='silicate')
    plt.hist(x=ironlist,bins=500,range=(0,xlim),color='red',alpha=0.4,label='iron')
    plt.xlabel(f'Radius ({r0:.1e} m)')
    plt.ylabel('Count')
    plt.title('Distribution of Iron (Yellow) and Silicate (Blue)')
    plt.legend()
    plt.show()

    radius=float(input('    Enter a guess for the planetary radius (1e6 m): '))

    return radius



def storing_data(cms,radius):

    #Compute the mass within the initial radius:

    print("\nFinding Initial Planetary Mass...\n")

    xcm,ycm,zcm=cms[0],cms[1],cms[2]
    M=0
    num=0

    for i in range(ncores):

        with open(f'{path}results.{outputnumber:05d}_{ncores:05d}_{i:05d}.dat','r') as file:

            timevalue=float(file.readline())
            num=num+int(file.readline())

            for line in file:

                elements=line.split()
                mass=float(elements[2])
                xx=float(elements[3])/r0-xcm
                yy=float(elements[4])/r0-ycm
                zz=float(elements[5])/r0-zcm
                
                if np.sqrt(xx**2+yy**2+zz**2)<=radius:

                    M=M+mass

    print("Reading and Storing Data...\n")

    particle = namedtuple('particle', ['id','tag','mass','x','y','z','r','vx','vy','vz',
                                       'v','dens','int_e','press','pot_e','ent','temp'])
    particles=[]

    for i in range(ncores):

        with open(f'{path}results.{outputnumber:05d}_{ncores:05d}_{i:05d}.dat','r') as file:

            file.readline()
            file.readline()

            for line in file:

                elements=line.split()
                ID=int(elements[0])
                tag=int(elements[1])
                mass=float(elements[2])
                xx=float(elements[3])-xcm*r0
                yy=float(elements[4])-ycm*r0
                zz=float(elements[5])-zcm*r0
                vx=float(elements[6])
                vy=float(elements[7])
                vz=float(elements[8])
                dens=float(elements[9])
                int_e=float(elements[10])
                press=float(elements[11])
                pot_e=float(elements[12])
                ent=float(elements[13])
                temp=float(elements[14])

                r=np.array([xx,yy,zz])
                v=np.array([vx,vy,vz])

                particles.append(particle(ID,tag,mass,xx,yy,zz,r,vx,vy,vz,v,dens,int_e,press,pot_e,ent,temp))

    return particles,M,timevalue,num



def iterate(iterations,radius,particles,M):

    if iterations != 0:

        print("Beginning Iterations...\n")

    radius=radius*r0

    for i in range(iterations):  

        M_new=0
        radiuslist=[]

        for particle in particles:

            rmag=np.linalg.norm(particle.r)
            vmag=np.linalg.norm(particle.v)

            E=((1/2)*(vmag)**2-(G*M)/rmag)
            a=-(G*M)/(2*E) 
            L=np.linalg.norm(np.cross(particle.r,particle.v)) 
            ecc=np.sqrt(1+((2*E*L**2)/(G*M)**2)) 
            rperi=(a*(1-ecc)) 

            if E<0 and rperi <= radius:

                M_new=M_new+particle.mass
                radiuslist.append(rmag)

        M=M_new
        radius=np.percentile(radiuslist,percentile)

        print(f"    Iteration {i+1}: R={radius:0.4e} m, M={M:0.4e} kg")

    if iterations != 0:

        print()

    print(f"    Final planetary radius: {radius:0.4e} m")
    print(f"    Final planetary mass: {M:0.4e} kg\n")

    return radius, M



def write_files(timevalue,num,radius,M,particles):

    print("Writing output file...\n")

    with open(f'{outputpath}/SortedData.txt','w') as file:

        file.write(f'{timevalue}\n{num}\n{radius}\n{M}\n')

        k=0
        percent=0

        for particle in particles:

            rmag=np.linalg.norm(particle.r)
            vmag=np.linalg.norm(particle.v)

            E=((1/2)*(vmag)**2-(G*M)/rmag)
            a=-(G*M)/(2*E) 
            L=np.linalg.norm(np.cross(particle.r,particle.v)) 
            ecc=np.sqrt(1+((2*E*L**2)/(G*M)**2)) 
            rperi=(a*(1-ecc))
            
            if E<0:

                if rperi <= radius:

                    mat=0

                else:

                    mat=1

            else:

                mat=2

            file.write(f'{particle.id}\t{particle.tag}\t{particle.mass}\t'+
                       f'{particle.x}\t{particle.y}\t{particle.z}\t{particle.vx}\t{particle.vy}\t{particle.vz}\t'+
                       f'{particle.dens}\t{particle.int_e}\t{particle.press}\t{particle.pot_e}\t'+
                       f'{particle.ent}\t{particle.temp}\t{mat}\n')
                    

            if k%((num-1)//10) == 0:

                print(f"    {percent}% complete")

                percent=percent+10

            k=k+1
    
    print("\nAll particles have been sorted in SortedData.txt\n")



def main():

    cms,totals,irons,silis=center_of_mass()
    radius=plotdist(totals, irons, silis,xlim)
    particles,M,timevalue,num=storing_data(cms,radius)
    radius,M=iterate(iterations,radius,particles,M)
    write_files(timevalue,num,radius,M,particles)



main()

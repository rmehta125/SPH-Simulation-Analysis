import matplotlib.pyplot as plt
import numpy as np
from collections import namedtuple


#USER INPUTS_________________________________________________________________

outputnumber=1200
ncores=150
path=r"C:\Users\nakaj\OneDrive\Desktop\2025Work\MeltScalingCollisions\FinalCollisions\0.3\60Deg\\"
outputpath=path
xlim=20
percentile=99
iterations=5

#____________________________________________________________________________

r0=1e6
G=6.67*10**(-11)

def center_of_mass():   #Determines the center of mass of the main planet

    print("\nDetermining center of mass and plotting particle distributions...\n")

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

    for i in range(ncores):

        with open(f'{path}/results.{outputnumber:05d}_{ncores:05d}_{i:05d}.dat','r') as file:

            file.readline()
            file.readline()

            #Store data

            for line in file:

                elements=line.split()
                ID=elements[0]
                tag=int(elements[1])
                m=float(elements[2])
                xx=float(elements[3])/r0
                yy=float(elements[4])/r0
                zz=float(elements[5])/r0

                xtotal.append(xx)
                ytotal.append(yy)
                ztotal.append(zz)
                radiuslist.append(np.sqrt(xx**2+yy**2+zz**2))

                #Sort data by tags

                if tag == 1:

                    x.append(xx)
                    y.append(yy)
                    z.append(zz)
                    masslist.append(m)
                
                if tag == 0 or tag == 2:

                    xsili.append(xx)
                    ysili.append(yy)
                    zsili.append(zz)

                if tag == 1 or tag == 3:

                    xiron.append(xx)
                    yiron.append(yy)
                    ziron.append(zz)

    #Compute the center of mass using target core particles

    x=np.array(x)
    y=np.array(y)
    z=np.array(z)
    masslist=np.array(masslist)

    xcm=(np.sum(x*masslist))/np.sum(masslist)
    ycm=(np.sum(y*masslist))/np.sum(masslist)
    zcm=(np.sum(z*masslist))/np.sum(masslist)  
    cms=[xcm,ycm,zcm]     

    #Center data by the center of mass

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



def plotdist(totals, irons, silis,xlim):    #Plots particle distributions and determines initial radius

    #Plot particle distributions

    xtotal,ytotal,ztotal=totals[0],totals[1],totals[2]
    xiron,yiron,ziron=irons[0],irons[1],irons[2]
    xsili,ysili,zsili=silis[0],silis[1],silis[2]

    radiuslist=np.sqrt(xtotal**2+ytotal**2+ztotal**2)
    ironlist=np.sqrt(xiron**2+yiron**2+ziron**2)
    sililist=np.sqrt(xsili**2+ysili**2+zsili**2)

    if xlim=='max':

        xlim=max(radiuslist)

    plt.figure(figsize=(8,5))
    plt.hist(x=sililist,bins=500,range=(0,xlim),color='blue',alpha=0.4,label='Silicate')
    plt.hist(x=ironlist,bins=500,range=(0,xlim),color='red',alpha=0.4,label='Iron')
    plt.xlabel(f'Radius ({r0:.1e} m)')
    plt.ylabel('Count')
    plt.title('Distribution of Iron and Silicate')
    plt.legend()
    plt.show()

    #Determine initial guess for the radius

    radius=float(input('    Enter a guess for the planetary radius (1e6 m): '))

    return radius



def storing_data(cms,radius):   #Reads particle data, centers it, and stores it

    #Compute the mass within the initial radius:

    print("\nFinding initial planetary mass...\n")

    xcm,ycm,zcm=cms[0],cms[1],cms[2]
    mass=0
    num=0

    for i in range(ncores):

        with open(f'{path}/results.{outputnumber:05d}_{ncores:05d}_{i:05d}.dat','r') as file:

            timevalue=float(file.readline())
            num=num+int(file.readline())

            for line in file:

                elements=line.split()
                m=float(elements[2])
                xx=float(elements[3])/r0-xcm
                yy=float(elements[4])/r0-ycm
                zz=float(elements[5])/r0-zcm
                
                if np.sqrt(xx**2+yy**2+zz**2)<=radius:

                    mass=mass+m

    #Store data

    print("Reading and storing data...\n")

    particle = namedtuple('particle', ['id','tag','m','x','y','z','r','vx','vy','vz',
                                       'v','dens','int_e','press','pot_e','ent','temp'])
    particles=[]

    for i in range(ncores):

        with open(f'{path}/results.{outputnumber:05d}_{ncores:05d}_{i:05d}.dat','r') as file:

            file.readline()
            file.readline()

            for line in file:

                elements=line.split()
                ID=int(elements[0])
                tag=int(elements[1])
                m=float(elements[2])
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

                particles.append(particle(ID,tag,m,xx,yy,zz,r,vx,vy,vz,v,dens,int_e,press,pot_e,ent,temp))

    return particles,mass,timevalue,num



def iterate(iterations,radius,particles,mass):     #Determine the final mass and radius with iterative scheme

    if iterations != 0:

        print("Beginning iterations...\n")

    else:

        print("Printing final data...\n")

    radius=radius*r0

    #Begin iterative scheme

    for i in range(iterations):  

        mass_new=0
        radiuslist=[]

        for particle in particles:

            #Compute orbital parameters

            rmag=np.linalg.norm(particle.r)
            vmag=np.linalg.norm(particle.v)

            E=((1/2)*(vmag)**2-(G*mass)/rmag)
            a=-(G*mass)/(2*E) 
            L=np.linalg.norm(np.cross(particle.r,particle.v)) 
            ecc=np.sqrt(1+((2*E*L**2)/(G*mass)**2)) 
            rperi=(a*(1-ecc)) 

            #Determine which particles are part of the planet

            if E<0 and rperi <= radius:

                mass_new=mass_new+particle.m
                radiuslist.append(rmag)

        #Determine new radius and mass based on these particles

        mass=mass_new
        radius=np.percentile(radiuslist,percentile)

        print(f"    Iteration {i+1}: R={radius:0.4e} m, M={mass:0.4e} kg")

    if iterations != 0:

        print()
        
    print(f"    Final planetary radius: {radius:0.4e} m")
    print(f"    Final planetary mass: {mass:0.4e} kg\n")

    return radius, mass



def write_files(timevalue,num,radius,mass,cms,particles):      #Stores the data in the output file

    print("Writing output file...\n")

    with open(f'{outputpath}/SortedData.txt','w') as file:

        #Write time, number of particles, radius, mass, and center of mass

        xcm,ycm,zcm=cms[0]*r0,cms[1]*r0,cms[2]*r0

        file.write(f'{timevalue}\n{num}\n{radius}\n{mass}\n{xcm}\t{ycm}\t{zcm}\n')

        k=0
        percent=0

        for particle in particles:

            rmag=np.linalg.norm(particle.r)
            vmag=np.linalg.norm(particle.v)

            E=((1/2)*(vmag)**2-(G*mass)/rmag)
            a=-(G*mass)/(2*E) 
            L=np.linalg.norm(np.cross(particle.r,particle.v)) 
            ecc=np.sqrt(1+((2*E*L**2)/(G*mass)**2)) 
            rperi=(a*(1-ecc))
            
            if E<0:

                if rperi <= radius:

                    fate=0

                else:

                    fate=1

            else:

                fate=2

            #Store the previous particle data as well as the particle fate (0=planet, 1=disk, 2=escaping)

            file.write(f'{particle.id}\t{particle.tag}\t{particle.m}\t'+
                       f'{particle.x+xcm}\t{particle.y+ycm}\t{particle.z+zcm}\t{particle.vx}\t{particle.vy}\t{particle.vz}\t'+
                       f'{particle.dens}\t{particle.int_e}\t{particle.press}\t{particle.pot_e}\t'+
                       f'{particle.ent}\t{particle.temp}\t{fate}\n')
                    

            if k%((num-1)//10) == 0:

                print(f"    {percent}% complete")

                percent=percent+10

            k=k+1
    
    print("\n    Outputted SortedData.txt\n")



def main():

    cms,totals,irons,silis=center_of_mass()
    radius=plotdist(totals, irons, silis,xlim)
    particles,mass,timevalue,num=storing_data(cms,radius)
    radius,mass=iterate(iterations,radius,particles,mass)
    write_files(timevalue,num,radius,mass,cms,particles)



main()


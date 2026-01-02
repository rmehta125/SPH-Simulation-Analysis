import matplotlib.pyplot as plt
import numpy as np
from collections import namedtuple

#USER INPUTS_________________________________________________________________

path = 
outputpath =
outputnumber =
ncores =
xlim = 20
percentile = 99
iterations = 5

#____________________________________________________________________________

r0=1e6
G=6.67*10**(-11)

def center_of_mass():   # Determines the center of mass of the main planet

    print('\nDetermining center of mass...\n')

    x=[]
    y=[]
    z=[]
    xtotal=[]
    ytotal=[]
    ztotal=[]
    masslist=[]

    for i in range(ncores):

        with open(f'{path}/results.{outputnumber:05d}_{ncores:05d}_{i:05d}.dat','r') as file:

            file.readline()
            file.readline()

            # Store data

            for line in file:

                elements=line.split()
                tag=int(elements[1])
                m=float(elements[2])
                xx=float(elements[3])/r0
                yy=float(elements[4])/r0
                zz=float(elements[5])/r0

                xtotal.append(xx)
                ytotal.append(yy)
                ztotal.append(zz)

                # Sort data by tags

                if tag == 1:

                    x.append(xx)
                    y.append(yy)
                    z.append(zz)
                    masslist.append(m)

    # Compute the center of mass using target core particles

    x=np.array(x)
    y=np.array(y)
    z=np.array(z)
    masslist=np.array(masslist)

    xcm=(np.sum(x*masslist))/np.sum(masslist)
    ycm=(np.sum(y*masslist))/np.sum(masslist)
    zcm=(np.sum(z*masslist))/np.sum(masslist)  
    cms=[xcm,ycm,zcm]     

    # Center data by the center of mass

    xtotal=np.array(xtotal)-xcm
    ytotal=np.array(ytotal)-ycm
    ztotal=np.array(ztotal)-zcm
    totals=[xtotal,ytotal,ztotal]

    return cms,totals



def on_click(event):    # Detects a double-click on particle distribution plot

    fig = event.canvas.figure
    ax = fig.axes[0]

    if event.dblclick and event.inaxes == ax and event.xdata is not None:

        fig.radius = event.xdata
        fig.vline.set_xdata([fig.radius])
        fig.canvas.draw_idle()

        if iterations != 0:

            print(f'    Initial radius = {(fig.radius*r0):0.4e} m')
    
        else:

            print(f'    Radius = {(fig.radius*r0):0.4e} m')



def plotdist(totals,xlim):    # Plots particle distributions and determines initial radius

    print('Plotting particle distributions...\n')

    # Plot particle distributions

    xtotal,ytotal,ztotal=totals[0],totals[1],totals[2]

    radiuslist=np.sqrt(xtotal**2+ytotal**2+ztotal**2)

    plt.figure(figsize=(8,5))
    plt.hist(x=radiuslist,bins=500,range=(0,xlim),color='blue')
    plt.xlabel('Radius (1e6 m)')
    plt.ylabel('Count')
    plt.title('Radial Particle Distribution')

    # Determine an initial radius

    fig = plt.gcf()
    fig.radius = None
    fig.vline = plt.axvline(0,color='red',linestyle='--')
    fig.canvas.mpl_connect('button_press_event',on_click)

    if iterations != 0:
        
        print('    Please double-click on an initial guess for the planetary radius in the ' +
              '\n    histogram, and exit the plot when you are finished.\n')
        
    else:

        print('    Please double-click on a guess for the planetary radius in the histogram, and ' +
              '\n    exit the plot when you are finished.\n')

    plt.show()

    return fig.radius



class Particle:    # Defines a particle class

    def __init__(self,id,tag,m,x,y,z,r,vx,vy,vz,v,dens,int_e,press,pot_e,ent,temp,fate):

        self.id = id
        self.tag = tag
        self.m = m
        self.x = x
        self.y = y
        self.z = z
        self.r = r
        self.vx = vx
        self.vy = vy
        self.vz = vz
        self.v = v
        self.dens = dens
        self.int_e = int_e
        self.press = press
        self.pot_e = pot_e
        self.ent = ent
        self.temp = temp
        self.fate = fate
    


def storing_data(cms,radius):   # Reads particle data, centers it, and stores it

    # Compute the mass within the initial radius:

    if iterations != 0:
    
        print('\nFinding initial planetary mass...\n')

    else:

        print('\nFinding planetary mass...\n')

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
                
                if np.sqrt(xx**2+yy**2+zz**2) <= radius:

                    mass=mass+m

    if iterations != 0:
        
        print(f'    Initial mass: {mass:0.4e} kg\n')

    else:

        print(f'    Mass: {mass:0.4e} kg\n')

    # Store data

    print('Reading and storing data...\n')

    particles=[]

    for i in range(ncores):

        with open(f'{path}/results.{outputnumber:05d}_{ncores:05d}_{i:05d}.dat','r') as file:

            file.readline()
            file.readline()

            for line in file:

                elements=line.split()
                id=int(elements[0])
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
                fate=0

                particles.append(Particle(id,tag,m,xx,yy,zz,r,vx,vy,vz,v,dens,int_e,press,pot_e,ent,temp,fate))

    return particles,mass,timevalue,num



def iterate(iterations,radius,particles,mass):     # Determine the final mass and radius with iterative scheme

    if iterations != 0:

        print('Beginning iterations...\n')

    radius=radius*r0

    # Begin iterative scheme

    for i in range(iterations):  

        mass_new=0
        radiuslist=[]

        for particle in particles:

            # Compute orbital parameters

            rmag=np.linalg.norm(particle.r)
            vmag=np.linalg.norm(particle.v)

            E=((1/2)*(vmag)**2-(G*mass)/rmag)
            a=-(G*mass)/(2*E) 
            L=np.linalg.norm(np.cross(particle.r,particle.v)) 
            ecc=np.sqrt(1+((2*E*L**2)/(G*mass)**2)) 
            rperi=(a*(1-ecc)) 

            # Determine which particles are part of the planet

            if E < 0 and rperi <= radius:

                mass_new=mass_new+particle.m
                radiuslist.append(rmag)

        # Determine new radius and mass based on these particles

        mass=mass_new
        radius=np.percentile(radiuslist,percentile)

        print(f'    Iteration {i+1}: R={radius:0.4e} m, M={mass:0.4e} kg')

    if iterations != 0:

        print(f'\n    Final planetary radius: {radius:0.4e} m')
        print(f'    Final planetary mass: {mass:0.4e} kg\n')

    return radius,mass



def write_files(timevalue,num,radius,mass,cms,particles):      # Stores the data in the output file

    print('Writing output file...\n')

    with open(f'{outputpath}/SortedData_{outputnumber:05d}.txt','w') as file:

        # Write time, number of particles, radius, mass, and center of mass

        xcm,ycm,zcm=cms[0]*r0,cms[1]*r0,cms[2]*r0

        file.write(f'{timevalue}\n{num}\n{radius}\n{mass}\n{xcm}\t{ycm}\t{zcm}\n')

        percent=0

        for i, particle in enumerate(particles):

            rmag=np.linalg.norm(particle.r)
            vmag=np.linalg.norm(particle.v)

            E=((1/2)*(vmag)**2-(G*mass)/rmag)
            a=-(G*mass)/(2*E) 
            L=np.linalg.norm(np.cross(particle.r,particle.v)) 
            ecc=np.sqrt(1+((2*E*L**2)/(G*mass)**2)) 
            rperi=(a*(1-ecc))
            
            if E < 0:

                if rperi <= radius:

                    particle.fate=0

                else:

                    particle.fate=1

            else:

                particle.fate=2

            # Store the previous particle data as well as the particle fate (0=planet, 1=disk, 2=escaping)

            file.write(f'{particle.id}\t{particle.tag}\t{particle.m}\t'+
                       f'{particle.x+xcm}\t{particle.y+ycm}\t{particle.z+zcm}\t{particle.vx}\t{particle.vy}\t{particle.vz}\t'+
                       f'{particle.dens}\t{particle.int_e}\t{particle.press}\t{particle.pot_e}\t'+
                       f'{particle.ent}\t{particle.temp}\t{particle.fate}\n')
                    

            if i % ((num-1)//10) == 0:

                print(f'    {percent}% complete')

                percent=percent+10
    
    print(f'\n    Outputted SortedData_{outputnumber:05d}.txt\n')



def main():

    cms,totals=center_of_mass()
    radius=plotdist(totals,xlim)
    particles,mass,timevalue,num=storing_data(cms,radius)
    radius,mass=iterate(iterations,radius,particles,mass)
    write_files(timevalue,num,radius,mass,cms,particles)



main()


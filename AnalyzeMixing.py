import matplotlib.pyplot as plt
import numpy as np
from matplotlib.gridspec import GridSpec
from scipy.spatial import cKDTree

#USER INPUTS_________________________________________________________________

path = 
outputpath =
outputnumber = 
gamma = 
angle = 
axesdim = 20
azimuth = 120
elevation = 10

#____________________________________________________________________________

r0=1e6

class Particle:    # Defines a particle class

    def __init__(self,tag,x,y,z,r,fate,neighbors):

        self.tag = tag
        self.x = x
        self.y = y
        self.z = z
        self.r = r
        self.fate = fate
        self.neighbors = neighbors



def read_data():    # Reads and stores all data

    print('\nReading data...')

    particles=[]

    with open(f'{path}/SortedData_{outputnumber:05d}.txt','r') as file:

        timevalue=float(file.readline())
        file.readline()
        radius=float(file.readline())
        file.readline()
        cms=file.readline().split()
        xcm,ycm,zcm=float(cms[0]),float(cms[1]),float(cms[2])    

        for line in file:

            elements=line.split()
            tag=int(elements[1])
            xx=(float(elements[3])-xcm)/r0
            yy=(float(elements[4])-ycm)/r0
            zz=(float(elements[5])-zcm)/r0
            fate=int(elements[15])
            r=np.sqrt(xx**2+yy**2+zz**2)
            neighbors=0

            particles.append(Particle(tag,xx,yy,zz,r,fate,neighbors))

    return radius,particles,timevalue



def on_click(event):    # Detects a double-click on particle distribution plot

    fig = event.canvas.figure
    ax = fig.axes[0]

    if event.dblclick and event.inaxes == ax and event.xdata is not None:

        fig.cutoff = int(event.xdata)
        fig.vline.set_xdata([fig.cutoff])
        fig.canvas.draw_idle()

        print(f'    Cutoff = {fig.cutoff} neighbors')



def find_cutoff(radius,particles):    # Finds a cutoff for the amount of neighboring iron

    print('\nPlotting distribution of neighboring iron...\n')

    # Use a SciPy tree for fast sorting 

    ironparticles = [p for p in particles if p.tag == 3 or p.tag == 1]
    ironpositions = np.array([[p.x, p.y, p.z] for p in ironparticles])
    irontree = cKDTree(ironpositions)
    neighborradius = (radius/20)/r0  
    nearbylist=[]

    print(f'    Neighbor radius: {neighborradius*r0:0.2e} m\n')

    percent=0

    for i, particle in enumerate(ironparticles):

        xx = particle.x
        yy = particle.y
        zz = particle.z

        # Find the number of neighboring iron particles, excluding itself

        indices = irontree.query_ball_point([xx, yy, zz], r=neighborradius)
        neighbors = len(indices) - 1
        particle.neighbors=neighbors
        nearbylist.append(neighbors)

        if i % ((len(ironparticles)-1)//10) == 0:

            print(f'    {percent}% complete')

            percent=percent+10

    # Plot the distribution of neighbors and determine cutoff

    print('\n    Please double-click on a guess for the neighboring iron cutoff ' +
          '\n    in the histogram near the start of the main distribution, and exit ' +
          '\n    the plot when you are finished.\n')

    plt.figure(figsize=(7,5))
    plt.hist(nearbylist,bins=240,color='blue')
    plt.xlabel(f'Number of Iron Neighbors within {neighborradius*r0:0.2e} m')
    plt.ylabel('Count')
    plt.title('Distribution of Neighboring Iron Particles')
    plt.tight_layout()
    fig = plt.gcf()
    fig.cutoff = None
    fig.vline = plt.axvline(0,color='red',linestyle='--')
    fig.canvas.mpl_connect('button_press_event',on_click)
    plt.show()

    cutoff=fig.cutoff
    return cutoff,ironparticles



def analyze_mixing(cutoff,ironparticles,timevalue):

    print('\nAnalyzing mixing...\n')

    impcore=[p for p in ironparticles if p.tag == 3]
    core=len(impcore)
    mixed=0

    mixedx=[]
    mixedy=[]
    mixedz=[]

    sunkx=[]
    sunky=[]
    sunkz=[]

    # Determine which impactor core particles have mixed and which have sunken

    for particle in impcore:

        xx = particle.x
        yy = particle.y
        zz = particle.z
        tag=particle.tag
        fate=particle.fate
        neighbors=particle.neighbors

        if neighbors < cutoff and fate != 2 and tag == 3:

            mixed=mixed+1

            mixedx.append(xx)
            mixedy.append(yy)
            mixedz.append(zz)

        elif fate != 2 and tag == 3:

            sunkx.append(xx)
            sunky.append(yy)
            sunkz.append(zz)

    xtarcore = [p.x for p in ironparticles if p.tag == 1]
    ytarcore = [p.y for p in ironparticles if p.tag == 1]
    ztarcore = [p.z for p in ironparticles if p.tag == 1]

    print('Generating mixing plots and printing results...')

    # Generate projection plot

    ticks=np.linspace(-axesdim/2,axesdim/2,5)
    mixper=round((mixed/core)*100,2)
    hour=round((((timevalue)//10)*10)/3600,2)

    plt.figure(figsize=(8,6))
    plt.scatter(mixedx,mixedy,c='red',marker='.',s=1.7)
    plt.scatter(xtarcore,ytarcore,c='gray',marker='.',s=1.7, alpha=0.01)
    plt.scatter(sunkx,sunky,c='blue',marker='.',s=1.7)       
    plt.xlabel(f'x (1e6 m)')
    plt.ylabel(f'y (1e6 m)')
    plt.xticks(ticks)
    plt.yticks(ticks)
    plt.xlim(-axesdim/2,axesdim/2)
    plt.ylim(-axesdim/2,axesdim/2)
    plt.title(fr'Projection of Mixing, t={hour} h, $\gamma={gamma}$, ${angle}^\circ$')
    plt.text(0.98, 0.02, f'Mixing %: {mixper}',transform=plt.gca().transAxes,ha='right', 
             va='bottom',fontsize=10,bbox=dict(facecolor='white',alpha=0.7,edgecolor='none'))
    plt.gca().set_aspect('equal')
    plt.savefig(f'{outputpath}/MixingProj_{outputnumber:05d}.png',dpi=300)

    # Generate 3D render

    fig=plt.figure(figsize=(8,7))
    gs=GridSpec(1,2,width_ratios=[20,0.5],figure=fig)
    ax=fig.add_subplot(gs[0],projection='3d')
    ax.set_box_aspect([1,1,1])
    ax.view_init(elev=elevation, azim=azimuth, roll=0)
    ax.scatter(mixedx,mixedy,mixedz,c='red',marker='.',s=1.7)
    ax.scatter(xtarcore,ytarcore,ztarcore,c='gray',marker='.',s=1.7)
    ax.scatter(sunkx,sunky,sunkz,c='blue',marker='.',s=1.7)   
    ax.set_xlim(-axesdim/2,axesdim/2)
    ax.set_ylim(-axesdim/2,axesdim/2)
    ax.set_zlim(-axesdim/2,axesdim/2)
    ax.set_xticks(ticks)
    ax.set_yticks(ticks)
    ax.set_zticks(ticks)
    ax.set_xlabel('x (1e6 m)')
    ax.set_ylabel('y (1e6 m)')
    ax.set_zlabel('z (1e6 m)')
    ax.set_title(fr'3D Render of Mixing, t={hour} h, $\gamma={gamma}$, ${angle}^\circ$')
    fig.text(0.98, 0.02, f'Mixing %: {mixper}',ha='right',va='bottom',fontsize=10,
             bbox=dict(facecolor='white',alpha=0.7,edgecolor='none'))
    fig.savefig(f'{outputpath}/Mixing3D_{outputnumber:05d}.png',dpi=300)

    print(f'\n    The number of impactor core particles in the mantle is: {mixed}')
    print(f'    The total number of impactor core particles is: {core}')
    print(f'    The mixing percentage is: {mixper}%')
    print(f'\n    Outputted MixingProj_{outputnumber:05d}.png, Mixing3D_{outputnumber:05d}.png\n')

    plt.show()



def main():

    radius,particles,timevalue=read_data()
    cutoff,ironparticles=find_cutoff(radius,particles)
    analyze_mixing(cutoff,ironparticles,timevalue)




main()

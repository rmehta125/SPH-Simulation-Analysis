import matplotlib.pyplot as plt
import numpy as np
from collections import namedtuple

#USER INPUTS_________________________________________________________________

outputnumber=599
ncores=100
path=r"C:\Users\nakaj\OneDrive\Desktop\2025Work\MeltScalingCollisions\FinalCollisions\0.01\60Deg\\"
outputpath=path
axesdim = 22

#____________________________________________________________________________

r0=1e6

def read_data():    #Reads and stores all data

    print('\nReading data...')

    xiron=[]
    yiron=[]
    ziron=[]
    xsili=[]
    ysili=[]
    zsili=[]
    particles=[]

    particle = namedtuple('particle',['tag','x','y','z','r','fate'])

    with open(f'{path}/SortedData.txt','r') as file:

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

            #Sort data by tags

            if tag == 0 or tag == 2:

                xsili.append(xx)
                ysili.append(yy)
                zsili.append(zz)

            if tag == 1 or tag == 3:

                xiron.append(xx)
                yiron.append(yy)
                ziron.append(zz)

            particles.append(particle(tag,xx,yy,zz,r,fate))

    xiron,yiron,ziron=np.array(xiron),np.array(yiron),np.array(ziron)
    xsili,ysili,zsili=np.array(xsili),np.array(ysili),np.array(zsili)
    ironlist=np.sqrt(xiron**2+yiron**2+ziron**2)
    sililist=np.sqrt(xsili**2+ysili**2+zsili**2)

    return radius,sililist,ironlist,particles,timevalue



def on_click(event):    #Detects a double-click on particle distribution plot

    fig = event.canvas.figure
    ax = fig.axes[0]

    if event.dblclick and event.inaxes == ax and event.xdata is not None:

        fig.CMB = event.xdata
        fig.vline.set_xdata([fig.CMB])
        fig.canvas.draw_idle()

        print(f'\n    CMB (1e6 m) = {round(fig.CMB,2)}')



def plot_distributions(radius,sililist,ironlist):    #Plots distributions and determines CMB

    print('\nPlotting particle distributions...')

    plt.figure(figsize=(8,5))
    plt.hist(x=sililist,bins=700,range=(0,radius/r0),color='blue',alpha=0.4,label='Silicate')
    plt.hist(x=ironlist,bins=700,range=(0,radius/r0),color='red',alpha=0.4,label='Iron')
    plt.xlabel(f'Radius ({r0:.1e} m)')
    plt.ylabel('Count')
    plt.title('Distribution of Iron and Silicate')
    plt.legend()
    fig = plt.gcf()
    fig.CMB = None
    fig.vline = plt.axvline(0,color='b',linestyle='--',alpha=0.7)
    fig.canvas.mpl_connect('button_press_event',on_click)

    print('\n    Please double-click on where you believe the CMB is in the histogram ' + 
          '\n    and exit the plot when you are finished.  Make sure to use the pan ' +
          '\n    and zoom options to get a more accurate value.')

    plt.show()

    return fig.CMB



def analyze_mixing(CMB,particles,timevalue):    #Computes mixing percentage

    print('\nAnalyzing mixing...')

    mixed=0
    core=0

    xtarcore=[]
    ytarcore=[]
    ztarcore=[]

    mixedx=[]
    mixedy=[]
    mixedz=[]

    sunkx=[]
    sunky=[]
    sunkz=[]

    for particle in particles:

        tag=particle.tag
        xx=particle.x
        yy=particle.y
        zz=particle.z
        r=particle.r
        fate=particle.fate

        if tag == 1:

            xtarcore.append(xx)
            ytarcore.append(yy)
            ztarcore.append(zz)

        #Determine which nonescaping core particles have mixed with the mantle

        if tag == 3:

            core=core+1

            if CMB < r and fate != 2:

                mixed=mixed+1

                mixedx.append(xx)
                mixedy.append(yy)
                mixedz.append(zz)

            elif fate != 2:

                sunkx.append(xx)
                sunky.append(yy)
                sunkz.append(zz)

    #Generate mixing plot and print results

    plt.figure(figsize=(8,6))
    plt.scatter(mixedx,mixedy,c='red',marker='.',s=1.7)
    plt.scatter(xtarcore,ytarcore,c='gray',marker='.',s=1.7, alpha=0.01)
    plt.scatter(sunkx,sunky,c='blue',marker='.',s=1.7)       
    plt.xlabel(f'x (1e6 m)')
    plt.ylabel(f'y (1e6 m)')
    ticks=np.linspace(-axesdim/2,axesdim/2,5)
    plt.xticks(ticks)
    plt.yticks(ticks)
    plt.xlim(-axesdim/2,axesdim/2)
    plt.ylim(-axesdim/2,axesdim/2)
    mixper=round((mixed/core)*100,2)
    hour=round((((timevalue)//10)*10)/3600,2)
    plt.title(f'Projection Visualization at t={hour} hrs')
    plt.text(0.98, 0.02, f'Mixing %: {mixper}',transform=plt.gca().transAxes,ha='right', 
             va='bottom',fontsize=10,bbox=dict(facecolor='white',alpha=0.7,edgecolor='none'))
    plt.gca().set_aspect('equal')
    plt.savefig(f'{outputpath}/Mixing_{outputnumber:05d}.png',dpi=300)

    print(f"\n    The number of core particles in the mantle is: {mixed}")
    print(f"    The total number of impactor core particles is: {core}")
    print(f"    The mixing percentage is: {mixper}\n")

    plt.show()



def main():

    radius,sililist,ironlist,particles,timevalue=read_data()
    CMB=plot_distributions(radius,sililist,ironlist)
    analyze_mixing(CMB,particles,timevalue)



main()
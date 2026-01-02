# SPH Simulation Analysis

## Overview

This repository allows users to analyze planetary collision simulations generated using smoothed particle hydrodynamics (SPH) code.  SPH is a Lagrangian method of simulating particle systems as fluids.  Here, it treats the collision between two planets as such, and generates data frames that can be analyzed for various properties post-impact.  This repository provides code to estimate the amount of melting that occurs in the mantle, determine how much of the impactor's core mixes with the target body's mantle, as well as visualize the pressure, temperature, entropy, etc. as a cross section or 3D render.  This code uses Matplotlib, Numpy, and SciPy in Python 3 and analyzes data generated using the Nakajima Lab's SPH code at the University of Rochester (https://github.com/NatsukiHosono/FDPS_SPH).  

A full data set generated from a collision can be storage intensive.  For convenience, one sample timestep from a low resolution canonical impact scenario has been uploaded at the attached Dropbox link for users to try analyzing (https://www.dropbox.com/scl/fo/omhu89fb82087rrr11p68/ABkQkBSbzLosi3UvUJS1GYU?rlkey=178ipj8oxtva3upz7obvhy8qn&st=1ub217ll&dl=0).

For a full instruction manual of using the code, please see the attached link: https://drive.google.com/file/d/1FRybHX2HlgJuGFtZvrIDdQGYykU5z5VT/view?usp=sharing.

## Gallery

<div align="center">

https://github.com/user-attachments/assets/5d47f62f-f200-4169-93ec-5466018443ba

<img width="900" alt="DensityCS" src="https://github.com/user-attachments/assets/ccfc51d3-d789-40cd-b457-5aedd2f0b4cc" />
<img width="900" alt="TemperatureCS" src="https://github.com/user-attachments/assets/ddf86ae6-ff1b-4f76-a37b-20941ad55cb6" />

</div>




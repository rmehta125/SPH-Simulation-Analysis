# SPH Simulation Analysis

## Overview

This repository allows users to analyze planetary collision simulations generated using smoothed particle hydrodynamics (SPH) code.  SPH is a Lagrangian method of simulating particle systems as fluids.  Here, it treats the collision between two planets as such, and generates data frames that can be analyzed for various properties post-impact.  This repository provides code to estimate the amount of melting that occurs in the mantle, determine how much of the impactor's core mixes with the target body's mantle, as well as visualize the pressure, temperature, entropy, etc. as a cross section or 3D render.  This code uses Matplotlib, Numpy, and SciPy in Python 3 and analyzes data generated using the Nakajima Lab's SPH code at the University of Rochester (https://github.com/NatsukiHosono/FDPS_SPH).  

A full data set generated from a collision can be storage intensive.  For convenience, one sample timestep from a low resolution canonical impact scenario has been uploaded at the attached Dropbox link for users to try analyzing (https://www.dropbox.com/scl/fo/omhu89fb82087rrr11p68/ABkQkBSbzLosi3UvUJS1GYU?rlkey=178ipj8oxtva3upz7obvhy8qn&st=1ub217ll&dl=0).

For a full instruction manual of using the code, please see the attached link: https://drive.google.com/file/d/1FRybHX2HlgJuGFtZvrIDdQGYykU5z5VT/view?usp=sharing.

## Gallery

<div align="center">

https://github.com/user-attachments/assets/5d47f62f-f200-4169-93ec-5466018443ba

<table align="center">
  <tr>
    <td>
      <img width="900" alt="DensityCS"
           src="https://github.com/user-attachments/assets/ccfc51d3-d789-40cd-b457-5aedd2f0b4cc" />
    </td>
    <td>
      <img width="900" alt="Energy3D" 
           src="https://github.com/user-attachments/assets/0f18d4ec-2293-4aee-883c-f4c6b5bf1e3e" /> 
    </td>
  </tr>
    <tr>
    <td>
      <img width="900" alt="Pressure3D" 
        src="https://github.com/user-attachments/assets/71b772c6-32ea-4dd0-8139-64466dc63a64" />
    </td>
    <td>
      <img width="900" alt="TemperatureCS" 
           src="https://github.com/user-attachments/assets/76a57886-d702-4be4-948a-3cd17834a757" />
    </td>
  </tr>
</table>


</div>




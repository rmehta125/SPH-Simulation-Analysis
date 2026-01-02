# SPH Simulation Analysis

## Overview

This repository allows users to analyze planetary collision simulations generated using smoothed particle hydrodynamics (SPH) code.  SPH is a Lagrangian method of simulating particle systems as fluids.  Here, it treats the collision between two planets as such, and generates data frames that can be analyzed for various properties post-impact.  This repository provides code to estimate the amount of melting that occurs in the mantle, determine how much of the impactor's core mixes with the target body's mantle, as well as visualize the pressure, temperature, entropy, etc. as a cross section or 3D render.  This code uses Matplotlib, Numpy, and SciPy in Python 3 and analyzes data generated using the Nakajima Lab's SPH code at the University of Rochester (https://github.com/NatsukiHosono/FDPS_SPH).  

A full data set generated from a collision can be storage intensive.  For convenience, one sample timestep from a low resolution canonical impact scenario has been uploaded at the attached Dropbox link for users to try analyzing (https://www.dropbox.com/scl/fo/omhu89fb82087rrr11p68/ABkQkBSbzLosi3UvUJS1GYU?rlkey=178ipj8oxtva3upz7obvhy8qn&st=1ub217ll&dl=0).

For a full instruction manual of using the code, please see the attached link: https://drive.google.com/file/d/1FRybHX2HlgJuGFtZvrIDdQGYykU5z5VT/view?usp=sharing.

## Gallery

<div align="center">

https://github.com/user-attachments/assets/5d47f62f-f200-4169-93ec-5466018443ba

<table align="center">
  <!-- Row 1: THREE images -->
  <tr>
    <td>
      <img width="900" alt="Melting_00740" src="https://github.com/user-attachments/assets/414d60d3-08c6-4c64-aa53-a1d52962fae0" />
    </td>
    <td>
      <img width="900" alt="Mixing3D_00740" src="https://github.com/user-attachments/assets/808dec53-8c6c-4029-aabd-095d328db2cf" />
    </td>
  </tr>
  <tr>
    <td>
      <img width="900" alt="MixingProj_00740" src="https://github.com/user-attachments/assets/dfa5678c-a1ea-441f-8931-a66714a667ff" />
    </td>
    <td>
      <img width="900" height="1808" alt="Energy3D" src="https://github.com/user-attachments/assets/8dbcf20f-3ca6-429d-a45a-32b00502a294" />    
    </td>
  </tr>
  
</table>

</div>




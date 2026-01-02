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
      <img width="900" alt="Pressure3D" src="https://github.com/user-attachments/assets/7d6e4cd5-6503-43ed-8ed7-cd7f47daa184" />
    </td>
    <td>
      <img width="900" alt="Mixing3D_00740" src="https://github.com/user-attachments/assets/54f56ac0-759f-4af5-86d9-7419acc572a8" />
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
  <tr>
    <td>
      <img width="2112" height="1808" alt="TemperatureCS" src="https://github.com/user-attachments/assets/69a09fc7-4eb2-4f3c-b5b6-a3aea2c1e638" />
    </td>
    <td>
      <img width="2400" height="1800" alt="Melting_00740" src="https://github.com/user-attachments/assets/d28e76a5-eec8-4b52-b726-7659d4a28107" />
    </td>
  </tr>
  
</table>

</div>




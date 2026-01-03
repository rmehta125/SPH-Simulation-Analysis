# SPH Simulation Analysis

## Overview

This repository allows users to analyze planetary collision simulations generated using smoothed particle hydrodynamics (SPH) code.  SPH is a Lagrangian method of simulating particle systems as fluids.  Here, it treats the collision between two planets as such, and generates data frames that can be analyzed for various properties post-impact.  This repository provides code to estimate the amount of melting that occurs in the mantle, determine how much of the impactor's core mixes with the target body's mantle, as well as visualize the pressure, temperature, entropy, etc. as a cross section or 3D render.  This code uses Matplotlib, Numpy, and SciPy in Python 3 and analyzes data generated using the Nakajima Lab's SPH code at the University of Rochester (https://github.com/NatsukiHosono/FDPS_SPH).  

A full data set generated from a collision can be storage intensive.  For convenience, one sample timestep from a low resolution canonical impact scenario has been uploaded at the attached Dropbox link for users to try analyzing (https://www.dropbox.com/scl/fo/omhu89fb82087rrr11p68/ABkQkBSbzLosi3UvUJS1GYU?rlkey=178ipj8oxtva3upz7obvhy8qn&st=1ub217ll&dl=0).

For a full instruction manual of using the code, please see the attached link: https://drive.google.com/file/d/1FRybHX2HlgJuGFtZvrIDdQGYykU5z5VT/view?usp=sharing.

## Gallery

Shown below are several example plots and animations that have been generated using this repository.

<div align="center">

https://github.com/user-attachments/assets/677d4dc0-790d-4ea4-9379-2b7e1bffbcd4

https://github.com/user-attachments/assets/35a39216-b505-4fa7-a606-d0ede24e80d9

<table align="center">
  <!-- Row 1: THREE images -->
  <tr>
    <td>
      <img width="900" alt="DensityCS" src="https://github.com/user-attachments/assets/1754bb47-ac0a-42dd-8915-564820c2e36e" />
    </td>
    <td>
      <img width="900" alt="Mixing3D_00740" src="https://github.com/user-attachments/assets/54f56ac0-759f-4af5-86d9-7419acc572a8" />
    </td>
  </tr>
  <tr>
    <td>
      <img width="900" alt="Melting_00537" src="https://github.com/user-attachments/assets/b1ad3e38-5f73-49e9-8ef5-4261f9741f85" />
    </td>
    <td>
        <img width="900" alt="3D_00660" src="https://github.com/user-attachments/assets/f136bb1c-11ef-418c-a165-20e4477fc5b3" />
    </td>
  </tr>
  <tr>
    <td>
      <img width="900" alt="TemperatureCS" src="https://github.com/user-attachments/assets/69a09fc7-4eb2-4f3c-b5b6-a3aea2c1e638" />
    </td>
    <td>
      <img width="900" alt="Melting_00740" src="https://github.com/user-attachments/assets/d28e76a5-eec8-4b52-b726-7659d4a28107" />
    </td>
  </tr>
  <tr>
    <td>
      <img width="900" alt="MixingProj_00740" src="https://github.com/user-attachments/assets/dfa5678c-a1ea-441f-8931-a66714a667ff" />
    </td>
    <td>
      <img width="900" alt="Pressure3D" src="https://github.com/user-attachments/assets/f33e86ee-f5c6-4e2f-9960-73bf628d4340" />
    </td>
  </tr>
  
  
</table>

</div>




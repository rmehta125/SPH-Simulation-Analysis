# SPH Simulation Analysis

## Overview

This repository allows users to analyze planetary collision simulations generated using smoothed particle hydrodynamics (SPH) code.  SPH is a lagrangian method of simulating systems of particles as fluids.  Here, it treats the collision between two planets as such, and generates data frames that can be analyzed for various properties post-impact.  This repository provides code to analyze the amount of melting that occurs in the mantle, determine how much of the impactor's core mixes with the target body's mantle, as well as visualize the pressure, temperature, entropy, etc. as a cross section or 3D render.  This code uses Matplotlib, Numpy, and SciPy in Python 3 and analyzes data generated using the Nakajima Lab's SPH code at the University of Rochester (https://github.com/NatsukiHosono/FDPS_SPH).  

The full data set generated from a collision can be storage intensive.  For convenience, one sample timestep from two different collisions have been uploaded to this repository for users to try analyzing.  Both collisions occur at 45°, use initial surface temperatures of 2000K, and have an Earth-mass target body.  One collision has an impactor-to-total mass ratio of γ=0.3, while the other has a ratio of γ=0.01.  

For a full instruction manual of using the code and data uploaded here, please see the attached link: [INSERT LINK].

## Gallery

[INSERT PRETTY PICTURE AND VIDEOS]

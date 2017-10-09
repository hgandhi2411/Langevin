![code coverage](img/coverage.svg)

CHE 477 Langevin Dynamics Project
======

*Heta Gandhi*

Overview
-------

This is a python implementation of the Langevin Dynamics Simulation. This simulator uses Euler's integration to simulate the position and velocity of a particle. 

Installation
---------
To install this simulator, run the following commands from the terminal:

`git clone https://github.com/hgandhi2411/Langevin.git

pip install Langevin`

Usage
-----
The simulator has a command line interface where the user can input initial position, initial velocity, temperature, damping coefficient, total time for which simulation must run and the time step using flags. The help[-h, --help] option show the different flags that can be used. In addition, the model also takes as input a file which specifies the potential energy associated with position of the particle. 

Output is in the form of a file which contains position and velocity for each time step.

The file can be run using the command `langevin` along with different flags as described above. The visualization of the simulation can be seen on a browser at `localhost:8888`. 


(c) 2017
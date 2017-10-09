![code coverage](img/coverage.svg)

CHE 477 Langevin Dynamics Project
======

*Heta Gandhi*

Overview
-------

This is a python implementation of the Langevin Dynamics Simulation. The Langevin equations which describe brownian motion are:

$ ma = - \lambda v + <\eta> - \frac{\del U}{\del x} $

$ <\eta(t) \eta(t')> = 2 T k_b \lambda \delta(t-t') $

This simulator uses Euler's integration to simulate the position and velocity of a particle. 

Installation
---------
To install this simulator, run the following commands from the terminal:

`git clone https://github.com/hgandhi2411/Langevin.git
pip install Langevin`

Usage
-----
The simulator has a command line interface where the user can input initial position, initial velocity, temperature, damping coefficient, total time for which simulation must run and the time step. In addition, the model also takes as input a file which specifies the potential energy associated with position of the particle. The command line options are as below.

`optional arguments:
  -h, --help            show this help message and exit
  -x0 [INITIAL_POSITION], --initial_position [INITIAL_POSITION]
                        Initial position of the molecule, default = 1
  -v0 [INITIAL_VELOCITY], --initial_velocity [INITIAL_VELOCITY]
                        Velocity of particle at initial position, default = 0.1
  -temp [TEMPERATURE], --temperature [TEMPERATURE]
                        Temperature at which simulation runs, default = 1
  -dc [DAMPING_COEFF], --damping_coeff [DAMPING_COEFF]
                        Damping coefficient for the system, default = 1
  -dt [TIME_STEP], --time_step [TIME_STEP]
                        Time step for simulation, default = 0.1
  -t [TOTAL_TIME], --total_time [TOTAL_TIME]
                        Total time for which simulation should run, default = 1
  --input_file [INPUT_FILE]
                        Specify the path of input file, default = './Lans/Pot_example.txt'
  --out_file [OUT_FILE]
                        Specify file path where you want output, default = './Lans/output.txt' `

Output is in the form of a file which contains position and velocity for each time step.

License
-----
(c) 2017
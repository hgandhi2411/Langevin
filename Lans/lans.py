import numpy as np
import asyncio
from .visualization import SimVis, start_server
import argparse


def ReadEnergy(input_file):
    '''Reading potential energy from an input file'''
    data = np.transpose(np.genfromtxt(input_file, delimiter = ' ', skip_header = 1, dtype = float))
    return data[1], data[2], data[3]

def CreateParser():
    '''Creating a parser for command line options for this simulator'''
    parser = argparse.ArgumentParser(description = "Inputs to get Langevin Simulator started")
    parser.add_argument('-x0', '--initial_position', nargs = '?', type = float, default = 1, help = 'Initial position of the molecule' )
    parser.add_argument('-v0', '--initial_velocity', nargs = '?', type = float, default = 0.1, help = 'Velocity of particle at initial position')
    parser.add_argument('-temp','--temperature', nargs = '?', type = float, default = 1, help = 'Temperature at which simulation runs')
    parser.add_argument('-dc', '--damping_coeff', nargs = '?', type = float, default = 1, help = 'Damping coefficient for the system')
    parser.add_argument('-dt', '--time_step', nargs = '?', type = float, default = 1, help = 'Time step for simulation')
    parser.add_argument('-t', '--total_time', nargs = '?', type = float, default = 1, help = 'Total time for which simulation should run')
    parser.add_argument('--input_file', nargs = '?', type = str, default = './Pot_example.txt', help = 'Specify the path of input file')
    parser.add_argument('--out_file', nargs = '?', type = str, default = './output.txt', help = 'Specify file path where you want output')
    return parser

def GetInputs(): 
    parser = CreateParser()
    args = parser.parse_args()
    if(args.damping_coeff<=0 or args.temperature<=0 or args.time_step<=0 or args.total_time<=0):
        raise ValueError("Damping coefficient, temperature, time_step and total_time must be non-zero positive values")
    else:
        return args.initial_position, args.initial_velocity, args.temperature, args.damping_coeff, args.time_step, args.total_time, args.input_file, args.out_file

kb = 1
x0, v0, temp, Lambda, dt, time, input_file, out_file = GetInputs()

def Random(T, l):
    '''Calculate the random component of force i.e. solvent force'''
    solvent_force = np.random.normal(loc = 0, scale = (2*T*l*kb)**0.5, size = 1)
    return solvent_force

def PotentialForce(x, input_file):
    '''Calculates and return the potential force'''
    pos, force, energy = ReadEnergy(input_file)
    potential_force = np.interp(x, pos, energy)
    return potential_force



async def main(sv): # pragma: no cover
    #create a simple energy
    x, f, y = ReadEnergy('./Lans/Pot_example.txt')

    sv.set_energy(x, y)

    while True:
        sv.set_position(np.random.random(1))
        await asyncio.sleep(0.5)

def start():    # pragma: no cover
    sv = SimVis()
    start_server(sv)
    asyncio.ensure_future(main(sv))
    loop = asyncio.get_event_loop()
    loop.run_forever()
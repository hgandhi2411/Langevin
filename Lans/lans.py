import numpy as np
import asyncio
from .visualization import SimVis, start_server
import argparse
import matplotlib.pyplot as plt


def ReadEnergy(input_file):
    '''Reading potential energy from an input file'''
    data = np.transpose(np.genfromtxt(input_file, delimiter = ' ', skip_header = 1, dtype = float))
    return data[1], data[2], data[3]

def CreateParser():
    '''Creating a parser for command line options for this simulator'''
    parser = argparse.ArgumentParser(description = "Inputs to get Langevin Simulator started")
    parser.add_argument('-x0', '--initial_position', nargs = '?', type = float, default = 1, help = 'Initial position of the molecule, default = 1' )
    parser.add_argument('-v0', '--initial_velocity', nargs = '?', type = float, default = 0.1, help = 'Velocity of particle at initial position, default = 0.1')
    parser.add_argument('-temp','--temperature', nargs = '?', type = float, default = 1, help = 'Temperature at which simulation runs, default = 1')
    parser.add_argument('-dc', '--damping_coeff', nargs = '?', type = float, default = 1, help = 'Damping coefficient for the system, default = 1')
    parser.add_argument('-dt', '--time_step', nargs = '?', type = float, default = 0.1, help = 'Time step for simulation, default = 0.1')
    parser.add_argument('-t', '--total_time', nargs = '?', type = float, default = 1, help = 'Total time for which simulation should run, default = 1')
    parser.add_argument('--input_file', nargs = '?', type = str, default = './Lans/Pot_example.txt', help = 'Specify the path of input file, default = \'./Lans/Pot_example.txt\'')
    parser.add_argument('--out_file', nargs = '?', type = str, default = './Lans/output.txt', help = 'Specify file path where you want output, default = \'./Lans/output.txt\' ')
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
N = int(time/dt)
pos, force, energy = ReadEnergy(input_file)

def Random(T, l):
    '''Calculate and return the random component of force i.e. solvent force'''
    solvent_force = np.random.normal(loc = 0, scale = (2*T*l*kb)**0.5, size = 1)
    return float(solvent_force)

def PotentialForce(x, pos, energy):
    '''Calculate and return the potential force'''
    potential_force = np.interp(x, pos, energy)
    return potential_force

def DragForce(l, v):
    '''Calculate and return the drag component of force'''
    return -l*v

def Euler(position, velocity):
    acc = DragForce(Lambda, velocity) + Random(temp, Lambda) + PotentialForce(position, pos, energy)
    velocity += acc*dt
    position += velocity*dt
    return acc, velocity, position

async def main(sv): 
    '''Run simulation and send real-time position to visualization'''
    kb = 1
    x0, v0, temp, Lambda, dt, total_time, input_file, out_file = GetInputs()
    N = int(total_time/dt)
    pos, force, energy = ReadEnergy(input_file)
    position = x0
    velocity = v0
    time = 0
    count = 0
    x, y = pos, energy
    sv.set_energy(x, y)

    f = open(out_file, 'w')
    f.write('index time position velocity\n')
    for i in range(N):
        sv.set_position(position)
        new_acc, new_vel, new_pos = Euler(position, velocity)
        time += dt
        count += 1
        f.write('{} {:.4f} {:.4f} {:.4f}\n'.format(count, time, new_pos, new_vel))
        position = new_pos
        velocity = new_vel
        await asyncio.sleep(0.05)
    print('Final position = {:.4f}, Final velocity = {:.4f}'.format(position, velocity))
    f.close()
    return None
    

def start():    # pragma: no cover
    sv = SimVis()
    start_server(sv)
    asyncio.ensure_future(main(sv))
    loop = asyncio.get_event_loop()
    loop.run_forever()
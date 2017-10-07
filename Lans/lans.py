import numpy as np
import asyncio
from .visualization import SimVis, start_server
import argparse


class Langevin():
    
    def read_energy(input_file):
        '''Reading potential energy from an input file'''
        data = np.transpose(np.genfromtxt(input_file, delimiter = ' ', skip_header = 1, dtype = float))
        pos = data[1]
        force = data[2]
        energy = data[3]
        return pos, force, energy

    def create_parser():
        '''Creating a parser for command line options for this simulator'''
        parser = argparse.ArgumentParser(description = "Inputs to get Langevin Simulator started")
        parser.add_argument('-x0', '--initial_position', nargs = '?', type = float, default = 1, help = 'Initial position of the molecule' )
        parser.add_argument('-v0', '--initial_velocity', nargs = '?', type = float, default = 0.1, help = 'Velocity of particle at initial position')
        parser.add_argument('-temp','--temperature', nargs = '?', type = float, default = 27, help = 'Temperature in degree celsius')
        parser.add_argument('-dc', '--damping_coeff', nargs = '?', type = float, default = 1, help = 'Damping coefficient for the system')
        parser.add_argument('-dt', '--time_step', nargs = '?', type = float, default = 1, help = "Time step for simulation (seconds)" )
        parser.add_argument('-t', '--total_time', nargs = '?', type = float, default = 1, help = "Total time for which simulation should run (seconds)")
        return parser

    def get_inputs(): 
        parser = create_parser()
        args = parser.parse_args()
        return args.initial_position, args.initial_velocity, args.temperature, args.damping_coeff, args.time_step, args.total_time

    async def main(sv): # pragma: no cover
        #create a simple energy

        x = np.linspace(-1, 1, 100)
        y = x**2
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
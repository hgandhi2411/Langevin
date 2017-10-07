import io
import Lans
import numpy as np
import argparse
import unittest


class Test_Langevin(unittest.TestCase):
    
    def test_read_energy_read(self):
        '''Tests if the function reads and returns correctly for given input file'''

        pos, force, energy = Lans.read_energy(r"c:\Users\hetag\Desktop\CHE477\Langevin\tests\testfile.txt")
        assert(np.isclose(pos, [0.0001,0.010099,0.020099,0.030098])).all()
        assert(np.isclose(force, [0.010675, 0.010675, 0.010675, 0.012945])).all()
        assert(np.isclose(energy, [-0.113475, -0.113475, -0.113475, -0.060178])).all()

    def test_inputs(self):
        ''' Tests if the parser reads correctly and if no inputs are given, uses default values'''
        self.parser = Lans.create_parser()
        parsed = self.parser.parse_args(['--initial_velocity', '2.5', '--total_time', '20', '--damping_coeff', '0.1'])
        self.assertEqual([parsed.initial_position, parsed.initial_velocity, parsed.time_step, parsed.total_time, parsed.temperature, parsed.damping_coeff], [1, 2.5, 1, 20, 27, 0.1])
        
        self.results = Lans.get_inputs()
        self.assertEqual(self.results, (1,0.1,27,1,1,1))
        

import io
import Lans
import numpy as np
import argparse
import unittest

class Test_Langevin(unittest.TestCase):
    
    def test_read_energy_read(self):
        '''Tests if the function reads and returns correctly for given input file'''
        pos, force, energy = Lans.ReadEnergy(r"./tests/testfile.txt")
        assert(np.isclose(pos, [0.0001,0.010099,0.020099,0.030098])).all()
        assert(np.isclose(force, [0.010675, 0.010675, 0.010675, 0.012945])).all()
        assert(np.isclose(energy, [-0.113475, -0.113475, -0.113475, -0.060178])).all()

    def test_inputs(self):
        ''' Tests if the parser reads correctly and if no inputs are given, uses default values'''
        self.parser = Lans.CreateParser()
        parsed = self.parser.parse_args(['--initial_velocity', '2.5', '--total_time', '20', '--damping_coeff', '0.1', '--input_file', 'C:/Users/hetag/Desktop/input.txt'])
        self.assertEqual([parsed.initial_position, parsed.initial_velocity, parsed.time_step, parsed.total_time, parsed.temperature, parsed.damping_coeff, parsed.input_file], [1, 2.5, 1, 20, 27, 0.1, 'C:/Users/hetag/Desktop/input.txt'])

        self.results = Lans.GetInputs()
        self.assertEqual(self.results, (1,0.1,27,1,1,1, './Pot_example.txt', './output.txt'))


        

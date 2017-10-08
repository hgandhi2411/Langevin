import io
import Lans
import numpy as np
import argparse
import unittest

class Test_Langevin(unittest.TestCase):
    
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
        
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
        self.assertEqual([parsed.initial_position, parsed.initial_velocity, parsed.time_step, parsed.total_time, parsed.temperature, parsed.damping_coeff, parsed.input_file], [1, 2.5, 1, 20, 1, 0.1, 'C:/Users/hetag/Desktop/input.txt'])

        self.results = Lans.GetInputs()
        self.assertEqual(self.results, (1,0.1,1,1,1,1, './Lans/Pot_example.txt', './Lans/output.txt')) 

    def test_random(self):
        '''Tests if random generator works fine'''
        self.assertEqual(Lans.Random(1,0), 0)

    def test_potential_force(self):
        '''Tests the function producing potential force'''
        sample_pos = [0,1,2,3,4,5]
        sample_energy = [0,10,20,30,40,50]
        self.assertEqual(Lans.PotentialForce(2.5,sample_pos,sample_energy), 25)

    def test_drag_force(self):
        self.assertEqual(Lans.DragForce(0.5, 2), -1)

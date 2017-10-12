import io
import os
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
        # Tests if the parser reads correctly and if no inputs are given, uses default values
        self.parser = Lans.CreateParser()
        parsed = self.parser.parse_args(['--initial_velocity', '2.5', '--total_time', '20', '--damping_coeff', '0.1', '--input_file', 'C:/Users/hetag/Desktop/input.txt'])
        self.assertEqual([parsed.initial_position, parsed.initial_velocity, parsed.time_step, parsed.total_time, parsed.temperature, parsed.damping_coeff, parsed.input_file], [1, 2.5, 0.1, 20, 1, 0.1, 'C:/Users/hetag/Desktop/input.txt'])
        '''
        self.results = list(Lans.GetInputs())
        self.assertEqual(self.results, [1,0.1,1,1,0.1,1, './Lans/Pot_example.txt', './Lans/output.txt']) 
        self.assertTrue(os.path.exists(self.results[6])), 'input file doesn\'t exist'
        '''
    kb = 1

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

    def test_euler(self):
        '''Tests if the force, position and velocity calculated are correct'''
        self.pos = 1
        self.vel = 1
        data = [[1, 2, 3, 4], [10, 20, 30, 40]]
        self.assertEqual(Lans.Euler(self.pos, self.vel, 0, 1, *data, dt = 0.5), (-10, -4, -1))

    def test_write_output(self):
        '''Tests if the output file is written correctly'''
        test_string = [[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]]
        test_string2 = '1 2.0000 3.0000 4.0000 \n'
        test_string3 = '5 6.0000 7.0000 8.0000 \n' 
        out_file = './tests/test_output.txt'
        Lans.write_output(out_file, test_string)
        f = open(out_file, 'r')
        test_data = list(f.readlines())
        f.close()
        self.assertEqual(test_data[1], test_string2)
        self.assertEqual(test_data[2], test_string3)

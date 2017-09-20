import Lans
import io
import numpy as np

def test_read_energy_read():
    '''TEsts if the function reads and returns for given input file'''

    test_string = '''
    #test input enegry
    #x energy
    0   -2
    1   -1
    2    0
    3    0
    4    3
    '''
    #''' starts literal mode

    test_file = io.StringIO(test_string)
    pos, energy = Lans.read_energy(test_file)
    assert(np.isclose(pos, [0,1,2,3,4]))
    assert(np.isclose(energy, [-2, -1, 0, 0, 3]))

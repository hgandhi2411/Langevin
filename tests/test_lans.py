import Lans
import io
import numpy as np

def test_read_energy_read():
    '''TEsts if the function reads and returns correctly for given input file'''

    pos, energy = Lans.read_energy(r"C:\Users\hetag\Desktop\CHE477\Langevin\testfile.txt")
    assert(np.isclose(pos, [0,1,2,3,4])).all()
    assert(np.isclose(energy, [-2, -1, 0, 0, 3])).all()


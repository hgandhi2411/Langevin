import numpy as np

def read_energy(input_file):
    data = np.genfromtxt(input_file, delimiter = ' ', skip_header=1)
    data = np.transpose(data)
    return data[0], data[1]

def start():
    print("Welcome to the Langevin Simulator!!!\n Starting up...")
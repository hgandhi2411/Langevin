import numpy as np
import asyncio
from .visualization import SimVis, start_server

def read_energy(input_file):
    data = np.genfromtxt(input_file, delimiter = ' ', skip_header=1)
    data = np.transpose(data)
    return data[0], data[1]

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
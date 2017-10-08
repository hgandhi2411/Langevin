'''Minimal sevrer to send/receive updates via HTTP instead of ZMQ'''

import tornado.web
from tornado.platform.asyncio import AsyncIOMainLoop
import asyncio
import os
import io
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

AsyncIOMainLoop().install()
RESOURCES = os.path.join(os.path.dirname(__file__), os.pardir, 'resources')

class SimVis:
    def __init__(self):
        pass
    
    def set_energy(self, pos, energy):
        self.energy = pos, energy

    def set_position(self, x):
        self.pos = x
        asyncio.sleep(0)

    def plot(self):
        fig = plt.figure()
        plt.plot(*self.energy, '-', label='potential energy')
        # get potential energy nearest to current position
        idx = (np.abs(self.energy[0] - self.pos)).argmin()
        pos_e = self.energy[1][idx]
        plt.plot(self.pos, pos_e, 'ro', label='current position')
        plt.legend()
        plt.xlabel('Position')
        plt.ylabel('Energy')
        plt.tight_layout()
        with io.BytesIO() as output:
            fig.savefig(output, format='jpg')
            plt.clf()
            plt.close('all')
            return output.getvalue()
        
class HtmlPageHandler(tornado.web.RequestHandler):
    async def get(self, file_name='index.html'):
        # Check if page exists
        www = os.path.join(RESOURCES, file_name)
        if os.path.exists(www):
            # Render it
            self.render(www)
        else:
            # Page not found, generate template
            err_tmpl = tornado.template.Template("<html> Err 404, Page {{ name }} not found</html>")
            err_html = err_tmpl.generate(name=file_name)
            # Send response
            self.finish(err_html)

class StreamHandler(tornado.web.RequestHandler):
    def initialize(self, simulation):
        self.simulation = simulation

    async def get(self):
        '''
        Build MJPEG stream using the multipart HTTP header protocol
        '''
        # Set http header fields
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.set_header('Cache-Control',
                        'no-store, no-cache, must-revalidate, pre-check=0, post-check=0, max-age=0')
        self.set_header('Connection', 'close')
        self.set_header('Content-Type', 'multipart/x-mixed-replace;boundary=--boundarydonotcross')
        self.set_header( 'Pragma', 'no-cache')
        print('Received request, sending stream')

        while True:
            if self.request.connection.stream.closed():
                print('Request closed')
                return
            jpeg = self.simulation.plot()
            img = jpeg
            self.write("--boundarydonotcross\n")
            self.write("Content-type: image/jpeg\r\n")
            self.write("Content-length: %s\r\n\r\n" % len(img))
            self.write(img)
            await tornado.gen.Task(self.flush)
            await asyncio.sleep(0)
            del jpeg

def start_server(simulation, port=8888):
    app = tornado.web.Application([
        (r"/",HtmlPageHandler),
        (r"/stream.mjpg", StreamHandler, {'simulation': simulation})
    ])
    print('Starting server on port {}'.format(port))
    app.listen(port)
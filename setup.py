from distutils.core import setup

with open('Redme.md') as f:
      long_description = ''.join(f.readlines())

setup(name='Langevin',
      version='0.1',
      description='Langevin Simulator',
      author='Heta Gandhi',
      author_email='hgandhi@ur.rochester.edu',
      packages=['Lans'],
     )
     
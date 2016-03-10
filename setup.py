#!/usr/bin/env python

#from distutils.core import setup
from setuptools import setup, find_packages

setup(name='pyOmniDriver',
      version='0.1',
      description='A python interface to the Ocean Optics OmniDriver',
      author='Catherine Holloway',
      author_email='milankie@gmail.com',
      url='https://github.com/CatherineH/pyOmniDriver',
      py_modules=['spectrometer'],
      #packages=[''],
      package_dir={"": "src"},
      package_data={'': ['bin/SpectrometerServer.class']},
      include_package_data=True,
      install_requires=[]
     )


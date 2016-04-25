#!/usr/bin/env python

from setuptools import setup, find_packages

print(find_packages())

setup(name='pyOmniDriver',
      version='0.1',
      description='A python interface to the Ocean Optics OmniDriver',
      author='Catherine Holloway',
      author_email='milankie@gmail.com',
      url='https://github.com/CatherineH/pyOmniDriver',
      zip_safe=False,
      packages=find_packages(),
      #package_dir={'spectrometer': ''},
      package_data={
        'spectrometer': ['SpectrometerServer.class'],
      })
#!/usr/bin/env python

from distutils.core import setup

setup(name='pyOmniDriver',
      version='0.1',
      description='A python interface to the Ocean Optics OmniDriver',
      author='Catherine Holloway',
      author_email='milankie@gmail.com',
      url='https://github.com/CatherineH/pyOmniDriver',
      py_modules=['spectrometer'],
      #packages=['spectrometer'],
      package_dir={"" : "src"}
     )
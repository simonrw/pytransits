#!/usr/bin/env python

from setuptools import setup
from setuptools.extension import Extension
from Cython.Build import cythonize
from numpy import get_include

package_name = 'transitgen'

libraries = ['stdc++'] if os.uname()[0] == 'Darwin' else []

ext_modules = [
    Extension('{}._Modelgen'.format(package_name),
              ['{}/_Modelgen.pyx'.format(package_name),
               'Modelgen/src/GenerateModel.cpp'],
              language='c++',
              include_dirs=['Modelgen/include', get_include()],
              libraries=libraries,
              )]


setup(name=package_name,
      version='0.0.1',
      author='Simon Walker',
      author_email='s.r.walker101@googlemail.com',
      license='MIT',
      packages=[package_name, ],
      ext_modules=cythonize(ext_modules),
      )

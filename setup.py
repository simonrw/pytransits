#!/usr/bin/env python

from setuptools import setup
from setuptools.extension import Extension
from Cython.Distutils import build_ext
from numpy import get_include


setup(name='transitgen',
      version='0.0.1',
      author='Simon Walker',
      author_email='s.r.walker101@googlemail.com',
      license='MIT',
      packages=['transitgen',],
      ext_modules=[Extension(
          "transitgen._Modelgen", ['transitgen/_Modelgen.pyx', 'Modelgen/src/GenerateModel.cpp'],
          language="c++", include_dirs=['Modelgen/include', get_include()]), ],
      cmdclass={'build_ext': build_ext, }
)

#!/usr/bin/env python

from setuptools import setup
from setuptools.extension import Extension
from Cython.Distutils import build_ext
from numpy import get_include


setup(ext_modules=[Extension(
    "_Modelgen", ['_Modelgen.pyx', 'Modelgen/src/GenerateModel.cpp'],
    language="c++", include_dirs=['Modelgen/include', get_include()]), ],
    cmdclass={'build_ext': build_ext, }
    )

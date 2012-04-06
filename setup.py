#!/usr/bin/env python

from distutils.core  import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
from numpy import get_include


setup(ext_modules=[Extension(
    "Modelgen", ['Modelgen.pyx', 'Modelgen/src/GenerateModel.cpp'],
    language="c++", include_dirs=['Modelgen/include', get_include()]), ],
    cmdclass={'build_ext': build_ext, }
    )

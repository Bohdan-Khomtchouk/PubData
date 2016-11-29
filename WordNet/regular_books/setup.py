from distutils.core import setup
from Cython.Build import cythonize

setup(name='general',
      ext_modules=cythonize("general.pyx"),)

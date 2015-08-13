from distutils.core import setup
from Cython.Build import cythonize

# python compile.py build_ext --inplace --compiler=msvc
setup(
    ext_modules=cythonize("_bbn.pyx"),
)

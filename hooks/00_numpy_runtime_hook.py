# This must run before Torch or anything else
import builtins
import importlib

# Force NumPy C extensions to load
import numpy
import numpy.core._multiarray_umath

# Some packages check builtins._NUMPY_AVAILABLE; ensure PyTorch sees NumPy
builtins._NUMPY_AVAILABLE = True


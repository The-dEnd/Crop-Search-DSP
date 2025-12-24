# hooks/hook-torch.py
from PyInstaller.utils.hooks import collect_submodules

# Include Python modules only
hiddenimports = collect_submodules('torch')

# Prevent PyInstaller from scanning Torch binaries for CUDA shared libraries
binaries = []
datas = []


import os
import sys

os.environ["TORCH_DISABLE_DYNAMO"] = "1"
os.environ["TORCH_COMPILE"] = "0"


if hasattr(sys, '_MEIPASS'):
    torch_lib_path = os.path.join(sys._MEIPASS, 'torch', 'lib')
    os.environ['LD_LIBRARY_PATH'] = (
        torch_lib_path + ':' + os.environ.get('LD_LIBRARY_PATH', '')
    )


import os
import sys

# Force Qt to use PyQt's plugins, not OpenCV's
if hasattr(sys, '_MEIPASS'):
    qt_plugin_path = os.path.join(sys._MEIPASS, 'PyQt5', 'Qt5', 'plugins')
    if os.path.exists(qt_plugin_path):
        os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = qt_plugin_path


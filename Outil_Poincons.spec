# -*- mode: python ; coding: utf-8 -*-
import os
import cv2

datas = []

# Add only necessary files for cv2 (config + data)
cv2_dir = os.path.dirname(cv2.__file__)

# Add any config*.py files
for fname in os.listdir(cv2_dir):
    if fname.startswith('config') and fname.endswith('.py'):
        datas.append((os.path.join(cv2_dir, fname), 'cv2'))

# Add data directory if present (haarcascades, etc.)
cv2_data_dir = os.path.join(cv2_dir, 'data')
if os.path.exists(cv2_data_dir):
    datas.append((cv2_data_dir, 'cv2/data'))

a = Analysis(
    ['display.py'],
    pathex=['.'],
	excludes=['cv2'], 
    binaries=[],
    datas=datas + [
        ('resources/', 'resources/'),
        ('tmp/', 'tmp/'),
        ('doc/', 'doc/'),
		('libs/cv2/', 'cv2/'),
		('libs/ultralytics/', 'ultralytics/'),
		('libs/torchvision-0.22.1.dist-info/', 'torchvision-0.22.1.dist-info/'),
		('libs/torchvision/', 'torchvision/'),
        ('models/', 'models/')
    ],
    hiddenimports=[
        'sklearn.externals.array_api_compat.numpy.fft',
		'requests',
		'seaborn',
    ],
    hookspath=['hooks'],
    hooksconfig={},
    runtime_hooks=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Outil_poincons',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon="resources/media/icon.ico",
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Outil_poincons'
)

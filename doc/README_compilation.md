This document covers the compilation progress of the Python code into an executable format. The syntax is designed for Windows, but should be very similar for Linux compilation.
Of course, all necessary Python packages and libraries must be installed before compiling. Please refer to the requirements.txt file for a list of packages to install.

The application was developped under Python 3.11, with following packages:
PyQt5                     5.15.9
PyQt5-Qt5                 5.15.2
PyQt5-sip                 12.12.2
PyQt5Designer             5.14.1
imagesize                 1.4.1
pillow                    11.1.0
joblib                    1.5.1
torch                     2.7.1
torchvision               0.22.1
opencv-python             4.11.0.86
numpy                     2.1.2


To compile:

_Windows_
rm dist -Recurse; rm build -Recurse; ~\AppData\Local\Programs\Python\Python311\Scripts\pyinstaller.exe --clean -y .\Outil_Poincons.spec

Then you can run the following command:
mv .\dist\Outil_poincons\_internal\doc .\dist\Outil_poincons\; mv .\dist\Outil_poincons\_internal\models .\dist\Outil_poincons\; mv .\dist\Outil_poincons\_internal\resources .\dist\Outil_poincons\; mv .\dist\Outil_poincons\_internal\tmp .\dist\Outil_poincons\;rm .\dist\Outil_poincons\_internal\torch\lib\dnnl.lib;rm .\dist\Outil_poincons\_internal\cv2\opencv_videoio_ffmpeg4110_64.dll

It will:
-move the following from _internal folder to the same level than the .exe file:
doc/
resources/
tmp/
models/
Thisis necessary for the compiled version to work as expected.

-in _internal/, remove:
torch/lib/dnnl.lib (700MB file)
torch/lib/*cuda*/
cv2/opencv_videoio_ffmpeg4110_64.dll
This will save some space.

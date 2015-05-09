# CannyBot
getting the NAO Robot to draw the shapes it "sees" using OpenCV

![screenshot](/debug/NAOVISION.png)

*Currently works on Windows, see notes below!*

To run just enter into terminal,
* python CannyBot.py

Dependencies:
* Python 2.7.8 / Anaconda
* NAO Python SDK for Windows
* OpenCV 2.3.1 (only version that currently runs on NAO)

## OpenCV Setup

On Windows:
* http://docs.opencv.org/trunk/doc/py_tutorials/py_setup/py_setup_in_windows/py_setup_in_windows.html

On OSX:
* brew tap homebrew/science
* brew install opencv
* cd /usr/local/Cellar/opencv/2.x.x/
* cd /Library/Python/2.7/site-packages/
* ln -s /usr/local/Cellar/opencv/2.x.x/lib/python2.7/site-packages/cv.py cv.py
* ln -s /usr/local/Cellar/opencv/2.x.x/lib/python2.7/site-packages/cv2.so cv2.so
* Done!

On Ubuntu:
* sudo apt-get update
* sudo apt-get upgrade
* sudo apt-get dist-upgrade
* sudo apt-get install build-essential cmake
* sudo apt-get install python-dev python-tk python-numpy python3-dev python3-tk python3-numpy
* sudo apt-get install sudo apt-get install libopencv-dev
* Done!

## Notes
Was not able to test on other operating systems because we did not have access to the other SDKs.

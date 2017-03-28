# iMouse
Controlling the Laptop mouse using only head movements. A proof of concept prototype to help realize the possibilities which will help quadriplegia patients use a Laptop.

## How to use
For common users:
Extract the iMouse_test1_windows.zip and run the iMouse.exe file.
Users are advised not to use this while wearing sepctacles. A good camera is recommended for better results.

For developers:
1. Download the Code folder
2. Install OpenCV
3. Run iMouse_test1.py

## How it works
A simple haarcascade classification is done to first detect eyes of the user. The centroid of the eyes is used to move the mouse pointer after interpolation. A mean filter is applied on the centroid values for smoother results.

## How can you contribute
Developers can try and make this more dependable and reliable by using better Machine Learning techniques. Also left click, right click can be added via eye blinks. Feel free to fork! 

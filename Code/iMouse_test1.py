import numpy as np
import cv2
import win32api
from imutils.video import WebcamVideoStream
import win32api, win32con

def left_click(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
    
def right_click(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,x,y,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,x,y,0,0)


eye_cascade1 = cv2.CascadeClassifier('xml/haarcascade_mcs_eyepair_big.xml')
eye_cascade2 = cv2.CascadeClassifier('xml/haarcascade_mcs_eyepair_small.xml')
eye_cascade3 = cv2.CascadeClassifier('xml/haarcascade_eye_tree_eyeglasses.xml')
eye_cascade4 = cv2.CascadeClassifier('xml/haarcascade_eye.xml')

window_size = 5
windowX = []
windowY = []

cap = WebcamVideoStream(src=0).start()

mx = 0
my = 0

upper_mx = 0
lower_mx = 0

upper_my = 0
lower_my = 0

start_flag = True

while True:
    img = cap.read()
    img = cv2.flip(img, 1)

    cv2.normalize(img, img, 0, 255, cv2.NORM_MINMAX)

    img_yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)

    # equalize the histogram of the Y channel
    img_yuv[:,:,0] = cv2.equalizeHist(img_yuv[:,:,0])

    # convert the YUV image back to RGB format
    img = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    gray = clahe.apply(gray)
    
    eyes = eye_cascade1.detectMultiScale(gray)
    if len(eyes) == 0:
        eyes = eye_cascade2.detectMultiScale(gray)

    area = 0
    x = 0
    y = 0
    w = 0
    h = 0
        
    for (ex,ey,ew,eh) in eyes:
        if ew*eh > area:
            x = ex
            y = ey
            h = eh
            w = ew
            area = w*h

    if area > 0:
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
        cv2.rectangle(img,(x+w/2-5,y+h/2-5),(x+w/2+5,y+h/2+5),(255,0,0),2)
        mx = x + w/2
        my = y + h/2
        roi_gray = gray[y-20:y+h+20, x-20:x+w+20]
        roi_color = img[y-20:y+h+20, x-20:x+w+20]

        '''
        eyesLR = eye_cascade3.detectMultiScale(roi_gray)
        if len(eyesLR) == 0:
            eyesLR = eye_cascade4.detectMultiScale(roi_gray)
        
        for (ex,ey,ew,eh) in eyesLR:
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,0,255),2)
        '''
        
        if start_flag == True:
            upper_mx = mx + 35
            lower_mx = mx - 20
            upper_my = my + 35
            lower_my = my - 20
            start_flag = False
            
        mx = np.interp(mx,[lower_mx,upper_mx],[0,1366])
        my = np.interp(my,[lower_my,upper_my],[0,768])

        windowX.append(mx)
        windowY.append(my)

        if len(windowX) > window_size:
            del windowX[0]
        if len(windowY) > window_size:
            del windowY[0]

        mx = int(np.mean(windowX))
        my = int(np.mean(windowY))
        
        win32api.SetCursorPos((mx,my))


    img = cv2.resize(img, (0,0), fx=0.5, fy=0.5)
    cv2.imshow('img',img)
    print "mx: " + str(mx) + " ! my: " + str(my)
    if cv2.waitKey(1) == ord('q'):
        break
    
cap.stop()
cv2.destroyAllWindows()

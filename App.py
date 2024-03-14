import cv2 as cv
import numpy as np
import os
import pyautogui
from time import time
import win32gui
import win32ui
import win32con

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def Za_Capture(box_size=(500, 500)):
    w, h = box_size

    # Get screen res
    screen_width, screen_height = pyautogui.size()

    # locates middle of the screen
    box_x = (screen_width - w) // 2
    box_y = (screen_height - h) // 2

    hwnd = None

    wDC = win32gui.GetWindowDC(hwnd)
    dcObj = win32ui.CreateDCFromHandle(wDC)
    cDC = dcObj.CreateCompatibleDC()
    dataBitMap = win32ui.CreateBitmap()
    dataBitMap.CreateCompatibleBitmap(dcObj, w, h)
    cDC.SelectObject(dataBitMap)
    cDC.BitBlt((0, 0), (w, h), dcObj, (box_x, box_y), win32con.SRCCOPY)
    bmpinfo = dataBitMap.GetInfo()
    bmpstr = dataBitMap.GetBitmapBits(True)

    captured_image = np.fromstring(bmpstr, dtype='uint8')
    captured_image.shape = (h, w, 4)

    dcObj.DeleteDC()
    cDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, wDC)
    win32gui.DeleteObject(dataBitMap.GetHandle())

    return captured_image

    # Display 

loopt = time()
while(True):
    ss = Za_Capture((500, 500))
    cv.imshow('Screen Capture', ss)

    print('FPS {}'.format(1 / (time() - loopt)))
    loopt = time()

    cv.waitKey(1)
    # end
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break


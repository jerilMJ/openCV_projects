'''
Python Painting App made using OpenCV functions along with numpy
This app is just for testing various OpenCV drawing features.

OpenCV version: 4.1.1
'''

import cv2 as cv
import numpy as np

# font used for text
font = cv.FONT_HERSHEY_DUPLEX

drawing = False
rectangle = False
line = False

fillPercentage = 1
fillShape = True

circleSize = 70
lineSize = 6

menuFontSize = 0.8

toolSpecColor = (100, 150, 255)
colors = [(0, 0, 0), (255, 0, 0), (0, 255, 0),
          (0, 0, 255), (255, 255, 255)]
colorIndex = 1

# Coordinates of top-left and bottom-right vertices of rectangle
rectTop = tuple()
rectBot = tuple()
# To store previous coords for deleting corner-indicators
prevTop = tuple()
prevBot = tuple()

# Coordinates of line end-points
lpoint1 = tuple()
lpoint2 = tuple()
# Same as rectangle
prevlpoint1 = tuple()
prevlpoint2 = tuple()

# Creating blank black canvas with numpy
img = np.zeros((512, 512, 3), np.uint8)
menu = np.zeros((512, 512, 3), np.uint8)

# Finding max width and height of the menu window
menuWidth = menu.shape[1]
menuHeight = menu.shape[0]

# Function that triggers upon specific mouse events


def draw_stuff(event, x, y, flags, param):
    global circleSize
    global colors
    global colorIndex
    global drawing
    global rectTop
    global rectBot
    global lpoint1
    global lpoint2

    if not rectangle and not line and event == cv.EVENT_LBUTTONDOWN:
        drawing = True
    elif event == cv.EVENT_LBUTTONUP:
        drawing = False
    elif event == cv.EVENT_MOUSEMOVE:
        if drawing:
            if fillShape:   # -1 means fill the entire area
                cv.circle(img, (x, y), circleSize, colors[colorIndex], -1)
            else:
                cv.circle(img, (x, y), circleSize, colors[colorIndex], int(
                    circleSize*2*(fillPercentage/10)))
    elif event == cv.EVENT_MOUSEWHEEL:
        if flags > 0:
            if colorIndex + 1 == len(colors):
                colorIndex = 0
            else:
                colorIndex += 1
        else:
            if colorIndex - 1 == -1:
                colorIndex = len(colors) - 1
            else:
                colorIndex -= 1
    elif event == cv.EVENT_LBUTTONDBLCLK and rectangle:
        global prevTop
        rectTop = (x, y)
        cv.line(img, (rectTop[0]+2, rectTop[1]+2),
                (rectTop[0]+2, rectTop[1]+2), toolSpecColor, 2)
        if len(prevTop) != 0:
            cv.line(img, (prevTop[0]+2, prevTop[1]+2),
                    (prevTop[0]+2, prevTop[1]+2), (0, 0, 0), 2)
        prevTop = rectTop
    elif event == cv.EVENT_RBUTTONDBLCLK and rectangle:
        global prevBot
        rectBot = (x, y)
        cv.line(img, (rectBot[0]-2, rectBot[1]-2),
                (rectBot[0]-2, rectBot[1]-2), toolSpecColor, 2)
        if len(prevBot) != 0:
            cv.line(img, (prevBot[0]-2, prevBot[1]-2),
                    (prevBot[0]-2, prevBot[1]-2), (0, 0, 0), 2)
        prevBot = rectBot
    elif rectangle and event == cv.EVENT_MBUTTONDOWN:
        if rectTop and rectBot:
            if fillShape:
                cv.rectangle(img, rectTop, rectBot, colors[colorIndex], -1)
            else:
                if rectBot[0] > rectTop[0]:
                    cv.rectangle(img, rectTop, rectBot, colors[colorIndex], int(
                        (rectBot[0]-rectTop[0])*(fillPercentage/10)))
                else:
                    cv.rectangle(img, rectTop, rectBot, colors[colorIndex], int(
                        (rectTop[0]-rectBot[0])*(fillPercentage/10)))
            rectTop = tuple()
            rectBot = tuple()
    elif line and event == cv.EVENT_LBUTTONDBLCLK:
        global prevlpoint1
        lpoint1 = (x, y)
        cv.line(img, (lpoint1[0], lpoint1[1]),
                (lpoint1[0], lpoint1[1]), toolSpecColor, 2)
        if len(prevlpoint1) != 0:
            cv.line(img, (prevlpoint1[0], prevlpoint1[1]),
                    (prevlpoint1[0], prevlpoint1[1]), (0, 0, 0), 2)
        prevlpoint1 = lpoint1
    elif line and event == cv.EVENT_RBUTTONDBLCLK:
        global prevlpoint2
        lpoint2 = (x, y)
        cv.line(img, (lpoint2[0], lpoint2[1]),
                (lpoint2[0], lpoint2[1]), toolSpecColor, 2)
        if len(prevlpoint2) != 0:
            cv.line(img, (prevlpoint2[0], prevlpoint2[1]),
                    (prevlpoint2[0], prevlpoint2[1]), (0, 0, 0), 2)
        prevlpoint2 = lpoint2
    elif line and event == cv.EVENT_MBUTTONDOWN:
        if lpoint1 and lpoint2:
            cv.line(img, lpoint1, lpoint2, colors[colorIndex], lineSize)
            lpoint1 = tuple()
            lpoint2 = tuple()


cv.namedWindow('menu')
cv.namedWindow('image')
cv.setMouseCallback('image', draw_stuff)
cv.rectangle(menu, (0, 0), (menuWidth, 40), (100, 99, 100), -1)
cv.putText(menu, "OpenCV - Paint: Menu",
           (0, 30), font, 1, (0, 255, 0), 2)
cv.putText(menu, "Current Tool: ", (0, 80), font,
           menuFontSize, (255, 255, 255), 1)

while(1):
    cv.imshow('image', img)
    cv.rectangle(menu, (menuWidth-50, 10),
                 (menuWidth-10, 30), colors[colorIndex], -1)
    if rectangle:
        cv.rectangle(menu, (0, 90), (menuWidth, menuHeight), (0, 0, 0), -1)
        cv.putText(
            menu, f"Top-left coords: {rectTop}", (0, 120), font, menuFontSize, toolSpecColor, 1)
        cv.putText(
            menu, f"Bottom-right coords: {rectBot}", (0, 160), font, menuFontSize, toolSpecColor, 1)
    elif not rectangle and not line:
        cv.rectangle(
            menu, (0, 90), (menuWidth, menuHeight), (0, 0, 0), -1)
        cv.putText(
            menu, f"Circle Size: {circleSize}", (0, 120), font, menuFontSize, toolSpecColor, 1)
        if fillShape:
            cv.circle(menu, (int(menuWidth/2+100), menuHeight-circleSize),
                      circleSize, toolSpecColor, -1)
        else:
            cv.circle(menu, (int(menuWidth/2+100), menuHeight-circleSize-100),
                      circleSize, toolSpecColor, int(circleSize*2*(fillPercentage/10)))
    else:
        cv.rectangle(
            menu, (0, 90), (menuWidth, menuHeight), (0, 0, 0), -1)
        cv.putText(
            menu, f"Line Size: {lineSize}", (0, 120), font, menuFontSize, toolSpecColor, 1)
        cv.line(menu, (int(menuWidth/4), int(menuHeight/2)),
                (int(3*menuWidth/4), int(menuHeight/2)), toolSpecColor, lineSize)

    if not line:
        cv.putText(menu, f"Fill Shape? {fillShape}",
                   (0, 200), font, menuFontSize, toolSpecColor, 1)
        if not fillShape:
            cv.putText(menu, f"Fill Percentage: {fillPercentage*10}",
                       (0, 240), font, menuFontSize, toolSpecColor, 1)
    cv.imshow('menu', menu)
    key = cv.waitKey(20) & 0xFF
    if key == 27:
        break
    elif key == ord('r'):
        rectangle = not rectangle
    elif key == ord('s'):
        fname = input('Input file name to save: ')
        cv.imwrite('./images/'+fname+'.jpeg', img)
    elif key == ord('d'):
        img = np.zeros((512, 512, 3), np.uint8)
    elif key == ord('+'):
        if not line and not rectangle:
            if circleSize + 5 > 100:
                circleSize = 5
            else:
                circleSize += 5
        else:
            if lineSize + 2 > 40:
                lineSize = 2
            else:
                lineSize += 2
    elif key == ord('-'):
        if not line and not rectangle:
            if circleSize - 5 < 5:
                circleSize = 100
            else:
                circleSize -= 5
        else:
            if lineSize - 2 < 2:
                lineSize = 40
            else:
                lineSize -= 2

    elif key == ord('f'):
        fillShape = not fillShape
        if not fillShape:
            try:
                fillPercentage = int(chr(cv.waitKey(0) & 0xFF))
            except:
                pass
    elif key == ord('l'):
        line = not line
        if rectangle:
            rectangle = not rectangle

    curTool = "Rectangle" if rectangle else "Circle" if not line else "Line"
    cv.rectangle(menu, (180, 60), (320, 90), (0, 0, 0), -1)
    cv.putText(menu, curTool, (180, 80), font,
               menuFontSize, toolSpecColor, 1)

cv.destroyAllWindows()

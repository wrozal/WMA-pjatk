import numpy as np
import cv2 as cv

cap = cv.VideoCapture('resources/movingball.mp4')

kernel = np.ones((5, 5), np.uint8)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    resized_frame = cv.resize(frame, (350, 500), interpolation=cv.INTER_AREA)

    hsv = cv.cvtColor(resized_frame, cv.COLOR_BGR2HSV)

    lower_red = np.array([0, 100, 10])
    upper_red = np.array([10, 255, 255])
    mask1 = cv.inRange(hsv, lower_red, upper_red)

    lower_red = np.array([160, 100, 20])
    upper_red = np.array([179, 255, 255])
    mask2 = cv.inRange(hsv, lower_red, upper_red)

    mask = mask1 + mask2

    mask = cv.bitwise_and(resized_frame, resized_frame, mask=mask)

    opening = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel)
    closing = cv.morphologyEx(opening, cv.MORPH_CLOSE, kernel)

    edges = cv.Canny(closing, 100, 200)
    edges = cv.dilate(edges, kernel, iterations=1)
    edges = cv.morphologyEx(edges, cv.MORPH_CLOSE, kernel)

    M = cv.moments(edges)

    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])

    cv.circle(resized_frame, (cX, cY), 5, (255, 0, 0), -1)

    cv.imshow('closing', closing)
    cv.imshow('edges', edges)
    cv.imshow('mask', mask)
    cv.imshow('image', resized_frame)

    k = cv.waitKey(5) & 0xFF
    if k == 27:
        break

cap.release()
cv.destroyAllWindows()
import cv2
import numpy as np

img = cv2.imread('resources/tray2.jpg')

img_blur = cv2.medianBlur(img, 3)

img_gray = cv2.cvtColor(img_blur, cv2.COLOR_BGR2GRAY)

edges = cv2.Canny(img_gray, 500, 650, apertureSize=5)

lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 90, minLineLength=50, maxLineGap=5)

x_coords = [line[0][0] for line in lines]
y_coords = [line[0][1] for line in lines]
low_x = min(x_coords)
high_x = max(x_coords)
low_y = min(y_coords)
high_y = max(y_coords)

circles = cv2.HoughCircles(img_gray, cv2.HOUGH_GRADIENT, 1, 10, param1=100, param2=35, minRadius=20, maxRadius=40)

circles = np.uint16(np.around(circles))

count_inside = {'big': 0, 'small': 0}
count_outside = {'big': 0, 'small': 0}

for circle in circles[0]:
    x, y, r = circle
    if low_x < x < high_x and low_y < y < high_y:
        if r > 31:
            count_inside['big'] += 1
            color = (100, 0, 255)
        else:
            count_inside['small'] += 1
            color = (255, 0, 0)
    else:
        if r > 31:
            count_outside['big'] += 1
            color = (100, 0, 255)
        else:
            count_outside['small'] += 1
            color = (255, 0, 0)
    cv2.circle(img, (x, y), r, color, 2)

print('Counter of 5 zl coin inside:', count_inside['big'])
print('Counter of 5 zl coin outside:', count_outside['big'])
print('Counter of 0.05 zl coin inside:', count_inside['small'])
print('Counter of 0.05 zl coin outside:', count_outside['small'])

cv2.imshow('detected coins', img)

cv2.waitKey(0)
cv2.destroyAllWindows()

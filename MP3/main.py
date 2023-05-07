import cv2 as cv
import pyautogui


def prepare(orb, img):
    kp, des = orb.detectAndCompute(img, None)
    return des


def resize(frame):
    height, width, _ = frame.shape
    screen_height, screen_width = pyautogui.size()
    new_height = int(height * (screen_width / width))
    new_width = screen_width
    resized_frame = cv.resize(frame, (new_width, new_height))
    return resized_frame


images = []
for i in range(1, 5):
    img = cv.imread(f'resources/saw{i}.jpg')
    images.append(img)

cap = cv.VideoCapture('resources/sawmovie.mp4')

orb = cv.ORB_create(100)
des = [prepare(orb, img) for img in images]
bf = cv.BFMatcher(cv.NORM_HAMMING, crossCheck=True)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = resize(frame)

    kp = orb.detect(frame, None)
    kp, descriptor = orb.compute(frame, kp)
    matches = bf.match(des[0], descriptor) + bf.match(des[1], descriptor) + bf.match(des[2], descriptor) + bf.match(
        des[3], descriptor)
    matches = [m for m in matches if m.distance < 60]

    if len(matches) > 2:
        idx = [i.queryIdx for i in matches]
        xs = sorted([int(i.pt[0]) for i in [kp[m] for m in idx]])
        ys = sorted([int(i.pt[1]) for i in [kp[m] for m in idx]])

        sumx = sum(xs) // len(xs)
        sumy = sum(ys) // len(ys)

        xs = list(filter(lambda x: abs(x - sumx) < 150, xs))
        xy = list(filter(lambda y: abs(y - sumy) < 150, ys))

        kp = [kp[m] for m in idx]

        if len(xs) > 0 and len(ys) > 0:
            frame = cv.rectangle(frame, (xs[0] - 40, ys[0] - 40), (xs[::-1][0] + 40, ys[::-1][0] + 40), (0, 255, 0), 2)

    cv.imshow('Chainsaw movie', frame)
    k = cv.waitKey(5) & 0xFF
    if k == 27:
        break

cap.release()
cv.destroyAllWindows()

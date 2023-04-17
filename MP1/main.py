import numpy as np
import cv2 as cv

# Load the video
cap = cv.VideoCapture('resources/movingball.mp4')

# Create a kernel for morphological operations
kernel = np.ones((5, 5), np.uint8)

# Loop through the video frames
while cap.isOpened():
    # Read the next frame from the video
    ret, frame = cap.read()

    # If there are no more frames, break out of the loop
    if not ret:
        break

    # Resize the frame to a smaller size to fit all the results on the screen
    resized_frame = cv.resize(frame, (350, 500), interpolation=cv.INTER_AREA)

    # Convert the resized frame to the HSV color space
    hsv = cv.cvtColor(resized_frame, cv.COLOR_BGR2HSV)

    # Create two masks to isolate the red color range
    lower_red = np.array([0, 100, 10])
    upper_red = np.array([10, 255, 255])
    mask1 = cv.inRange(hsv, lower_red, upper_red)

    lower_red = np.array([160, 100, 20])
    upper_red = np.array([179, 255, 255])
    mask2 = cv.inRange(hsv, lower_red, upper_red)

    # Combine the two masks into one
    mask = mask1 + mask2

    # Apply the mask to the resized frame to isolate the red areas
    mask = cv.bitwise_and(resized_frame, resized_frame, mask=mask)

    # Apply morphological operations to the mask to remove noise and fill gaps
    opening = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel)
    closing = cv.morphologyEx(opening, cv.MORPH_CLOSE, kernel)

    # Apply the Canny edge detection algorithm to the closing
    edges = cv.Canny(closing, 100, 200)

    # Dilate the edges to make them more visible
    edges = cv.dilate(edges, kernel, iterations=1)

    # Apply morphological operations to the edges to fill in any gaps
    edges = cv.morphologyEx(edges, cv.MORPH_CLOSE, kernel)

    # Calculate the moments of the edges to find the center of the ball
    M = cv.moments(edges)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])

    # Draw a circle at the center of the ball
    cv.circle(resized_frame, (cX, cY), 5, (255, 0, 0), -1)

    # Display the different stages of processing
    cv.imshow('closing', closing)
    cv.imshow('edges', edges)
    cv.imshow('mask', mask)
    cv.imshow('image', resized_frame)

    # Check for a key press and break out of the loop if the 'Esc' key is pressed
    k = cv.waitKey(5) & 0xFF
    if k == 27:
        break

# Release the video and destroy all windows
cap.release()
cv.destroyAllWindows()

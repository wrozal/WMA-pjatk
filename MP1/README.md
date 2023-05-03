# Tracking a colored object (red ball)

Write a program to track a colored object (red ball). In the movingball.mp4 video there is a moving object. You need to specify the color range of the red ball. For each frame of the video, you should:

1. Change the image format to HSV  
2. Identify the pixels that meet the color requirements (red object)  
3. Apply morphological operations to improve the mask (remove noise and fill in gaps)  
4. Determine the center of gravity of the ball - the coordinates of its center  
5. Mark the center of gravity on the video  

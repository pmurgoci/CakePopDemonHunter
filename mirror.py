# This file will be minimal openCV file for mirroring  the webcam
import numpy as np
import cv2 as cv
import random

print('This is mirror.py')
cap = cv.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

# score
score = 0

# face detection model
face_cascade = cv.CascadeClassifier('/Users/cislab/PM/haarcascade_frontalface_default.xml')
if face_cascade.empty():
    print("Error loading face cascade")
    exit()
threshold = 200000
bl_on = True
br_on = True 
tl_on = True 
tr_on = True  

# variables for falling "demons"
fall_x = None
fall_y = None
fall_speed = 6
fall_width = 80
fall_height = 80


first = True
while True:
    
    if random.random() > 295/300:
        bl_on = True
        print('bl demon appears')

    if random.random() > 295/300:
        br_on = True
        print('br demon appears')

    if random.random() > 295/300:
        tl_on = True
        print('tl demon appears')

    if random.random() > 295/300:
        tr_on = True
        print('tr demon appears')


    # Capture frame-by-frame
    ret, frame = cap.read()

    # turn the image into mirror image
    frame = cv.flip(frame, 1)
    height, width = frame.shape[:2]

    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    # Our operations on the frame come here
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    if first:
        prev_gray = gray
        first = False

    # detect face and draw the rectangle
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    for (x, y, w, h) in faces:
        cv.rectangle(frame, (x, y), (x + w, y + h), (0 , 255, 255), (2))

    # Calculate change in gray
    # delta = cv.absdiff(gray, prev_gray).sum()

    

    delta = cv.absdiff(gray[0:100], 
                       prev_gray[0:100]).sum()


    if tl_on:
        delta_tl = cv.absdiff(gray[0:100, 0:100], 
                              prev_gray[0:100, 0:100]).sum()
        cv.rectangle(frame, (0,0), (100,100), (100,100,100), 2)
        if delta_tl > threshold:
            score += 1
            # cv.rectangle(frame, (width-100, 0), (width, 100), (0, 0, 0), -1)
            tl_on = False
            print('tl detected')

    
    if tr_on:
        delta_tr = cv.absdiff(gray[0:100, width-100:width],
                              prev_gray[0:100, width-100:width]).sum()
        cv.rectangle(frame, (width-100, 0), (width, 100), (100, 100, 100), -1)
        if delta_tr > threshold:
            score += 1
            # cv.rectangle(frame, (width-100, 0), (width, 100), (0, 0, 0), -1)
            tr_on = False
            print('tr detected')

    if bl_on:

        delta_bl = cv.absdiff(gray[height-100: height, 0:100],
                              prev_gray[height-100:height, 0:100]).sum()
        cv.rectangle(frame, (0, height-100), (100, height), (100, 100, 100), -1)
        if delta_bl > threshold:
            score += 1
            #cv.rectangle(frame, (0, height-100), (100, height), (0, 0, 0), -1) 
            bl_on = False
            print('bl detected')

    if br_on:

        delta_br = cv.absdiff(gray[height-100:height, width-100:width],
                          prev_gray[height-100:height, width-100:width]).sum()
        cv.rectangle(frame, (width-100, height-100), (width, height), (100,100,100), -1)
        if delta_br > threshold:
            score += 1
            # cv.rectangle(frame, (width-100, height-100), (width, height), (0,0,0), -1)
            br_on = False
            print('br detected')

    if fall_x is None:
        fall_x = width // 2 - fall_width // 2
        fall_y = 0

    cv.rectangle(frame, (fall_x, fall_y), 
                (fall_x + fall_width, fall_y + fall_height),
                (255, 0, 0), -1)

    fall_y += fall_speed

    for (fx, fy, fw, fh) in faces:
        dx1 = fall_x
        dy1 = fall_y
        dx2 = fall_x + fall_width
        dy2 = fall_y + fall_height

        fx1 = fx 
        fy1 = fy 
        fx2 = fx + fw 
        fy2 = fy + fh 

        overlap = not (fx2 < dx1 or fx1 > dx2 or fy2 < dy1 or fy1 > dy2)

        if overlap:
            print('GAME OVER')
            cv.putText(frame, 'GAME OVER', (150 , 200),
                       cv.FONT_HERSHEY_SIMPLEX, 2, (0,0,255), 4)
            cv.imshow('frame', frame)
            cv.waitKey(3000)
            exit()

        if fall_y > height:
            fall_x = None
            fall_y = None


   # Display text

    cv.putText(frame, str(delta), (50, 300),
        cv.FONT_HERSHEY_SIMPLEX,  
        2,  # font scale
        (0,255,255),  # color
        4) # thickness

    cv.putText(frame, "Hello", (50, 100),
        cv.FONT_HERSHEY_SIMPLEX,  
        2,  # font scale
        (150,0,150),  # color
        4) # thickness

    cv.putText(frame, f"Score: {score}", (20, 40),
        cv.FONT_HERSHEY_SIMPLEX,  
        1,  # font scale
        (255,255,255),  # color
        2) # thickness

    # Display the resulting frame
    # cv.imshow('frame', gray)
    cv.imshow('frame', frame)

    # Save prev frame
    prev_gray = gray


    # see if user wants to quit
    if cv.waitKey(1) == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()


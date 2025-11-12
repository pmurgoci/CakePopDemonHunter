# This file will be minimal openCV file for mirroring  the webcam
import numpy as np
import cv2 as cv

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


first = True
while True:
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
    cv.rectangle(frame, (0,0), (100,100), (100,100,100), 2)


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


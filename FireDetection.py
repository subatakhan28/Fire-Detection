# -*- coding: utf-8 -*-
"""Untitled6.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1n4qhhNx2N-1nzosuBkWgeC9KJNQmPjhd
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
import beepy as beep
import threading
import smtplib

def send_email():
    server = smtplib.SMTP_SSL("smtp.gmail.com",465) # initializing the
    server and port number for SMTP
    server.login('os.project.demo@gmail.com','hsbjbfzvonpmqdoi') # defining the email address

server.sendmail('os.project.demo@gmail.com','aahadraja70@gmail.com','Hurry! There is a fire detected.') # writing the email message and the recipients
server.quit()

def play_audio():
    beep.beep(sound="wilhelm") # buzzer

live_Camera = cv2.VideoCapture(0) # start video capturing
lower_bound1 = np.array([0, 0, 255]) # min of the range of hues, saturation and value
upper_bound1 = np.array([13, 100, 255]) # max of the range of hues, saturation and value
lower_bound1 = np.array(lower_bound1, dtype = "uint8") # changing the datatype to unsigned integer
upper_bound1 = np.array(upper_bound1, dtype = "uint8")
lower_bound2 = np.array([0, 43, 68]) # min of the range of hues, saturation and value
upper_bound2 = np.array([7, 130, 217]) # max of the range of hues,saturation and value
lower_bound2 = np.array(lower_bound2, dtype = "uint8")
upper_bound2 = np.array(upper_bound2, dtype = "uint8")

while (live_Camera.isOpened()): # read the footage in an infinite loop till the camera remains open
    ret, frame = live_Camera.read() # reading data from the live camera, ret is a boolean indicating whether there is a frame or not

    if ret == False: # if camera not initialised properly dont read andbreak the loop
        break
    frame = cv2.resize(frame, (1280, 720)) # to resize the video being captured to cover the entire screen
    frame = cv2.flip(frame, 9) # flipping to avoid mirror-image, 9 to flip around y-axis
    frame_smooth = cv2.GaussianBlur(frame, (15, 15), 0) # to remove noise from the footage
    frame_hsv = cv2.cvtColor(frame_smooth, cv2.COLOR_BGR2HSV) #converting the image to HSV
    mask1 = cv2.inRange(frame_hsv,lower_bound1,upper_bound1) # creating the mask
    mask2 = cv2.inRange(frame_hsv,lower_bound2,upper_bound2) # creating the mask
    image_binary1 = cv2.bitwise_and(frame, frame_hsv, mask = mask1) # masking the image obtained
    image_binary2 = cv2.bitwise_and(frame, frame_hsv, mask = mask2) # masking the image obtained
    check_if_fire_detected1 = cv2.countNonZero(mask1) # counting the number of non zero pixels in the mask
    check_if_fire_detected2 = cv2.countNonZero(mask2) # counting the number of non zero pixels in the mask
    contours,_ = cv2.findContours(image = mask1, mode = cv2.RETR_EXTERNAL, method = cv2.CHAIN_APPROX_SIMPLE) # checking the cntours in the mask obtained

    for contour in contours:
        if cv2.contourArea(contour)<50: # area very small so ignore it
            continue
        (x, y, w, h) = cv2.boundingRect(contour)

        frame = cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2) # drawing a rectangle for the fire detected

    if (int(check_if_fire_detected1) >= 10000) and (int(check_if_fire_detected2) >= 30000): # checking if fire is detected in the image
        cv2.putText(frame, "Fire Detected!", (300, 360), cv2.FONT_HERSHEY_COMPLEX, 3, (0, 0, 255), 5)
        t1 = threading.Thread(target = play_audio) # creating the audio thread
        t2 = threading.Thread(target = send_email) # creating the mail thread
        t1.start() # calling the audio thread
        t2.start() # calling the mail thread

    cv2.imshow("Fire Detection", frame)
    if cv2.waitKey(10) == 27: # exit the loop when esc key is pressed
        break

live_Camera.release()
cv2.destroyAllWindows()
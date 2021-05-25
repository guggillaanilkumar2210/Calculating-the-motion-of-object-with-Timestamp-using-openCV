import cv2
import pandas,time
from datetime import datetime
first_frame = None
status_list = [None,None]
times = []
#Data Frame to store the time values during which object detection and movement appears. 
df = pandas.DataFrame(columns=["Start","End"])
video = cv2.VideoCapture(0,cv2.CAP_DSHOW) #create a video capture object to record video using webcam
while True:
    check,frame = video.read()
    #Status at the beginning of the object is 0 as the object is not visible.
    status = 0
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY) #convert the frame color to gray scale
    gray = cv2.GaussianBlur(gray,(21,21),0) #convert the grayscale frame to Gaussian Blur
    if first_frame is None:
        first_frame = gray
        continue                #This is used to store first image frame or the video. 
    delta_frame = cv2.absdiff(first_frame,gray) #It calculates the difference between the first frame and the other frames. 
    #Provides a threshold value such that it will convert the difference value with less than 30 to black. If the difference is greather than 30 it will convert those pixels to white.
    thresh_delta = cv2.threshold(delta_frame,30,255,cv2.THRESH_BINARY)[1] 
    thresh_delta = cv2.dilate(thresh_delta,None,iterations = 0)
    #Define the contour Area. Basically add the borders
    (cnts, _) = cv2.findContours(thresh_delta.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #Removes noise and shadows. Basically it will keep only that part white, which has area grater than 1000 pixels.
    for contour in cnts:
        if cv2.contourArea(contour)<10000:
            continue
        #change in status when the object is being detected.
        status = 1
        #creates a rectangular box around the object in the frame.
        (x,y,w,h)=cv2.boundingRect(contour)
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3)
    #List of status for every frame
    status_list.append(status)
    status_list = status_list[-2:]
    #Record date time in list when change occurs
    if status_list[-1]==1 and status_list[-2]==0:
        times.append(datetime.now())
    if status_list[-1]==0 and status_list[-2]==1:
        times.append(datetime.now())
    cv2.imshow('frame',frame)
    cv2.imshow('Capturing',gray)
    cv2.imshow('delta',delta_frame)
    cv2.imshow('thresh',thresh_delta)
    #Frame will change in 1 ,illisecond
    key = cv2.waitKey(1)
    #This will beak the loop once the user presses q
    if key == ord('q'):
        break

print(status_list)
print(times)
#Store time values in data Frame
for i in range(0,len(times),2):
    df = df.append({"Start":times[i],"End":times[i+1]},ignore_index=True)

#Write the dataFrame to a CSV file
df.to_csv("Times.csv")
video.release()
#All the windows gets closed. 
cv2.destroyAllWindows()

#!/usr/bin/env python3

# NOTE: this example requires PyAudio because it uses the Microphone class

import speech_recognition as sr
import cv2
import cv
import numpy as np

# this is called from the background thread
def callback(recognizer, audio):
    # received audio data, now we'll recognize it using Google Speech Recognition
    try:
	outp=recognizer.recognize_google(audio)
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        
	global val#global val will be read in main while loop
	if (outp!="can you hear me" and outp!="exit" and outp!="very good" and outp!="excellent" and outp!="can you see me" and outp!="next question who am I"):
		print("you said: " + outp)
	if (outp=="can you hear me"):
		print "Yes"
	if (outp=="exit"):#this works
		val=1
		print "Exiting..."
		
	if (outp=="put text"):
		val=2
	if (outp=="refresh"):
		val=0
	if (outp=="can you see me"):
		val=8
		print "Yes"
	if (outp=="next question who am I"):
		print "Admin"
		val=9
	if (outp=="very good" or outp=="excellent"):
		print "Thank You"
		#stop_listening() # calling this function requests that the background listener stop listening
    except sr.UnknownValueError:
        print("could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

r = sr.Recognizer()
m = sr.Microphone()
cap = cv2.VideoCapture(0)
val=0
imgsq=cv2.imread("Admin2.jpg")
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
with m as source:
    r.adjust_for_ambient_noise(source) # we only need to calibrate once, before we start listening

# start listening in the background (note that we don't have to do this inside a `with` statement)
stop_listening = r.listen_in_background(m, callback)

# `stop_listening` is now a function that, when called, stops background listening

# do some other computation for 5 seconds, then stop listening and keep doing other computations
import time
#for x in range(50): time.sleep(0.1) # we're still listening even though the main thread is doing other things
#stop_listening() # calling this function requests that the background listener stop listening
while True: 
	#print "out"
	ret,img=cap.read()
	#print val
	if(val==2):
		cv2.putText(img,"I can hear you",(30,80),cv2.FONT_HERSHEY_SIMPLEX,1.5,(0,255,255),2)
	if(val==8):
		faces = face_cascade.detectMultiScale(img, 1.3, 5)
    		for (x,y,w,h) in faces:
        		#cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
			roi_color = img[y:y+h, x:x+w]
			rect=img[y+h/2-100:y+h/2+100,x+w/2-100:x+w/2+100]
			cv2.addWeighted(rect,1,imgsq,1,0,rect)
			
        if(val==9):
		faces = face_cascade.detectMultiScale(img, 1.3, 5)
    		for (x,y,w,h) in faces:
	    		#cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
			roi_color = img[y:y+h, x:x+w]
			rect=img[y+h/2-100:y+h/2+100,x+w/2-100:x+w/2+100]
			cv2.addWeighted(rect,1,imgsq,1,0,rect)
			cv2.putText(img,"ADMIN",(x+h/2,y+w+40),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,255,255),2)
			
         
	if(cv2.waitKey(10) & 0xFF == ord('b')):
        	break
	if(val==1):
		break
	
	#cv2.imshow('sq',imgsq)
	cv2.imshow('Video', img)
	#time.sleep(0.5)

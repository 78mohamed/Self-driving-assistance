import numpy as np
import matplotlib.pyplot as plt
import cv2 
import h5py

filename = "2016-01-30--11-24-51.h5"
def readData(filename, start = 0, end = -1):

	camera_file = "camera/" + filename
	log_file = "log/" + filename

	print("Reading file ...")
	camera = h5py.File(camera_file, 'r')
	log = h5py.File(log_file, 'r')
	print("Done file")
	print(dict(log))

	images = camera['X'][()]
	steering_angle = log["steering_angle"][()]
	speed = log["speed"][()]
	idxs = np.linspace(0, steering_angle.shape[0]-1, images.shape[0]).astype("int")  # approximate alignment
	angles = steering_angle[idxs]
	speed = speed[idxs]

	#print(np.max(speed), np.min(speed))
	print("before",len(angles))

	good_steering = (np.abs(angles) < 180)
	good_velocity = speed > 5

	goods = good_steering * good_velocity
	good_images = images[goods]
	good_angles = angles[goods]
	good_speed = speed[goods]
	print("after",len(good_angles))
	good_images = good_images[start:end]
	good_angles = good_angles[start:end]
	good_speed = good_speed[start:end]

	camera.close()
	log.close()

	return good_images, good_angles, good_speed



def createVideo(images, angles, speed):

	# font
	font = cv2.FONT_HERSHEY_SIMPLEX 
	  
	# fontScale 
	fontScale = 1
	   
	# Blue color in BGR 
	color = (255, 255, 255) 
	  
	# Line thickness of 3 px 
	thickness = 3

	n_images = len(images)
	frameSize = (1280, 720)
	print("Creating video ...")
	out = cv2.VideoWriter('output_video.mp4',cv2.VideoWriter_fourcc(*'mp4v'), 20, frameSize, True)

	for i in range(n_images):

	    img = images[i]
	    img = img.transpose(1,2,0)
	    img = cv2.resize(img, frameSize)
	    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
	    img = cv2.putText(img, 'Frame: '+str(i+1), (50, 50) , font, fontScale, color, thickness, cv2.LINE_AA)
	    img = cv2.putText(img, 'Steering angle: '+str(angles[i]), (50, 100) , font, fontScale, color, thickness, cv2.LINE_AA) 
	    img = cv2.putText(img, 'Speed: '+str(speed[i]), (50, 150) , font, fontScale, color, thickness, cv2.LINE_AA)   
	    print("Frame:", str(i+1)+"/"+str(n_images))
	    out.write(img)

	out.release()





images, angles, speed = readData(filename)
#createVideo(images, angles, speed)

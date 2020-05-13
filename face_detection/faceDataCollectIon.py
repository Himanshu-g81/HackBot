import cv2
import numpy as np

#Initialize camera
cam = cv2.VideoCapture(0)

#haarcacade file for face detection
face_cascade = cv2.CascadeClassifier("haarcascades/haarcascade_frontalface_alt.xml")


skip = 0
face_data = []
dataset_path = 'data/'

file_name = input("enter name of person: ")
while True:
	ret, frame = cam.read()

	if False == ret:    # If there is error in frame capture
		continue


	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	"""
	Get the faces present in frame
		it take three parameters 
		1. frame
		2. scaling factor : the haarcascade is modeled to train over image of fixed size, therefore scaling of got image is required
		3. number of neighbours to be looked for detecting. ( It is best between 3 - 6)
		
		it returns a list of tuples ( x, y, w, h) : (x,y) : top left corner of face ***____*** (w,h): width and height	 
	"""
	
	faces = face_cascade.detectMultiScale(frame, 1.3, 5)
	faces = sorted(faces, key = lambda f: f[2]*f[3], reverse = True)
	print(len(faces))

	
	
	for (x, y, w, h) in faces[0:1]:																#get only the largest area face
		cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,255), 3)


		#Extract REGION OF INTEREST s
		offset = 10								#padding of 10 px in all sides of square
		face_selection = frame[ y - offset : y + h + offset, x - offset : x + w + offset]

		face_selection = cv2.resize(face_selection, (100, 100))

		skip += 1
		if skip%10 == 0:
			face_data.append(face_selection)
			print(len(face_data))



		cv2.imshow("You", frame)
		cv2.imshow("Your section", face_selection)
	#Capture every 10th face
	if skip%10 == 0:
		pass

	key_pressed = cv2.waitKey(1) & 0xFF
	if ord('q') == key_pressed:
		break


#Convert list to a np array
face_data = np.asarray(face_data)
face_data = face_data.reshape((face_data.shape[0], -1) )
print(face_data.shape)

#Save data in file
np.save(dataset_path + file_name + ".npy", face_data)
print("Data stored at ", dataset_path + file_name + '.npy')
cam.release()
cv2.destroyAllWindows()
import numpy as np 
import cv2
import os


""" ******************* KNN  *********************** """
# takes two position vectors(arrays) and returns euclidean distance between them
def distance(x1, x2):
    result = np.sqrt(np.sum((x1-x2)**2))
    return result

# Main knn function X: dataSet Y: target value  k: number of neighbours to check for
def knn(X, Y, query_point, k = 6):
    
    values = []
  
    numOfValues = X.shape[0]
    
    for i in range(numOfValues):
        dist = distance(X[i], query_point)
        values.append((dist, Y[i]))
    
    values = sorted(values)
    
    #Get first k elements:
    values = values[:k]
    
    values = np.array(values)
    
    new = np.unique(values[:,1], return_counts = True)
    
    #new is a tuple of two elements : 1st is unique values in array "values" 2nd: count of each unique values
    #so we will take that value(1st element) which has maximum count
    
    max_index = new[1].argmax()
    pred = new[0][max_index]
    
    return pred[0]
""" ************************** KNN ends  ************** """


#Initialize camera
cam = cv2.VideoCapture(0)

#haarcacade file for face detection
face_cascade = cv2.CascadeClassifier("haarcascades/haarcascade_frontalface_alt.xml")

skip = 0
face_data = []
dataset_path = 'data/'
label = []

class_id = 0  # maintains id of each file  ** Label of each file  **
names = {}    # mapping of id to file name


# Load Data
for fx in os.listdir(dataset_path):
	
	if fx.endswith('.npy'):

		data_item = np.load(dataset_path + fx)

		face_data.append(data_item)

		names[class_id] = fx[:-4]

		""" Now each file has some entries of faces of same person 
		So we need to give each entry same id
		However for each person id is different
		so within a file each entry is having a (same id) and each file has a unique id """

		target = class_id*np.ones((data_item.shape[0], ))
		class_id += 1
		label.append(target)

# ***** X_TRAIN ******
face_dataset = np.concatenate(face_data, axis = 0)
face_labelss = np.concatenate(label, axis = 0)

# ****** Y_TRAIN  **********
face_labelss = face_labelss.reshape((-1, 1))

###### print(face_dataset.shape)
cnt = 0
while True:
	ret, frame = cam.read()

	if False == ret:
		print("errror reading")
		continue

	faces = face_cascade.detectMultiScale(frame, 1.3, 5)
#	cv2.imshow("You ", frame)

#	print(len(faces))

	key_pressed = cv2.waitKey(1) & 0xFF
	if ord('a') == key_pressed:
		break


	for (x, y, w, h) in faces:

		offset = 10

		#Getting region of interest :

		face_select = frame[y-offset : y + h + offset, x - offset : x + w + offset]
		face_select = cv2.resize(face_select, (100, 100))

#		cv2.imshow("face: ", face_select);

		pred = knn(face_dataset, face_labelss, face_select.flatten())

		name = "detecting..."
		if names.get(pred, None) is not None:
			name = names[pred]

		if name == 'himanshu':
			cnt += 1

		

		cv2.putText(frame, name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
		cv2.rectangle(frame, (x,y), (x + w, y + h), (0, 255, 254), 3)

		cv2.imshow('You', frame)

	if cnt == 50:
		break

cam.release()
cv2.destroyAllWindows()

print("Hello Himanshu!!")
os.system('python3.7 ./main.py')
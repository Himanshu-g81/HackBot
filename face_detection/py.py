import cv2

"""
***********************8#For reading and displaying image****************************

img = cv2.imread("dog.webp")
gry = cv2.imread("dog.webp", cv2.IMREAD_GRAYSCALE)

cv2.imshow("a dog", gry)
cv2.imshow("a one dog", gry)
cv2.waitKey(0)
cv2.destroyAllWindows()
"""

"""

****************************Use of webcam                  **********************************


cam = cv2.VideoCapture (0) # 0 means default device

while True:
	ret, frame = cam.read() # ret is bool to show wheather capture is done or not
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	if ret == False:
		continue

	cv2.imshow("You", gray)

	#Wait until key pressed

	key_pressed = cv2.waitKey(1) & 0xFF  #waitKey(1) returns 32 bit number, we convert it by & 0xFF to 8 bit because 8 bit is used to store characters
	if key_pressed == ord('q'):
		break

cam.release()
cv2.destroyAllWindows()

"""

"""
****************************************capture face and draw a rectangle*************************************************
cam = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier("haarcascades/haarcascade_frontalface_alt.xml")

while True:
	ret, frame = cam.read()

	if ret == False:
		continue

	faces = face_cascade.detectMultiScale(frame, 1.3, 5) # 1.3 : scaling factor :: 5: number of neighbours checked

	#faces : list of tuples ( x, y, w, h) (x, y): start of face, (w,h): height and weidth

	for (x,y,w,h) in faces:
		cv2.rectangle(frame, (x,y), (x+w, y+h), (0,0,0), 4)
	cv2.imshow("You", frame)

	key_pressed = cv2.waitKey(1) & 0xFF

	if key_pressed == ord('q'):
		break


cam.release()
cv2.destroyAllWindows()





"""
print(2)

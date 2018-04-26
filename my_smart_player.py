import cv2
import my_player
#import numpy as np


class Editor:
	def __init__(self):
		self.__haarDir__ = 'Haarcascade/'
		self.__cam__ = None
		self.__maxFace_count = 50
		self.__maxEye_count = 10


	def isFaceExist(self):
		faceDetect = cv2.CascadeClassifier(self.__haarDir__+'haarcascade_frontalface_default.xml')
		eyeDetect = cv2.CascadeClassifier(self.__haarDir__+'haarcascade_eye.xml')

		isFace = -1
		isEye = -1

		ret,image = self.__cam__.read()
		
		if(not ret):
			print("Camera is not able to click images")
			return None,None

		gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
		faces = faceDetect.detectMultiScale(gray,1.3,5)
        
		cv2.imshow("Faces",image)
		cv2.waitKey(10)

		for (x,y,w,h) in faces:
			isFace = 1
			cv2.rectangle(image, (x,y),(x+w,y+h),(0,0,255),2)
			roi_gray = gray[y:y+h//2,x:x+w]
			roi_img = image[y:y+h//2,x:x+w]
			eyes = eyeDetect.detectMultiScale(roi_gray)
			for (ex,ey,ew,eh) in eyes:
				if(3 < h//eh < 6):
					isEye = 1
					cv2.rectangle(roi_img,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
			cv2.imshow("Faces",image)
			cv2.waitKey(1)

		return isFace, isEye


	def start(self):
		self.__cam__ = cv2.VideoCapture(0)
		face_count = 0
		eye_count = 0
		quit = 0
		OUTERLOOP = True
		playlist = 'playlist'
		player = my_player.Player(playlist)

		while OUTERLOOP:
			while True:
				_face_count,_eye_count = self.isFaceExist()
				face_count = face_count + _face_count
				eye_count = eye_count + _eye_count
				if(face_count >= self.__maxEye_count):
					quit = 0
				else:
					quit = quit + 1

#				print('Face Count : ',face_count)
#				print('Eye Count : ',eye_count)
#				print('Quit Count : ',quit)
				if(not player.isPause()):
					if(player.checkComplete()>0.99):
						print('Video is almost complete.')
						player.next()

				if(face_count > self.__maxFace_count):
					face_count = self.__maxFace_count
					if(player.isStop()):
						eye_count = self.__maxEye_count
						print('Video is already stopped.')
						player.selectVideo()
						
				if(eye_count > self.__maxEye_count):
					eye_count  = self.__maxEye_count
					player.resume()

				if(eye_count < -self.__maxEye_count):
					eye_count = -self.__maxEye_count
					player.pause(False)

				if(face_count < -self.__maxFace_count):
					face_count = -self.__maxFace_count
					player.stop()
					break
				
				if(cv2.waitKey(10) & 0xFF == ord('q')):
					OUTERLOOP = False
					print ('Quit by User')
					break

			if(quit >250):
				print('Quit')
				OUTERLOOP = False



		self.__cam__.release()
		cv2.destroyAllWindows()
		print("Thank You")

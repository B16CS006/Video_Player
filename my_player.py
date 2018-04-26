import os
import vlc


class Player:
	def __init__(self,playlist_dir,fullscreen = True):
		self.instance = vlc.Instance(['--no-xlib'])
		self.player = self.instance.media_player_new()
		self.player.set_fullscreen(fullscreen)

		self.playlist_dir = playlist_dir
		self.playlist = []

		self._pause = True
		self._stop = True
		self._currentPointer = 0
		self._currentVideo = -1

		for root,dirs,files in os.walk(self.playlist_dir):
			for file in files:
				#avi|mpg|mov|flv|wmv|asf|mpeg|m4v|divx|mp4|mkv
				self.playlist.append(file)

	def setTitle(self):
		title = self.playlist[self._currentVideo]
		print (self.player.get_title())

#		self.player.set_title(title)

	def isPause(self):
		return self._pause

	def isStop(self):
		return self._stop

	def checkComplete(self):
		return self.player.get_position()

	def updateCurrentPointer(self):
		print('Updating Current Pointer')
		self._currentPointer = self.player.get_position()
		if(self._currentPointer <0):
				self._currentPointer = 0
		return self._currentPointer

	def increaseCurrentVideo(self):
		print('Increase Video Counter')
		self._currentVideo = self._currentVideo + 1
		if(self._currentVideo >= self.playlist.__len__()):
			self._currentVideo = 0

	def resume(self):
		if ((not self._stop) & self._pause):
			print('Resume')
			self.player.play()
			self.setTitle()
			self._pause = False

	def pause(self,changePointer = True):
		if((not self._stop) & ~self._pause):
			self._pause = True
			if(changePointer):
				self.updateCurrentPointer()
			print('Pause')
			self.player.pause()
			

	def play(self,_currentVideo = 0):
		self.stop()
		resume = False
		if(_currentVideo == -1):
			resume = True
		else:
			self._currentVideo = _currentVideo
		self.player.set_mrl(self.playlist_dir + '/' + self.playlist[self._currentVideo])
		self.player.play()
		self.setTitle()
		if(resume):
			self.player.set_position(self._currentPointer)
		self._stop = False
		self._pause = False


	def stop(self,changePointer = True):
		self.pause(changePointer)
		if (not self._stop):
			self._pause = True
			self._stop = True
			if(changePointer):
				self.updateCurrentPointer()
			print('Stop')
			self.player.stop()

	def next(self):
		self.increaseCurrentVideo()
		self.play(self._currentVideo)
		print('Next')

	def selectVideo(self):
		print('Selecting video.....')
		if(self._currentVideo != -1):
			confirm = str(input('Want to resume the Previous Video : '))
			if((confirm == 'y') or (confirm =='yes') or (confirm =='Y') or (confirm =='Yes') or (confirm =='YES')):
				self.play(-1)
				return
		index = 0
		for video in self.playlist:
			print(index,"------",video)
			index = index + 1
		choice = int(input("\nChoose Video to play : "))
		print("choice : ",choice,self.playlist.__len__())
		if(choice >= 0 & choice < self.playlist.__len__()):
			if(self._currentVideo == choice):
				confirm = str(input('Want to resume the Previous Video : '))
				if((confirm == 'y')|(confirm =='yes')|(confirm =='Y')|(confirm =='Yes')|(confirm =='YES')):
					self.play(-1)
				else:
					self.play(choice)	
			else:
				self.play(choice)
		else:
			print('Option ',choice,' is not present in above list to we take 0 as input.')
			self.play()

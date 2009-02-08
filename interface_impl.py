true=1
false=0


from qt import *
from interface import Interface
from storyboard import Storyboard
from frameinfo import FrameInfo




class Interface_Impl(Interface):
	def __init__(self,parent=None,name=None,f1=0):
		Interface.__init__(self,parent,name,f1)
		
		self.setInitValues()#set initial values for a session of storyboarding
				
		self.cursor=QCursor(3)#set cursor to the 'HourGlass' symbol
		
		self.shtLen.insert("0")
				
		#when a paint event occurs on the drawing area - 'drawingPaintEvent' repaint it
		self.fmDraw.__class__.paintEvent=self.drawingPaintEvent
				
		self.xoff=self.fmToolBox.width() #Offset of X-axis
		self.yoff=self.MenuBar.height()+self.Toolbar.height() #Offset of Y-axis
		
		
		#create a pixmap on the drawing area
		self.rec=QRect(0,self.fmDraw.y(),self.fmDraw.width(),self.fmDraw.height())
		self.pix=QPixmap(self.rec.size())
		self.pix.fill(self.fmDraw,self.rec.topLeft())
	
		
		#showing all signals connected to the appropriate slots	
				
		#****************************FILE Menu****************************#
		self.connect(self.fileNew,SIGNAL('activated()'),self.newStoryboard)
		self.connect(self.filOpen,SIGNAL('activated()'),self.fileOpen)
		self.connect(self.filSave,SIGNAL('activated()'),self.fileSave)
		self.connect(self.fileSavAs,SIGNAL('activated()'),self.fileSaveAs)	
		self.connect(self.filePrintAction,SIGNAL('activated()'),self.printing)
		self.connect(self.fileExit,SIGNAL('activated()'),self.exitStoryboard)
		#*************************************************************#
		
		
		#****************************VIEW Menu****************************#
		self.connect(self.undo,SIGNAL('activated()'),self.undoDeleteFrame)
		self.connect(self.copy,SIGNAL('activated()'),self.copyFrame)
		self.connect(self.paste,SIGNAL('activated()'),self.pasteFrame)
		self.connect(self.newFrm,SIGNAL('activated()'),self.newFrame)
		self.connect(self.deleteFrame,SIGNAL('activated()'),self.delFrame) 
		self.connect(self.clrScreen,SIGNAL('activated()'),self.clearFrame)
		#*************************************************************#
		
		#****************************HELP Menu****************************#
		self.connect(self.hlpAbtBE,SIGNAL('activated()'),self.helpAbout)
		self.connect(self.hlpAbtQt,SIGNAL('activated()'),self.helpAboutQt)
		#*************************************************************#	
		
		
		#***************************BUTTONS***************************#
		self.connect(self.fstButton,SIGNAL('clicked()'),self.fstFrame)
		self.connect(self.lstButton,SIGNAL('clicked()'),self.lstFrame)
		self.connect(self.preButton,SIGNAL('clicked()'),self.previousFrame)
		self.connect(self.nxtButton,SIGNAL('clicked()'),self.nextFrame)	
		self.connect(self.pbPlay,SIGNAL('clicked()'),self.playStoryboard)
		self.connect(self.pbPause,SIGNAL('clicked()'),self.pauseStoryboard)
		#*************************************************************#	
		
		
		#****************************TOOLS****************************#
		self.connect(self.eraser,SIGNAL('clicked()'),self.setEraser)
		self.connect(self.pen,SIGNAL('clicked()'),self.restorePen)
		self.connect(self.chooseColor,SIGNAL('clicked()'),self.showColor)
		#*************************************************************#	
		
		#***************************PENSIZE***************************#	
		self.connect(self.sizeOne,SIGNAL('clicked()'),self.setOne)
		self.connect(self.sizeTwo,SIGNAL('clicked()'),self.setTwo)
		self.connect(self.sizeThree,SIGNAL('clicked()'),self.setThree)
		self.connect(self.sizeFour,SIGNAL('clicked()'),self.setFour)
		self.connect(self.sizeFive,SIGNAL('clicked()'),self.setFive)
		#*************************************************************#	
		
		
		#*************************ERASERSIZE**************************#	
		self.connect(self.erase1,SIGNAL('clicked()'),self.eraseOne)
		self.connect(self.erase2,SIGNAL('clicked()'),self.eraseTwo)
		self.connect(self.erase3,SIGNAL('clicked()'),self.eraseThree)
		self.connect(self.erase4,SIGNAL('clicked()'),self.eraseFour)
		self.connect(self.erase5,SIGNAL('clicked()'),self.eraseFive)
		#*************************************************************#	
		
#****************************************************************************************#
	def setInitValues(self):
		
		self.story=Storyboard()		#create an instance of Storyboard
		
		self.color=Qt.black
                self.penStyle=Qt.SolidLine
                self.myPenWidth=1  
              	self.nextFrameNum=0
		self.setOne()
				
		self.frmErase.hide()
		self.frmSize.show()
	
		self.freshFrame=true		#keep track of the addition of a fresh frame
		self.fmLast=false		#keep track of the last Frame
		self.alreadySaved=false		#whether the current storyboard has already been saved
		self.loading=false		#whether the current storyboard has been loaded
		self.erase=false		#whether the tool 'eraser' has been chosen
		self.modified=false 		#keep track of changes made to the current Storyboard
		self.play=false			#whether the play button has been pressed
				
		#disable some 'Edit' options and the scrolls ,play and stop buttons
		self.preButton.setEnabled(0)
		self.nxtButton.setEnabled(0)		
		self.lstButton.setEnabled(0)
		self.fstButton.setEnabled(0)
		self.pbPlay.setEnabled(0)
		self.pbPause.setEnabled(0)
		self.undo.setEnabled(0)
		self.paste.setEnabled(0)
		self.deleteFrame.setEnabled(0)
		
		
#****************************************************************************************#	

	def drawingPaintEvent(self,ev):
		
		p=QPainter()
        	p.begin(self.fmDraw)
	 	p.drawPixmap(self.rec.topLeft(),self.pix)
   	        p.flush()
     		p.end()
		
#****************************************************************************************#
	#For right click on the mouse
	def contextMenuEvent(self,ev):
		self.contextMenu=QPopupMenu()
		self.copy.addTo(self.contextMenu)
		self.paste.addTo(self.contextMenu)
		self.newFrm.addTo(self.contextMenu)
		self.deleteFrame.addTo(self.contextMenu)
		self.clrScreen.addTo(self.contextMenu)
		self.contextMenu.show()
		
#****************************************************************************************#
	#validate changes made to a storyboard before closing the application
	def closeEvent(self,ev):

		if self.maybeSave():
			ev.accept()
		else:
			ev.ignore()
			
#****************************************************************************************#

	def mouseMoveEvent(self, ev):

	    	position=ev.pos()
            	position.setX(position.x()-self.xoff)
	    	position.setY(position.y()-self.yoff)

            	p=QPainter()
            	p.begin(self.pix)
            	p.setPen(QPen(self.color,self.myPenWidth,self.penStyle))
            	if self.erase==true:
                   	self.eraseDrawing(QPoint(position))

            	else:
			p.drawLine(self.currentPos,position)
	    	self.currentPos=QPoint(position)	
	    	p.flush()
            	p.end()

		
	    	#This is to draw on the frame	
	    	p.begin(self.fmDraw)
	    	p.drawPixmap(self.rec.topLeft(),self.pix)
  			
#****************************************************************************************#

	def mousePressEvent(self, ev):
	
            	position=ev.pos()
            	position.setX(position.x()-self.xoff)
            	position.setY(position.y()-self.yoff)
             	self.currentPos=position
	    	
		self.modified=true	
			
#****************************************************************************************#
	def copyFrame(self):
		self.paste.setEnabled(1)
		self.copyPix=QPixmap(self.pix)
		
#****************************************************************************************#
	def pasteFrame(self):
		
		self.clearFrame()
		self.pix=QPixmap(self.copyPix)
		p=QPainter()
		p.begin(self.fmDraw)
	    	p.drawPixmap(self.rec.topLeft(),self.pix)
		p.end()
#****************************************************************************************#
	
	def setEraser(self):
		
		p=QPainter()
		p.begin(self.pix)
		self.erase=true
		self.frmSize.hide()
		self.frmErase.show()
		p.setPen(Qt.white)
		self.eraseOne()
		p.end()
		 	
#****************************************************************************************#

	def restorePen(self):
		
		 self.erase=false
		 self.frmSize.show()
		 self.frmErase.hide()
		 self.fmDraw.setCursor(Qt.crossCursor)
		 self.setOne()
		 
				 
#****************************************************************************************#

	def eraseDrawing(self,position):
		
		painter=QPainter(self.pix)
            	pen=QPen(Qt.white,self.eraseWidth)
		painter.setPen(pen)
	    	painter.drawLine(self.currentPos,position)
		self.currentPos=position
	    	painter.flush()
            	painter.end()	

	    	painter.begin(self.fmDraw)
	  	painter.drawPixmap(self.rec.topLeft(),self.pix)

#****************************************************************************************#
	
	def newFrame(self):
		
		#get current frame number before creating a fresh frame
                currentFrameNum = int(self.lineEdit7.text().ascii())
								
		frameInfo=self.getFrameInfo()# get information about the current frame
		
		#store current frame if the latter is a fresh frame
		if self.freshFrame==true:
			self.story.storeCurrentFrame(frameInfo,currentFrameNum)
			
		#update current frame 
		else:
			self.story.updateCurrentFrame(frameInfo,currentFrameNum)	
		 
		self.nextFrameNum = currentFrameNum + 1

		self.preButton.setEnabled(1) 
		self.fstButton.setEnabled(1)
		
		self.clearFrame()
                self.clearFrameInfo()
		self.lineEdit7.insert(str(self.nextFrameNum))#set the next frame number

		#This is the default values for some widgets
		self.radButLit1.setChecked(1)
		self.radButSnd1.setChecked(1)
		self.shtLen.insert("0")	
		self.freshFrame=true#a new frame has been added, so set freshFrame to true
		self.pbPlay.setEnabled(1)
		self.deleteFrame.setEnabled(1)
		self.undo.setEnabled(0)
		self.modified=true
		
									
#****************************************************************************************#

	def showColor(self):
		c=QColorDialog.getColor(self.colour(),self)
		if(c.isValid()):
			self.setColor(c)
			
#****************************************************************************************#
	
	def colour(self):
		
		return self.color
	
#****************************************************************************************#
	
	def setColor(self,col):
		
		self.color=col	

#****************************************************************************************#

	def previousFrame(self):
		
		currentFrameNum=int(self.lineEdit7.text().ascii())#get current frame number
		
		frameInfo=self.getFrameInfo()# get the current settings of the frame
		
		#try to view the previous frame but have not yet store current frame
		if currentFrameNum==self.nextFrameNum: #(previously from newframe)
			self.story.storeCurrentFrame(frameInfo,currentFrameNum)
			self.nextFrameNum=0
			
		else:#current frame have already been stored,so just update it
			self.story.updateCurrentFrame(frameInfo,currentFrameNum)
		
		preFrame=self.story.getPreviousFrame(currentFrameNum)#get the previous frame
		
		self.retrieveInfo(preFrame)#retrieve all the information of the frame
		
		self.clearFrame()#clear the drawing area
                self.clearFrameInfo()#clear the 'data entry' region (e.g) radioButtons,textBoxes etc....
		
		self.setFrame()# set all the retrieved information on screen
		
		# disable 'Previous Button' if previous frame is the first one
		if currentFrameNum==2:
			self.preButton.setEnabled(0)
			self.fstButton.setEnabled(0)
			
		self.nxtButton.setEnabled(1)	
		self.lstButton.setEnabled(1)
		self.freshFrame=false
		
#****************************************************************************************#

	def nextFrame(self):
		
		currentFrameNum=int(self.lineEdit7.text().ascii())#get current frame number
				
		frameInfo=self.getFrameInfo()
		
		#try to view the next frame but have not yet store current frame
		if currentFrameNum==self.nextFrameNum:
			self.story.storeCurrentFrame(frameInfo,currentFrameNum)
			self.nextFrameNum=0
			
		else:#current frame have already been stored,so just update it
			self.story.updateCurrentFrame(frameInfo,currentFrameNum)
					
		nxtFrame=self.story.getNextFrame(currentFrameNum)
		
		self.retrieveInfo(nxtFrame)
		self.ms=self.getRatio(int(self.getShtLen))
				
		if(self.play==true):
			#change interval of the timer to reflect shot length of each frame
			self.timer.changeInterval(self.ms)
			
			#update cummulative shot Length
			self.cumLen.setNum(int(str(self.cumLen.text()))+int(self.getShtLen))
		
				
		self.clearFrame()
                self.clearFrameInfo()
		
		#No addition of frame(s) in between the sequence of frames
		if int(self.getFNum)-currentFrameNum==1:
			self.setFrame()
			

		else:#if frame(s) have been inserted in between a sequence of frames
			nextFNum=currentFrameNum+1
			self.getFNum=str(nextFNum) #update frame number with regard to previous frame
			self.setFrame()	
					
		#when doing next frame and not playing the storyboard
		if self.play==false:
			self.preButton.setEnabled(1)
		
			self.fstButton.setEnabled(1)
						
		#disable 'next Button' if the next frame is the last one
		if (currentFrameNum + 1) == self.story.getListLen():
			self.nxtButton.setEnabled(0)
			self.lstButton.setEnabled(0)
			self.pbPause.setEnabled(0)
			
			# if the play option has been pressed and the last frame is reached,stop the timer
			if(self.play==true):
				self.timer.stop()
				self.play=false
				self.preButton.setEnabled(1)
				self.fstButton.setEnabled(1)
		
		self.freshFrame=false		
				
#****************************************************************************************#

	def playStoryboard(self): 
		
		currentFrameNum=int(self.lineEdit7.text().ascii())
		
		frameInfo=self.getFrameInfo()
		self.play=true
		self.timer=QTimer(self)#create a timer
		
				
		if currentFrameNum==self.nextFrameNum:
			self.story.storeCurrentFrame(frameInfo,currentFrameNum)
			self.nextFrameNum=0
					
		else:
			self.story.updateCurrentFrame(frameInfo,currentFrameNum)
		
		#In case we have reached the last frame
		if(currentFrameNum==self.story.getListLen()):
			firstFrame=self.story.getFirstFrame()
			self.clearFrame()
			self.clearFrameInfo()
			self.retrieveInfo(firstFrame)
			self.ms=self.getRatio(int(self.getShtLen))
			self.setFrame()
			self.cumLen.setNum(int(self.getShtLen))#current frame is the first frame
			self.connect(self.timer,SIGNAL('timeout()'),self.nextFrame)
		
		else:
			self.connect(self.timer,SIGNAL('timeout()'),self.nextFrame)
			self.ms=self.getRatio(int(self.shtLen.text().ascii()))
			loop=currentFrameNum
			num=0
			sum=0
			
			while(loop):#current frame is not the first frame,so calculate cummulative shot length 
				sum=sum+int(self.story.getShotlength(num))
				num=num+1
				loop=loop-1
			
			self.cumLen.setNum(sum)	
		
		self.timer.start(self.ms,true)# a 'timeout' signal is emitted by the timer every 'ms' milliseconds
		self.freshFrame=false
		
		self.pbPause.setEnabled(1)
		self.preButton.setEnabled(0)
		self.nxtButton.setEnabled(0)		
		self.lstButton.setEnabled(0)
		self.fstButton.setEnabled(0)
		
#****************************************************************************************#
	#calculate a 'play ratio' from the value of the shot Length for each shot,e.g a shot of shot Length 1 second will play for a duration of 100 milliseconds when the play button is pressed  
	def getRatio(self,sec):
		if sec ==1:
			ratio=100
			
		elif sec ==2 or sec==3:
			ratio=200
			
		elif sec==4 or sec==5:
			ratio=500
			
		elif sec==6 or sec==7:
			ratio=800
			
		else:
			ratio=1000
			
		
		return ratio				
			
		
#***************************************************************************************#
	def pauseStoryboard(self):
		
		currentFrameNum=int(self.lineEdit7.text().ascii())
		self.timer.stop() # stop the timer
		self.play=false
		
		if currentFrameNum == self.story.getListLen():
			self.nxtButton.setEnabled(0)
			self.lstButton.setEnabled(0)
		else:
			self.nxtButton.setEnabled(1)		
			self.lstButton.setEnabled(1)
		
		self.pbPause.setEnabled(0)
		self.preButton.setEnabled(1)
		self.fstButton.setEnabled(1)
				
#****************************************************************************************#

	def delFrame(self):
		
		self.undo.setEnabled(1)
	
		currentFrameNum=int(self.lineEdit7.text().ascii())
		listLen=self.story.getListLen()#get the length of the 'List' containing all the frames
		
		
		frameInfo=self.getFrameInfo()
		
		#deleting the last Frame
		if currentFrameNum==self.story.getListLen() or currentFrameNum==self.nextFrameNum:
			frm=self.story.getPreviousFrame(currentFrameNum)
			self.fmLast=true
		
		else:#deleting the first or the middle frame
			frm=self.story.getNextFrame(currentFrameNum)	
			self.fmLast=false	
		
		#deleting a stored frame
		if currentFrameNum != self.nextFrameNum :
			self.story.updateCurrentFrame(frameInfo,currentFrameNum)
			self.story.deleteCurrentFrame(currentFrameNum)
			
		else:#push the unsaved frame in the undo Buffer
			frameInfo=self.getFrameInfo()
			self.story.pushInBuf(frameInfo)
			
		self.clearFrame()
                self.clearFrameInfo()	
		
		self.retrieveInfo(frm)
		
		if self.fmLast==false:#update next frame number if deleting first or middle frame
			self.getFNum=str(currentFrameNum)
			
		self.setFrame()
				
		if currentFrameNum + 1 == listLen :#if the frame before the last one is deleted
			self.nxtButton.setEnabled(0)
			self.lstButton.setEnabled(0)	
				
			
		if (listLen-1)==1:
			self.preButton.setEnabled(0)
			self.fstButton.setEnabled(0)
			self.deleteFrame.setEnabled(0)
					
		self.nextFrameNum=0
		self.freshFrame=false
		self.modified=true
	
#****************************************************************************************#

	def undoDeleteFrame(self):
		
		self.deleteFrame.setEnabled(1)
				
		currentFrameNum=int(self.lineEdit7.text().ascii())		
		frameInfo=self.getFrameInfo()
		self.story.updateCurrentFrame(frameInfo,currentFrameNum)
		
		frm=self.story.popFromBuf()
		self.retrieveInfo(frm)
		
		self.story.storeCurrentFrame(frm,int(self.getFNum))
		self.clearFrame()
                self.clearFrameInfo()
		self.setFrame()
		listLen=self.story.getListLen()
				
		if int(self.getFNum)==1 :
			self.nxtButton.setEnabled(1)		
			self.lstButton.setEnabled(1)
			self.preButton.setEnabled(0)
			self.fstButton.setEnabled(0)
			
		
		elif int(self.getFNum)==listLen :
			self.preButton.setEnabled(1)
			self.fstButton.setEnabled(1)
			self.nxtButton.setEnabled(0)		
			self.lstButton.setEnabled(0)
			
		else:
			self.nxtButton.setEnabled(1)		
			self.lstButton.setEnabled(1)
			self.preButton.setEnabled(1)
			self.fstButton.setEnabled(1)
			
					
		if self.story.getUndoLen()==0:
			self.undo.setEnabled(0)
			
		self.freshFrame=false
		self.modified=true	
				
#****************************************************************************************#

	def fileSaveAs(self):
 		
		fileName=QFileDialog.getSaveFileName("./examples","*.sbrd",self,"Save","Save Storyboard As - BEstory")
				
		path=str(fileName)+'.sbrd'
		name=QFileInfo(fileName)
				
		if(not fileName.isEmpty()):
			if(QFile.exists(path)):
			
				ret=QMessageBox.warning(self,"Warning - BEstory",QString("Saving Failed!!\n' %1 ' already exists").arg(name.fileName()))
			
			else:				
				self.saveStoryboard(fileName)
				
#****************************************************************************************#

	def saveStoryboard(self,path):
		
		qApp.setOverrideCursor(self.cursor)
		
		currentFrameNum=int(self.lineEdit7.text().ascii())
		
		frameInfo=self.getFrameInfo()
		
		if currentFrameNum==self.nextFrameNum or self.story.getListLen()==0:
			self.story.storeCurrentFrame(frameInfo,currentFrameNum)
			self.nextFrameNum=0
			
		else:
			self.story.updateCurrentFrame(frameInfo,currentFrameNum)
			
		self.story.saveCurrentStoryboard(path)	
		self.alreadySaved=true
		self.modified=false
		self.freshFrame=false
		
		qApp.restoreOverrideCursor()	
#****************************************************************************************#

	def fileOpen(self):
		
			self.maybeSave()
			fileName=QFileDialog.getOpenFileName("./examples","*.sbrd \nImages (*.png *.xpm *.jpg)",self,"Open ","Open - BEstory") 
		
			if(not fileName.isEmpty()):
				self.loadStoryboard(fileName)
													
#****************************************************************************************#

	def loadStoryboard(self,path):
		
		qApp.setOverrideCursor(self.cursor)
		
		self.clearFrame()
		
		
		check=path[len(path)-4:len(path)]# get the extension of the file only
				
		if check=='sbrd':#if loading a storyboard i.e. a database file
			
			self.setInitValues()
			self.loading=true
			self.story.loadFromFile(path)
			firstFrame=self.story.getFirstFrame()
			
			self.retrieveInfo(firstFrame)
		
			self.clearFrameInfo()
			self.setFrame()
						
			if self.story.getListLen() > 1:
				 self.nxtButton.setEnabled(1)
				 self.lstButton.setEnabled(1)
				 self.pbPlay.setEnabled(1)
				 self.deleteFrame.setEnabled(1)
				 			
			
		else:#if loading an image only
			
			image=QImage()
			image.load(path)						
			im=image.smoothScale(self.fmDraw.width(),self.fmDraw.height(),QImage.ScaleFree)#scaled the image to the width and height of the drawing area
			
			paint=QPainter()
			
			#paint the scaled image on the drawing area's 'Pixmap' 
			paint.begin(self.pix)
			paint.drawImage(self.rec.topLeft(),im)
			paint.flush()
			paint.end()
			self.modified=true	
			
		self.freshFrame=false
		qApp.restoreOverrideCursor()	
#****************************************************************************************#

	def fileSave(self):
				
		if self.alreadySaved==false and self.loading==false:
			self.fileSaveAs()
		else:
			qApp.setOverrideCursor(self.cursor)
			currentFrameNum=int(self.lineEdit7.text().ascii())
		
			frameInfo=self.getFrameInfo()
					
			if currentFrameNum==self.nextFrameNum or self.story.getListLen()==0:
				self.story.storeCurrentFrame(frameInfo,currentFrameNum)
				self.nextFrameNum=0
							
			else:
				self.story.updateCurrentFrame(frameInfo,currentFrameNum)
							
			self.story.saveChanges()	
			self.modified=false
			self.freshFrame=false
		
			qApp.restoreOverrideCursor()	
##****************************************************************************************#

	def fstFrame(self):
		
		currentFrameNum=int(self.lineEdit7.text().ascii())
		frameInfo=self.getFrameInfo()
		
		if currentFrameNum==self.nextFrameNum:
			self.story.storeCurrentFrame(frameInfo,currentFrameNum)
			self.nextFrameNum=0
			
		else:
			self.story.updateCurrentFrame(frameInfo,currentFrameNum)
		
		
		firstFrame=self.story.getFirstFrame()
		self.clearFrame()
		self.clearFrameInfo()
		self.retrieveInfo(firstFrame)
		self.setFrame()
		
		self.preButton.setEnabled(0)
				
		self.fstButton.setEnabled(0)
		
		self.nxtButton.setEnabled(1)
				
		self.lstButton.setEnabled(1)
		self.freshFrame=false
						
#****************************************************************************************#

	def lstFrame(self):
		
		currentFrameNum=int(self.lineEdit7.text().ascii())
		frameInfo=self.getFrameInfo()

		if currentFrameNum==self.nextFrameNum:
			self.story.storeCurrentFrame(frameInfo,currentFrameNum)
			self.nextFrameNum=0

		else:
			self.story.updateCurrentFrame(frameInfo,currentFrameNum)

		#if not the last frame,update frame num of the the following frames
		if not(currentFrameNum == self.story.getListLen()):
			
			index=currentFrameNum
			diff=self.story.getListLen()-index
			while(diff):
				self.story.updateList(index)
				diff=diff-1
				index=index+1
		
		lastFrame=self.story.getLastFrame()
		self.clearFrame()
		self.clearFrameInfo()
		self.retrieveInfo(lastFrame)
		self.setFrame()


		self.nxtButton.setEnabled(0)
		self.lstButton.setEnabled(0)
		self.fstButton.setEnabled(1) 
		self.preButton.setEnabled(1)
		self.freshFrame=false
		

#****************************************************************************************#

	def printing(self):
		
		currentFrameNum=int(self.lineEdit7.text().ascii())
		
		#lists containing options for shot size and camera movement
		self.stSize=['XLS','LS','MLS','MS','MCU','CU','BCU','XCU']
		self.cmMov=['Fx','PR','PL','PU','PD','ZI','TF','TB','TV','TL','TC','ZO']
		
		brush=QBrush(Qt.lightGray,Qt.SolidPattern)
		printer=QPrinter(QPrinter.ScreenResolution)
		
		frameInfo=self.getFrameInfo()
		
		if currentFrameNum==self.nextFrameNum or self.story.getListLen()==0:
			self.story.storeCurrentFrame(frameInfo,currentFrameNum)
			self.nextFrameNum=0
								
		else:
			self.story.updateCurrentFrame(frameInfo,currentFrameNum)
		
		listLen=self.story.getListLen()
		
		if(printer.setup(self)):#if user presses OK on the print dialog,printing is processed 
			p=QPainter()
			p.begin(printer)
			shot=1
			cumLen=0
			qApp.setOverrideCursor(self.cursor)
			
			while(listLen):
				
				printFrame=self.story.getFrame(shot)
				self.retrieveInfo(printFrame)
				cumLen=cumLen+int(self.getShtLen)
				
				#resize the image before printing so as to fit two shots on a single page 
				self.printWidth=(self.fmDraw.width()*3)/4
				self.printHeight=(self.fmDraw.height()*3)/4
				
				#this code segment caters for printing two shots on a single page
				newY=0
				#if shot number is even,printing is carried out on the 2nd half of the page
				if (int(self.getFNum)%2)==0:
					newY=self.printHeight+220
					
				#print the image and a surrounding rectangle
				image=self.getPixmap.convertToImage()
				im=image.smoothScale(self.printWidth,self.printHeight,QImage.ScaleFree)
				rec=QRect(0,self.fmDraw.y()+newY,self.printWidth,self.printHeight)
				p.drawImage(rec.topLeft(),im)
				p.drawRect(rec)
			
				#Frame Number
				p.drawText(self.printWidth+10,self.fmDraw.y()+newY,self.textLabel2_3.text(),-1,p.Auto)
				p.drawLine(self.printWidth+70,self.fmDraw.y()+3+newY,self.printWidth+120,self.fmDraw.y()+3+newY)
				p.drawText(self.printWidth+70,self.fmDraw.y()+1+newY,self.getFNum,-1,p.Auto)
			
				#Lighting
				p.drawText(self.printWidth+10,self.fmDraw.y()+40+newY,self.groupBox2.title(),-1,p.Auto)
				self.drawNum(p,self.fmDraw.y()+40+newY,1)
				self.drawCircle1(p,int(self.getButLit),self.fmDraw.y()+20+newY)
				
				#Sound
				p.drawText(self.printWidth+10,self.fmDraw.y()+80+newY,self.groupBox3.title(),-1,p.Auto)
				self.drawNum(p,self.fmDraw.y()+80+newY,2)
				self.drawCircle1(p,int(self.getButSnd),self.fmDraw.y()+60+newY)
			
				#Shot Size
				p.drawRect(self.printWidth+10,self.fmDraw.y()+110+newY,260,20)
				p.fillRect(self.printWidth+10,self.fmDraw.y()+110+newY,260,20,brush)
				p.drawText(self.printWidth+110,self.fmDraw.y()+125+newY,self.textLabel3.text(),9,p.Auto)
				
				p.drawText(self.printWidth+10,self.fmDraw.y()+160+newY,"XLS",-1,p.Auto)
				p.drawText(self.printWidth+80,self.fmDraw.y()+160+newY,"LS",-1,p.Auto)
				p.drawText(self.printWidth+150,self.fmDraw.y()+160+newY,"MLS",-1,p.Auto)
				p.drawText(self.printWidth+220,self.fmDraw.y()+160+newY,"MS",-1,p.Auto)
												
				p.drawText(self.printWidth+10,self.fmDraw.y()+190+newY,"MCU",-1,p.Auto)
				p.drawText(self.printWidth+80,self.fmDraw.y()+190+newY,"CU",-1,p.Auto)
				p.drawText(self.printWidth+150,self.fmDraw.y()+190+newY,"BCU",-1,p.Auto)
				p.drawText(self.printWidth+220,self.fmDraw.y()+190+newY,"XCU",-1,p.Auto)
				
				self.drawCircle2(p,1,self.getShtSize,self.fmDraw.y()+140+newY)
				
			
				#Camera Movement
				p.drawRect(self.printWidth+10,self.fmDraw.y()+210+newY,260,20)
				p.fillRect(self.printWidth+10,self.fmDraw.y()+210+newY,260,20,brush)
				p.drawText(self.printWidth+85,self.fmDraw.y()+225+newY,self.textLabel4.text(),15,p.Auto)
				
				p.drawText(self.printWidth+10,self.fmDraw.y()+260+newY,"Fx",-1,p.Auto)
				p.drawText(self.printWidth+60,self.fmDraw.y()+260+newY,"PR",-1,p.Auto)
				p.drawText(self.printWidth+110,self.fmDraw.y()+260+newY,"PL",-1,p.Auto)
				p.drawText(self.printWidth+160,self.fmDraw.y()+260+newY,"PU",-1,p.Auto)
				p.drawText(self.printWidth+210,self.fmDraw.y()+260+newY,"PD",-1,p.Auto)
				p.drawText(self.printWidth+260,self.fmDraw.y()+260+newY,"ZI",-1,p.Auto)
				
				p.drawText(self.printWidth+10,self.fmDraw.y()+290+newY,"TF",-1,p.Auto)
				p.drawText(self.printWidth+60,self.fmDraw.y()+290+newY,"TB",-1,p.Auto)
				p.drawText(self.printWidth+110,self.fmDraw.y()+290+newY,"TV",-1,p.Auto)
				p.drawText(self.printWidth+160,self.fmDraw.y()+290+newY,"TL",-1,p.Auto)
				p.drawText(self.printWidth+210,self.fmDraw.y()+290+newY,"TC",-1,p.Auto)
				p.drawText(self.printWidth+260,self.fmDraw.y()+290+newY,"ZO",-1,p.Auto)
				
				self.drawCircle2(p,2,self.getCamMov,self.fmDraw.y()+240+newY)
			
				#Shot Length
				p.drawText(0,self.printHeight+40+newY,self.textLabel6.text(),-1,p.Auto)
				p.drawLine(80,self.printHeight+40+newY,300,self.printHeight+40+newY)
				p.drawText(80,self.printHeight+38+newY,self.getShtLen,-1,p.Auto)
			
				#Music
				p.drawText(self.printWidth-100,self.printHeight+40+newY,self.textLabel12.text(),-1,p.Auto)
				p.drawLine(self.printWidth-50,self.printHeight+40+newY,700,self.printHeight+40+newY)
				p.drawText(self.printWidth-50,self.printHeight+38+newY,self.getMusic,-1,p.Auto)
			
				#Cummulative Length
				p.drawText(0,self.printHeight+80+newY,self.textLabel7.text(),-1,p.Auto)
				p.drawLine(130,self.printHeight+80+newY,300,self.printHeight+80+newY)
				p.drawText(130,self.printHeight+78+newY,str(cumLen),-1,p.Auto)
			
				#Sound Effect
				p.drawText(self.printWidth-100,self.printHeight+80+newY,self.textLabel13.text(),-1,p.Auto)
				p.drawLine(self.printWidth-10,self.printHeight+80+newY,700,self.printHeight+80+newY)
				p.drawText(self.printWidth-10,self.printHeight+78+newY,self.getSndEff,-1,p.Auto)
			
				#Text
				p.drawText(0,self.printHeight+120+newY,self.textLabel14.text(),-1,p.Auto)
				p.drawLine(40,self.printHeight+120+newY,700,self.printHeight+120+newY)
				p.drawLine(0,self.printHeight+140+newY,700,self.printHeight+140+newY)
				p.drawText(40,self.printHeight+118+newY,self.getText,-1,p.Auto)
			
				#Transition
				p.drawText(0,self.printHeight+180+newY,self.textLabel5.text(),-1,p.Auto)
				p.drawText(120,self.printHeight+180+newY,"Cut",-1,p.Auto)
				p.drawText(180,self.printHeight+180+newY,"Dissolve(mix)",-1,p.Auto)
				p.drawText(300,self.printHeight+180+newY,"Fade in",-1,p.Auto)
				p.drawText(380,self.printHeight+180+newY,"Fade out",-1,p.Auto)
				self.drawCircle3(p,self.getTrans,newY)
				
				shot=shot+1
				listLen=listLen-1
				
				#when ListLen=0 and shot having odd 'shot number' has been printed, no new page is generated
				if listLen>0 and (int(self.getFNum)%2)==0:
					printer.newPage()
					 
									
			p.end()
			
			qApp.restoreOverrideCursor()
		self.freshFrame=false		
#****************************************************************************************#
	def drawNum(self,d,y,option):# draw Number for 'Lighting' and 'Sound' when printing
		
		d.drawText(self.printWidth+70,y,QString('1'),-1,d.Auto)
		d.drawText(self.printWidth+100,y,QString('2'),-1,d.Auto)
		d.drawText(self.printWidth+130,y,QString('3'),-1,d.Auto)
		if option==2:#for Sound
			d.drawText(self.printWidth+160,y,QString('OFF'),-1,d.Auto)
			

#****************************************************************************************#

	def drawCircle1(self,d,x,y):#draw circle to indicate chose of lighting and sound
		d.drawRoundRect(self.printWidth+(30*x+30),y,35,30,70,70)
#*****************************************************************************************#
	def drawCircle2(self,d,option,chose,y):#draw circle to indicate chose of shot size and Camera Movement
		
		
		if option==1:#encircle 'size(XLS,LS,....)' of shot 
			index=3
			offset=4
			x=0
			interval=70
			for w in self.stSize:
				if(w==chose):
					break
				x=x+1
		
		else:#encircle 'movement(Fx,PR,....)' of camera 
			index=5
			offset=6
			x=0
			interval=50
			for w in self.cmMov:
				if(w==chose):
					break
				x=x+1
								
		if x>index:#set x in the appropriate range,(0-3) for shot size and (0-5) for camera movement
			x=x-offset
			y=y+30
		
		d.drawRoundRect(self.printWidth+(interval*x+5),y,35,30,70,70)
#*****************************************************************************************#
	def drawCircle3(self,d,chose,y):#draw circle to indicate type of Transition
		
		if chose=='Cut':
			d.drawRoundRect(110,self.printHeight+160+y,60,30,70,70)
		
		elif chose=='Dissolve(mix)':
			d.drawRoundRect(170,self.printHeight+160+y,90,30,70,70)
		
		elif chose=='Fade In':
			d.drawRoundRect(290,self.printHeight+160+y,60,30,70,70)
		else:
			d.drawRoundRect(370,self.printHeight+160+y,60,30,70,70)	
				
				
		
#****************************************************************************************#
	def retrieveInfo(self,fm):

		self.getPixmap=QPixmap(fm.pixmap)
		self.getButLit=fm.buttonLit
		self.getButSnd=fm.buttonSnd
		self.getShtLen=fm.shtLength
		self.getMusic=fm.musicType
		self.getSndEff=fm.sndEffect
		self.getText=fm.enterText
		self.getFNum=fm.frmNum
		self.getShtSize=fm.shotSize
		self.getCamMov=fm.cameraMov
		self.getTrans=fm.transitn

#****************************************************************************************#
	#set image and textual information for the 'current shot' on the screen
	def setFrame(self):

		pixm=QPixmap(self.getPixmap)

		#draw on the pixamp because the latter is actually blank
		paint=QPainter()
		paint.begin(self.pix)
		paint.drawPixmap(self.rec.topLeft(),pixm)
		paint.flush()
		paint.end()

		#Draw on the screen
		paint.begin(self.fmDraw)
		paint.drawPixmap(self.rec.topLeft(),self.pix)
		paint.end()

		# This is for the light style
		if self.getButLit=='1':
			self.radButLit1.setChecked(1)
		if self.getButLit=='2':
			self.radButLit2.setChecked(1)
		if self.getButLit=='3':
			self.radButLit3.setChecked(1)

		#This is for the sound style
		if self.getButSnd=='1':
			self.radButSnd1.setChecked(1)
		if self.getButSnd=='2':
			self.radButSnd2.setChecked(1)
		if self.getButSnd=='3':
			self.radButSnd3.setChecked(1)
		if self.getButSnd=='4':
			self.radButSndOff.setChecked(1)	

		#This is for the LineEdit and TextEdit
		self.shtLen.insert(self.getShtLen)
		self.music.insert(self.getMusic)
		self.sndEff.insert(self.getSndEff)
		self.textEdit3.setText(self.getText)
		self.lineEdit7.insert(self.getFNum)

		#This is for the comboBoxes
		self.comboBox1.setCurrentText(self.getShtSize)
		self.comboBox2.setCurrentText(self.getCamMov)
		self.comboBox3.setCurrentText(self.getTrans)

#****************************************************************************************#
	#clear the drawing area
	def clearFrame(self):

		self.pix.fill(self.fmDraw,self.rec.topLeft())
		self.fmDraw.erase(0,0,550,460)

#****************************************************************************************#
	#clear widgets holding the textual information
	def clearFrameInfo(self):

            	self.radButLit1.setChecked(0)
	    	self.radButLit2.setChecked(0)
            	self.radButLit3.setChecked(0)
	    	self.radButSnd1.setChecked(0)
            	self.radButSnd2.setChecked(0)
	    	self.radButSnd3.setChecked(0)
	       	self.radButSndOff.setChecked(0)
	    	self.shtLen.clear()
            	self.music.clear()
            	self.sndEff.clear()
            	self.textEdit3.clear()
            	self.lineEdit7.clear()
		
		if self.play==false:
			self.cumLen.clear()

#****************************************************************************************#
	#get image and textual information for the 'current shot' from the screen
	def getFrameInfo(self):
		pm=QPixmap(self.pix)  #Save a copy of the pixmap in the first buffer
		
		if self.radButLit1.isChecked()==1:
			butLit='1'
		if self.radButLit2.isChecked()==1:	
			butLit='2'
		if self.radButLit3.isChecked()==1:	
                	butLit='3'
		if self.radButSnd1.isChecked()==1:
			butSnd='1'
		if self.radButSnd2.isChecked()==1:
			butSnd='2'
		if self.radButSnd3.isChecked()==1:
			butSnd='3'
		if self.radButSndOff.isChecked()==1:
			butSnd='4'

                shotLen=self.shtLen.text().ascii()
                setMusic=self.music.text().ascii()
                soundEff=self.sndEff.text().ascii()
        	userText=self.textEdit3.text().ascii()
		fNum=self.lineEdit7.text().ascii()
		combo1=self.comboBox1.currentText().ascii()
		combo2=self.comboBox2.currentText().ascii()
		combo3=self.comboBox3.currentText().ascii()

		store=FrameInfo(pm,butLit,butSnd,shotLen,setMusic,soundEff,userText,fNum,combo1,combo2,combo3)
	
		return store


#****************************************************************************************#	
	def maybeSave(self):
	

		if (self.modified):
			ret=QMessageBox.warning(self,"Warning-BEstory",
			"The current StoryBoard has been modified.\n"
			"Do you want to save it?",
			QMessageBox.Yes|QMessageBox.Default,
			QMessageBox.No,
			QMessageBox.Cancel|QMessageBox.Escape)
			
			if (ret==QMessageBox.Yes):
				if self.alreadySaved==true or self.loading==true:
					
					self.fileSave()
					return true	
				
				else:
					self.fileSaveAs()
					return true	
								
			elif(ret==QMessageBox.No):
				return true
			
			else:
				if(ret==QMessageBox.Cancel):
					return false
		return true

#****************************************************************************************#
	
	def newStoryboard(self):
		
		if (self.maybeSave()):
			self.setInitValues()
		
			self.clearFrame()
			self.clearFrameInfo()
			self.shtLen.insert("0")		
			self.lineEdit7.insert('1')
			self.radButLit1.setChecked(1)
			self.radButSnd1.setChecked(1)
				
#****************************************************************************************#
	
  	def exitStoryboard(self): 
		
		if(self.maybeSave()):
			qApp.quit()
				
#****************************************************************************************#			
	def helpAboutQt(self):
		
		QMessageBox.aboutQt(self,"BEstory -- About Qt")
				
#****************************************************************************************#
		
	def helpAbout(self):
		
		QMessageBox.about(self,"About BEstory",
               		"<h2>BEstory 1.0</h2>"
               		"<p>Copyright &copy;2006 Kervin & Rina."
               		"<p>BEstory is an application that allow users to rapidly create "
               		"<b>Storyboards</b>.")
		
#****************************************************************************************#
	
	def pen(self):
		
		return self.myPenWidth
	
#****************************************************************************************#
	
	def setPenWidth(self,newWidth):
		
		self.myPenWidth=newWidth
		
#****************************************************************************************#
		
	def setOne(self):
				
		self.sizeOne.setPaletteBackgroundColor(QColor(150,150,150))
		self.sizeTwo.setPaletteBackgroundColor(QColor(230,230,230))
		self.sizeThree.setPaletteBackgroundColor(QColor(230,230,230))
		self.sizeFour.setPaletteBackgroundColor(QColor(230,230,230))
		self.sizeFive.setPaletteBackgroundColor(QColor(230,230,230))
		
		self.setPenWidth(1)
	
	
#****************************************************************************************#

	def setTwo(self):
		
		self.sizeOne.setPaletteBackgroundColor(QColor(230,230,230))
		self.sizeTwo.setPaletteBackgroundColor(QColor(150,150,150))
		self.sizeThree.setPaletteBackgroundColor(QColor(230,230,230))
		self.sizeFour.setPaletteBackgroundColor(QColor(230,230,230))
		self.sizeFive.setPaletteBackgroundColor(QColor(230,230,230))
		self.setPenWidth(2)
		
		
#****************************************************************************************#

	def setThree(self):
		
		self.sizeOne.setPaletteBackgroundColor(QColor(230,230,230))
		self.sizeThree.setPaletteBackgroundColor(QColor(150,150,150))
		self.sizeTwo.setPaletteBackgroundColor(QColor(230,230,230))
		self.sizeFour.setPaletteBackgroundColor(QColor(230,230,230))
		self.sizeFive.setPaletteBackgroundColor(QColor(230,230,230))
		self.setPenWidth(3)
		
#****************************************************************************************#
	
	def setFour(self):
		
		self.sizeOne.setPaletteBackgroundColor(QColor(230,230,230))
		self.sizeFour.setPaletteBackgroundColor(QColor(150,150,150))
		self.sizeThree.setPaletteBackgroundColor(QColor(230,230,230))
		self.sizeTwo.setPaletteBackgroundColor(QColor(230,230,230))
		self.sizeFive.setPaletteBackgroundColor(QColor(230,230,230))
		
		
		self.setPenWidth(4)
			
#****************************************************************************************#
	
	def setFive(self):
		
		self.sizeOne.setPaletteBackgroundColor(QColor(230,230,230))
		self.sizeFive.setPaletteBackgroundColor(QColor(150,150,150))
		self.sizeThree.setPaletteBackgroundColor(QColor(230,230,230))
		self.sizeFour.setPaletteBackgroundColor(QColor(230,230,230))
		self.sizeTwo.setPaletteBackgroundColor(QColor(230,230,230))
		
		
		self.setPenWidth(5)
		
#****************************************************************************************#		
	def pen(self):
		return self.eraseWidth
	
#****************************************************************************************#
	
	def setEraseWidth(self,newWidth):
		
		self.eraseWidth=newWidth
		
#****************************************************************************************#
		
	def eraseOne(self):
				
		pix1=QPixmap()
		pix1.load("./eraser/s1.png")
		self.erase1.setPaletteBackgroundColor(QColor(150,150,150))
		
		self.erase2.setPaletteBackgroundColor(QColor(230,230,230))
		self.erase3.setPaletteBackgroundColor(QColor(230,230,230))
		self.erase4.setPaletteBackgroundColor(QColor(230,230,230))
		self.erase5.setPaletteBackgroundColor(QColor(230,230,230))
		self.fmDraw.setCursor(QCursor(pix1,16,16))
		self.setEraseWidth(5)
	
	
#****************************************************************************************#

	def eraseTwo(self):
		
		
		pix2=QPixmap()
		pix2.load("./eraser/s2.png")
		self.erase2.setPaletteBackgroundColor(QColor(150,150,150))
		
		self.erase1.setPaletteBackgroundColor(QColor(230,230,230))
		self.erase3.setPaletteBackgroundColor(QColor(230,230,230))
		self.erase4.setPaletteBackgroundColor(QColor(230,230,230))
		self.erase5.setPaletteBackgroundColor(QColor(230,230,230))
		self.fmDraw.setCursor(QCursor(pix2,16,16))
		self.setEraseWidth(10)
		
		
#****************************************************************************************#

	def eraseThree(self):
		
		pix3=QPixmap()
		pix3.load("./eraser/s3.png")
		self.erase3.setPaletteBackgroundColor(QColor(150,150,150))		
		
		self.erase1.setPaletteBackgroundColor(QColor(230,230,230))
		self.erase2.setPaletteBackgroundColor(QColor(230,230,230))
		self.erase4.setPaletteBackgroundColor(QColor(230,230,230))
		self.erase5.setPaletteBackgroundColor(QColor(230,230,230))
		self.fmDraw.setCursor(QCursor(pix3,16,16))
		self.setEraseWidth(15)
		
#****************************************************************************************#
	
	def eraseFour(self):
		pix4=QPixmap()
		pix4.load("./eraser/s4.png")
		self.erase4.setPaletteBackgroundColor(QColor(150,150,150))
		
		self.erase1.setPaletteBackgroundColor(QColor(230,230,230))
		self.erase2.setPaletteBackgroundColor(QColor(230,230,230))
		self.erase3.setPaletteBackgroundColor(QColor(230,230,230))
		self.erase5.setPaletteBackgroundColor(QColor(230,230,230))
		self.fmDraw.setCursor(QCursor(pix4,16,16))
		self.setEraseWidth(25)
			
#****************************************************************************************#
	
	def eraseFive(self):
		pix5=QPixmap()
		pix5.load("./eraser/s5.png")	
		self.erase5.setPaletteBackgroundColor(QColor(150,150,150))
		
		self.erase1.setPaletteBackgroundColor(QColor(230,230,230))
		self.erase2.setPaletteBackgroundColor(QColor(230,230,230))
		self.erase3.setPaletteBackgroundColor(QColor(230,230,230))
		self.erase4.setPaletteBackgroundColor(QColor(230,230,230))
		
		self.fmDraw.setCursor(QCursor(pix5,16,16))
		self.setEraseWidth(35)
		
#****************************************************************************************#		
				
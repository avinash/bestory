from database import Database
from frameinfo import FrameInfo
from qt import *



class Storyboard:
	
	def __init__(self):
		
		#these two 'lists' hold the textual information for each image
        	self.frameList=[]
		self.undoBuffer=[]
				
		self.cntUndoBuf=0
					
		self.pxm=QPixmap()
								
#****************************************************************************************#
		
	def storeCurrentFrame(self,frame,num):
		
		self.frameList.insert(num-1,frame)
		
#****************************************************************************************#
	
	def updateCurrentFrame(self,frame,num):
		
		self.frameList[(num-1)]=frame
					
#****************************************************************************************#	

	def getPreviousFrame(self,num):
   			
		fm=self.frameList[(num-2)]
		return fm
	
#****************************************************************************************#

	def getNextFrame(self,num):
		
		frame=self.frameList[num]
		return frame
	
#****************************************************************************************#

	def getFirstFrame(self):
		
		frame=self.frameList[0]
		return frame
	
#****************************************************************************************#

	def getLastFrame(self):
		
		frame=self.frameList[(len(self.frameList)-1)]
		return frame
		
#****************************************************************************************#

 	def getListLen(self):
		
		return len(self.frameList)
	
#****************************************************************************************#
	def updateList(self,index):
		self.frameList[index].frmNum=str(index+1)
#****************************************************************************************#
	def getShotlength(self,num):
		return self.frameList[num].shtLength
#****************************************************************************************#

	def deleteCurrentFrame(self,num):
		
		self.pushInBuf(self.frameList[(num-1)])
		self.frameList.remove(self.frameList[(num-1)])
			
#****************************************************************************************#

	def getFrame(self,num): 
		
		frame=self.frameList[(num-1)]
		return frame
	
#****************************************************************************************#	

	def popFromBuf(self):
		
	   	frame=self.undoBuffer.pop()
		self.cntUndoBuf=self.cntUndoBuf - 1
		return frame
	
#****************************************************************************************#
	
	def pushInBuf(self,frame):
		
		if self.cntUndoBuf==2:
			self.undoBuffer[0]=self.undoBuffer[1]
			del self.undoBuffer[1]
			self.cntUndoBuf=self.cntUndoBuf-1
					
		self.undoBuffer.append(frame)
			
		self.cntUndoBuf=self.cntUndoBuf+1
				
#****************************************************************************************#
	def getUndoLen(self):
		
		return len(self.undoBuffer)
	
#****************************************************************************************#

	def saveCurrentStoryboard(self,path):
		
		self.filepath=str(path)
		count=len(self.filepath)
		
		#get only the 'storyboard name' from the path
		while(count):
			count=count-1
			if self.filepath[count]=="/":
				count=0
			else:
				storyName=self.filepath[count:len(self.filepath)]
				
		path=self.filepath+".sbrd" #add .sbrd to the path
		
		self.db=Database(path)
			
		self.db.createTable()
		self.db.insertIntoBoard(storyName,self.getListLen())
		self.db.insertIntoFrame(self.frameList,self.filepath)
		
#****************************************************************************************#
		
	def loadFromFile(self,path):
		
		self.filepath=str(path[:len(path)-5])#get file path without .sbrd extension
		
		self.frameList=[]
		self.db=Database(str(path))
		
		numF=self.db.getNumOfFrame()
				
		sData=self.db.getStoryboardData()
				
		cnt=len(self.filepath)	
		
		#remove the 'storyboard Name' from the path
		while(cnt):
			cnt=cnt-1
			if self.filepath[cnt]=="/":
				imagePath=self.filepath[:cnt+1]
				cnt=0
			
						
		while(numF):
			
			#get textual information from the database file
			shtNum=str(sData[cnt].shotNum)
			light=sData[cnt].lighting
			snd=sData[cnt].sound
			shtSize=sData[cnt].shotSize
			camera=sData[cnt].camMov
			shtLen=str(sData[cnt].shotLen)
			musicType=sData[cnt].music
			sndEff=sData[cnt].soundEff
			text=sData[cnt].comment
			transitn=sData[cnt].transition
			imFileName=sData[cnt].imageFileName
						
			#get the images from the image files
			self.pxm.load(imagePath+imFileName)
			
			pixm=QPixmap(self.pxm)
			store=FrameInfo(pixm,light,snd,shtLen,musicType,sndEff,text,shtNum,shtSize,camera,transitn)
			self.frameList[cnt:]=[store]
			
			cnt=cnt+1
			numF=numF-1
	
	
#****************************************************************************************#

	def saveChanges(self):
		self.db.updateBoard(self.getListLen())
		self.db.deleteFromFrame()
		self.db.insertIntoFrame(self.frameList,self.filepath)
		
#****************************************************************************************#	
	
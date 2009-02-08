import sqlite


class Database:
			
	def __init__(self,filePath):
		self.cx=sqlite.connect(filePath)
		self.cu=self.cx.cursor()
		
		
#********************************************************************************#		
	
	def createTable(self):
				
		self.cu.execute("""Create table frame(fmId INTEGER PRIMARY KEY,
				shotNum integer (2),
				lighting varchar(15),
				sound varchar (15),
				shotSize varchar,  
				camMov  varchar(15),
				shotLen  integer,
				music    text,
				soundEff  text,
				comment   text,
				transition varchar(15),
				imageFileName varchar(225))""")
					
		
		self.cu.execute("""create table board (storyId integer Primary Key,	
				storyName varchar(225),
				numOfFrame  integer)""")
					
		self.cx.commit()
#********************************************************************************#		
		    
	def getNumOfFrame(self):
		self.cu.execute("--types integer")
		self.cu.execute("select numOfFrame from board")
		row=self.cu.fetchone()
		num=row.numOfFrame
		return num
#********************************************************************************#		
			
	def getStoryboardData(self):
		
		self.cu.execute("""--types integer, varchar,varchar,varchar,varchar,integer,text,text,text,varchar,varchar""")
			
		self.cu.execute("select * from frame ")
		row=self.cu.fetchall()
		return row
	
#********************************************************************************#		
		
	def insertIntoFrame(self,storyData,fPath):
		
		numFrame=self.getNumOfFrame()
		
		count=0
		while(numFrame):
			self.getFrameData(storyData[count])
			imagePath=fPath+'_'+str(count+1)+'.png'
			
			#gets the 'storyboard Name' from table 'board'
			self.cu.execute("--types varchar")
			self.cu.execute("select storyName from board")
			row=self.cu.fetchone()
			imageName=row.storyName+'_'+str(count+1)+'.png'
			
			self.cu.execute("""insert into frame
			(shotNum,lighting,sound,shotSize,camMov,shotLen,music,soundEff,comment,
			transition,imageFileName)
			values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
			(self.fNum,self.butLit,self.butSnd,self.shtSize,self.camMov,self.sLen,self.music,self.sndEff,self.text,self.transitn,imageName))
			
			self.cx.commit()
			numFrame=numFrame-1
			count=count+1
			self.pixm.save(imagePath ,"PNG")#save images for a storyboard at location specified by 'imagePath'	
		
#********************************************************************************#		
					
	def insertIntoBoard(self,SName,numOfFrame):
		
		self.cu.execute("""insert into board(storyName,numOfFrame)
		values(%s,%s)""",
		(SName,numOfFrame))
						
		self.cx.commit()  
#********************************************************************************#		
	
	def deleteFromFrame(self):
				
		self.cu.execute("delete from frame")
		self.cx.commit()		
#********************************************************************************#		
					
	def updateBoard(self,cntFrame):
				
		self.cu.execute("update board set numOfFrame=%s",(cntFrame))
		self.cx.commit()
#********************************************************************************#		
	#extract textual information for each image in the storyboard						
	def getFrameData(self,fm):

		self.pixm=fm.pixmap
		self.butLit=fm.buttonLit
		self.butSnd=fm.buttonSnd
		self.sLen=fm.shtLength
		self.music=fm.musicType
		self.sndEff=fm.sndEffect
		self.text=fm.enterText
		self.fNum=fm.frmNum
		self.shtSize=fm.shotSize
		self.camMov=fm.cameraMov
		self.transitn=fm.transitn					
#*************************************************************************************#
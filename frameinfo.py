from qt import *
import sys
 
class FrameInfo:
	 def __init__(self,pm,butLit,butSnd,shotLen,setMusic,soundEff,userText,fNum,combo1,combo2,combo3):
		 
		 self.pixmap=pm
		 self.buttonLit=butLit
		 self.buttonSnd=butSnd
		 self.shtLength=shotLen
		 self.musicType=setMusic
		 self.sndEffect=soundEff
		 self.enterText=userText
		 self.frmNum=fNum
		 self.shotSize=combo1
		 self.cameraMov=combo2
		 self.transitn=combo3
#*************************************************************************************#
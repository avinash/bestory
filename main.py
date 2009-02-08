# -*- coding: utf-8 -*-


#	 TITLE          : BEstory - An Interactive  Storyboard Builder
#
#	 DESCRIPTION    : To be able to rapidly create storyboards
#
#	 COPYRIGHT      : Copyright © 16-06-2006
#
#	 COMPANY        : Computer Science and Engineering Dept, University of Mauritius
#	
#	 AUTHOR         : Kervin and Rina
#
#	 VERSION        : 1.0
#
#	 LICENSE        : GPL



import sys
from qt import *
from interface_impl import Interface_Impl
import locale



def main(args):
    app=QApplication(args)
    
    #Loading the appropriate translation file if present
    translator=QTranslator(app)
    translator.load("story_"+locale.getdefaultlocale()[0][0:2]+".qm",".")
    app.installTranslator(translator)
        
    d = QApplication.desktop()#gets the desktop widget - useful for obtaining size of the screen
    x=d.width()#gets desktop width
    y=d.height()#gets desktop height
    
     
    win=Interface_Impl()
    win.resize(x,y)
    app.setMainWidget(win)
    win.show()
    app.connect(app, SIGNAL("lastWindowClosed()"),app,SLOT("quit()"))
    app.exec_loop()
    
	    
    
if __name__=="__main__":
    main(sys.argv)

#**********************************************************************************#
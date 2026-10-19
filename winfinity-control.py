#!/usr/bin/env python3
from gui.uil import *
from themeparser import *
from PyTQt.tqt import *
from gui.winfinityControlGui import controlWindow
from gui.image import genImg
from io import StringIO, BytesIO
import pprint

class uidControlWindow(controlWindow):
	def __init__(self):
		controlWindow.__init__(self)
		
		# add code to window init function here
		
		#setup env
		#self.system = getSystemInfo()
		self.themeParser = ThemeParser()
		
		self.setValues()
		
		# add placeholder text in style box
		self.cb_style.insertItem(" === COMING SOON === ")
		
		#actions
		self.connect(self.buttonInstall,TQ_SIGNAL("clicked()"), self.installTheme)
		self.connect(self.buttonApply,TQ_SIGNAL("clicked()"), self.apply)
		self.connect(self.cb_color,TQ_SIGNAL("activated(int)"), self.cbUpdateImg)
		
	def setValues(self):
		self.themes = self.themeParser.getThemeList()
		self.currentTheme = "windowsstandard"		
		self.populateColorCB(self.themes)		
		self.updateImg(self.themes[self.currentTheme]['colors'])
		self.cb_color.setCurrentItem(list(self.themes.keys()).index(self.currentTheme))
		
	def updateImg(self, c):
		im = genImg(c)
		##s = StringIO()
		#s = ""
		#im.save(s, format="BMP")
		###s.seek(0)
		#qim = TQImage()
		#qim.loadFromData(s.read())
		
		
		s = BytesIO()
		im.save(s, format="BMP")
		
		qim = TQImage()
		qim.loadFromData(s.getvalue())
		
		pix = TQPixmap()
		pix.convertFromImage(qim)
		self.img_preview.setPixmap(pix)
		
	def cbUpdateImg(self):
		item = str(self.cb_color.currentText())
		for k, v in self.themes.items():
			if v['displayName'] == item:
				colIndex = k
				break
		self.updateImg(self.themes[colIndex]['colors'])
		
	def populateColorCB(self, themes):
		self.cb_color.clear()
		for k, t in themes.items():
			#print(t['displayName'] + ', ' + k)
			self.cb_color.insertItem(t['displayName'])
	def installTheme(self):
		file = TQFileDialog.getOpenFileName()
		t = self.themeParser.parseMsTheme(str(file))
		self.themes[sanStr(t['displayName'])] = t
		self.themeParser.saveThemeList(self.themes)
		self.setValues()
	
	def getSelectedTheme(self):
		item = str(self.cb_color.currentText())
		for k, v in self.themes.items():
			if v['displayName'] == item:
				colIndex = k
				break
		return colIndex
	
	def enableThemeGui(self, theme):
		self.themeParser.enableTheme(theme)
		
		msg = "Your theme " + theme + " has been enabled. You must log out and log back in for some changes to take effect."
		TQMessageBox.information(self, "Winfinity Control Panel - Theme", msg)
	
	def accept(self):
		theme = self.getSelectedTheme()
		self.enableThemeGui(theme)
		#issue main accept call
		super(uidControlWindow, self).accept()
		
	def apply(self):
		theme = self.getSelectedTheme()
		self.enableThemeGui(theme)
		
if __name__ == "__main__":
	#start window
	a = TQApplication(sys.argv)
	TQObject.connect(a,TQ_SIGNAL("lastWindowClosed()"),a,TQ_SLOT("quit()"))
	w = uidControlWindow()
	a.setMainWidget(w)
	w.show()
	a.exec_loop()
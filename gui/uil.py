# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mydialog2.ui'
#
# Created: Wed Jan 20 19:31:47 2021
#      by: The PyTQt User Interface Compiler (pyuic) 3.18.1
#
# WARNING! All changes made in this file will be lost!


from PyTQt.tqt import *
#from PyTQt import TQDialog


class controlWindow(TQDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        TQDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("controlWindow")

        self.setSizeGripEnabled(0)


        self.buttonCancel = TQPushButton(self,"buttonCancel")
        self.buttonCancel.setGeometry(TQRect(210,440,73,24))
        self.buttonCancel.setAutoDefault(1)

        self.buttonApply = TQPushButton(self,"buttonApply")
        self.buttonApply.setGeometry(TQRect(290,440,73,24))

        self.buttonOk = TQPushButton(self,"buttonOk")
        self.buttonOk.setGeometry(TQRect(130,440,73,24))
        self.buttonOk.setAutoDefault(1)
        self.buttonOk.setDefault(1)

        self.tabWidget = TQTabWidget(self,"tabWidget")
        self.tabWidget.setGeometry(TQRect(17,11,345,422))

        self.Widget2 = TQWidget(self.tabWidget,"Widget2")

        self.textLabel2 = TQLabel(self.Widget2,"textLabel2")
        self.textLabel2.setGeometry(TQRect(10,270,191,21))

        self.cb_style = TQComboBox(self.Widget2,"cb_style")
        self.cb_style.setGeometry(TQRect(10,240,190,20))

        self.cb_color = TQComboBox(self.Widget2,"cb_color")
        self.cb_color.setGeometry(TQRect(10,290,191,21))

        self.img_preview = TQLabel(self.Widget2,"img_preview")
        self.img_preview.setGeometry(TQRect(10,10,320,200))
        self.img_preview.setScaledContents(1)

        self.textLabel1 = TQLabel(self.Widget2,"textLabel1")
        self.textLabel1.setGeometry(TQRect(10,220,190,20))

        self.buttonInstall = TQPushButton(self.Widget2,"buttonInstall")
        self.buttonInstall.setGeometry(TQRect(230,240,90,24))
        self.tabWidget.insertTab(self.Widget2,TQString.fromLatin1(""))

        self.languageChange()

        self.resize(TQSize(373,476).expandedTo(self.minimumSizeHint()))
        self.clearWState(TQt.WState_Polished)

        self.connect(self.buttonOk,SIGNAL("clicked()"),self.accept)
        self.connect(self.buttonCancel,SIGNAL("clicked()"),self.reject)


    def languageChange(self):
        self.setCaption(self.__tr("Winfinity Control Panel"))
        self.buttonCancel.setText(self.__tr("&Cancel"))
        self.buttonCancel.setAccel(TQKeySequence(TQString.null))
        self.buttonApply.setText(self.__tr("Apply"))
        self.buttonOk.setText(self.__tr("&OK"))
        self.buttonOk.setAccel(TQKeySequence(TQString.null))
        self.textLabel2.setText(self.__tr("Color scheme:"))
        self.textLabel1.setText(self.__tr("Windows and buttons:"))
        self.buttonInstall.setText(self.__tr("Install Theme"))
        self.tabWidget.changeTab(self.Widget2,self.__tr("Theme"))


    def __tr(self,s,c = None):
        return tqApp.translate("controlWindow",s,c)

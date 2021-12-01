# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'steganography.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QInputDialog, QLineEdit, QFileDialog, QHBoxLayout, QLabel, QTextEdit
from PyQt5.QtGui import QIcon, QPixmap  
import webbrowser
from PyQt5.QtCore import pyqtSlot
import sys
import os
import steanograph as st


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(786, 505)
        self.fileName1 = ''
        self.fileName2 = ''
        self.generatedImage = ''
        self.option = ''
        self.msg = ''
        self.horizontalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(430, 450, 292, 39))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.gen_image_btn = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.gen_image_btn.setObjectName("gen_image_btn")
        self.horizontalLayout.addWidget(self.gen_image_btn)
        self.insert_btn = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.insert_btn.setObjectName("insert_btn")
        self.horizontalLayout.addWidget(self.insert_btn)
        self.exit_btn = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.exit_btn.setObjectName("exit_btn")
        self.horizontalLayout.addWidget(self.exit_btn)
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(30, 410, 161, 41))
        self.label_3.setObjectName("label_3")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(30, 110, 321, 238))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.r1 = QtWidgets.QRadioButton(self.verticalLayoutWidget_2)
        self.r1.setObjectName("r1")
        self.verticalLayout.addWidget(self.r1)
        self.r2 = QtWidgets.QRadioButton(self.verticalLayoutWidget_2)
        self.r2.setObjectName("r2")
        self.verticalLayout.addWidget(self.r2)
        self.r3_2 = QtWidgets.QRadioButton(self.verticalLayoutWidget_2)
        self.r3_2.setObjectName("r3_2")
        self.verticalLayout.addWidget(self.r3_2)
        self.r4 = QtWidgets.QRadioButton(self.verticalLayoutWidget_2)
        self.r4.setObjectName("r4")
        self.verticalLayout.addWidget(self.r4)
        self.verticalLayout_3.addLayout(self.verticalLayout)
        self.message = QtWidgets.QTextEdit(self.verticalLayoutWidget_2)
        self.message.setObjectName("message")
        self.verticalLayout_3.addWidget(self.message)
        self.img_3 = QtWidgets.QLabel(Dialog)
        self.img_3.setGeometry(QtCore.QRect(20, 370, 158, 28))
        self.img_3.setText("")
        self.img_3.setObjectName("img_3")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(30, 380, 91, 41))
        self.label_2.setObjectName("label_2")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(30, 350, 91, 31))
        self.label.setObjectName("label")
        self.textBrowser = QtWidgets.QTextBrowser(Dialog)
        self.textBrowser.setGeometry(QtCore.QRect(220, 10, 327, 70))
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(400, 110, 321, 238))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.r1_2 = QtWidgets.QRadioButton(self.verticalLayoutWidget_3)
        self.r1_2.setObjectName("r1_2")
        self.verticalLayout_5.addWidget(self.r1_2)
        self.r2_2 = QtWidgets.QRadioButton(self.verticalLayoutWidget_3)
        self.r2_2.setObjectName("r2_2")
        self.verticalLayout_5.addWidget(self.r2_2)
        self.r3_3 = QtWidgets.QRadioButton(self.verticalLayoutWidget_3)
        self.r3_3.setObjectName("r3_3")
        self.verticalLayout_5.addWidget(self.r3_3)
        self.r4_2 = QtWidgets.QRadioButton(self.verticalLayoutWidget_3)
        self.r4_2.setObjectName("r4_2")
        self.verticalLayout_5.addWidget(self.r4_2)
        self.verticalLayout_4.addLayout(self.verticalLayout_5)
        self.message_2 = QtWidgets.QTextEdit(self.verticalLayoutWidget_3)
        self.message_2.setObjectName("message_2")
        self.verticalLayout_4.addWidget(self.message_2)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        self.initUI()

    def initUI(self):
        self.exit_btn.clicked.connect(self.on_click)
        self.gen_image_btn.clicked.connect(self.openGenImage)

        #Encode
        self.r1.clicked.connect(self.options_1)
        self.r2.clicked.connect(self.options_2)
        self.r3_2.clicked.connect(self.options_3)
        self.r4.clicked.connect(self.options_4)

        #Decode
        self.r1_2.clicked.connect(self.options_1_decode)
        self.r2_2.clicked.connect(self.options_2_decode)
        self.r3_3.clicked.connect(self.options_3_decode)
        self.r4_2.clicked.connect(self.options_4_decode)


        self.show()

    def options_1(self):
        self.option = '1'
        self.msg = self.message.toPlainText()
        self.insert_btn.clicked.connect(self.openFileNameDialog_1)

    def options_2(self):   
        self.option = '2'
        msg = self.message.toPlainText()
        self.insert_btn.clicked.connect(self.openFileNameDialog_1)

    def options_3(self):
        self.option = '3'
        self.insert_btn.clicked.connect(self.openFileNameDialog_1)
        self.insert_btn.clicked.connect(self.openFileNameDialog_2)
    
    def options_4(self):
        self.option = '4'
        self.msg = self.message.toPlainText()
        self.insert_btn.clicked.connect(self.openFileNameDialog_1)
    
    

    def options_1_decode(self):
        self.option = '1d'
        self.insert_btn.clicked.connect(self.openFileNameDialog_1)

    def options_2_decode(self):   
        self.option = '2d'
        self.insert_btn.clicked.connect(self.openFileNameDialog_1)

    def options_3_decode(self):
        self.option = '3d'
        self.insert_btn.clicked.connect(self.openFileNameDialog_1)

    def options_4_decode(self):
        self.option = '4d'
        self.insert_btn.clicked.connect(self.openFileNameDialog_1)


    @pyqtSlot()
    def openFileNameDialog_1(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.fileName1, _ = QFileDialog.getOpenFileName(self,"Select file to insert", "","All Files (*);;Python Files (*.py)", options=options)
        if self.fileName1:
            print(self.fileName1)
            self.label.setText("Image 1: "+self.fileName1)
            pixmap = QPixmap(self.fileName1)
            pixmap2 = pixmap.scaledToWidth(100)
            pixmap3 = pixmap.scaledToHeight(400)
            #testing 
            #sample_images(1000)
            #self.showImg(self.fileName1)


    @pyqtSlot()
    def openFileNameDialog_2(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.fileName2, _ = QFileDialog.getOpenFileName(self,"Select file to insert", "","All Files (*);;Python Files (*.py)", options=options)
        if self.fileName2:
            print(self.fileName2)
            self.label_2.setText("Image 2: "+self.fileName2)
            pixmap = QPixmap(self.fileName2)
            pixmap2 = pixmap.scaledToWidth(100)
            pixmap3 = pixmap.scaledToHeight(400)
            #testing 
            #sample_images(1000)
            #self.showImg(self.fileName2)

    @pyqtSlot()
    def openGenImage(self):
        if (self.option == '1'):
            n = st.LSB_encoding(self.fileName1, self.msg)
            self.label_3.setText(f"Generated: {n}")
            
        elif (self.option == '2'):
            n = st.metadata_encode(self.fileName1, self.msg)
            self.label_3.setText(f"Generated: {n}")

        elif (self.option == '3'):
            n = st.image_hide(self.fileName1, self.fileName2)
            self.label_3.setText(f"Generated: {n}")

        elif (self.option == '4'):
            n = st.DCT_encode(self.fileName1, self.msg)
            self.label_3.setText(f"Generated: {n}")

        elif (self.option == '1d'):
            m = st.LSB_Decode(self.fileName1)
            print ('Idhr')
            print (self.msg)
            self.label_3.setText(f"Generated: {m}")

        elif (self.option == '2d'):
            m = st.metadata_decode(self.fileName1)
            self.label_3.setText(f"Generated: {m}")

        elif (self.option == '3d'):
            m = st.image_hide_extract(self.fileName1)
            self.label_3.setText(f"Generated: {m}")
        
        elif (self.option == '4d'):
            m = st.DCT_decode(self.fileName1)
            self.label_3.setText(f"Generated: {m}")

        #self.generatedImage = fuse.fusion(self.fileName1, self.fileName2)    

    @pyqtSlot()
    def on_click(self):
        sys.exit()




    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.gen_image_btn.setText(_translate("Dialog", "Generate Image"))
        self.insert_btn.setText(_translate("Dialog", "Insert"))
        self.exit_btn.setText(_translate("Dialog", "Exit"))
        self.label_3.setText(_translate("Dialog", "Generated Image"))
        self.r1.setText(_translate("Dialog", "Least Significant bit insertion"))
        self.r2.setText(_translate("Dialog", "Hiding Metadata"))
        self.r3_2.setText(_translate("Dialog", "Hiding image in another image"))
        self.r4.setText(_translate("Dialog", "DCT"))
        self.message.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Garuda\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Message</p></body></html>"))
        self.label_2.setText(_translate("Dialog", "Image 2"))
        self.label.setText(_translate("Dialog", "Image 1"))
        self.textBrowser.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Garuda\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">Open Source </span><span style=\" font-size:12pt; font-weight:600;\">Steganography </span><span style=\" font-size:12pt;\">tool</span></p></body></html>"))
        self.r1_2.setText(_translate("Dialog", "Least Significant bit insertion"))
        self.r2_2.setText(_translate("Dialog", "Hiding Metadata Decode"))
        self.r3_3.setText(_translate("Dialog", "Image Hide Extract"))
        self.r4_2.setText(_translate("Dialog", "DCT Decode"))
        self.message_2.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Garuda\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Message</p></body></html>"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())


# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog, QDialog
from PyQt5.QtGui import QPixmap
from objectdetection import objectdetection 
from posedetection import *
import emotion_detection
import os.path
import os,sys
import cv2
#globalne varijable
working_image_path = ''
temp = None
temps = {'p':None,'d':None,'e':None,'pd':None,'pe':None,'de':None,'a':None}
temp_pose = ''
ui = None
class Ui_MainWindow(QDialog):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        # MainWindow.resize(800, 604)
        MainWindow.setFixedSize(800,604)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(0, 10, 791, 531))
        self.graphicsView.setObjectName("graphicsView")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(10, 550, 131, 27))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.object_detection_action)
        
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(150, 550, 121, 27))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.pose_detection_action)
        
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(280, 550, 141, 27))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.emotion_detection_action)
        
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(700, 550, 91, 27))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.clicked.connect(self.save_action)
        
        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(600, 550, 91, 27))
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_5.clicked.connect(self.open_action)
        
        self.pushButton_6 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_6.setGeometry(QtCore.QRect(500, 550, 91, 27))
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_6.clicked.connect(self.reset_action)
        
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Detection"))
        self.pushButton.setText(_translate("MainWindow", "Object detection"))
        self.pushButton_2.setText(_translate("MainWindow", "Pose detection"))
        self.pushButton_3.setText(_translate("MainWindow", "Emotion detection"))
        self.pushButton_4.setText(_translate("MainWindow", "Save"))
        self.pushButton_5.setText(_translate("MainWindow", "Open"))
        self.pushButton_6.setText(_translate("MainWindow", "Reset"))
        
    def showImage(self,image_path):
        scene = QtWidgets.QGraphicsScene(self)
        pixmap = QPixmap(image_path)
        pixmap_scaled_to_height = pixmap.scaled(791, 531, QtCore.Qt.KeepAspectRatio)
        item = QtWidgets.QGraphicsPixmapItem(pixmap_scaled_to_height)
        
        scene.addItem(item)
        # self.graphicsView.fitInView()
        self.graphicsView.setScene(scene)

    def object_detection_action(self):
        print('object_detection_action')

    def pose_detection_action(self):
        print('pose_detection_action')
        
    def emotion_detection_action(self):
        print('emotion_detection_action')
            
    def save_action(self):
        print('save_action')
    
    def open_action(self):
        global working_image_path,temp
        print('open_action')
        fd = File_Dialog()
        working_image_path = fd.openFileNameDialog()
        input_path_head,input_path_tail = os.path.split(working_image_path)
        temp = cv2.imread(working_image_path)
        w,h,c = temp.shape
        status = (input_path_tail+" :: "+str(w) + "x" + str(h))
        self.showImage(working_image_path)
        self.statusbar.showMessage(status)
        
    def reset_action(self):
        global working_image_path,temp
        print('reset_action')
        temp = cv2.imread(working_image_path)
        self.showImage(working_image_path)
        self.statusbar.showMessage('No image selected.')
class File_Dialog(QWidget):

    def __init__(self):
        super().__init__()
    
    
    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"Detection: Open image", "","All Files (*);;Python Files (*.py)", options=options)
        print(fileName)
        if fileName:
            return(fileName)
        else: #no picture selected
            exit(0)
    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self,"QFileDialog.getOpenFileNames()", "","All Files (*);;Python Files (*.py)", options=options)
        if files:
            return(files)
    
    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","All Files (*);;Text Files (*.txt)", options=options)
        if fileName:
            return(fileName)
def main():
    global working_image_path,temp,temp_pose,temps,ui
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    fd = File_Dialog()
    working_image_path = fd.openFileNameDialog() #image path used for detection/s
    temp_pose = pose_detection.poseDetection(working_image_path)
    print(temp_pose)
    # if '/' in working_image_path:
    #     split_ch = '/'
    # else:
    #     split_ch = '\\'
    input_path_head,input_path_tail = os.path.split(working_image_path)

    temp = cv2.imread(working_image_path)
    w,h,c = temp.shape
    status = (input_path_tail+" :: "+str(w) + "x" + str(h))

    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    ui.statusbar.showMessage(status)
    ui.showImage(working_image_path)



    MainWindow.show()
    sys.exit(app.exec_())
        
if __name__ == "__main__":
    main()
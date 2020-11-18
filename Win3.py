# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Win3.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import (QApplication, QWidget, QFileDialog, QTextEdit, QPushButton, QLabel, QVBoxLayout)
from PyQt5.QtGui import QImage,QPixmap
from PyQt5.QtCore import QDir
import cv2
import numpy as np
#import matplotlib.pyplot as plt
import glob
import tensorflow as tf

class Ui_MainWindow2(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(890, 442)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.B1 = QtWidgets.QPushButton(self.centralwidget)
        self.B1.setGeometry(QtCore.QRect(20, 97, 201, 41))
        self.B1.setObjectName("B1")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(50, 40, 141, 41))
        self.pushButton.setObjectName("pushButton")
        self.image_frame = QtWidgets.QLabel(self.centralwidget)
        self.image_frame.setGeometry(QtCore.QRect(270, 20, 581, 371))
        self.image_frame.setText("")
        self.image_frame.setScaledContents(True)
        self.image_frame.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 890, 26))
        self.menubar.setObjectName("menubar")
        self.menuPlik = QtWidgets.QMenu(self.menubar)
        self.menuPlik.setObjectName("menuPlik")
        self.menuabout = QtWidgets.QMenu(self.menubar)
        self.menuabout.setObjectName("menuabout")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.menuPlik.addAction(self.actionOpen)
        self.menuPlik.addAction(self.actionSave)
        self.menuPlik.addAction(self.actionExit)
        self.menubar.addAction(self.menuPlik.menuAction())
        self.menubar.addAction(self.menuabout.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.B1.setText(_translate("MainWindow", "Diagnoza"))
        self.pushButton.setText(_translate("MainWindow", "Wczytaj zdjęcie"))
        self.menuPlik.setTitle(_translate("MainWindow", "File"))
        self.menuabout.setTitle(_translate("MainWindow", "About"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))

        self.pushButton.clicked.connect(self.openFile)
        self.B1.clicked.connect(self.diagnoza)

    def openFile(self):
        filename, _ = QFileDialog.getOpenFileName(None, 'Buscar Imagen', 'C:\\Users\\Asia\\Desktop\\rozpoznawanie obrazów\\naczynia krwonośne\\images', 'Image Files (*.png *.jpg *.jpeg *.bmp)')
        if filename:
            with open(filename, "rb") as file:
                data = np.array(bytearray(file.read()))

                self.image = cv2.imdecode(data, cv2.IMREAD_UNCHANGED)
                # self.image = cv2.imread(filename, cv2.IMREAD_UNCHANGED)
                self.mostrarImagen()

    def prepare(self):
        IMG_SIZE = 50
        img_array = cv2.cvtColor(self.image, cv2.COLOR_RGB2GRAY)
        new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
        return new_array.reshape(-1, IMG_SIZE, IMG_SIZE, 1)

    def diagnoza(self):
        if self.image is not None:
            CATEGORIES = ["Jaskra", "Zdrowe", "Cukrzyca"]

            model = tf.keras.models.load_model("C:\\Users\\Asia\\Desktop\\Image Classification\\CNN.model")
            #image = "C:\\Users\\Asia\\Desktop\\Image Classification\\jaskra.jpg"  # your image path
            #image= self.image
            prediction = model.predict([self.prepare()])
            prediction = list(prediction[0])
            print(CATEGORIES[prediction.index(max(prediction))])
    def mostrarImagen(self):
        size = self.image.shape
        step = self.image.size / size[0]
        qformat = QImage.Format_Indexed8

        if len(size) == 3:
            if size[2] == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888

        img = QImage(self.image, size[1], size[0], step, qformat)
        img = img.rgbSwapped()

        self.image_frame.setPixmap(QPixmap.fromImage(img))
        #self.resize(self.image_frame.pixmap().size())
if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow2()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
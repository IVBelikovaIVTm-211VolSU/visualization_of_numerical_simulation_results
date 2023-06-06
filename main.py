import sys
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import (QMainWindow,QWidget, QToolTip, 
    QPushButton, QApplication,QLineEdit,QGroupBox,QLabel,QComboBox,QCheckBox,QGraphicsView,QErrorMessage)
from PyQt5.QtGui import QFont,QPixmap
import numpy as np 
import math 
import matplotlib 
import matplotlib.pyplot as plt
from matplotlib import ticker
import os
import io
home = os.getenv("HOME")

plt.rcParams['font.size'] = 14
plt.rcParams['font.family'] = 'Times New Roman'

font = {'family': 'serif',
        'color':  'black',
        'weight': 'normal',
        'size': 28,
        }

font_legend = matplotlib.font_manager.FontProperties(family='serif', weight='normal', size=25)


class Ui_MainWindow(object):
    global batchMode

    def colormap(self):
        self.label_10.setText(self.comboBox1.currentText())
        self.label_10.setPixmap(QtGui.QPixmap("colormap/rgb.PNG"))
        self.label_10.setScaledContents(True)
        self.comboBox1.activated.connect(self.onActivated)
    #----------функция выбора директории------------
    def browse_folder(self):
        global directory
        directory = QtWidgets.QFileDialog.getExistingDirectory(None, "Выберите папку")
        # открыть диалог выбора директории и установить значение переменной
        # равной пути к выбранной директории
        if directory:  # не продолжать выполнение, если пользователь не выбрал директорию
            self.lineEditDir.setText(directory)
            self.lineEdit1.setEnabled(True)
            
    def onActivated(self, text):
        #self.label_10.setText(self.comboBox1.currentText())
        index = self.comboBox1.currentIndex()
        if index==0:
            self.cmp=plt.cm.brg
            self.label_10.setPixmap(QPixmap("colormap/rgb.PNG"))
        if index==1:
            self.cmp=plt.cm.CMRmap
            self.label_10.setPixmap(QPixmap("colormap/cmrmap.PNG"))
        if index==2:
            self.cmp=plt.cm.cubehelix
            self.label_10.setPixmap(QPixmap("colormap/cubehelix.PNG"))
        if index==3:
            self.cmp=plt.cm.gist_earth
            self.label_10.setPixmap(QPixmap("colormap/gist_earth.PNG"))
        if index==4:
            self.cmp=plt.cm.gist_earth
            self.label_10.setPixmap(QPixmap("colormap/cmrmap.PNG"))
        if index==5:
            self.cmp=plt.cm.gnuplot
            self.label_10.setPixmap(QPixmap("colormap/gnuplot.PNG"))
        if index==6:
            self.cmp=plt.cm.hsv
            self.label_10.setPixmap(QPixmap("colormap/hsv.PNG"))
        if index==7:
            self.cmp=plt.cm.jet
            self.label_10.setPixmap(QPixmap("colormap/jet.PNG"))
        if index==8:
            self.cmp=plt.cm.ocean
            self.label_10.setPixmap(QPixmap("colormap/ocean.PNG"))
        if index==9:
            self.cmp=plt.cm.terrain
            self.label_10.setPixmap(QPixmap("colormap/terrain.PNG"))
    
    #-----------выбор гафика, при выборе сразу выводит----------------------
    def graph(self, MainWindow):
        indexMenu = int(self.lineEdit12.text())
        batchMode = int(self.lineEdit13.text())
        if self.lineEditDir.text()=="Выберите папку":
            errorMessage = QtWidgets.QErrorMessage(self.centralwidget)
            errorMessage.showMessage('Выберите папку с файлами!')
        else:
            #формат выходного изображения
            dpi = int(self.lineEdit.text())
            format_image = self.comboBox.currentText()
            #распределения
            colormap = self.cmp 
            #График построения
            curGraph = self.lineEdit1.text()
            #Минимальное значение шкалы
            vmin = float(self.lineEdit2.text())
            #Максимальное значение шкалы
            vmax = float(self.lineEdit3.text())
            #Максимальный радиус диска
            maxRdRaspr = float(self.lineEdit4.text())
            #временные графики radius, radius2
            radius = self.lineEdit9.text()
            timeStart = float(self.lineEdit10.text())
            timeEnd = self.lineEdit11.text()
            logTimeStart = float(self.lineEdit14.text())
            logTimeEnd = float(self.lineEdit15.text())
            m_1, m_2,m_3,m_4,m_5,m_6=0,0,0,0,0,0
            if self.checkBox_7.isChecked():
                m_1 = 1
            if self.checkBox_8.isChecked():
                m_2 = 1
            if self.checkBox_9.isChecked():
                m_3 = 1
            if self.checkBox_10.isChecked():
                m_4 = 1
            if self.checkBox_11.isChecked():
                m_5 = 1
            if self.checkBox_12.isChecked():
                m_6 = 1
            #графики логарифма плотности от угла
            radius2 = self.lineEdit9.text()
            #начальные параметры
            xlim1 = float(self.lineEdit5.text())
            xlim2 = float(self.lineEdit6.text())
            ylim1 = float(self.lineEdit7.text())
            ylim2 = float(self.lineEdit8.text())
            Vphi,vphi_2,sigma,omega,kappa,qt=0,0,0,0,0,0
            if self.checkBox_1.isChecked():
                Vphi = 1
            if self.checkBox_2.isChecked():
                vphi_2 = 1
            if self.checkBox_3.isChecked():
                sigma = 1
            if self.checkBox_4.isChecked():
                omega = 1
            if self.checkBox_5.isChecked():
                kappa = 1
            if self.checkBox_6.isChecked():
                qt = 1
            #проверка максимального t
            if not self.lineEdit11.text() or self.lineEdit11.text() =="":
                files = os.listdir(directory)
                dat = filter(lambda x: x.endswith('.dat'), files)
                l = list(dat)
                dat = filter(lambda x: x.endswith('.dat'), files)
                length = len(l)
                Input = open(directory + '//' + l[length-1],'rb')
                gam = np.fromfile(Input,np.float64,1)
                timeEnd = np.fromfile(Input,np.float64,1)
                Input.close()
                if indexMenu == 7 or indexMenu == 12:
                    errorMessage = QtWidgets.QErrorMessage(self.centralwidget)
                    errorMessage.showMessage('Не указано максимальное время! Расчет будет произведен до %.2f'%timeEnd)
                    errorMessage.exec_()
                self.MainGrapher(directory,indexMenu,dpi,format_image,colormap,float(vmin),float(vmax),float(maxRdRaspr),radius,radius2,
                        [xlim1,xlim2],[ylim1,ylim2],[Vphi,vphi_2,sigma,omega,kappa,qt],[m_1,m_2,m_3,m_4,m_5,m_6],timeEnd, curGraph, batchMode, timeStart, logTimeStart, logTimeEnd)
            else:
                timeEnd = float(self.lineEdit11.text())
                files = os.listdir(directory)
                dat = filter(lambda x: x.endswith('.dat'), files)
                l = list(dat)
                dat = filter(lambda x: x.endswith('.dat'), files)
                length = len(l)
                Input = open(directory + '//' + l[length-1],'rb')
                gam = np.fromfile(Input,np.float64,1)
                t = np.fromfile(Input,np.float64,1)
                Input.close()
                if float(timeEnd)>t:
                    errorMessage = QtWidgets.QErrorMessage(self.centralwidget)
                    errorMessage.showMessage('Указанное значение времени превышает время выбранного расчета! Расчет будет произведен до %.2f'%t)
                    errorMessage.exec_()
                    self.MainGrapher(directory,indexMenu,dpi,format_image,colormap,float(vmin),float(vmax),float(maxRdRaspr),radius,radius2,
                        [xlim1,xlim2],[ylim1,ylim2],[Vphi,vphi_2,sigma,omega,kappa,qt],[m_1,m_2,m_3,m_4,m_5,m_6],t, curGraph, batchMode, timeStart, logTimeStart, logTimeEnd)
                else:
                    self.MainGrapher(directory,indexMenu,dpi,format_image,colormap,float(vmin),float(vmax),float(maxRdRaspr),radius,radius2,
                        [xlim1,xlim2],[ylim1,ylim2],[Vphi,vphi_2,sigma,omega,kappa,qt],[m_1,m_2,m_3,m_4,m_5,m_6],timeEnd, curGraph, batchMode, timeStart, logTimeStart, logTimeEnd)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1180, 750)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        indexMenu = -1
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 241, 41))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 60, 241, 41))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(10, 110, 321, 41))
        self.label_3.setObjectName("label_3")
              
        #Файл предварительной визуализации
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(10, 160, 321, 81))
        self.label_6.setObjectName("label_6")

        #Минимальное значение шкалы
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(10, 250, 321, 81))
        self.label_5.setObjectName("label_5")
        self.label_5.hide()
        
        #Максимальное значение шкалы
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(10, 330, 321, 81))
        self.label_7.setObjectName("label_7")
        self.label_7.hide()
        
        #Максимальный радиус диска
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(10, 410, 321, 81))
        self.label_8.setObjectName("label_8")
        self.label_8.hide()
        
        #Цветовая шкала
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(10, 470, 321, 81))
        self.label_9.setObjectName("label_9")
        self.label_9.hide()
        
        self.cmp=None
        
        #Цветовая шкала цвета
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setGeometry(QtCore.QRect(320, 550, 92, 25))
        self.label_10.setObjectName("label_10")
        self.label_10.hide()
        
        #Выбрать параметры построения
        self.label_11 = QtWidgets.QLabel(self.centralwidget)
        self.label_11.setGeometry(QtCore.QRect(10, 230, 321, 81))
        self.label_11.setObjectName("label_11")
        self.label_11.hide()
        
        #1
        self.checkBox_1 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_1.setGeometry(QtCore.QRect(30, 305, 101, 23))
        self.checkBox_1.setObjectName("checkBox_1")
        self.checkBox_1.hide()
        self.label_12 = QtWidgets.QLabel(self.centralwidget)
        self.label_12.setGeometry(QtCore.QRect(50, 280, 321, 81))
        self.label_12.setObjectName("label_12")
        self.label_12.hide()
        
        #2
        self.checkBox_2 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_2.setGeometry(QtCore.QRect(30, 345, 101, 23))
        self.checkBox_2.setObjectName("checkBox_2")
        self.checkBox_2.hide()
        self.label_13 = QtWidgets.QLabel(self.centralwidget)
        self.label_13.setGeometry(QtCore.QRect(50, 320, 321, 81))
        self.label_13.setObjectName("label_13")
        self.label_13.hide()
        
        #3
        self.checkBox_3 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_3.setGeometry(QtCore.QRect(30, 385, 101, 23))
        self.checkBox_3.setObjectName("checkBox_3")
        self.checkBox_3.hide()
        self.label_14 = QtWidgets.QLabel(self.centralwidget)
        self.label_14.setGeometry(QtCore.QRect(50, 360, 321, 81))
        self.label_14.setObjectName("label_14")
        self.label_14.hide()
        
        #4
        self.checkBox_4 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_4.setGeometry(QtCore.QRect(180, 305, 101, 23))
        self.checkBox_4.setObjectName("checkBox_4")
        self.checkBox_4.hide()
        self.label_15 = QtWidgets.QLabel(self.centralwidget)
        self.label_15.setGeometry(QtCore.QRect(205, 275, 321, 81))
        self.label_15.setObjectName("label_15")
        self.label_15.hide()
        
        #5
        self.checkBox_5 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_5.setGeometry(QtCore.QRect(180, 345, 101, 23))
        self.checkBox_5.setObjectName("checkBox_5")
        self.checkBox_5.hide()
        self.label_16 = QtWidgets.QLabel(self.centralwidget)
        self.label_16.setGeometry(QtCore.QRect(205, 320, 321, 81))
        self.label_16.setObjectName("label_16")
        self.label_16.hide()
        
        #6
        self.checkBox_6 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_6.setGeometry(QtCore.QRect(180, 385, 101, 23))
        self.checkBox_6.setObjectName("checkBox_6")
        self.checkBox_6.hide()
        self.label_17 = QtWidgets.QLabel(self.centralwidget)
        self.label_17.setGeometry(QtCore.QRect(205, 355, 321, 81))
        self.label_17.setObjectName("label_17")
        self.label_17.hide()
        
        #Интервал по Х
        self.label_18 = QtWidgets.QLabel(self.centralwidget)
        self.label_18.setGeometry(QtCore.QRect(10, 400, 321, 81))
        self.label_18.setObjectName("label_18")
        self.label_18.hide()
        
        #От
        self.label_19 = QtWidgets.QLabel(self.centralwidget)
        self.label_19.setGeometry(QtCore.QRect(10, 430, 321, 81))
        self.label_19.setObjectName("label_19")
        self.label_19.hide()
        
        #До
        self.label_20 = QtWidgets.QLabel(self.centralwidget)
        self.label_20.setGeometry(QtCore.QRect(160, 430, 321, 81))
        self.label_20.setObjectName("label_20")
        self.label_20.hide()
        
        #Интервал по Y
        self.label_21 = QtWidgets.QLabel(self.centralwidget)
        self.label_21.setGeometry(QtCore.QRect(10, 470, 321, 81))
        self.label_21.setObjectName("label_21")
        self.label_21.hide()
        
        #От
        self.label_22 = QtWidgets.QLabel(self.centralwidget)
        self.label_22.setGeometry(QtCore.QRect(10, 500, 321, 81))
        self.label_22.setObjectName("label_22")
        self.label_22.hide()
        
        #До
        self.label_23 = QtWidgets.QLabel(self.centralwidget)
        self.label_23.setGeometry(QtCore.QRect(160, 500, 321, 81))
        self.label_23.setObjectName("label_23")
        self.label_23.hide()
        
        #Радиусы (кпк)
        self.label_24 = QtWidgets.QLabel(self.centralwidget)
        self.label_24.setGeometry(QtCore.QRect(10, 240, 321, 81))
        self.label_24.setObjectName("label_24")
        self.label_24.hide()
        
        #Начальное время
        self.label_25 = QtWidgets.QLabel(self.centralwidget)
        self.label_25.setGeometry(QtCore.QRect(10, 280, 321, 81))
        self.label_25.setObjectName("label_25")
        self.label_25.hide()
        
        #Максимальное время
        self.label_26 = QtWidgets.QLabel(self.centralwidget)
        self.label_26.setGeometry(QtCore.QRect(10, 320, 321, 81))
        self.label_26.setObjectName("label_26")
        self.label_26.hide()
        
        #Мод 
        self.label_27 = QtWidgets.QLabel(self.centralwidget)
        self.label_27.setGeometry(QtCore.QRect(10, 360, 321, 81))
        self.label_27.setObjectName("label_27")
        self.label_27.hide()
        
        #Показывает сколько файлов осталось посчитать 
        self.label_28 = QtWidgets.QLabel(self.centralwidget)
        self.label_28.setGeometry(QtCore.QRect(10, 540, 321, 81))
        self.label_28.setObjectName("label_28")
        self.label_28.hide()
        
        #Нижнее значение логарифма
        self.label_29 = QtWidgets.QLabel(self.centralwidget)
        self.label_29.setGeometry(QtCore.QRect(10, 380, 321, 81))
        self.label_29.setObjectName("label_29")
        self.label_29.hide()
        
        #Верхнее значение логарифма
        self.label_30 = QtWidgets.QLabel(self.centralwidget)
        self.label_30.setGeometry(QtCore.QRect(10, 450, 321, 81))
        self.label_30.setObjectName("label_30")
        self.label_30.hide()
        
        #1
        self.checkBox_7 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_7.setGeometry(QtCore.QRect(30, 420, 101, 23))
        self.checkBox_7.setObjectName("checkBox_7")
        self.checkBox_7.hide()
        
        #2
        self.checkBox_8 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_8.setGeometry(QtCore.QRect(30, 460, 101, 23))
        self.checkBox_8.setObjectName("checkBox_8")
        self.checkBox_8.hide()
        
        #3
        self.checkBox_9 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_9.setGeometry(QtCore.QRect(30, 500, 101, 23))
        self.checkBox_9.setObjectName("checkBox_9")
        self.checkBox_9.hide()
        
        #4
        self.checkBox_10 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_10.setGeometry(QtCore.QRect(130, 420, 101, 23))
        self.checkBox_10.setObjectName("checkBox_10")
        self.checkBox_10.hide()
        
        #5
        self.checkBox_11 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_11.setGeometry(QtCore.QRect(130, 460, 101, 23))
        self.checkBox_11.setObjectName("checkBox_11")
        self.checkBox_11.hide()
        
        #6
        self.checkBox_12 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_12.setGeometry(QtCore.QRect(130, 500, 101, 23))
        self.checkBox_12.setObjectName("checkBox_12")
        self.checkBox_12.hide()
        
        
        #Формат изображения
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(320, 120, 92, 25))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        
        #Цветовая шкала
        self.comboBox1 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox1.setGeometry(QtCore.QRect(320, 500, 92, 25))
        self.comboBox1.setObjectName("comboBox1")
        self.comboBox1.hide()
        self.comboBox1.addItem("")
        self.comboBox1.addItem("")
        self.comboBox1.addItem("")
        self.comboBox1.addItem("")
        self.comboBox1.addItem("")
        self.comboBox1.addItem("")
        self.comboBox1.addItem("")
        self.comboBox1.addItem("")
        self.comboBox1.addItem("")
        self.comboBox1.addItem("")
        
        #DPI
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(320, 70, 92, 25))
        self.lineEdit.setObjectName("lineEdit")
        #self.lineEdit.setEnabled(False)
        
        #Tvd
        self.lineEdit1 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit1.setGeometry(QtCore.QRect(310, 180, 102, 25))
        self.lineEdit1.setObjectName("lineEdit1")
        self.lineEdit1.setEnabled(False)
        
        #Минимальное значение шкалы - 1
        self.lineEdit2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit2.setGeometry(QtCore.QRect(320, 270, 92, 25))
        self.lineEdit2.setObjectName("lineEdit2")
        self.lineEdit2.hide()
        
        #Максимальное значение шкалы
        self.lineEdit3 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit3.setGeometry(QtCore.QRect(320, 350, 92, 25))
        self.lineEdit3.setObjectName("lineEdit3")
        self.lineEdit3.hide()
        
        #Максимальный радиус диска
        self.lineEdit4 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit4.setGeometry(QtCore.QRect(320, 430, 92, 25))
        self.lineEdit4.setObjectName("lineEdit4")
        self.lineEdit4.hide()
        
        #Интервал по Х от
        self.lineEdit5 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit5.setGeometry(QtCore.QRect(50, 460, 92, 25))
        self.lineEdit5.setObjectName("lineEdit5")
        self.lineEdit5.hide()
        
        #Интервал по Х до
        self.lineEdit6 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit6.setGeometry(QtCore.QRect(200, 460, 92, 25))
        self.lineEdit6.setObjectName("lineEdit6")
        self.lineEdit6.hide()
        
        #Интервал по Y от
        self.lineEdit7 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit7.setGeometry(QtCore.QRect(50, 530, 92, 25))
        self.lineEdit7.setObjectName("lineEdit7")
        self.lineEdit7.hide()
        
        #Интервал по Y до
        self.lineEdit8 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit8.setGeometry(QtCore.QRect(200, 530, 92, 25))
        self.lineEdit8.setObjectName("lineEdit8")
        self.lineEdit8.hide()
        
        #Радиусы (кпк) 6,12
        self.lineEdit9 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit9.setGeometry(QtCore.QRect(240, 270, 172, 25))
        self.lineEdit9.setObjectName("lineEdit9")
        self.lineEdit9.hide()
        
        #Начальное время
        self.lineEdit10 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit10.setGeometry(QtCore.QRect(240, 310, 172, 25))
        self.lineEdit10.setObjectName("lineEdit10")
        self.lineEdit10.hide()
        
        #Максимальное время
        self.lineEdit11 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit11.setGeometry(QtCore.QRect(240, 350, 172, 25))
        self.lineEdit11.setObjectName("lineEdit11")
        self.lineEdit11.hide()
        
        #Directory
        self.lineEditDir = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEditDir.setGeometry(QtCore.QRect(240, 350, 172, 25))
        self.lineEditDir.setObjectName("lineEditDir")
        self.lineEditDir.hide()
        
        #Определяет какой параметр строится
        self.lineEdit12 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit12.setGeometry(QtCore.QRect(240, 350, 172, 25))
        self.lineEdit12.setObjectName("lineEdit12")
        self.lineEdit12.hide()
        
        #Batch mode
        self.lineEdit13 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit13.setGeometry(QtCore.QRect(240, 350, 172, 25))
        self.lineEdit13.setObjectName("lineEdit13")
        self.lineEdit13.hide()
        
        #Нижнее значение логарифма
        self.lineEdit14 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit14.setGeometry(QtCore.QRect(240, 380, 172, 25))
        self.lineEdit14.setObjectName("lineEdit14")
        self.lineEdit14.hide()
        
        #Верхнее значение логарифма
        self.lineEdit15 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit15.setGeometry(QtCore.QRect(240, 450, 172, 25))
        self.lineEdit15.setObjectName("lineEdit15")
        self.lineEdit15.hide()
        
        #---------------кнопка построения-------------------
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(770, 620, 112, 34))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.graph)
        
        #Вывод изображения
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(440, 10, 750, 600))
        self.label_4.setText("")
        self.label_4.setObjectName("label_4")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1058, 31))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu_3 = QtWidgets.QMenu(self.menu)
        self.menu_3.setObjectName("menu_3")
        self.menu_4 = QtWidgets.QMenu(self.menu)
        self.menu_4.setObjectName("menu_4")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.directoryMenu = QtWidgets.QAction(MainWindow)
        
        #-------------выбор дикертории------------
        self.directoryMenu.setObjectName("directoryMenu")
        self.directoryMenu.triggered.connect(self.browse_folder)
        
        
        #Выгрузить данные          
        self.action_2 = QtWidgets.QAction(MainWindow)
        self.action_2.setObjectName("action_2")
        self.action_2.triggered.connect(lambda:  self.lineEdit13.setText("1"))
        self.action_2.triggered.connect(lambda:  self.graph(MainWindow))
        
        self.action_3 = QtWidgets.QAction(MainWindow)
        self.action_3.setObjectName("action_3")
        self.action_4 = QtWidgets.QAction(MainWindow)
        self.action_4.setObjectName("action_4")
        self.action_r = QtWidgets.QAction(MainWindow)
        self.action_r.setObjectName("action_r")
        self.action_7 = QtWidgets.QAction(MainWindow)
        self.action_7.setObjectName("action_7")
        self.action_8 = QtWidgets.QAction(MainWindow)
        self.action_8.setObjectName("action_8")
        self.action_9 = QtWidgets.QAction(MainWindow)
        self.action_9.setObjectName("action_9")
        self.action_10 = QtWidgets.QAction(MainWindow)
        self.action_10.setObjectName("action_10")
        self.action_11 = QtWidgets.QAction(MainWindow)
        self.action_11.setObjectName("action_11")
        self.action_12 = QtWidgets.QAction(MainWindow)
        self.action_12.setObjectName("action_12")
        self.action_13 = QtWidgets.QAction(MainWindow)
        self.action_13.setObjectName("action_13")
        self.action_14 = QtWidgets.QAction(MainWindow)
        self.action_14.setObjectName("action_14")
        self.action_15 = QtWidgets.QAction(MainWindow)
        self.action_15.setObjectName("action_15")
        self.action_16 = QtWidgets.QAction(MainWindow)
        self.action_16.setObjectName("action_16")
        self.action_17 = QtWidgets.QAction(MainWindow)
        self.action_17.setObjectName("action_17")
        self.menuFile.addAction(self.directoryMenu)
        self.menuFile.addAction(self.action_2)
        self.menuFile.addAction(self.action_3)
        self.menuFile.addAction(self.action_4)
        
        #Распределение параметров системы вдоль r
        self.menu_3.addAction(self.action_r)
        #Show
        self.action_r.triggered.connect(lambda:  self.label_11.show())
        self.action_r.triggered.connect(lambda:  self.checkBox_1.show())
        self.action_r.triggered.connect(lambda:  self.label_12.show())
        self.action_r.triggered.connect(lambda:  self.checkBox_2.show())
        self.action_r.triggered.connect(lambda:  self.label_13.show())
        self.action_r.triggered.connect(lambda:  self.checkBox_3.show())
        self.action_r.triggered.connect(lambda:  self.label_14.show())
        self.action_r.triggered.connect(lambda:  self.checkBox_4.show())
        self.action_r.triggered.connect(lambda:  self.label_15.show())
        self.action_r.triggered.connect(lambda:  self.checkBox_5.show())
        self.action_r.triggered.connect(lambda:  self.label_16.show())
        self.action_r.triggered.connect(lambda:  self.checkBox_6.show())
        self.action_r.triggered.connect(lambda:  self.label_17.show())
        self.action_r.triggered.connect(lambda:  self.label_18.show())
        self.action_r.triggered.connect(lambda:  self.label_19.show())
        self.action_r.triggered.connect(lambda:  self.lineEdit5.show())
        self.action_r.triggered.connect(lambda:  self.label_20.show())
        self.action_r.triggered.connect(lambda:  self.lineEdit6.show())
        self.action_r.triggered.connect(lambda:  self.label_21.show())
        self.action_r.triggered.connect(lambda:  self.label_22.show())
        self.action_r.triggered.connect(lambda:  self.lineEdit7.show())
        self.action_r.triggered.connect(lambda:  self.label_23.show())
        self.action_r.triggered.connect(lambda:  self.lineEdit8.show())
        self.action_r.triggered.connect(lambda:  self.lineEdit12.setText("1"))
        self.action_r.triggered.connect(lambda:  self.lineEdit13.setText("0"))
        
        #Hide
        self.action_r.triggered.connect(lambda:  self.label_5.hide())
        self.action_r.triggered.connect(lambda:  self.label_7.hide())
        self.action_r.triggered.connect(lambda:  self.label_8.hide())
        self.action_r.triggered.connect(lambda:  self.label_9.hide())
        self.action_r.triggered.connect(lambda:  self.label_10.hide())
        self.action_r.triggered.connect(lambda:  self.lineEdit2.hide())
        self.action_r.triggered.connect(lambda:  self.lineEdit3.hide())
        self.action_r.triggered.connect(lambda:  self.lineEdit4.hide())
        self.action_r.triggered.connect(lambda:  self.comboBox1.hide())
        #self.action_r.triggered.connect(lambda:  self.colormap())
        self.action_r.triggered.connect(lambda:  self.label_24.hide())
        self.action_r.triggered.connect(lambda:  self.lineEdit9.hide())
        self.action_r.triggered.connect(lambda:  self.label_25.hide())
        self.action_r.triggered.connect(lambda:  self.lineEdit10.hide())
        self.action_r.triggered.connect(lambda:  self.label_26.hide())
        self.action_r.triggered.connect(lambda:  self.lineEdit11.hide())
       
        self.action_r.triggered.connect(lambda:  self.label_27.hide())
        self.action_r.triggered.connect(lambda:  self.label_29.hide())
        self.action_r.triggered.connect(lambda:  self.label_30.hide())
        self.action_r.triggered.connect(lambda:  self.checkBox_7.hide())
        self.action_r.triggered.connect(lambda:  self.checkBox_8.hide())
        self.action_r.triggered.connect(lambda:  self.checkBox_9.hide())
        self.action_r.triggered.connect(lambda:  self.checkBox_10.hide())
        self.action_r.triggered.connect(lambda:  self.checkBox_11.hide())
        self.action_r.triggered.connect(lambda:  self.checkBox_12.hide())
        self.action_r.triggered.connect(lambda:  self.lineEdit14.hide())
        self.action_r.triggered.connect(lambda:  self.lineEdit15.hide())
       
        #Распределение плотности
        self.menu_3.addAction(self.action_7)
        #Show
        self.action_7.triggered.connect(lambda:  self.label_5.show())
        self.action_7.triggered.connect(lambda:  self.label_7.show())
        self.action_7.triggered.connect(lambda:  self.label_8.show())
        self.action_7.triggered.connect(lambda:  self.label_9.show())
        self.action_7.triggered.connect(lambda:  self.label_10.show())
        self.action_7.triggered.connect(lambda:  self.lineEdit2.show())
        self.action_7.triggered.connect(lambda:  self.lineEdit3.show())
        self.action_7.triggered.connect(lambda:  self.lineEdit4.show())
        self.action_7.triggered.connect(lambda:  self.comboBox1.show())
        self.action_7.triggered.connect(lambda:  self.colormap())
        self.action_7.triggered.connect(lambda:  self.lineEdit12.setText("2"))
        self.action_7.triggered.connect(lambda:  self.lineEdit13.setText("0"))
        #Hide
        self.action_7.triggered.connect(lambda:  self.label_11.hide())
        self.action_7.triggered.connect(lambda:  self.checkBox_1.hide())
        self.action_7.triggered.connect(lambda:  self.label_12.hide())
        self.action_7.triggered.connect(lambda:  self.checkBox_2.hide())
        self.action_7.triggered.connect(lambda:  self.label_13.hide())
        self.action_7.triggered.connect(lambda:  self.checkBox_3.hide())
        self.action_7.triggered.connect(lambda:  self.label_14.hide())
        self.action_7.triggered.connect(lambda:  self.checkBox_4.hide())
        self.action_7.triggered.connect(lambda:  self.label_15.hide())
        self.action_7.triggered.connect(lambda:  self.checkBox_5.hide())
        self.action_7.triggered.connect(lambda:  self.label_16.hide())
        self.action_7.triggered.connect(lambda:  self.checkBox_6.hide())
        self.action_7.triggered.connect(lambda:  self.label_17.hide())
        self.action_7.triggered.connect(lambda:  self.label_18.hide())
        self.action_7.triggered.connect(lambda:  self.label_19.hide())
        self.action_7.triggered.connect(lambda:  self.lineEdit5.hide())
        self.action_7.triggered.connect(lambda:  self.label_20.hide())
        self.action_7.triggered.connect(lambda:  self.lineEdit6.hide())
        self.action_7.triggered.connect(lambda:  self.label_21.hide())
        self.action_7.triggered.connect(lambda:  self.label_22.hide())
        self.action_7.triggered.connect(lambda:  self.lineEdit7.hide())
        self.action_7.triggered.connect(lambda:  self.label_23.hide())
        self.action_7.triggered.connect(lambda:  self.lineEdit8.hide())
        
        self.action_7.triggered.connect(lambda:  self.label_24.hide())
        self.action_7.triggered.connect(lambda:  self.lineEdit9.hide())
        self.action_7.triggered.connect(lambda:  self.label_25.hide())
        self.action_7.triggered.connect(lambda:  self.lineEdit10.hide())
        self.action_7.triggered.connect(lambda:  self.label_26.hide())
        self.action_7.triggered.connect(lambda:  self.lineEdit11.hide())
        
        self.action_7.triggered.connect(lambda:  self.label_27.hide())
        self.action_7.triggered.connect(lambda:  self.checkBox_7.hide())
        self.action_7.triggered.connect(lambda:  self.checkBox_8.hide())
        self.action_7.triggered.connect(lambda:  self.checkBox_9.hide())
        self.action_7.triggered.connect(lambda:  self.checkBox_10.hide())
        self.action_7.triggered.connect(lambda:  self.checkBox_11.hide())
        self.action_7.triggered.connect(lambda:  self.checkBox_12.hide())
        self.action_7.triggered.connect(lambda:  self.label_29.hide())
        self.action_7.triggered.connect(lambda:  self.label_30.hide())
        self.action_7.triggered.connect(lambda:  self.lineEdit14.hide())
        self.action_7.triggered.connect(lambda:  self.lineEdit15.hide())
       
        #Распределение логарифма плотности
        self.menu_3.addAction(self.action_8)
        #Show
        self.action_8.triggered.connect(lambda:  self.label_5.show())
        self.action_8.triggered.connect(lambda:  self.label_7.show())
        self.action_8.triggered.connect(lambda:  self.label_8.show())
        self.action_8.triggered.connect(lambda:  self.label_9.show())
        self.action_8.triggered.connect(lambda:  self.label_10.show())
        self.action_8.triggered.connect(lambda:  self.lineEdit2.show())
        self.action_8.triggered.connect(lambda:  self.lineEdit3.show())
        self.action_8.triggered.connect(lambda:  self.lineEdit4.show())
        self.action_8.triggered.connect(lambda:  self.comboBox1.show())
        self.action_8.triggered.connect(lambda:  self.colormap())
        self.action_8.triggered.connect(lambda:  self.lineEdit12.setText("4"))
        self.action_8.triggered.connect(lambda:  self.lineEdit13.setText("0"))
        #Hide
        self.action_8.triggered.connect(lambda:  self.label_11.hide())
        self.action_8.triggered.connect(lambda:  self.checkBox_1.hide())
        self.action_8.triggered.connect(lambda:  self.label_12.hide())
        self.action_8.triggered.connect(lambda:  self.checkBox_2.hide())
        self.action_8.triggered.connect(lambda:  self.label_13.hide())
        self.action_8.triggered.connect(lambda:  self.checkBox_3.hide())
        self.action_8.triggered.connect(lambda:  self.label_14.hide())
        self.action_8.triggered.connect(lambda:  self.checkBox_4.hide())
        self.action_8.triggered.connect(lambda:  self.label_15.hide())
        self.action_8.triggered.connect(lambda:  self.checkBox_5.hide())
        self.action_8.triggered.connect(lambda:  self.label_16.hide())
        self.action_8.triggered.connect(lambda:  self.checkBox_6.hide())
        self.action_8.triggered.connect(lambda:  self.label_17.hide())
        self.action_8.triggered.connect(lambda:  self.label_18.hide())
        self.action_8.triggered.connect(lambda:  self.label_19.hide())
        self.action_8.triggered.connect(lambda:  self.lineEdit5.hide())
        self.action_8.triggered.connect(lambda:  self.label_20.hide())
        self.action_8.triggered.connect(lambda:  self.lineEdit6.hide())
        self.action_8.triggered.connect(lambda:  self.label_21.hide())
        self.action_8.triggered.connect(lambda:  self.label_22.hide())
        self.action_8.triggered.connect(lambda:  self.lineEdit7.hide())
        self.action_8.triggered.connect(lambda:  self.label_23.hide())
        self.action_8.triggered.connect(lambda:  self.lineEdit8.hide())
        
        self.action_8.triggered.connect(lambda:  self.label_24.hide())
        self.action_8.triggered.connect(lambda:  self.lineEdit9.hide())
        self.action_8.triggered.connect(lambda:  self.label_25.hide())
        self.action_8.triggered.connect(lambda:  self.lineEdit10.hide())
        self.action_8.triggered.connect(lambda:  self.label_26.hide())
        self.action_8.triggered.connect(lambda:  self.lineEdit11.hide())
    
        self.action_8.triggered.connect(lambda:  self.label_27.hide())
        self.action_8.triggered.connect(lambda:  self.checkBox_7.hide())
        self.action_8.triggered.connect(lambda:  self.checkBox_8.hide())
        self.action_8.triggered.connect(lambda:  self.checkBox_9.hide())
        self.action_8.triggered.connect(lambda:  self.checkBox_10.hide())
        self.action_8.triggered.connect(lambda:  self.checkBox_11.hide())
        self.action_8.triggered.connect(lambda:  self.checkBox_12.hide())
        self.action_8.triggered.connect(lambda:  self.label_29.hide())
        self.action_8.triggered.connect(lambda:  self.label_30.hide())
        self.action_8.triggered.connect(lambda:  self.lineEdit14.hide())
        self.action_8.triggered.connect(lambda:  self.lineEdit15.hide())
       
        
        #Распределение радиальной скорости
        self.menu_3.addAction(self.action_9)
        #Show
        self.action_9.triggered.connect(lambda:  self.label_5.show())
        self.action_9.triggered.connect(lambda:  self.label_7.show())
        self.action_9.triggered.connect(lambda:  self.label_8.show())
        self.action_9.triggered.connect(lambda:  self.label_9.show())
        self.action_9.triggered.connect(lambda:  self.label_10.show())
        self.action_9.triggered.connect(lambda:  self.lineEdit2.show())
        self.action_9.triggered.connect(lambda:  self.lineEdit3.show())
        self.action_9.triggered.connect(lambda:  self.lineEdit4.show())
        self.action_9.triggered.connect(lambda:  self.comboBox1.show())
        self.action_9.triggered.connect(lambda:  self.colormap())
        self.action_9.triggered.connect(lambda:  self.lineEdit12.setText("5"))
        self.action_9.triggered.connect(lambda:  self.lineEdit13.setText("0"))
        #Hide
        self.action_9.triggered.connect(lambda:  self.label_11.hide())
        self.action_9.triggered.connect(lambda:  self.checkBox_1.hide())
        self.action_9.triggered.connect(lambda:  self.label_12.hide())
        self.action_9.triggered.connect(lambda:  self.checkBox_2.hide())
        self.action_9.triggered.connect(lambda:  self.label_13.hide())
        self.action_9.triggered.connect(lambda:  self.checkBox_3.hide())
        self.action_9.triggered.connect(lambda:  self.label_14.hide())
        self.action_9.triggered.connect(lambda:  self.checkBox_4.hide())
        self.action_9.triggered.connect(lambda:  self.label_15.hide())
        self.action_9.triggered.connect(lambda:  self.checkBox_5.hide())
        self.action_9.triggered.connect(lambda:  self.label_16.hide())
        self.action_9.triggered.connect(lambda:  self.checkBox_6.hide())
        self.action_9.triggered.connect(lambda:  self.label_17.hide())
        self.action_9.triggered.connect(lambda:  self.label_18.hide())
        self.action_9.triggered.connect(lambda:  self.label_19.hide())
        self.action_9.triggered.connect(lambda:  self.lineEdit5.hide())
        self.action_9.triggered.connect(lambda:  self.label_20.hide())
        self.action_9.triggered.connect(lambda:  self.lineEdit6.hide())
        self.action_9.triggered.connect(lambda:  self.label_21.hide())
        self.action_9.triggered.connect(lambda:  self.label_22.hide())
        self.action_9.triggered.connect(lambda:  self.lineEdit7.hide())
        self.action_9.triggered.connect(lambda:  self.label_23.hide())
        self.action_9.triggered.connect(lambda:  self.lineEdit8.hide())
        
        self.action_9.triggered.connect(lambda:  self.label_24.hide())
        self.action_9.triggered.connect(lambda:  self.lineEdit9.hide())
        self.action_9.triggered.connect(lambda:  self.label_25.hide())
        self.action_9.triggered.connect(lambda:  self.lineEdit10.hide())
        self.action_9.triggered.connect(lambda:  self.label_26.hide())
        self.action_9.triggered.connect(lambda:  self.lineEdit11.hide())
        
        self.action_9.triggered.connect(lambda:  self.label_27.hide())
        self.action_9.triggered.connect(lambda:  self.checkBox_7.hide())
        self.action_9.triggered.connect(lambda:  self.checkBox_8.hide())
        self.action_9.triggered.connect(lambda:  self.checkBox_9.hide())
        self.action_9.triggered.connect(lambda:  self.checkBox_10.hide())
        self.action_9.triggered.connect(lambda:  self.checkBox_11.hide())
        self.action_9.triggered.connect(lambda:  self.checkBox_12.hide())
        self.action_9.triggered.connect(lambda:  self.label_29.hide())
        self.action_9.triggered.connect(lambda:  self.label_30.hide())
        self.action_9.triggered.connect(lambda:  self.lineEdit14.hide())
        self.action_9.triggered.connect(lambda:  self.lineEdit15.hide())
       
        #Распределение азимутальной скорости
        self.menu_3.addAction(self.action_10)
        #Show
        self.action_10.triggered.connect(lambda:  self.label_5.show())
        self.action_10.triggered.connect(lambda:  self.label_7.show())
        self.action_10.triggered.connect(lambda:  self.label_8.show())
        self.action_10.triggered.connect(lambda:  self.label_9.show())
        self.action_10.triggered.connect(lambda:  self.label_10.show())
        self.action_10.triggered.connect(lambda:  self.lineEdit2.show())
        self.action_10.triggered.connect(lambda:  self.lineEdit3.show())
        self.action_10.triggered.connect(lambda:  self.lineEdit4.show())
        self.action_10.triggered.connect(lambda:  self.comboBox1.show())
        self.action_10.triggered.connect(lambda:  self.colormap())
        self.action_10.triggered.connect(lambda:  self.lineEdit12.setText("6"))
        self.action_10.triggered.connect(lambda:  self.lineEdit13.setText("0"))
        #Hide
        self.action_10.triggered.connect(lambda:  self.label_11.hide())
        self.action_10.triggered.connect(lambda:  self.checkBox_1.hide())
        self.action_10.triggered.connect(lambda:  self.label_12.hide())
        self.action_10.triggered.connect(lambda:  self.checkBox_2.hide())
        self.action_10.triggered.connect(lambda:  self.label_13.hide())
        self.action_10.triggered.connect(lambda:  self.checkBox_3.hide())
        self.action_10.triggered.connect(lambda:  self.label_14.hide())
        self.action_10.triggered.connect(lambda:  self.checkBox_4.hide())
        self.action_10.triggered.connect(lambda:  self.label_15.hide())
        self.action_10.triggered.connect(lambda:  self.checkBox_5.hide())
        self.action_10.triggered.connect(lambda:  self.label_16.hide())
        self.action_10.triggered.connect(lambda:  self.checkBox_6.hide())
        self.action_10.triggered.connect(lambda:  self.label_17.hide())
        self.action_10.triggered.connect(lambda:  self.label_18.hide())
        self.action_10.triggered.connect(lambda:  self.label_19.hide())
        self.action_10.triggered.connect(lambda:  self.lineEdit5.hide())
        self.action_10.triggered.connect(lambda:  self.label_20.hide())
        self.action_10.triggered.connect(lambda:  self.lineEdit6.hide())
        self.action_10.triggered.connect(lambda:  self.label_21.hide())
        self.action_10.triggered.connect(lambda:  self.label_22.hide())
        self.action_10.triggered.connect(lambda:  self.lineEdit7.hide())
        self.action_10.triggered.connect(lambda:  self.label_23.hide())
        self.action_10.triggered.connect(lambda:  self.lineEdit8.hide())
        
        self.action_10.triggered.connect(lambda:  self.label_24.hide())
        self.action_10.triggered.connect(lambda:  self.lineEdit9.hide())
        self.action_10.triggered.connect(lambda:  self.label_25.hide())
        self.action_10.triggered.connect(lambda:  self.lineEdit10.hide())
        self.action_10.triggered.connect(lambda:  self.label_26.hide())
        self.action_10.triggered.connect(lambda:  self.lineEdit11.hide())
        
        self.action_10.triggered.connect(lambda:  self.label_27.hide())
        self.action_10.triggered.connect(lambda:  self.checkBox_7.hide())
        self.action_10.triggered.connect(lambda:  self.checkBox_8.hide())
        self.action_10.triggered.connect(lambda:  self.checkBox_9.hide())
        self.action_10.triggered.connect(lambda:  self.checkBox_10.hide())
        self.action_10.triggered.connect(lambda:  self.checkBox_11.hide())
        self.action_10.triggered.connect(lambda:  self.checkBox_12.hide())
        self.action_10.triggered.connect(lambda:  self.label_29.hide())
        self.action_10.triggered.connect(lambda:  self.label_30.hide())
        self.action_10.triggered.connect(lambda:  self.lineEdit14.hide())
        self.action_10.triggered.connect(lambda:  self.lineEdit15.hide())
        
        #Распределение радиальной гравитационной силы
        self.menu_3.addAction(self.action_11)
        #Show
        self.action_11.triggered.connect(lambda:  self.label_5.show())
        self.action_11.triggered.connect(lambda:  self.label_7.show())
        self.action_11.triggered.connect(lambda:  self.label_8.show())
        self.action_11.triggered.connect(lambda:  self.label_9.show())
        self.action_11.triggered.connect(lambda:  self.label_10.show())
        self.action_11.triggered.connect(lambda:  self.lineEdit2.show())
        self.action_11.triggered.connect(lambda:  self.lineEdit3.show())
        self.action_11.triggered.connect(lambda:  self.lineEdit4.show())
        self.action_11.triggered.connect(lambda:  self.comboBox1.show())
        self.action_11.triggered.connect(lambda:  self.colormap())
        self.action_11.triggered.connect(lambda:  self.lineEdit12.setText("8"))
        self.action_11.triggered.connect(lambda:  self.lineEdit13.setText("0"))
        #Hide
        self.action_11.triggered.connect(lambda:  self.label_11.hide())
        self.action_11.triggered.connect(lambda:  self.checkBox_1.hide())
        self.action_11.triggered.connect(lambda:  self.label_12.hide())
        self.action_11.triggered.connect(lambda:  self.checkBox_2.hide())
        self.action_11.triggered.connect(lambda:  self.label_13.hide())
        self.action_11.triggered.connect(lambda:  self.checkBox_3.hide())
        self.action_11.triggered.connect(lambda:  self.label_14.hide())
        self.action_11.triggered.connect(lambda:  self.checkBox_4.hide())
        self.action_11.triggered.connect(lambda:  self.label_15.hide())
        self.action_11.triggered.connect(lambda:  self.checkBox_5.hide())
        self.action_11.triggered.connect(lambda:  self.label_16.hide())
        self.action_11.triggered.connect(lambda:  self.checkBox_6.hide())
        self.action_11.triggered.connect(lambda:  self.label_17.hide())
        self.action_11.triggered.connect(lambda:  self.label_18.hide())
        self.action_11.triggered.connect(lambda:  self.label_19.hide())
        self.action_11.triggered.connect(lambda:  self.lineEdit5.hide())
        self.action_11.triggered.connect(lambda:  self.label_20.hide())
        self.action_11.triggered.connect(lambda:  self.lineEdit6.hide())
        self.action_11.triggered.connect(lambda:  self.label_21.hide())
        self.action_11.triggered.connect(lambda:  self.label_22.hide())
        self.action_11.triggered.connect(lambda:  self.lineEdit7.hide())
        self.action_11.triggered.connect(lambda:  self.label_23.hide())
        self.action_11.triggered.connect(lambda:  self.lineEdit8.hide())
        
        self.action_11.triggered.connect(lambda:  self.label_24.hide())
        self.action_11.triggered.connect(lambda:  self.lineEdit9.hide())
        self.action_11.triggered.connect(lambda:  self.label_25.hide())
        self.action_11.triggered.connect(lambda:  self.lineEdit10.hide())
        self.action_11.triggered.connect(lambda:  self.label_26.hide())
        self.action_11.triggered.connect(lambda:  self.lineEdit11.hide())
        
        self.action_11.triggered.connect(lambda:  self.label_27.hide())
        self.action_11.triggered.connect(lambda:  self.checkBox_7.hide())
        self.action_11.triggered.connect(lambda:  self.checkBox_8.hide())
        self.action_11.triggered.connect(lambda:  self.checkBox_9.hide())
        self.action_11.triggered.connect(lambda:  self.checkBox_10.hide())
        self.action_11.triggered.connect(lambda:  self.checkBox_11.hide())
        self.action_11.triggered.connect(lambda:  self.checkBox_12.hide())
        self.action_11.triggered.connect(lambda:  self.label_29.hide())
        self.action_11.triggered.connect(lambda:  self.label_30.hide())
        self.action_11.triggered.connect(lambda:  self.lineEdit14.hide())
        self.action_11.triggered.connect(lambda:  self.lineEdit15.hide())
       
        #Распределение азимутальной гравитационной силы
        self.menu_3.addAction(self.action_12)
        #Show
        self.action_12.triggered.connect(lambda:  self.label_5.show())
        self.action_12.triggered.connect(lambda:  self.label_7.show())
        self.action_12.triggered.connect(lambda:  self.label_8.show())
        self.action_12.triggered.connect(lambda:  self.label_9.show())
        self.action_12.triggered.connect(lambda:  self.label_10.show())
        self.action_12.triggered.connect(lambda:  self.lineEdit2.show())
        self.action_12.triggered.connect(lambda:  self.lineEdit3.show())
        self.action_12.triggered.connect(lambda:  self.lineEdit4.show())
        self.action_12.triggered.connect(lambda:  self.comboBox1.show())
        self.action_12.triggered.connect(lambda:  self.colormap())
        self.action_12.triggered.connect(lambda:  self.lineEdit12.setText("9"))
        self.action_12.triggered.connect(lambda:  self.lineEdit13.setText("0"))
        #Hide
        self.action_12.triggered.connect(lambda:  self.label_11.hide())
        self.action_12.triggered.connect(lambda:  self.checkBox_1.hide())
        self.action_12.triggered.connect(lambda:  self.label_12.hide())
        self.action_12.triggered.connect(lambda:  self.checkBox_2.hide())
        self.action_12.triggered.connect(lambda:  self.label_13.hide())
        self.action_12.triggered.connect(lambda:  self.checkBox_3.hide())
        self.action_12.triggered.connect(lambda:  self.label_14.hide())
        self.action_12.triggered.connect(lambda:  self.checkBox_4.hide())
        self.action_12.triggered.connect(lambda:  self.label_15.hide())
        self.action_12.triggered.connect(lambda:  self.checkBox_5.hide())
        self.action_12.triggered.connect(lambda:  self.label_16.hide())
        self.action_12.triggered.connect(lambda:  self.checkBox_6.hide())
        self.action_12.triggered.connect(lambda:  self.label_17.hide())
        self.action_12.triggered.connect(lambda:  self.label_18.hide())
        self.action_12.triggered.connect(lambda:  self.label_19.hide())
        self.action_12.triggered.connect(lambda:  self.lineEdit5.hide())
        self.action_12.triggered.connect(lambda:  self.label_20.hide())
        self.action_12.triggered.connect(lambda:  self.lineEdit6.hide())
        self.action_12.triggered.connect(lambda:  self.label_21.hide())
        self.action_12.triggered.connect(lambda:  self.label_22.hide())
        self.action_12.triggered.connect(lambda:  self.lineEdit7.hide())
        self.action_12.triggered.connect(lambda:  self.label_23.hide())
        self.action_12.triggered.connect(lambda:  self.lineEdit8.hide())
        
        self.action_12.triggered.connect(lambda:  self.label_24.hide())
        self.action_12.triggered.connect(lambda:  self.lineEdit9.hide())
        self.action_12.triggered.connect(lambda:  self.label_25.hide())
        self.action_12.triggered.connect(lambda:  self.lineEdit10.hide())
        self.action_12.triggered.connect(lambda:  self.label_26.hide())
        self.action_12.triggered.connect(lambda:  self.lineEdit11.hide())
        
        self.action_12.triggered.connect(lambda:  self.label_27.hide())
        self.action_12.triggered.connect(lambda:  self.checkBox_7.hide())
        self.action_12.triggered.connect(lambda:  self.checkBox_8.hide())
        self.action_12.triggered.connect(lambda:  self.checkBox_9.hide())
        self.action_12.triggered.connect(lambda:  self.checkBox_10.hide())
        self.action_12.triggered.connect(lambda:  self.checkBox_11.hide())
        self.action_12.triggered.connect(lambda:  self.checkBox_12.hide())
        self.action_12.triggered.connect(lambda:  self.label_29.hide())
        self.action_12.triggered.connect(lambda:  self.label_30.hide())
        self.action_12.triggered.connect(lambda:  self.lineEdit14.hide())
        self.action_12.triggered.connect(lambda:  self.lineEdit15.hide())
       
        #Распределение возмущения поверхностной плотности
        self.menu_3.addAction(self.action_13)
        #Show
        self.action_13.triggered.connect(lambda:  self.label_5.show())
        self.action_13.triggered.connect(lambda:  self.label_7.show())
        self.action_13.triggered.connect(lambda:  self.label_8.show())
        self.action_13.triggered.connect(lambda:  self.label_9.show())
        self.action_13.triggered.connect(lambda:  self.label_10.show())
        self.action_13.triggered.connect(lambda:  self.lineEdit2.show())
        self.action_13.triggered.connect(lambda:  self.lineEdit3.show())
        self.action_13.triggered.connect(lambda:  self.lineEdit4.show())
        self.action_13.triggered.connect(lambda:  self.comboBox1.show())
        self.action_13.triggered.connect(lambda:  self.colormap())
        self.action_13.triggered.connect(lambda:  self.lineEdit12.setText("3"))
        self.action_13.triggered.connect(lambda:  self.lineEdit13.setText("0"))
        #Hide
        self.action_13.triggered.connect(lambda:  self.label_11.hide())
        self.action_13.triggered.connect(lambda:  self.checkBox_1.hide())
        self.action_13.triggered.connect(lambda:  self.label_12.hide())
        self.action_13.triggered.connect(lambda:  self.checkBox_2.hide())
        self.action_13.triggered.connect(lambda:  self.label_13.hide())
        self.action_13.triggered.connect(lambda:  self.checkBox_3.hide())
        self.action_13.triggered.connect(lambda:  self.label_14.hide())
        self.action_13.triggered.connect(lambda:  self.checkBox_4.hide())
        self.action_13.triggered.connect(lambda:  self.label_15.hide())
        self.action_13.triggered.connect(lambda:  self.checkBox_5.hide())
        self.action_13.triggered.connect(lambda:  self.label_16.hide())
        self.action_13.triggered.connect(lambda:  self.checkBox_6.hide())
        self.action_13.triggered.connect(lambda:  self.label_17.hide())
        self.action_13.triggered.connect(lambda:  self.label_18.hide())
        self.action_13.triggered.connect(lambda:  self.label_19.hide())
        self.action_13.triggered.connect(lambda:  self.lineEdit5.hide())
        self.action_13.triggered.connect(lambda:  self.label_20.hide())
        self.action_13.triggered.connect(lambda:  self.lineEdit6.hide())
        self.action_13.triggered.connect(lambda:  self.label_21.hide())
        self.action_13.triggered.connect(lambda:  self.label_22.hide())
        self.action_13.triggered.connect(lambda:  self.lineEdit7.hide())
        self.action_13.triggered.connect(lambda:  self.label_23.hide())
        self.action_13.triggered.connect(lambda:  self.lineEdit8.hide())
        
        self.action_13.triggered.connect(lambda:  self.label_24.hide())
        self.action_13.triggered.connect(lambda:  self.lineEdit9.hide())
        self.action_13.triggered.connect(lambda:  self.label_25.hide())
        self.action_13.triggered.connect(lambda:  self.lineEdit10.hide())
        self.action_13.triggered.connect(lambda:  self.label_26.hide())
        self.action_13.triggered.connect(lambda:  self.lineEdit11.hide())
        
        self.action_13.triggered.connect(lambda:  self.label_27.hide())
        self.action_13.triggered.connect(lambda:  self.checkBox_7.hide())
        self.action_13.triggered.connect(lambda:  self.checkBox_8.hide())
        self.action_13.triggered.connect(lambda:  self.checkBox_9.hide())
        self.action_13.triggered.connect(lambda:  self.checkBox_10.hide())
        self.action_13.triggered.connect(lambda:  self.checkBox_11.hide())
        self.action_13.triggered.connect(lambda:  self.checkBox_12.hide())
        self.action_13.triggered.connect(lambda:  self.label_29.hide())
        self.action_13.triggered.connect(lambda:  self.label_30.hide())
        self.action_13.triggered.connect(lambda:  self.lineEdit14.hide())
        self.action_13.triggered.connect(lambda:  self.lineEdit15.hide())
       
        #Распределение возмущения плотности относительно нулевого значения времени
        self.menu_3.addAction(self.action_14)
        #Show
        self.action_14.triggered.connect(lambda:  self.label_5.show())
        self.action_14.triggered.connect(lambda:  self.label_7.show())
        self.action_14.triggered.connect(lambda:  self.label_8.show())
        self.action_14.triggered.connect(lambda:  self.label_9.show())
        self.action_14.triggered.connect(lambda:  self.label_10.show())
        self.action_14.triggered.connect(lambda:  self.lineEdit2.show())
        self.action_14.triggered.connect(lambda:  self.lineEdit3.show())
        self.action_14.triggered.connect(lambda:  self.lineEdit4.show())
        self.action_14.triggered.connect(lambda:  self.comboBox1.show())
        self.action_14.triggered.connect(lambda:  self.colormap())
        self.action_14.triggered.connect(lambda:  self.lineEdit12.setText("10"))
        self.action_14.triggered.connect(lambda:  self.lineEdit13.setText("0"))
        #Hide
        self.action_14.triggered.connect(lambda:  self.label_11.hide())
        self.action_14.triggered.connect(lambda:  self.checkBox_1.hide())
        self.action_14.triggered.connect(lambda:  self.label_12.hide())
        self.action_14.triggered.connect(lambda:  self.checkBox_2.hide())
        self.action_14.triggered.connect(lambda:  self.label_13.hide())
        self.action_14.triggered.connect(lambda:  self.checkBox_3.hide())
        self.action_14.triggered.connect(lambda:  self.label_14.hide())
        self.action_14.triggered.connect(lambda:  self.checkBox_4.hide())
        self.action_14.triggered.connect(lambda:  self.label_15.hide())
        self.action_14.triggered.connect(lambda:  self.checkBox_5.hide())
        self.action_14.triggered.connect(lambda:  self.label_16.hide())
        self.action_14.triggered.connect(lambda:  self.checkBox_6.hide())
        self.action_14.triggered.connect(lambda:  self.label_17.hide())
        self.action_14.triggered.connect(lambda:  self.label_18.hide())
        self.action_14.triggered.connect(lambda:  self.label_19.hide())
        self.action_14.triggered.connect(lambda:  self.lineEdit5.hide())
        self.action_14.triggered.connect(lambda:  self.label_20.hide())
        self.action_14.triggered.connect(lambda:  self.lineEdit6.hide())
        self.action_14.triggered.connect(lambda:  self.label_21.hide())
        self.action_14.triggered.connect(lambda:  self.label_22.hide())
        self.action_14.triggered.connect(lambda:  self.lineEdit7.hide())
        self.action_14.triggered.connect(lambda:  self.label_23.hide())
        self.action_14.triggered.connect(lambda:  self.lineEdit8.hide())
        
        self.action_14.triggered.connect(lambda:  self.label_24.hide())
        self.action_14.triggered.connect(lambda:  self.lineEdit9.hide())
        self.action_14.triggered.connect(lambda:  self.label_25.hide())
        self.action_14.triggered.connect(lambda:  self.lineEdit10.hide())
        self.action_14.triggered.connect(lambda:  self.label_26.hide())
        self.action_14.triggered.connect(lambda:  self.lineEdit11.hide())
    
        self.action_14.triggered.connect(lambda:  self.label_27.hide())
        self.action_14.triggered.connect(lambda:  self.checkBox_7.hide())
        self.action_14.triggered.connect(lambda:  self.checkBox_8.hide())
        self.action_14.triggered.connect(lambda:  self.checkBox_9.hide())
        self.action_14.triggered.connect(lambda:  self.checkBox_10.hide())
        self.action_14.triggered.connect(lambda:  self.checkBox_11.hide())
        self.action_14.triggered.connect(lambda:  self.checkBox_12.hide())
        self.action_14.triggered.connect(lambda:  self.label_29.hide())
        self.action_14.triggered.connect(lambda:  self.label_30.hide())
        self.action_14.triggered.connect(lambda:  self.lineEdit14.hide())
        self.action_14.triggered.connect(lambda:  self.lineEdit15.hide())
       
        #Построить график функции зависимости логарифма плотности от угла на различных радиусах
        self.menu_4.addAction(self.action_15)
        #Show
        self.action_15.triggered.connect(lambda:  self.label_24.show())
        self.action_15.triggered.connect(lambda:  self.lineEdit9.show())
        self.action_15.triggered.connect(lambda:  self.label_25.show())
        self.action_15.triggered.connect(lambda:  self.lineEdit10.show())
        self.action_15.triggered.connect(lambda:  self.label_26.show())
        self.action_15.triggered.connect(lambda:  self.lineEdit11.show())
        self.action_15.triggered.connect(lambda:  self.lineEdit11.setText("6.2"))
        self.action_15.triggered.connect(lambda:  self.lineEdit12.setText("11"))
        self.action_15.triggered.connect(lambda:  self.lineEdit13.setText("0"))
        self.action_15.triggered.connect(lambda:  self.label_29.show())
        self.action_15.triggered.connect(lambda:  self.label_30.show())
        self.action_15.triggered.connect(lambda:  self.lineEdit14.show())
        self.action_15.triggered.connect(lambda:  self.lineEdit15.show())
       
        #Hide
        self.action_15.triggered.connect(lambda:  self.label_11.hide())
        self.action_15.triggered.connect(lambda:  self.checkBox_1.hide())
        self.action_15.triggered.connect(lambda:  self.label_12.hide())
        self.action_15.triggered.connect(lambda:  self.checkBox_2.hide())
        self.action_15.triggered.connect(lambda:  self.label_13.hide())
        self.action_15.triggered.connect(lambda:  self.checkBox_3.hide())
        self.action_15.triggered.connect(lambda:  self.label_14.hide())
        self.action_15.triggered.connect(lambda:  self.checkBox_4.hide())
        self.action_15.triggered.connect(lambda:  self.label_15.hide())
        self.action_15.triggered.connect(lambda:  self.checkBox_5.hide())
        self.action_15.triggered.connect(lambda:  self.label_16.hide())
        self.action_15.triggered.connect(lambda:  self.checkBox_6.hide())
        self.action_15.triggered.connect(lambda:  self.label_17.hide())
        self.action_15.triggered.connect(lambda:  self.label_18.hide())
        self.action_15.triggered.connect(lambda:  self.label_19.hide())
        self.action_15.triggered.connect(lambda:  self.lineEdit5.hide())
        self.action_15.triggered.connect(lambda:  self.label_20.hide())
        self.action_15.triggered.connect(lambda:  self.lineEdit6.hide())
        self.action_15.triggered.connect(lambda:  self.label_21.hide())
        self.action_15.triggered.connect(lambda:  self.label_22.hide())
        self.action_15.triggered.connect(lambda:  self.lineEdit7.hide())
        self.action_15.triggered.connect(lambda:  self.label_23.hide())
        self.action_15.triggered.connect(lambda:  self.lineEdit8.hide())
        
        self.action_15.triggered.connect(lambda:  self.label_5.hide())
        self.action_15.triggered.connect(lambda:  self.label_7.hide())
        self.action_15.triggered.connect(lambda:  self.label_8.hide())
        self.action_15.triggered.connect(lambda:  self.label_9.hide())
        self.action_15.triggered.connect(lambda:  self.label_10.hide())
        self.action_15.triggered.connect(lambda:  self.lineEdit2.hide())
        self.action_15.triggered.connect(lambda:  self.lineEdit3.hide())
        self.action_15.triggered.connect(lambda:  self.lineEdit4.hide())
        self.action_15.triggered.connect(lambda:  self.comboBox1.hide())
    
        self.action_15.triggered.connect(lambda:  self.label_27.hide())
        self.action_15.triggered.connect(lambda:  self.checkBox_7.hide())
        self.action_15.triggered.connect(lambda:  self.checkBox_8.hide())
        self.action_15.triggered.connect(lambda:  self.checkBox_9.hide())
        self.action_15.triggered.connect(lambda:  self.checkBox_10.hide())
        self.action_15.triggered.connect(lambda:  self.checkBox_11.hide())
        self.action_15.triggered.connect(lambda:  self.checkBox_12.hide())
        
        
        #Построить график функции зависимости возмущения плотности от времени на различных радиусах
        self.menu_4.addAction(self.action_16)
        #Show
        self.action_16.triggered.connect(lambda:  self.label_24.show())
        self.action_16.triggered.connect(lambda:  self.lineEdit9.show())
        self.action_16.triggered.connect(lambda:  self.label_25.show())
        self.action_16.triggered.connect(lambda:  self.lineEdit10.show())
        self.action_16.triggered.connect(lambda:  self.label_26.show())
        self.action_16.triggered.connect(lambda:  self.lineEdit11.show())
        self.action_16.triggered.connect(lambda:  self.lineEdit12.setText("12"))
        self.action_16.triggered.connect(lambda:  self.lineEdit13.setText("0"))
        #Hide
        self.action_16.triggered.connect(lambda:  self.label_11.hide())
        self.action_16.triggered.connect(lambda:  self.checkBox_1.hide())
        self.action_16.triggered.connect(lambda:  self.label_12.hide())
        self.action_16.triggered.connect(lambda:  self.checkBox_2.hide())
        self.action_16.triggered.connect(lambda:  self.label_13.hide())
        self.action_16.triggered.connect(lambda:  self.checkBox_3.hide())
        self.action_16.triggered.connect(lambda:  self.label_14.hide())
        self.action_16.triggered.connect(lambda:  self.checkBox_4.hide())
        self.action_16.triggered.connect(lambda:  self.label_15.hide())
        self.action_16.triggered.connect(lambda:  self.checkBox_5.hide())
        self.action_16.triggered.connect(lambda:  self.label_16.hide())
        self.action_16.triggered.connect(lambda:  self.checkBox_6.hide())
        self.action_16.triggered.connect(lambda:  self.label_17.hide())
        self.action_16.triggered.connect(lambda:  self.label_18.hide())
        self.action_16.triggered.connect(lambda:  self.label_19.hide())
        self.action_16.triggered.connect(lambda:  self.lineEdit5.hide())
        self.action_16.triggered.connect(lambda:  self.label_20.hide())
        self.action_16.triggered.connect(lambda:  self.lineEdit6.hide())
        self.action_16.triggered.connect(lambda:  self.label_21.hide())
        self.action_16.triggered.connect(lambda:  self.label_22.hide())
        self.action_16.triggered.connect(lambda:  self.lineEdit7.hide())
        self.action_16.triggered.connect(lambda:  self.label_23.hide())
        self.action_16.triggered.connect(lambda:  self.lineEdit8.hide())
        
        self.action_16.triggered.connect(lambda:  self.label_5.hide())
        self.action_16.triggered.connect(lambda:  self.label_7.hide())
        self.action_16.triggered.connect(lambda:  self.label_8.hide())
        self.action_16.triggered.connect(lambda:  self.label_9.hide())
        self.action_16.triggered.connect(lambda:  self.label_10.hide())
        self.action_16.triggered.connect(lambda:  self.lineEdit2.hide())
        self.action_16.triggered.connect(lambda:  self.lineEdit3.hide())
        self.action_16.triggered.connect(lambda:  self.lineEdit4.hide())
        self.action_16.triggered.connect(lambda:  self.comboBox1.hide())
        
        self.action_16.triggered.connect(lambda:  self.label_27.hide())
        self.action_16.triggered.connect(lambda:  self.checkBox_7.hide())
        self.action_16.triggered.connect(lambda:  self.checkBox_8.hide())
        self.action_16.triggered.connect(lambda:  self.checkBox_9.hide())
        self.action_16.triggered.connect(lambda:  self.checkBox_10.hide())
        self.action_16.triggered.connect(lambda:  self.checkBox_11.hide())
        self.action_16.triggered.connect(lambda:  self.checkBox_12.hide())
        self.action_16.triggered.connect(lambda:  self.label_29.hide())
        self.action_16.triggered.connect(lambda:  self.label_30.hide())
        self.action_16.triggered.connect(lambda:  self.lineEdit14.hide())
        self.action_16.triggered.connect(lambda:  self.lineEdit15.hide())
       
        #Построить график функции график зависимости Фурье-коэффициентов от времени
        self.menu_4.addAction(self.action_17)
        #Show
        self.action_17.triggered.connect(lambda:  self.label_24.show())
        self.action_17.triggered.connect(lambda:  self.lineEdit9.show())
        self.action_17.triggered.connect(lambda:  self.label_25.show())
        self.action_17.triggered.connect(lambda:  self.lineEdit10.show())
        self.action_17.triggered.connect(lambda:  self.label_26.show())
        self.action_17.triggered.connect(lambda:  self.lineEdit11.show())
        self.action_17.triggered.connect(lambda:  self.label_27.show())
        self.action_17.triggered.connect(lambda:  self.checkBox_7.show())
        self.action_17.triggered.connect(lambda:  self.checkBox_8.show())
        self.action_17.triggered.connect(lambda:  self.checkBox_9.show())
        self.action_17.triggered.connect(lambda:  self.checkBox_10.show())
        self.action_17.triggered.connect(lambda:  self.checkBox_11.show())
        self.action_17.triggered.connect(lambda:  self.checkBox_12.show())
        self.action_17.triggered.connect(lambda:  self.lineEdit11.setText(""))
        self.action_17.triggered.connect(lambda:  self.lineEdit12.setText("7"))
        self.action_17.triggered.connect(lambda:  self.lineEdit13.setText("0"))
        #Hide
        self.action_17.triggered.connect(lambda:  self.label_11.hide())
        self.action_17.triggered.connect(lambda:  self.checkBox_1.hide())
        self.action_17.triggered.connect(lambda:  self.label_12.hide())
        self.action_17.triggered.connect(lambda:  self.checkBox_2.hide())
        self.action_17.triggered.connect(lambda:  self.label_13.hide())
        self.action_17.triggered.connect(lambda:  self.checkBox_3.hide())
        self.action_17.triggered.connect(lambda:  self.label_14.hide())
        self.action_17.triggered.connect(lambda:  self.checkBox_4.hide())
        self.action_17.triggered.connect(lambda:  self.label_15.hide())
        self.action_17.triggered.connect(lambda:  self.checkBox_5.hide())
        self.action_17.triggered.connect(lambda:  self.label_16.hide())
        self.action_17.triggered.connect(lambda:  self.checkBox_6.hide())
        self.action_17.triggered.connect(lambda:  self.label_17.hide())
        self.action_17.triggered.connect(lambda:  self.label_18.hide())
        self.action_17.triggered.connect(lambda:  self.label_19.hide())
        self.action_17.triggered.connect(lambda:  self.lineEdit5.hide())
        self.action_17.triggered.connect(lambda:  self.label_20.hide())
        self.action_17.triggered.connect(lambda:  self.lineEdit6.hide())
        self.action_17.triggered.connect(lambda:  self.label_21.hide())
        self.action_17.triggered.connect(lambda:  self.label_22.hide())
        self.action_17.triggered.connect(lambda:  self.lineEdit7.hide())
        self.action_17.triggered.connect(lambda:  self.label_23.hide())
        self.action_17.triggered.connect(lambda:  self.lineEdit8.hide())
        
        self.action_17.triggered.connect(lambda:  self.label_5.hide())
        self.action_17.triggered.connect(lambda:  self.label_7.hide())
        self.action_17.triggered.connect(lambda:  self.label_8.hide())
        self.action_17.triggered.connect(lambda:  self.label_9.hide())
        self.action_17.triggered.connect(lambda:  self.label_10.hide())
        self.action_17.triggered.connect(lambda:  self.lineEdit2.hide())
        self.action_17.triggered.connect(lambda:  self.lineEdit3.hide())
        self.action_17.triggered.connect(lambda:  self.lineEdit4.hide())
        self.action_17.triggered.connect(lambda:  self.comboBox1.hide())
        self.action_17.triggered.connect(lambda:  self.label_29.hide())
        self.action_17.triggered.connect(lambda:  self.label_30.hide())
        self.action_17.triggered.connect(lambda:  self.lineEdit14.hide())
        self.action_17.triggered.connect(lambda:  self.lineEdit15.hide())
       
        
        self.menu.addAction(self.menu_3.menuAction())
        self.menu.addAction(self.menu_4.menuAction())
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menu.menuAction())
        #self.menubar.addAction(self.menu_2.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        
        self.label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt;\">Параметры</span></p></body></html>"))
        self.label_2.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt;\">Разрешение (dpi)</span></p></body></html>"))
        self.label_3.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt;\">Формат изображения</span></p></body></html>"))
        self.label_6.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt;\">Файл для предвари-</span></p><p><span style=\" font-size:10pt;\">тельной визуализации</span></p></body></html>"))
        self.label_5.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt;\">Минимальное значение</span></p><p><span style=\" font-size:10pt;\">шкалы</span></p></body></html>"))
        self.label_7.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt;\">Максимальное значение</span></p><p><span style=\" font-size:10pt;\">шкалы</span></p></body></html>"))
        self.label_8.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt;\">Максимальный радиус</span></p><p><span style=\" font-size:10pt;\">диска (кпк)</span></p></body></html>"))
        self.label_9.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt;\">Цветовая шкала</span></p></body></html>"))
        self.label_11.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt;\">Выбрать параметры построения</span></p></body></html>"))
        self.label_12.setPixmap(QPixmap("colormap/1.PNG"))
        self.label_13.setPixmap(QPixmap("colormap/2.PNG"))
        self.label_14.setPixmap(QPixmap("colormap/3.PNG"))
        self.label_15.setPixmap(QPixmap("colormap/4.PNG"))
        self.label_16.setPixmap(QPixmap("colormap/5.PNG"))
        self.label_17.setPixmap(QPixmap("colormap/6.PNG"))
        self.label_18.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt;\">Интервал по Х</span></p></body></html>"))
        self.label_19.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt;\">От</span></p></body></html>"))
        self.label_20.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt;\">До</span></p></body></html>"))
        self.label_21.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt;\">Интервал по Y</span></p></body></html>"))
        self.label_22.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt;\">От</span></p></body></html>"))
        self.label_23.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt;\">До</span></p></body></html>"))
        self.label_24.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt;\">Радиусы (кпк)</span></p></body></html>"))
        self.label_25.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt;\">Начальное время (с)</span></p></body></html>"))
        self.label_26.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt;\">Максимальное время (с)</span></p></body></html>"))
        self.label_27.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt;\">Мод</span></p></body></html>"))
        self.label_29.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt;\">Нижнее значение</span></p><p><span style=\" font-size:10pt;\">логарифма</span></p></body></html>"))
        self.label_30.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt;\">Верхнее значение</span></p><p><span style=\" font-size:10pt;\">логарифма</span></p></body></html>"))
        
        self.checkBox_7.setText("1")
        self.checkBox_8.setText("2")
        self.checkBox_9.setText("3")
        self.checkBox_10.setText("4")
        self.checkBox_11.setText("5")
        self.checkBox_12.setText("6")
        
        self.comboBox.setItemText(0, _translate("MainWindow", "png"))
        self.comboBox.setItemText(1, _translate("MainWindow", "jpg"))
        self.comboBox.setItemText(2, _translate("MainWindow", "bmp"))
        self.comboBox.setItemText(3, _translate("MainWindow", "eps"))
        self.comboBox.setItemText(4, _translate("MainWindow", "pdf"))
        self.comboBox.setItemText(5, _translate("MainWindow", "pgf"))
        self.comboBox.setItemText(6, _translate("MainWindow", "ps"))
        self.comboBox.setItemText(7, _translate("MainWindow", "raw"))
        self.comboBox.setItemText(8, _translate("MainWindow", "rgba"))
        self.comboBox.setItemText(9, _translate("MainWindow", "svg"))
        self.comboBox.setItemText(10, _translate("MainWindow", "svgz"))
        
        self.comboBox1.setItemText(0, _translate("MainWindow", "rgb"))
        self.comboBox1.setItemText(1, _translate("MainWindow", "cmrmap"))
        self.comboBox1.setItemText(2, _translate("MainWindow", "cubehelix"))
        self.comboBox1.setItemText(3, _translate("MainWindow", "gist_earth"))
        self.comboBox1.setItemText(4, _translate("MainWindow", "gist_stern"))
        self.comboBox1.setItemText(5, _translate("MainWindow", "gnuplot"))
        self.comboBox1.setItemText(6, _translate("MainWindow", "hsv"))
        self.comboBox1.setItemText(7, _translate("MainWindow", "jet"))
        self.comboBox1.setItemText(8, _translate("MainWindow", "ocean"))
        self.comboBox1.setItemText(9, _translate("MainWindow", "terrain"))
        
        self.lineEdit.setText(_translate("MainWindow", "300"))
        self.lineEdit1.setText(_translate("MainWindow", "Tvd0001.dat"))
        self.lineEdit2.setText(_translate("MainWindow", "-1"))
        self.lineEdit3.setText(_translate("MainWindow", "1"))
        self.lineEdit4.setText(_translate("MainWindow", "30"))
        self.lineEdit5.setText(_translate("MainWindow", "0"))
        self.lineEdit6.setText(_translate("MainWindow", "10"))
        self.lineEdit7.setText(_translate("MainWindow", "0"))
        self.lineEdit8.setText(_translate("MainWindow", "60"))
        self.lineEdit9.setText(_translate("MainWindow", "6, 12, 18, 24, 30"))
        self.lineEdit10.setText(_translate("MainWindow", "0"))
        self.lineEditDir.setText(_translate("MainWindow", "Выберите папку"))
        self.lineEdit12.setText(_translate("MainWindow", "-1"))
        self.lineEdit14.setText(_translate("MainWindow", "-3.0"))
        self.lineEdit15.setText(_translate("MainWindow", "-0.5"))
        
        self.pushButton.setText(_translate("MainWindow", "Построить"))
        
        self.menuFile.setTitle(_translate("MainWindow", "Файл"))
        self.menu.setTitle(_translate("MainWindow", "Выбрать характеристику"))
        self.menu_3.setTitle(_translate("MainWindow", "Построить распределение"))
        self.menu_4.setTitle(_translate("MainWindow", "Построить график функции"))
        self.directoryMenu.setText(_translate("MainWindow", "Выбрать данные"))
        self.action_2.setText(_translate("MainWindow", "Выгрузить данные"))
        self.action_3.setText(_translate("MainWindow", "Сохранить настройки"))
        self.action_4.setText(_translate("MainWindow", "Загрузить настройки"))
        self.action_r.setText(_translate("MainWindow", "Параметров системы вдоль r"))
        self.action_7.setText(_translate("MainWindow", "Плотности"))
        self.action_8.setText(_translate("MainWindow", "Логарифма плотности"))
        self.action_9.setText(_translate("MainWindow", "Радиальной скорости"))
        self.action_10.setText(_translate("MainWindow", "Азимутальной скорости"))
        self.action_11.setText(_translate("MainWindow", "Радиальной гравитационной силы"))
        self.action_12.setText(_translate("MainWindow", "Азимутальной гравитационной силы"))
        self.action_13.setText(_translate("MainWindow", "Возмущения поверхностной плотности"))
        self.action_14.setText(_translate("MainWindow", "Возмущения плотности относительно нулевого значения времени"))
        self.action_15.setText(_translate("MainWindow", "Зависимости логарифма плотности от угла на различных радиусах"))
        self.action_16.setText(_translate("MainWindow", "Зависимости возмущения плотности от времени на различных радиусах"))
        self.action_17.setText(_translate("MainWindow", "График зависимости Фурье-коэффициентов от времени"))
        
    def MainGrapher(self,directory,Nmenu,dpi,format_image,colormap,vmin,vmax,maxRdRaspr,radius,radius2,xlim,ylim,Param,mody,timeEnd, curGraph, batchMode, timeStart, logTimeStart, logTimeEnd):
        files = os.listdir(directory)
        #Получаем список файлов в переменную files
        #Фильтруем список 
        dat = filter(lambda x: x.endswith('.dat'), files)
        length = list(dat)
        dat = filter(lambda x: x.endswith('.dat'), files)
        number_of_files = len(length)
        #список радиусов в вещественный массив
        radius = list(map(lambda x: float(x),radius.split(',')))
        radius2 = list(map(lambda x: float(x),radius2.split(',')))
        Omega = 0.0
        k = 0 #для меню №10
        N = len(radius) #для меню №10
        eps = sys.float_info.epsilon
        cmap=colormap #plt.cm.jet
        if timeStart<0:
            errorMessage = QtWidgets.QErrorMessage(self.centralwidget)
            errorMessage.showMessage('Начальное время не может быть меньше 0! Расчет будет произведен от 0')
            errorMessage.exec_()
            timeStart = 0
        #----------------------------------
        if batchMode == 0:
            if (Nmenu == 7):
                Param1 = None 
                Param2 = None
                Param1, Param2 = self.Fourier(directory,number_of_files,dat,font,font_legend,dpi,format_image,mody,timeEnd, batchMode, Param1, Param2, timeStart)
            elif (Nmenu == 12):
                dat = filter(lambda x: x.endswith('.dat'), files)
                length = list(dat)
                dat = filter(lambda x: x.endswith('.dat'), files)
                amp = None
                e1 = None
                amp, e1 = self.LDen2(number_of_files, dat, directory,batchMode,format_image, dpi, length, amp, e1, radius2, timeEnd, timeStart)
            else:
                #открываем 1 бинарный файл для чтения
                Input = open(directory + '//' + curGraph,'rb')
                self.ReadFile(Input, batchMode, directory, curGraph, length, Nmenu, format_image, dpi, number_of_files, dat, cmap, vmin,vmax,maxRdRaspr,radius,radius2,xlim,ylim,Param,mody, timeStart, timeEnd, logTimeStart, logTimeEnd) 
        else:
            if (Nmenu == 7):
                self.Fourier(directory,number_of_files,dat,font,font_legend,dpi,format_image,mody,timeEnd, batchMode, Param1, Param2, timeStart)
            elif (Nmenu == 12):
                self.LDen2(number_of_files, dat, directory,batchMode,format_image, dpi, length, amp, e1, radius2, timeEnd, timeStart)
            else:
                for img in dat:
                    #открываем бинарный файл для чтения один за другим
                    Input = open(directory + '//' + img,'rb') 
                    self.ReadFile(Input, batchMode, directory, img, length, Nmenu, format_image, dpi,  number_of_files,  dat, cmap, vmin,vmax,maxRdRaspr,radius,radius2,xlim,ylim,Param,mody, timeStart, timeEnd, logTimeStart, logTimeEnd)
                    Input.close()


    def ReadFile(self,Input, isWrite, directory, img, length, choice, format_image, dpi,  number_of_files, dat, cmap, vmin,vmax,maxRadius,radius,radius2,xlim,ylim,Param,mody, timeStart, timeEnd, logTimeStart, logTimeEnd):
        eps = sys.float_info.epsilon
        #гамма
        gamma = np.fromfile(Input,np.float64,1) #gam
        t = np.fromfile(Input,np.float64,1)
        #число ячеек по Оx
        nRadius = np.fromfile(Input,np.int32,1)
        #число ячеек по Оy
        nPhi = np.fromfile(Input,np.int32,1) 
        #число ячеек по Оz
        nz = np.fromfile(Input,np.int32,1) 

        #Массив радиусов #rad1
        rad1 = np.fromfile(Input,np.float64,int(nRadius)) 
        #Массив по фи
        phi = np.fromfile(Input,np.float64,int(nPhi)) 
        #z компонента отсутствует #z1
        z = np.fromfile(Input,np.float64,int(nz)) 

        #параметры расчетной сетки не меняются во всех файлах
        rho = np.zeros((int(nRadius),1))
        DS = np.zeros(nRadius)
        x1 = np.zeros((int(nRadius),int(nPhi)))
        y1 = np.zeros((int(nRadius),int(nPhi)))

        N = len(rad1)

        deltaRadius = rad1[2] - rad1[1]
        deltaPhi = phi[2] - phi[1]
        for i in range(int(nRadius)):
            DS[i] = math.pi*((rad1[i]+0.5*deltaRadius)**2 - ((rad1[i]-0.5*deltaRadius)**2))

        for i in range(int(nRadius)):
            for j in range(int(nPhi)):
                x1[i][j]=rad1[i]*np.cos(phi[j])
                y1[i][j]=rad1[i]*np.sin(phi[j])

        for i in range(int(nRadius)):
            x1[i][int(nPhi)-1] = x1[i][0]
            y1[i][int(nPhi)-1] = y1[i][0]


        if (choice == 10):
            den0 = np.fromfile(Input,np.float64,(int(nRadius)+4)*(int(nPhi)+4)*int(nz)).reshape((int(nRadius)+4,int(nPhi)+4))
            den0 = den0[3:int(nRadius+4)-1,3:int(nPhi+4)-1]

        if (choice == 1):
            rr = np.fromfile(Input,np.float64,(int(nRadius)+4)*(int(nPhi)+4)).reshape((int(nRadius)+4,int(nPhi)+4))
            pp = np.fromfile(Input,np.float64,(int(nRadius)+4)*(int(nPhi)+4)).reshape((int(nRadius)+4,int(nPhi)+4))
            ur = np.fromfile(Input,np.float64,(int(nRadius)+4)*(int(nPhi)+4)).reshape((int(nRadius)+4,int(nPhi)+4))
            uph = np.fromfile(Input,np.float64,(int(nRadius)+4)*(int(nPhi)+4)).reshape((int(nRadius)+4,int(nPhi)+4))
        elif (choice == 10):
            rrr = np.fromfile(Input,np.float64,(int(nRadius)+4)*(int(nPhi)+4)*int(nz)).reshape((int(nRadius)+4,int(nPhi)+4))
            rrr = rrr[3:int(nRadius+4)-1,3:int(nPhi+4)-1]
        else:
            rrr = np.fromfile(Input,np.float64,(int(nRadius)+4)*(int(nPhi)+4)*int(nz)).reshape((int(nRadius)+4,int(nPhi)+4))
            rrr = rrr[3:int(nRadius+4)-1,3:int(nPhi+4)-1]
            ppp = np.fromfile(Input,np.float64,(int(nRadius)+4)*(int(nPhi)+4)*int(nz)).reshape((int(nRadius)+4,int(nPhi)+4))
            ppp = ppp[3:int(nRadius+4)-1,3:int(nPhi+4)-1]
            uuu = np.fromfile(Input,np.float64,(int(nRadius)+4)*(int(nPhi)+4)*int(nz)).reshape((int(nRadius)+4,int(nPhi)+4))
            uuu = uuu[3:int(nRadius+4)-1,3:int(nPhi+4)-1]
            vvv = np.fromfile(Input,np.float64,(int(nRadius)+4)*(int(nPhi)+4)*int(nz)).reshape((int(nRadius)+4,int(nPhi)+4))
            vvv = vvv[3:int(nRadius+4)-1,3:int(nPhi+4)-1]
            rf = np.fromfile(Input,np.float64,(int(nRadius)+4)*(int(nPhi)+4)*int(nz)).reshape((int(nRadius)+4,int(nPhi)+4))
            rf = rf[3:int(nRadius+4)-1,3:int(nPhi+4)-1]
            af = np.fromfile(Input,np.float64,(int(nRadius)+4)*(int(nPhi)+4)*int(nz)).reshape((int(nRadius)+4,int(nPhi)+4))
            af = af[3:int(nRadius+4)-1,3:int(nPhi+4)-1]
        Input.close()
        Omega = 0.0
            
        #-----------------------------1 - График распределения начальных параметров---------------------------------
        if (choice == 1):
            # угловая скорсть вращения диска
            V=uph[3:int(nRadius+4)-1,int((nPhi+4)/2)]
            vs=rr[3:int(nRadius+4)-1,int((nPhi+4)/2)]
            vp=pp[3:int(nRadius+4)-1,int((nPhi+4)/2)]
            r=rad1

            # Азимутальная скорость
            Vom = V + r*Omega
            vo = V/r
            vc = (gamma*vp)/vs
            v5 = np.gradient(vo,r[1]-r[0])
            v5[0] = 0.0
            vk = 4.0*pow(vo,2)+2.0*r*vo*v5
            vq = (np.sqrt(vc*vk)*(1/vs))/math.pi
            Lambda = (2*pow(math.pi,2)*vs)/vk

            Param1=[Vom,V,vs,vo,pow(vk,0.5),vq]

            # Содержит заглавия легенды
            Param2=[r'$V_\phi$+r$\Omega$',r'$V_\phi$',r'$\sigma$',r'$\omega$',r'$\kappa$',r'$Q_T$']
            Parametry1=[]
            Parametry2=[]

            for i in range(len(Param)):
                if Param[i] == 1:
                    Parametry1.append(Param1[i])
                    Parametry2.append(Param2[i])

            self.drawGrapher(r,Parametry1,xlim,ylim, Parametry2, "r", "", t,
                       directory,"1-ParamDataTVDPolar", isWrite, img, format_image, dpi)
            del rad1,phi,z,rr,pp,ur,uph,r,V,vs,vp,Vom,vo,vc,v5,vk,vq,Lambda

        #---------------------------------------2 - Распределение плотности----------------------------------------
        elif (choice == 2):
            self.drawPcolor(x1,y1,rrr,cmap,vmin,vmax,maxRadius,r'$\sigma$',t,
                      directory,"2-Density", isWrite, img, format_image, dpi)
            del rad1,phi,z,uuu,rrr,ppp,vvv,rf,af
        #---------------------------------------3 - Возмущение поверхностной плотности----------------------------------------
        elif (choice == 3):
            rrr0 = np.zeros((int(nRadius),int(nPhi)))
            for i in range(int(nRadius)):
                for j in range(int(nPhi)):      #rrr0 средняя плотность в кольце
                    rho[i] = rho[i]+rrr[i][j]*DS[i]/nPhi

                for j in range(int(nPhi)):
                    rrr0[i][j] = rho[i]/DS[i]
            Value = (rrr-rrr0)/rrr0
            Value[nRadius-1,:] = Value[0,:]

            self.drawPcolor(x1,y1,Value,cmap,vmin,vmax,maxRadius,r'($\sigma$ - <$\sigma$>)/<$\sigma$>',t,
                      directory,"3-PertrubedDensity", isWrite, img, format_image, dpi)
            del rad1,phi,z,uuu,rrr,rrr0,Value,ppp,vvv,rf,af
        #---------------------------------------4 - Распределение логарифма плотности----------------------------------------
        elif (choice == 4):
            Lrrr = np.log10(rrr+eps)
            self.drawPcolor(x1,y1,Lrrr,cmap,vmin,vmax,maxRadius,r'log($\sigma$)',t,
                       directory,"4-LogDensity", isWrite, img, format_image, dpi)
            del rad1, phi,z,uuu,rrr,ppp,vvv,rf,af,Lrrr
        #---------------------------------------5 - Распределение радиальной скорости----------------------------------------
        elif (choice == 5):
            self.drawPcolor(x1,y1,uuu,cmap,vmin,vmax,maxRadius,r'radial velocity',t,
                      directory,"5-RadialVelocity", isWrite, img, format_image, dpi)
            del rad1,phi,z,uuu,rrr,ppp,vvv,rf,af
        #---------------------------------------6 - Распределение азимутальной скорoсти----------------------------------------
        elif (choice == 6):
            self.drawPcolor(x1,y1,vvv,cmap,vmin,vmax,maxRadius,r'angular velocity',t,
                       directory,'6-AngularVelocity', isWrite, img, format_image, dpi)
            del rad1, phi,z,uuu,rrr,ppp,vvv,rf,af
        #---------------------------------------8 - Распределение радиальной силы----------------------------------------
        elif (choice == 8):
            self.drawPcolor(x1,y1,rf,cmap,vmin,vmax,maxRadius,r'radial force',t,
                       directory,'8-RadialForce', isWrite, img, format_image, dpi)
            del rad1, phi,z,uuu,rrr,ppp,vvv,rf,af
        #---------------------------------------9 - Распределение азимутальной силы----------------------------------------
        elif (choice == 9):
            self.drawPcolor(x1,y1,af,cmap,vmin,vmax,maxRadius,r'angular force',t,
                       directory,'9-AngularForce',isWrite, img, format_image, dpi)
            del rad1, phi,z,uuu,rrr,ppp,vvv,rf,af
        #---------------------------------------10 - Распределение возмущения плотности относительно t=0----------------------------------------
        elif (choice == 10):
            Value = (rrr-den0)/den0 #относительное возмущение плотности относительно ее начального распределения
            self.drawPcolor(x1,y1,Value,cmap,vmin,vmax,maxRadius,r'($\sigma$ - $\sigma_0$)/$\sigma_0$',t,
                       directory,'10-PertrubedDensity', isWrite, img, format_image, dpi)
            del rad1, phi,z,rrr,Value, den0
        #---------------------------------------11 - График зависимости логарифма плотности от угла на различных радиусах----------------------------------------
        elif (choice == 11):
            maxRadius = rad1[-1]
            if isWrite == 0:
                for i in range(len(radius2)):
                    if (radius2[i] > maxRadius):
                        errorMessage = QtWidgets.QErrorMessage(self.centralwidget)
                        errorMessage.showMessage("Значение превышает максимальный радиус = %d!"% maxRadius)
                        errorMessage.exec_()
                        break
            k = 0 
            Lrrr = np.log10(rrr+eps)
            nnn = np.zeros(len(radius2))

            for i in range(len(radius2)):
                nnn[i] = radius2[i]
                nnn[i] = nnn[i]/deltaRadius

            nnn = np.fix(nnn+0.5)

            fig,ax = plt.subplots()
            for i in range(len(radius2)):
                a = nnn[i]
                maxrrr = np.max(Lrrr[int(a),:])
                r = nnn[i]*deltaRadius+0.5
                ax.plot(phi,Lrrr[int(a),:],label='r=%d'% r)

            ax.axis([timeStart, timeEnd, logTimeStart, logTimeEnd])
            plt.title(r'log($\sigma$)($\phi$), t=%1.1f'% t, fontdict=font)
            ax.legend(loc='upper right',prop=font_legend)
            plt.tick_params(axis='both', which='major', labelsize=20)
            plt.xlabel(r'$\phi$',fontdict=font)
            plt.ylabel(r'log($\sigma$)',fontdict=font)

            save_directory = "11-LSigma"
            save_img = save_directory.split('_')
            fig.set_size_inches(9.5, 8.7)
            grafic = plt.gcf()
            f = io.BytesIO()
            grafic.savefig(f)
            pixmap = QtGui.QPixmap()
            pixmap.loadFromData(f.getvalue())
            if isWrite == 0:
                self.label_4.setPixmap(pixmap)
            else:
                image = img.split('.')
                if not os.path.isdir(directory + '//' + save_directory):
                    os.mkdir(directory + '//' + save_directory)
                fig.savefig(directory + '//' + save_directory + '//'+ save_img[0]+ image[0] + '.'+format_image,dpi=int(dpi), format = format_image)
                plt.close('all')
            del rad1, phi,z,uuu,rrr,ppp,vvv,rf,af,Lrrr,nnn


    def drawGrapher(self,x,y,xlim,ylim, label, xlabel, ylabel, t, directory,save_directory,isWrite, 
                    img, format_image, dpi):
        fig,ax = plt.subplots()
        fig.set_size_inches(11, 8.7)
        xlim = list(map(lambda x: float(x),xlim))
        ylim = list(map(lambda x: float(x),ylim))
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)

        for i in range(len(y)):
            ax.plot(x,y[i], label=label[i])

        plt.title(r't=%1.1f'% t, fontdict=font)
        ax.legend(loc='upper right', prop=font_legend)
        # Сетка включена
        ax.grid(True)
        plt.tick_params(axis='both', which='major', labelsize=25)
        # Подписи к осям
        plt.xlabel(xlabel,fontdict=font)
        plt.ylabel(ylabel,fontdict=font)
        grafic = plt.gcf()
        f = io.BytesIO()
        grafic.savefig(f)
        pixmap = QtGui.QPixmap()
        pixmap.loadFromData(f.getvalue())
        if isWrite == 0:
            self.label_4.setPixmap(pixmap)
        else:
            image = img.split('.')
            save_img = save_directory.split('_')
            if not os.path.isdir(directory + '//' + save_directory):
                os.mkdir(directory + '//' + save_directory)
            fig.savefig(directory + '//' + save_directory + '//'+ save_img[0]+image[0]+"."+format_image,dpi=int(dpi), format = format_image)
            plt.close('all')

    
    def drawPcolor(self,x1,y1,Value,cmap,vmin,vmax,maxRdRaspr,title2,t,directory,save_directory,isWrite, img, format_image, dpi):
        fig,ax = plt.subplots()
        fig.set_size_inches(11, 8.7)
        ax.axis([-maxRdRaspr, maxRdRaspr, -maxRdRaspr, maxRdRaspr])
        plt.title(title2+', t=%1.1f'% t, fontdict=font)
        c = ax.pcolor(x1,y1,Value,cmap=cmap,vmin=vmin,vmax=vmax)
        cb = plt.colorbar(c,extend='both')
        tick_locator = ticker.MaxNLocator(nbins=5) 
        cb.locator = tick_locator 
        cb.update_ticks()
        plt.tick_params(axis='both', which='major', labelsize=25)
        grafic = plt.gcf()
        f = io.BytesIO()
        grafic.savefig(f)
        pixmap = QtGui.QPixmap()
        pixmap.loadFromData(f.getvalue())
        if isWrite == 0:
            self.label_4.setPixmap(pixmap)
        else:
            image = img.split('.')
            save_img = save_directory.split('_')
            if not os.path.isdir(directory + '//' + save_directory):
                os.mkdir(directory + '//' + save_directory)
            fig.savefig(directory + '//' + save_directory + '//'+save_img[0]+image[0]+"."+format_image,dpi=int(dpi), format = format_image)
            plt.close('all')
            del fig
    
    def LDen2(self, number_of_files, dat, directory,isWrite,format_image, dpi, length, amp, e1, radius2, timeEnd, timeStart):
        global tMax, t, gam, k, deltaRadius

        if isWrite == 0:
            dat = list(dat)
            for img in dat:
                if (img == dat[-1]):
                    Input = open(directory + '//' + img,'rb')
                    gam = np.fromfile(Input,np.float64,1)
                    t = np.fromfile(Input,np.float64,1)
                    tMax = t
                    #число ячеек по Оx
                    nRadius = np.fromfile(Input,np.int32,1)
                    #число ячеек по Оy
                    nPhi = np.fromfile(Input,np.int32,1) 
                    #число ячеек по Оz
                    nz = np.fromfile(Input,np.int32,1) 

                    #Массив радиусов #rad1
                    rad1  = np.fromfile(Input,np.float64,int(nRadius))
                    maxRadius = rad1[-1]
                    Input.close() 
            k=-1
            N = len(radius2)

            for img in dat:
                Input = open(directory + '//' + img,'rb')
                gamma = np.fromfile(Input,np.float64,1) #gam
                t = np.fromfile(Input,np.float64,1)
                #число ячеек по Оx
                nRadius = np.fromfile(Input,np.int32,1)
                #число ячеек по Оy
                nPhi = np.fromfile(Input,np.int32,1) 
                #число ячеек по Оz
                nz = np.fromfile(Input,np.int32,1) 

                #Массив радиусов #rad1
                rad1 = np.fromfile(Input,np.float64,int(nRadius)) 
                #Массив по фи
                phi = np.fromfile(Input,np.float64,int(nPhi)) 
                #z компонента отсутствует #z1
                z = np.fromfile(Input,np.float64,int(nz)) 

                #параметры расчетной сетки не меняются во всех файлах
                if img == length[0]:
                    rho = np.zeros((int(nRadius),1))
                    DS = np.zeros(nRadius)
                    x1 = np.zeros((int(nRadius),int(nPhi)))
                    y1 = np.zeros((int(nRadius),int(nPhi)))

                    u1 = np.zeros((N,number_of_files))
                    o1 = np.zeros((N,number_of_files))
                    e1 = np.zeros((N,number_of_files))
                    amp = np.zeros(number_of_files)
                    nnn = np.zeros(N)

                    deltaRadius = rad1[2] - rad1[1]

                rrr = np.fromfile(Input,np.float64,(int(nRadius)+4)*(int(nPhi)+4)*int(nz)).reshape((int(nRadius)+4,int(nPhi)+4))
                rrr = rrr[3:int(nRadius+4)-1,3:int(nPhi+4)-1]

                Input.close()

                amp[k+1] = t
                deltaRadius = rad1[2] - rad1[1]
                dN = nRadius/N
                dNN = 0

                nnn = np.zeros(N)
                for i in range(N):
                    nnn[i] = radius2[i]
                    nnn[i] = nnn[i]/deltaRadius

                nnn = np.fix(nnn+0.5) 

                for i in range(N):
                    local_max = -1
                    i_local_max = nnn[i]
                    for j in range(int(nPhi)):
                        if local_max < rrr[int(i_local_max),j]:
                            local_max = rrr[int(i_local_max),j]

                    u1[i][k] = local_max
                    o1[i][k] = np.sum(rrr[int(nnn[i])])/nPhi
                    e1[i][k] = (u1[i][k]-o1[i][k])/o1[i][k]

                #print(k/number_of_files*100)
                if float(timeEnd)<=amp[k]:
                    break
                k+=1
        else:
             N = len(radius2)

        fig,ax = plt.subplots()
        for i in range(N):
            ax.plot(amp,np.log10(e1[i]),label='r=%d'%radius2[i])

        ax.set_xlim(timeStart)
        ax.legend(loc='lower right',prop=font_legend)
        plt.xlabel('t',fontdict=font)
        plt.ylabel(r'($\sigma_{max}$ - <$\sigma$>)/<$\sigma$>  ',fontdict=font)
        plt.tick_params(axis='both', which='major', labelsize=20)
        save_directory = "12-LDen2"
        fig.set_size_inches(9.5, 8.7)
        grafic = plt.gcf()
        f = io.BytesIO()
        grafic.savefig(f)
        pixmap = QtGui.QPixmap()
        pixmap.loadFromData(f.getvalue())
        if isWrite == 0:
            self.label_4.setPixmap(pixmap)
            return amp, e1
            del radius, phi,z,rrr,nnn,u1,e1,o1,amp
        else:
            #image = img.split('.')
            if not os.path.isdir(directory + '//' + save_directory):
                os.mkdir(directory + '//' + save_directory)
            fig.savefig(directory + '//' + save_directory + '//LDen2'+  '.' + format_image,dpi=int(dpi), format = format_image)
            plt.close('all')
            del  e1, amp


    def Fourier(self, directory,number_of_files,dat,font,font_legend,dpi,format_image,mody,timeEnd, isWrite, Param1, Param2, timeStart):
        if (isWrite == 0):
            k=-1
            t = np.zeros((number_of_files,1))
            if timeStart < 0:
                timeStart = 0
            
            gamp_0 = np.zeros((number_of_files,1))
            gamp_1 = np.zeros((number_of_files,1))
            gamp_2 = np.zeros((number_of_files,1))
            gamp_3 = np.zeros((number_of_files,1))
            gamp_4 = np.zeros((number_of_files,1))
            gamp_5 = np.zeros((number_of_files,1))
            gamp_6 = np.zeros((number_of_files,1))
            
            s0=np.zeros((1,1))
            s1=np.zeros((1,1))
            s2=np.zeros((1,1))
            s3=np.zeros((1,1))
            s4=np.zeros((1,1))
            s5=np.zeros((1,1))
            s6=np.zeros((1,1))
            
            for img in dat:
                Input = open(directory + '//' + img,'rb')

                gam = np.fromfile(Input,np.float64,1)
                t[k+1] = np.fromfile(Input,np.float64,1)
                nrad = np.fromfile(Input,np.int32,1)
                nphi = np.fromfile(Input,np.int32,1)
                nz = np.fromfile(Input,np.int32,1)

                rad = np.fromfile(Input,np.float64,int(nrad))
                phi = np.fromfile(Input,np.float64,int(nphi))
                z = np.fromfile(Input,np.float64,int(nz))

                d = np.fromfile(Input,np.float64,(int(nrad)+4)*(int(nphi)+4)*int(nz)).reshape((int(nrad)+4,int(nphi)+4))
                d = d[3:int(nrad+4)-1,3:int(nphi+4)-1]
                Input.close()

                dr = rad[2]-rad[1]

                disk_mass = 0.0
                DS = np.zeros(nrad)

                for i in range(1,int(nrad)):
                    DS[i] = math.pi*((rad[i]+0.5*dr)*(rad[i]+0.5*dr)-(rad[i]-0.5*dr)*(rad[i]-0.5*dr))/nphi
                    for j in range(1,int(nphi)):
                        disk_mass=disk_mass+d[i,j]*DS[i]

                s1=0.0
                s2=0.0
                s3=0.0
                s4=0.0
                s5=0.0
                s6=0.0

                s1_ = 0.0
                s2_ = 0.0
                s3_ = 0.0
                s4_ = 0.0
                s5_ = 0.0
                s6_ = 0.0

                for i in range(int(nrad)):
                    for j in range(int(nphi)):
                        s1 = s1+d[i,j]*math.cos(1*phi[j])*DS[i]
                        s2 = s2+d[i,j]*math.cos(2*phi[j])*DS[i]
                        s3 = s3+d[i,j]*math.cos(3*phi[j])*DS[i]
                        s4 = s4+d[i,j]*math.cos(4*phi[j])*DS[i]
                        s5 = s5+d[i,j]*math.cos(5*phi[j])*DS[i]
                        s6 = s6+d[i,j]*math.cos(6*phi[j])*DS[i]

                        s1_ = s1_ +d[i,j]*math.sin(1*phi[j])*DS[i]
                        s2_ = s2_ +d[i,j]*math.sin(2*phi[j])*DS[i]
                        s3_ = s3_ +d[i,j]*math.sin(3*phi[j])*DS[i]
                        s4_ = s4_ +d[i,j]*math.sin(4*phi[j])*DS[i]
                        s5_ = s5_ +d[i,j]*math.sin(5*phi[j])*DS[i]
                        s6_ = s6_ +d[i,j]*math.sin(6*phi[j])*DS[i]

                gamp_1[k] = math.sqrt((pow(s1,2)+pow(s1_,2)))
                gamp_2[k] = math.sqrt((pow(s2,2)+pow(s2_,2)))
                gamp_3[k] = math.sqrt((pow(s3,2)+pow(s3_,2)))
                gamp_4[k] = math.sqrt((pow(s4,2)+pow(s4_,2)))
                gamp_5[k] = math.sqrt((pow(s5,2)+pow(s5_,2)))
                gamp_6[k] = math.sqrt((pow(s6,2)+pow(s6_,2)))

                #print(k/number_of_files*100)
                if float(timeEnd)==t[k]:
                    break
                k+=1
            
            del rad, phi, z, DS, d
        
            gamp_1 = np.log10(abs(gamp_1)/disk_mass)
            gamp_2 = np.log10(abs(gamp_2)/disk_mass)
            gamp_3 = np.log10(abs(gamp_3)/disk_mass)
            gamp_4 = np.log10(abs(gamp_4)/disk_mass)
            gamp_5 = np.log10(abs(gamp_5)/disk_mass)
            gamp_6 = np.log10(abs(gamp_6)/disk_mass)

            Param1=[gamp_1,gamp_2,gamp_3,gamp_4,gamp_5,gamp_6]
            Param2=['m=1','m=2','m=3','m=4','m=5','m=6']
            Parametry1=[]
            Parametry2=[]
            for i in range(len(mody)):
                if mody[i]==1:
                    Parametry1.append(Param1[i])
                    Parametry2.append(Param2[i])
            
            del gamp_1,gamp_2,gamp_3,gamp_4,gamp_5,gamp_6,s1,s2,s3,s4,s5,s6
    
        fig,ax = plt.subplots()
        for i in range(len(Parametry1)):
            ax.plot(t,Parametry1[i],label=Parametry2[i])
        
        ax.set_xlim(timeStart)
        ax.legend(loc='lower right',prop=font_legend)
        plt.xlabel(r't',fontdict=font)
        plt.ylabel(r'$\hat A$',fontdict=font)
        ax.grid(True)
        plt.title('global amplitude a growing',fontdict=font)
        plt.tick_params(axis='both', which='major', labelsize=24)
        fig.set_size_inches(11, 8.7)
        grafic = plt.gcf()
        f = io.BytesIO()
        grafic.savefig(f)
        pixmap = QtGui.QPixmap()
        pixmap.loadFromData(f.getvalue())
        if isWrite == 0:
            self.label_4.setPixmap(pixmap)
            return Parametry1, Parametry2
        else:
            if not os.path.isdir(directory + '//7-FourierCoefficients'):
                os.mkdir(directory + '//7-FourierCoefficients')
            fig.savefig(directory + '//7-FourierCoefficients//FourierCoefficients'+str(k)+"."+format_image,dpi=int(dpi), format = format_image)

        plt.close('all')
        del t

        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

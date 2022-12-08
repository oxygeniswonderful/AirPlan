from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *
from Core.ConfigReader import ConfigReader

class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(901, 900)

        config_reader = ConfigReader()

        QToolTip.setFont(QFont('Times', 14))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")

        """Info about weather at your destination"""
        label_weather = config_reader.read_config("main_window.stylesheets.label_weather")
        self.label_weather = QtWidgets.QLabel(self.centralwidget)
        self.label_weather.setGeometry(QtCore.QRect(10, 10, 301, 41))
        self.label_weather.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_weather.setObjectName("label_weather")
        self.label_weather.setToolTip("Here you can view the weather at your destination")
        self.label_weather.setStyleSheet(label_weather)

        """Info about distance at your destination"""
        label_distance = config_reader.read_config("main_window.stylesheets.label_distance")
        self.label_distance = QtWidgets.QLabel(self.centralwidget)
        self.label_distance.setGeometry(QtCore.QRect(10, 60, 231, 41))
        self.label_distance.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_distance.setObjectName("label_distance")
        self.label_distance.setToolTip("Here you can view the distance at your destination")
        self.label_distance.setStyleSheet(label_distance)

        """Info about price at your destination"""
        label_price = config_reader.read_config("main_window.stylesheets.label_price")
        self.label_price = QtWidgets.QLabel(self.centralwidget)
        self.label_price.setGeometry(QtCore.QRect(10, 110, 171, 41))
        self.label_price.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_price.setObjectName("label_price")
        self.label_price.setToolTip("Here you can view the price at your destination")
        self.label_price.setStyleSheet(label_price)

        """Build path"""
        stylesheet_pathButton = config_reader.read_config("main_window.stylesheets.pathButton")
        self.pathButton = QtWidgets.QPushButton(self.centralwidget)
        self.pathButton.setGeometry(QtCore.QRect(300, 350, 331, 41))
        self.pathButton.setToolTip("Click here to build path")
        self.pathButton.setStyleSheet(stylesheet_pathButton)
        self.pathButton.setObjectName("pathButton")

        """Show parameters"""
        stylesheet_showButton = config_reader.read_config("main_window.stylesheets.showButton")
        self.showButton = QtWidgets.QPushButton(self.centralwidget)
        self.showButton.setGeometry(QtCore.QRect(430, 450, 131, 41))
        self.showButton.setStyleSheet(stylesheet_showButton)
        self.showButton.setObjectName("showButton")

        """Build Tour"""
        stylesheet_tourButton = config_reader.read_config("main_window.stylesheets.tourButton")
        self.tourButton = QtWidgets.QPushButton(self.centralwidget)
        self.tourButton.setGeometry(QtCore.QRect(300, 400, 331, 41))
        self.tourButton.setToolTip("Click here to build path")
        self.tourButton.setStyleSheet(stylesheet_tourButton)
        self.tourButton.setObjectName("tourButton")

        """off/on music"""
        stylesheet_radioButton = config_reader.read_config("main_window.stylesheets.radioButton")
        self.radioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton.setGeometry(QtCore.QRect(780, 10, 100, 20))
        self.radioButton.setObjectName("radioButton")
        self.radioButton.setToolTip("Do you want to listen the radio?")
        self.radioButton.setStyleSheet(stylesheet_radioButton)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_weather.setText(_translate("MainWindow", " "))
        self.pathButton.setText(_translate("MainWindow", "Path"))
        self.tourButton.setText(_translate("MainWindow", "Tour"))
        self.radioButton.setText(_translate("MainWindow", "RadioButton"))
        self.showButton.setText(_translate("MainWindow", "Show"))
        self.label_distance.setText(_translate("MainWindow", " "))
        self.label_price.setText(_translate("MainWindow", " "))
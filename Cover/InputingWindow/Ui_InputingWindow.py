from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *
from Core.ConfigReader import ConfigReader

class Ui_InputingWindow(object):

    def setupUi(self, InputingWindow):
        InputingWindow.setObjectName("InputingWindow")
        InputingWindow.resize(900, 900)

        QToolTip.setFont(QFont('Times', 14))
        self.centralwidget = QtWidgets.QWidget(InputingWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.setWindowTitle("InputingWindow")

        config_reader = ConfigReader()

        """CloseButton"""
        stylesheet_closebutton = config_reader.read_config("inputing_window.stylesheets.close_button")
        self.closebutton = QtWidgets.QPushButton(self)
        self.closebutton.setObjectName("closebutton")
        self.closebutton.setText("Close")
        self.closebutton.setToolTip("Has the choice been made?")
        self.closebutton.setStyleSheet(stylesheet_closebutton)

        """lineEdit for inputing countries"""
        stylesheet_lineEdit_countries = config_reader.read_config("inputing_window.stylesheets.lineEdit_countries")
        self.lineEdit_countries = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_countries.setGeometry(QtCore.QRect(200, 370, 570, 41))
        self.lineEdit_countries.setAutoFillBackground(False)
        self.lineEdit_countries.setStyleSheet(stylesheet_lineEdit_countries)
        self.lineEdit_countries.setObjectName("lineEdit_countries")
        self.lineEdit_countries.setToolTip("Input the set of countries: (Country1, City1), (...)")

        """lineEdit for inputing markers"""
        stylesheet_lineEdit_markers = config_reader.read_config("inputing_window.stylesheets.lineEdit_markers")
        self.lineEdit_markers = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_markers.setGeometry(QtCore.QRect(430, 420, 281, 41))
        self.lineEdit_markers.setAutoFillBackground(False)
        self.lineEdit_markers.setStyleSheet(stylesheet_lineEdit_markers)
        self.lineEdit_markers.setObjectName("lineEdit_markers")
        self.lineEdit_markers.setToolTip("Here you can input the marker's color")

        color_list = ["red", "blue", "black", "green", "purple",
                      "yellow", "orange", "white",
                      "brown", "gray", "pink", "Red", "Blue", 'Black', 'Green', 'Purple',
                      "Yellow", "Orange", "White", "Brown", "Gray", "Pink"]

        colors = QCompleter(color_list, self.lineEdit_markers)
        self.lineEdit_markers.setCompleter(colors)

        """lineEdit for inputing kinds of map"""
        stylesheet_lineEdit_map = config_reader.read_config("inputing_window.stylesheets.lineEdit_map")
        self.lineEdit_map = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_map.setGeometry(QtCore.QRect(430, 470, 281, 41))
        self.lineEdit_map.setAutoFillBackground(False)
        self.lineEdit_map.setStyleSheet( stylesheet_lineEdit_map)
        self.lineEdit_map.setObjectName("lineEdit_map")
        self.lineEdit_map.setToolTip("Here you can input the type of map: "
                                   "Open street map,MapQuest Open Aerial, Mapbox Bright,Stamen Terrain, "
                                   "Stamen Toner, Stamen Watercolor,CartoDB Positron, CartoDB Dark Matter")

        strList = ["Open street map", "MapQuest Open Aerial", "Mapbox Bright",
                   "Stamen Terrain", "Stamen Toner", "Stamen Watercolor",
                   "CartoDB Positron", "CartoDB dark_matter"]

        completer = QCompleter(strList, self.lineEdit_map)
        self.lineEdit_map.setCompleter(completer)

        """label 1"""
        stylesheet_label_1 = config_reader.read_config("inputing_window.stylesheets.label_1")
        self.label_1 = QtWidgets.QLabel(self.centralwidget)
        self.label_1.setGeometry(QtCore.QRect(270, 420, 181, 41))
        self.label_1.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_1.setObjectName("label_1")
        self.label_1.setStyleSheet(stylesheet_label_1)

        """label 2"""
        stylesheet_label_2 = config_reader.read_config("inputing_window.stylesheets.label_2")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(290, 470, 181, 41))
        self.label_2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_2.setObjectName("label_2")
        self.label_2.setStyleSheet(stylesheet_label_2)

        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.addWidget(self.closebutton)

        self.statusbar = QtWidgets.QStatusBar(InputingWindow)
        self.statusbar.setObjectName("statusbar")
        InputingWindow.setStatusBar(self.statusbar)

        InputingWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi3(InputingWindow)
        QtCore.QMetaObject.connectSlotsByName(InputingWindow)

    def retranslateUi3(self, InputingWindow):
        _translate = QtCore.QCoreApplication.translate
        InputingWindow.setWindowTitle(_translate("InputingWindow", "InputingWindow"))
        self.label_1.setText(_translate("InputingWindow", "Marker's color is: "))
        self.label_2.setText(_translate("InputingWindow", "Map's type is: "))
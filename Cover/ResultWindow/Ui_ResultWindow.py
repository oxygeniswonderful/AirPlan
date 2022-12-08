from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *
from Core.ConfigReader import ConfigReader

class Ui_ResultWindow(object):

    def setupUi(self, ResultWindow):
        ResultWindow.setObjectName("ResultWindow")
        ResultWindow.resize(900, 900)

        QToolTip.setFont(QFont('Times', 14))
        self.centralwidget = QtWidgets.QWidget(ResultWindow)
        self.centralwidget.setObjectName("centralwidget")

        config_reader = ConfigReader()

        """Close Button"""
        stylesheet_closebutton = config_reader.read_config("result_window.stylesheets.closeButton")
        self.closebutton = QtWidgets.QPushButton(self)
        self.closebutton.setObjectName("closebutton")
        self.closebutton.setText("Close")
        self.closebutton.setToolTip("Has the choice been made?")
        self.closebutton.setStyleSheet(stylesheet_closebutton)

        """label City from"""
        stylesheet_label_city_from = config_reader.read_config("result_window.stylesheets.label_city_from")
        self.label_city_from = QtWidgets.QLabel(self.centralwidget)
        self.label_city_from.setGeometry(QtCore.QRect(585, 10, 101, 41))
        self.label_city_from.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_city_from.setStyleSheet("font: 20pt \"Times\";")
        self.label_city_from.setObjectName("label_city_from")
        self.label_city_from.setStyleSheet(stylesheet_label_city_from)

        """label City to"""
        stylesheet_label_city_to = config_reader.read_config("result_window.stylesheets.label_city_to")
        self.label_city_to = QtWidgets.QLabel(self.centralwidget)
        self.label_city_to.setGeometry(QtCore.QRect(595, 60, 101, 41))
        self.label_city_to.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_city_to.setStyleSheet("font: 20pt \"Times\";")
        self.label_city_to.setObjectName("label_city_to")
        self.label_city_to.setStyleSheet(stylesheet_label_city_to)

        """label Priority"""
        stylesheet_label_priority = config_reader.read_config("result_window.stylesheets.label_priority")
        self.label_priority = QtWidgets.QLabel(self.centralwidget)
        self.label_priority.setGeometry(QtCore.QRect(600, 110, 101, 41))
        self.label_priority.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_priority.setStyleSheet("font: 20pt \"Times\";")
        self.label_priority.setObjectName("label_priority")
        self.label_priority.setStyleSheet(stylesheet_label_priority)

        """label Markers"""
        stylesheet_label_markers = config_reader.read_config("result_window.stylesheets.label_markers")
        self.label_markers = QtWidgets.QLabel(self.centralwidget)
        self.label_markers.setGeometry(QtCore.QRect(540, 160, 131, 41))
        self.label_markers.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_markers.setStyleSheet("font: 20pt \"Times\";")
        self.label_markers.setObjectName("label_markers")
        self.label_markers.setStyleSheet(stylesheet_label_markers)

        """label Map"""
        stylesheet_label_map = config_reader.read_config("result_window.stylesheets.label_map")
        self.label_map = QtWidgets.QLabel(self.centralwidget)
        self.label_map.setGeometry(QtCore.QRect(570, 210, 101, 41))
        self.label_map.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_map.setStyleSheet("font: 20pt \"Times\";")
        self.label_map.setObjectName("label_map")
        self.label_map.setStyleSheet(stylesheet_label_map)

        """lineEdit City from"""
        stylesheet_lineEdit_city_from = config_reader.read_config("result_window.stylesheets.lineEdit_city_from")
        self.lineEdit_city_from = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_city_from.setGeometry(QtCore.QRect(680, 10, 201, 41))
        self.lineEdit_city_from.setAutoFillBackground(False)
        self.lineEdit_city_from.setStyleSheet(stylesheet_lineEdit_city_from)
        self.lineEdit_city_from.setObjectName("lineEdit_city_from")
        self.lineEdit_city_from.setToolTip("Here you can input city from: Country, City")

        """lineEdit City to"""
        stylesheet_lineEdit_city_to = config_reader.read_config("result_window.stylesheets.lineEdit_city_to")
        self.lineEdit_city_to = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_city_to.setGeometry(QtCore.QRect(680, 60, 201, 41))
        self.lineEdit_city_to.setAutoFillBackground(False)
        self.lineEdit_city_to.setStyleSheet(stylesheet_lineEdit_city_to)
        self.lineEdit_city_to.setObjectName("lineEdit_city_to")
        self.lineEdit_city_to.setToolTip("Here you can input city to: Country, City")

        """lineEdit Priority"""
        stylesheet_lineEdit_priority = config_reader.read_config("result_window.stylesheets.lineEdit_priority")
        self.lineEdit_priority = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_priority.setGeometry(QtCore.QRect(680, 110, 201, 41))
        self.lineEdit_priority.setAutoFillBackground(False)
        self.lineEdit_priority.setStyleSheet(stylesheet_lineEdit_priority)
        self.lineEdit_priority.setObjectName("lineEdit_priority")
        self.lineEdit_priority.setToolTip("Here you can input priority")
        priority = ["time", "money"]
        pr = QCompleter(priority, self.lineEdit_priority)
        self.lineEdit_priority.setCompleter(pr)

        """lineEdit Markers"""
        stylesheet_lineEdit_markers = config_reader.read_config("result_window.stylesheets.lineEdit_markers")
        self.lineEdit_markers = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_markers.setGeometry(QtCore.QRect(680, 160, 201, 41))
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

        """lineEdit Map"""
        stylesheet_lineEdit_map = config_reader.read_config("result_window.stylesheets.lineEdit_map")
        self.lineEdit_map = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_map.setGeometry(QtCore.QRect(680, 210, 201, 41))
        self.lineEdit_map.setAutoFillBackground(False)
        self.lineEdit_map.setStyleSheet(stylesheet_lineEdit_map)
        self.lineEdit_map.setObjectName("lineEdit_map")
        self.lineEdit_map.setToolTip("Here you can input the type of map: "
                                   "Open street map,MapQuest Open Aerial, Mapbox Bright,Stamen Terrain, "
                                   "Stamen Toner, Stamen Watercolor,CartoDB Positron, CartoDB Dark Matter")

        strList = ["Open street map", "MapQuest Open Aerial", "Mapbox Bright",
                   "Stamen Terrain", "Stamen Toner", "Stamen Watercolor",
                   "CartoDB Positron", "CartoDB dark_matter"]

        completer = QCompleter(strList, self.lineEdit_map)
        self.lineEdit_map.setCompleter(completer)

        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.addWidget(self.closebutton)

        self.statusbar = QtWidgets.QStatusBar(ResultWindow)
        self.statusbar.setObjectName("statusbar")
        ResultWindow.setStatusBar(self.statusbar)

        ResultWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi2(ResultWindow)
        QtCore.QMetaObject.connectSlotsByName(ResultWindow)

    def retranslateUi2(self, ResultWindow):
        _translate = QtCore.QCoreApplication.translate
        ResultWindow.setWindowTitle(_translate("ResultWindow", "ResultWindow"))
        self.label_city_from.setText(_translate("ResultWindow", "City from: "))
        self.label_city_to.setText(_translate("ResultWindow", "City to: "))
        self.label_priority.setText(_translate("ResultWindow", "Priority: "))
        self.label_markers.setText(_translate("ResultWindow", "Marker's color: "))
        self.label_map.setText(_translate("ResultWindow", "Map's type: "))
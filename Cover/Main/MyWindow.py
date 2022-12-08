import pygame
from PyQt5.QtWidgets import *
from Cover.InputingWindow.InputingWindow import InputingWindow
from Cover.Main.Ui_MainWindow import Ui_MainWindow
from Cover.ResultWindow.ResultWindow import ResultWindow
from Core.ConfigReader import ConfigReader

class MyWindow(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(MyWindow, self).__init__()

        self.setupUi(self)
        self.setWindowTitle("Main menu")

        self.pathButton.clicked.connect(self.openDialog)
        self.showButton.clicked.connect(self.print_weather_city)
        self.tourButton.clicked.connect(self.openDialog2)
        self.radioButton.clicked.connect(self.music)
        self.radioButton.setChecked(True)
        self.showButton.clicked.connect(self.print_cost)
        self.showButton.clicked.connect(self.print_distance)

        self.config_reader = ConfigReader()

    def openDialog(self):
        self.dialog = ResultWindow(self)
        self.dialog.show()

    def openDialog2(self):
        self.dialog2 = InputingWindow(self)
        self.dialog2.show()

    def print_weather_city(self):
        super(Ui_MainWindow, self).__init__()

        filename = self.config_reader.read_config("tmp.lines1")
        file = open(filename, "r")
        c = 0
        for line in file:
            if c == 0:
                temperature = float(line)
                self.label_weather.setText(f"Weather at your destination is: {temperature}")
            c += 1

    def music(self):
        radioButton = self.sender()
        music = self.config_reader.read_config("main_window.music")
        pygame.mixer.init()
        pygame.mixer.music.load(music)
        pygame.mixer.music.play(-1)
        if radioButton.isChecked():
            pygame.mixer.music.pause()

    def print_cost(self):
        filename = self.config_reader.read_config("tmp.lines2")
        file = open(filename, "r")
        for line in file:
            cost = float(line)
            self.label_price.setText(f"Cost : {cost}" + " $")

    def print_distance(self):
        filename = self.config_reader.read_config("tmp.lines3")
        file = open(filename, "r")
        for line in file:
            distance = float(line)
            self.label_distance.setText(f"Total distance: : {distance}" + " km")
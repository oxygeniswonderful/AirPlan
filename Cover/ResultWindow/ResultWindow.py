import pyowm
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
import webbrowser

from Algoritms.BuildingGraph import BuildingGraph
from Cover.ResultWindow.Ui_ResultWindow import Ui_ResultWindow
from Core.ConfigReader import ConfigReader


class ResultWindow(QMainWindow, Ui_ResultWindow):

    def __init__(self, parent=None):
        super(ResultWindow, self).__init__(parent)

        self.setupUi(self)
        self.setWindowTitle("ResultWindow")

        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.addWidget(self.closebutton)

        self.closebutton.clicked.connect(self.btnClosed)
        self.closebutton.clicked.connect(self.get_result)
        self.closebutton.clicked.connect(self.get_weather_city)

        self.config_reader = ConfigReader()

    def init_priority(self):
        priority = self.lineEdit_priority.text()
        return priority

    def init_type_of_map(self):
        type_of_map = self.lineEdit_map.text()
        return type_of_map

    def init_color_of_markers(self):
        color_of_markers = self.lineEdit_markers.text()
        return color_of_markers

    def get_result(self):
        map_html = self.config_reader.read_config("tmp.FeatureGroup")
        self.color = self.init_color_of_markers()
        self.type_of_map = self.init_type_of_map()
        self.priority = self.init_priority()
        all_dates = BuildingGraph(self.color, self.type_of_map, self.priority)
        city_from = self.lineEdit_city_from.text()
        city_to = self.lineEdit_city_to.text()
        l = "(" + city_from + ")," + " " + "(" + city_to + ")"
        line = list(map(str, l.split('), ')))
        if len(line) == 2:
            s = line[0][1:]
            city_from = list(map(str, s.split(', ')))
            s = line[1][1:-1]
            city_to = list(map(str, s.split(', ')))
        m = all_dates.dijkstra(city_from, city_to)
        webbrowser.open(map_html, new = 2)

    def btnClosed(self):
        self.close()

    def init_city(self):
        city_to = self.lineEdit_city_to.text()
        filename = self.config_reader.read_config("tmp.lines1")
        file = open(filename, "w")
        file.write(city_to + "\n")
        file.close()

    def get_weather_city(self):
        super(Ui_ResultWindow, self).__init__()

        filename = self.config_reader.read_config("tmp.lines1")
        file = open(filename, "w")
        owm = pyowm.OWM("ba791ca513afc4f135cdc07cbe59815b")
        s = self.lineEdit_city_to.text()
        city_to = s.split(",")[1]
        observation = owm.weather_manager().weather_at_place(city_to)
        w = observation.weather
        temperature = w.temperature('celsius')['temp']
        file.write(str(temperature) + "\n")
        file.close()
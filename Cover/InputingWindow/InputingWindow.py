import webbrowser
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from Algoritms.BuildingGraph import BuildingGraph
from Cover.InputingWindow.Ui_InputingWindow import Ui_InputingWindow
from Core.ConfigReader import ConfigReader


class InputingWindow(QMainWindow, Ui_InputingWindow):

    def __init__(self, parent=None):
        super(InputingWindow, self).__init__(parent)

        self.setupUi(self)
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.addWidget(self.closebutton)

        self.closebutton.clicked.connect(self.btnClosed)
        self.closebutton.clicked.connect(self.build_tsp)

    def btnClosed(self):
        self.close()

    def build_tsp(self):
        config_reader = ConfigReader()
        map_html = config_reader.read_config("tmp.FeatureGroup")
        color_of_markers = self.lineEdit_markers.text()
        type_of_map = self.lineEdit_map.text()
        all_dates = BuildingGraph(color_of_markers, type_of_map, "")
        self.points = self.lineEdit_countries.text()
        line = list(map(str, self.points.split('), ')))
        countries = []
        for i in range(len(line)):
            s = str(line[i][1:])
            if i == len(line) - 1:
                s = s[:-1]
            countries.append(list(map(str, s.split(', '))))
        m = all_dates.tsp(countries)
        webbrowser.open(map_html, new=2)

    def init_points(self):
        self.points = self.lineEdit_countries.text()
        return self.points
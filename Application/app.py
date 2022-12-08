import sys
from PyQt5 import QtWidgets
from Cover.Main.MyWindow import MyWindow
from Cover.Main.Ui_MainWindow import Ui_MainWindow
from Core.ConfigReader import ConfigReader


if __name__ == "__main__":

    """Set Stylesheet"""
    config_reader = ConfigReader()
    stylesheet = config_reader.read_config("fon.fon_stylesheet")
    fon_path = config_reader.read_config("fon.fon_path")
    stylesheet = stylesheet.replace("{}", fon_path)

    """Create application"""
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(stylesheet)

    """init"""
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    wonder = MyWindow()
    wonder.show()

    """Main loop"""
    sys.exit(app.exec_())
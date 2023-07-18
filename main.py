import sys
from PySide2.QtWidgets import QApplication
from PlotWidget import PlotWidget

if __name__ == "__main__":
    app = QApplication(sys.argv)
    PlotWidget = PlotWidget()
    PlotWidget.show()
    sys.exit(app.exec_())

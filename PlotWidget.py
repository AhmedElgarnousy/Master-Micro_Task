from PySide2.QtGui import QFont, QColor
from PySide2.QtCore import Slot
from PySide2.QtWidgets import (
    QLabel,
    QMessageBox,
    QPushButton,
    QWidget,
    QDoubleSpinBox,
    QGridLayout,
    QHBoxLayout,
    QLineEdit
)
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
import numpy as np
from utils import string_to_function

class PlotWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Function Plotter")

        # Create widgets
        self.canvas = FigureCanvas(Figure(figsize=(15, 10)))
        self.axes = self.canvas.figure.subplots()
        self.toolbar = NavigationToolbar2QT(self.canvas, self)

        # Min and max values of x
        self.min_x_input = QDoubleSpinBox()
        self.max_x_input = QDoubleSpinBox()

        self.min_x_input.setPrefix("min x: ")
        self.max_x_input.setPrefix("max x: ")

        self.min_x_input.setRange(-10, 10)
        self.min_x_input.setValue(-10)
        self.max_x_input.setValue(10)

        # Function input
        self.function_input = QLineEdit()

        self.function_label = QLabel(text="Enter the function: ")

        # Plot button
        self.plot_button = QPushButton(text="Plot")
        self.plot_button.setStyleSheet(
            "QPushButton { background-color: #007BFF; color: white; font-size: 14px; }")
        # Create layout
        grid_layout = QGridLayout()
        grid_layout.addWidget(self.function_label, 0, 0)
        grid_layout.addWidget(self.function_input, 0, 1)
        mnAndMx_layout = QHBoxLayout()
        mnAndMx_layout.addWidget(self.min_x_input)
        mnAndMx_layout.addWidget(self.max_x_input)
        grid_layout.addLayout(mnAndMx_layout,1, 0, 1, 2) 
        grid_layout.addWidget(self.toolbar, 2, 0, 1, 2)
        grid_layout.addWidget(self.canvas, 3, 0, 1, 2)
        grid_layout.addWidget(self.plot_button, 4, 0,1,2)
        self.setLayout(grid_layout)

        self.error_dialog = QMessageBox()

        # Connect inputs with on_change method
        self.min_x_input.valueChanged.connect(lambda _: self.on_input_change(1))
        self.max_x_input.valueChanged.connect(lambda _: self.on_input_change(2))
        self.plot_button.clicked.connect(lambda _: self.on_plot_button_clicked())

        self.update_plot()

    @Slot()
    def on_input_change(self, idx): 
        """Update the plot with the current input values"""
        min_x = self.min_x_input.value()
        max_x = self.max_x_input.value()

        # Warning: min x can't be greater than or equal to max x
        if idx == 1 and min_x >= max_x:
            self.min_x_input.setValue(max_x - 1)
            self.show_error_dialog("x limits Error!", "'min x' should be less than 'max x'.")
            return

        # Warning: max x can't be less than or equal to min x
        if idx == 2 and max_x <= min_x:
            self.max_x_input.setValue(min_x + 1)
            self.show_error_dialog("x limits Error!", "'max x' should be greater than 'min x'.")
            return

        self.update_plot()

    def on_plot_button_clicked(self):
        self.update_plot()

    def update_plot(self):
        min_x = self.min_x_input.value()
        max_x = self.max_x_input.value()

        x = np.linspace(min_x, max_x)
        try:
            y = string_to_function(self.function_input.text())(x)
        except ValueError as e:
            self.show_error_dialog("Function Error!", str(e))
            return

        self.axes.clear()
        self.axes.plot(x, y)
        self.canvas.draw()

    def show_error_dialog(self, title, message):
        self.error_dialog.setWindowTitle(title)
        self.error_dialog.setText(message)
        self.error_dialog.show()

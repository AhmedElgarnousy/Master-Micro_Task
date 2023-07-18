import pytest
import sys
from PySide2.QtWidgets import QApplication
from PySide2.QtTest import QTest
from PySide2.QtCore import Qt
from PlotWidget import PlotWidget

@pytest.fixture(scope='module')
def app():
    app = QApplication([])
    yield app
    app.quit()

def test_plotting_function(app):
    # Create the widget and show it
    widget = PlotWidget()

    # Set up the function and range values
    widget.function_input.setText("x**2")
    widget.min_x_input.setValue(-5)
    widget.max_x_input.setValue(5)

    # Click the plot button
    QTest.mouseClick(widget.plot_button, Qt.LeftButton)

    # Ensure the plot is displayed correctly
    assert len(widget.axes.lines) == 1
    assert len(widget.axes.lines[0].get_xdata()) > 0
    assert len(widget.axes.lines[0].get_ydata()) > 0

def test_invalid_function(app):
    # Create the widget and show it
    widget = PlotWidget()

    # Set up an invalid function
    widget.function_input.setText("2*x + ")

    # Click the plot button
    QTest.mouseClick(widget.plot_button, Qt.LeftButton)

    # Ensure an error dialog is shown
    assert widget.error_dialog.isVisible()
    assert widget.error_dialog.text() == "Function Error!"

def test_x_limits_error(app):
    # Create the widget and show it
    widget = PlotWidget()

    # Set up invalid x limits
    widget.min_x_input.setValue(10)
    widget.max_x_input.setValue(5)

    # Click the plot button
    QTest.mouseClick(widget.plot_button, Qt.LeftButton)

    # Ensure an error dialog is shown
    assert widget.error_dialog.isVisible()
    assert widget.error_dialog.text() == "x limits Error!"

def test_plot_button_disabled(app):
    # Create the widget and show it
    widget = PlotWidget()

    # Check that the plot button is initially disabled
    assert not widget.plot_button.isEnabled()

    # Set up a valid function to enable the plot button
    widget.function_input.setText("x**2")

    # Check that the plot button is now enabled
    assert widget.plot_button.isEnabled()

def test_plot_button_enabled_after_invalid_function(app):
    # Create the widget and show it
    widget = PlotWidget()

    # Set up an invalid function to disable the plot button
    widget.function_input.setText("2*x + ")

    # Check that the plot button is disabled
    assert not widget.plot_button.isEnabled()

    # Set up a valid function to enable the plot button
    widget.function_input.setText("x**2")

    # Check that the plot button is now enabled
    assert widget.plot_button.isEnabled()

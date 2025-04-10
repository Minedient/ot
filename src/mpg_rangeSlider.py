from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSlider, QLabel, QApplication, QStyleOptionSlider
from PySide6.QtCore import Qt, Signal, QPointF, QRectF, QSize
from PySide6.QtGui import QPainter, QPen, QColor, QBrush, QFont


class RangeSlider(QWidget):
    """
    A custom QWidget that implements a range slider

    A range slider allows the user to select a range of values by dragging two handles along a track.
    By default, the range slider is horizontal, but it can be set to vertical mode.
    When the user drag the slider, it will change the values of the slider returned and emit a signal called valuesChanged with the selected values. 
    When the user drag either end of the slider while holding shift, it will change the range of the slider selected. So the user can select a different range of values.
    A rangeChanged signal is also emitted during such operation.

    The range slider has a minimum and maximum value, which can be set using the setRange method.
    """
    rangeChanged = Signal(int, int, name="rangeChanged")
    valuesChanged = Signal(int, int, name="valuesChanged")

    def __init__(self, parent=None, width = 300, height = 50, startValue=0, endValue=100, defaultRange=(0,10)):
        super().__init__(parent)
        self.setMinimumSize(width, height)
        self.startValue = startValue
        self.endValue = endValue
        self.range = defaultRange
        self.sos = QStyleOptionSlider()

    def setGlobalRange(self, startValue, endValue):
        """
        Set the global range of the slider.
        """
        self.startValue = startValue
        self.endValue = endValue
        self.update()

    def setRange(self, startValue, endValue):
        """
        Set the range of the slider.
        """
        self.range = (startValue, endValue)
        self.update()
        self.rangeChanged.emit(self.range)

    def mouseMoveEvent(self, event):
        return super().mouseMoveEvent(event)


    
'''
 *  Original code from https://github.com/nlamprian/pyqt5-led-indicator-widget/tree/master
'''

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from dataclasses import dataclass
from enum import Enum, auto


class LedColor(Enum):
    GREEN = auto()
    RED = auto()
    YELLOW = auto()


@dataclass
class _LedColor:
    on_color_1: QColor
    on_color_2: QColor
    off_color_1: QColor
    off_color_2: QColor


_possible_LedColor = {
    LedColor.GREEN : _LedColor(QColor(0, 255, 0), QColor(0, 192, 0), QColor(0, 28, 0), QColor(0, 128, 0)),
    LedColor.RED   : _LedColor(QColor(255, 0, 0), QColor(176, 0, 0), QColor(28, 0, 0), QColor(156, 0, 0)),
    LedColor.YELLOW: _LedColor(QColor(255, 255, 0), QColor(192, 192, 0), QColor(28, 28, 0), QColor(128, 128, 0)),

}



class LedIndicator(QAbstractButton):
    # scaledSize = 1000.0

    def __init__(self, parent=None, changeOnClick = False, scale = 1.0):
        QAbstractButton.__init__(self, parent)

        self.setMinimumSize(24, 24)
        self.setCheckable(True)
        self.setDisabled(not changeOnClick)

        # Green
        self.on_color_1 = QColor(0, 255, 0)
        self.on_color_2 = QColor(0, 192, 0)
        self.off_color_1 = QColor(0, 28, 0)
        self.off_color_2 = QColor(0, 128, 0)

        self.scaledSize = 1000.0 + 1000.0 * (1 - scale)

    def resizeEvent(self, QResizeEvent):
        self.update()

    def paintEvent(self, QPaintEvent):
        realSize = min(self.width(), self.height())

        painter = QPainter(self)
        pen = QPen(Qt.black)
        pen.setWidth(1)

        painter.setRenderHint(QPainter.Antialiasing)
        painter.translate(self.width() / 2, self.height() / 2)
        painter.scale(realSize / self.scaledSize, realSize / self.scaledSize)

        gradient = QRadialGradient(QPointF(-500, -500), 1500, QPointF(-500, -500))
        gradient.setColorAt(0, QColor(224, 224, 224))
        gradient.setColorAt(1, QColor(28, 28, 28))
        painter.setPen(pen)
        painter.setBrush(QBrush(gradient))
        painter.drawEllipse(QPointF(0, 0), 500, 500)

        gradient = QRadialGradient(QPointF(500, 500), 1500, QPointF(500, 500))
        gradient.setColorAt(0, QColor(224, 224, 224))
        gradient.setColorAt(1, QColor(28, 28, 28))
        painter.setPen(pen)
        painter.setBrush(QBrush(gradient))
        painter.drawEllipse(QPointF(0, 0), 450, 450)

        painter.setPen(pen)
        if self.isChecked():
            gradient = QRadialGradient(QPointF(-500, -500), 1500, QPointF(-500, -500))
            gradient.setColorAt(0, self.on_color_1)
            gradient.setColorAt(1, self.on_color_2)
        else:
            gradient = QRadialGradient(QPointF(500, 500), 1500, QPointF(500, 500))
            gradient.setColorAt(0, self.off_color_1)
            gradient.setColorAt(1, self.off_color_2)

        painter.setBrush(gradient)
        painter.drawEllipse(QPointF(0, 0), 400, 400)

    def changeStatus(self):
        self.setChecked(not self.isChecked())

    def setStatus(self, status: bool):
        self.setChecked(status)

    def setColor(self, color : LedColor):
        _color = _possible_LedColor[color]
        self.on_color_1 = _color.on_color_1
        self.on_color_2 = _color.on_color_2
        self.off_color_1 = _color.off_color_1
        self.off_color_2 = _color.off_color_2



    @Property(QColor)
    def onColor1(self):
        return self.on_color_1

    @onColor1.setter
    def onColor1(self, color):
        self.on_color_1 = color

    @Property(QColor)
    def onColor2(self):
        return self.on_color_2

    @onColor2.setter
    def onColor2(self, color):
        self.on_color_2 = color

    @Property(QColor)
    def offColor1(self):
        return self.off_color_1

    @offColor1.setter
    def offColor1(self, color):
        self.off_color_1 = color

    @Property(QColor)
    def offColor2(self):
        return self.off_color_2

    @offColor2.setter
    def offColor2(self, color):
        self.off_color_2 = color
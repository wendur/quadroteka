import random
import sys
from QuadroGame import *

from PyQt5.QtCore import Qt, QRect, QRectF, QPointF, QPoint
from PyQt5.QtGui import QColor, QPainter, QBrush, QFont, QTextOption, QGradient, QLinearGradient
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class PyQtGame(QWidget):
    def __init__(self):
        super(PyQtGame, self).__init__()
        self.game = QuadroGame(5)
        self.colors = {
            1: QColor(0xFF0000),
            2: QColor(0xFFFF00),
            3: QColor(0x00FF00),
            4: QColor(0x00FFFF),
            5: QColor(0xFF00FF)
        }
        self.initUI()

    def initUI(self):
        self.setFixedSize(650, 500)
        self.centerWindow()
        self.setWindowTitle("Quadroteka")
        self.show()

    def centerWindow(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Up:
            self.game.up()
        elif e.key() == Qt.Key_Down:
            self.game.down()
        elif e.key() == Qt.Key_Left:
            self.game.left()
        elif e.key() == Qt.Key_Right:
            self.game.right()
        elif e.key() == Qt.Key_Z:
            self.game.counter_clockwise()
        elif e.key() == Qt.Key_X:
            self.game.clockwise()
        elif e.key() == Qt.Key_R:
            self.game.reset_game()
        self.update()

    def mousePressEvent(self, e):
        self.last_point = e.pos()

    def mouseReleaseEvent(self, e):
        self.shuffleRect = QRect(480, 175, 80, 20)
        if self.shuffleRect.contains(e.pos().x(), e.pos().y()) \
                and self.shuffleRect.contains(self.last_point.x(), self.last_point.y()):
            self.game.reset_game()
            self.update()

        self.upLevelRect = QRect(560, 340, 10, 20)
        if self.upLevelRect.contains(e.pos().x(), e.pos().y()) \
                and self.upLevelRect.contains(self.last_point.x(), self.last_point.y()):
            if self.game.level < 4:
                self.game.level += 1
                self.game.reset_game()
            self.update()

        self.downLevelRect = QRect(530, 340, 10, 20)
        if self.downLevelRect.contains(e.pos().x(), e.pos().y()) \
                and self.downLevelRect.contains(self.last_point.x(), self.last_point.y()):
            if self.game.level > 1:
                self.game.level -= 1
                self.game.reset_game()
            self.update()

        self.stayRect = QRect(150, 180, 50, 30)
        self.nextRect = QRect(210, 180, 120, 30)
        if self.game.win_cond:
            if self.stayRect.contains(e.pos().x(), e.pos().y()) \
                    and self.stayRect.contains(self.last_point.x(), self.last_point.y()):
                self.game.reset_game()

            if self.game.level != 4:
                if self.nextRect.contains(e.pos().x(), e.pos().y()) \
                        and self.nextRect.contains(self.last_point.x(), self.last_point.y()):
                    if self.game.level < 4:
                        self.game.level += 1
                    self.game.reset_game()
            self.update()

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setPen(Qt.NoPen)

        painter.setBrush(QBrush(QColor(0xFFFFFF)))
        painter.drawRect(self.rect())

        painter.setBrush(QBrush(QColor(0x999999)))
        painter.drawRoundedRect(QRect(20, 20, 600, 450), 10, 10)

        painter.setFont(QFont("Franklin Gothic Medium", 18))
        painter.setPen(QColor(0xFFFFFF))
        painter.drawText(QRectF(QRect(450, 100, 160, 40)), "Quarda 2.0", QTextOption(Qt.AlignLeft))
        painter.setPen(Qt.NoPen)

        painter.setFont(QFont("Franklin Gothic Medium", 16))
        painter.setPen(QColor(0xffffff))
        painter.drawText(QRectF(QRect(480, 175, 80, 20)), "Shuffle", QTextOption(Qt.AlignLeft | Qt.AlignVCenter))

        painter.drawText(QRectF(QRect(440, 250, 80, 20)), "Moves", QTextOption(Qt.AlignLeft))
        painter.drawText(QRectF(QRect(520, 250, 60, 20)), str(self.game.moves), QTextOption(Qt.AlignHCenter))

        painter.drawText(QRectF(QRect(440, 280, 80, 20)), "Turns", QTextOption(Qt.AlignLeft))
        painter.drawText(QRectF(QRect(520, 280, 60, 20)), str(self.game.turns), QTextOption(Qt.AlignHCenter))

        painter.drawText(QRectF(QRect(440, 310, 80, 20)), "Colums", QTextOption(Qt.AlignLeft))
        painter.drawText(QRectF(QRect(520, 310, 60, 20)), str(self.game.colums), QTextOption(Qt.AlignHCenter))
        painter.drawText(QRectF(QRect(547, 310, 40, 20)), "/5", QTextOption(Qt.AlignHCenter))

        painter.drawText(QRectF(QRect(440, 340, 60, 20)), "Level", QTextOption(Qt.AlignLeft))
        painter.drawText(QRectF(QRect(530, 340, 10, 20)), "-", QTextOption(Qt.AlignLeft))
        painter.drawText(QRectF(QRect(540, 340, 20, 20)), str(self.game.level), QTextOption(Qt.AlignHCenter))
        painter.drawText(QRectF(QRect(560, 340, 10, 20)), "+", QTextOption(Qt.AlignLeft))
        painter.setPen(Qt.NoPen)

        self.drawRectangles(painter)

        if self.game.win_cond:
            painter.setBrush(QBrush(QColor(80, 80, 80, 150)))
            painter.drawRoundedRect(QRect(78, 88, 317, 317), 10, 10)

            painter.setFont(QFont("Franklin Gothic Medium", 35))
            painter.setPen(QColor(0xffffff))
            painter.drawText(QRectF(QRect(128, 130, 400, 50)), "YOU WIN!!!", QTextOption(Qt.AlignLeft))
            painter.setPen(Qt.NoPen)

            painter.setFont(QFont("Franklin Gothic Medium", 20))
            painter.setPen(QColor(0xffffff))
            painter.drawText(QRectF(QRect(150, 180, 50, 30)), "stay", QTextOption(Qt.AlignLeft))
            if self.game.level != 4:
                painter.drawText(QRectF(QRect(210, 180, 120, 30)), "next level", QTextOption(Qt.AlignLeft))
            painter.setPen(Qt.NoPen)
        else:
            painter.setBrush(QBrush(QColor(255, 255, 255, 150)))
            painter.drawRoundedRect(QRect(96+(self.game.center.x-1)*64, 106+(self.game.center.y-1)*64, 160, 160), 10, 10)

    def drawRectangles(self, painter):
        for i in range(self.game.size):
            for j in range(self.game.size):
                painter.setBrush(QColor(0, 0, 0))
                painter.drawRoundedRect(QRect(80 + j * 64, 90 + i * 64, 60, 60), 10, 10)

                painter.setBrush(self.colors[self.game.field[i][j]])
                painter.drawRoundedRect(QRect(82 + j * 64, 92 + i * 64, 56, 56), 10, 10)

                painter.setBrush(Qt.NoBrush)
                painter.setPen(Qt.NoPen)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = PyQtGame()
    sys.exit(app.exec_())


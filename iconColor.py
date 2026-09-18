from PyQt6.QtGui import QIcon, QPixmap, QPainter, QPalette
from PyQt6.QtCore import Qt


def colorIcon(path, color):
    source = QPixmap(path)

    result = QPixmap(source.size())
    result.fill(Qt.GlobalColor.transparent)

    painter = QPainter(result)
    painter.drawPixmap(0, 0, source)

    painter.setCompositionMode(
        QPainter.CompositionMode.CompositionMode_SourceIn
    )
    painter.fillRect(result.rect(), color)
    painter.end()

    return QIcon(result)
    
def colorPixmap(path, color):
    source = QPixmap(path)

    result = QPixmap(source.size())
    result.fill(Qt.GlobalColor.transparent)

    painter = QPainter(result)
    painter.drawPixmap(0, 0, source)

    painter.setCompositionMode(
        QPainter.CompositionMode.CompositionMode_SourceIn
    )
    painter.fillRect(result.rect(), color)
    painter.end()

    return result
    
def updateIcon(button, icon_path):
    color = button.palette().color(
        QPalette.ColorRole.ButtonText
    )
    button.setIcon(colorIcon(icon_path, color))
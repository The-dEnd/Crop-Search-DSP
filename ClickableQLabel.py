from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import pyqtSignal, Qt

class ClickQLabel(QLabel):
    clicked = pyqtSignal()  # Custom signal

    def __init__(self, parent=None):
        super().__init__(parent)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()  # Emit signal when clicked

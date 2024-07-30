import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt, QRect

class CornerMarker(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Corner Marker")
        self.setGeometry(100, 100, 200, 200)  # Initial position and size
        self.setFixedSize(200, 200)  # Fixed size to keep the window consistent
        self.setWindowFlags(Qt.FramelessWindowHint)  # Remove window decorations
        self.setAttribute(Qt.WA_TranslucentBackground)  # Make the background transparent
        self.show()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))  # Thin border
        painter.drawRect(QRect(0, 0, self.width() - 1, self.height() - 1))

    def moveEvent(self, event):
        self.print_corner_coordinates()

    def print_corner_coordinates(self):
        geo = self.geometry()
        top_left = (geo.x(), geo.y())
        top_right = (geo.x() + geo.width(), geo.y())
        bottom_left = (geo.x(), geo.y() + geo.height())
        bottom_right = (geo.x() + geo.width(), geo.y() + geo.height())
        print(f"Top Left: {top_left}, Top Right: {top_right}, Bottom Left: {bottom_left}, Bottom Right: {bottom_right}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CornerMarker()
    sys.exit(app.exec_())
# Import necessary modules
import sys

from PyQt5.QtWidgets import (QApplication, QGraphicsView, QGraphicsScene, QGraphicsRectItem)


# Create Objects class that defines the position property of
# instances of the class using pyqtProperty.


class SlamBoard(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.scene = None
        self.rect: QGraphicsRectItem = None
        self.initializeView()

    def initializeView(self):
        """
        Initialize the graphics view and display its contents
        to the screen.
        """
        self.setGeometry(100, 100, 700, 450)
        self.setWindowTitle('Whiteboard Test')
        # self.createObjects()
        self.setMouseTracking(True)
        self.createScene()
        # self.showMaximized()
        self.show()

    def mouseMoveEvent(self, event):
        pos = event.pos()
        self.rect.setX(pos.x())
        self.rect.setY(pos.y())

    def createScene(self):
        """
        Create the graphics scene and add Objects instances
        to the scene.
        """
        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(0, 0, 700, 450)
        self.rect = QGraphicsRectItem(10, 10, 40, 40)
        self.scene.addItem(self.rect)
        self.setScene(self.scene)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SlamBoard()
    sys.exit(app.exec_())

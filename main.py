# Import necessary modules
import sys
from typing import Optional

from PyQt5.QtGui import QPixmap, QColor, QIcon
from PyQt5.QtWidgets import (QApplication, QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsTextItem,
                             QMainWindow, qApp, QAction, QStyle, QLabel, QWidget, QSizePolicy)


# Create Objects class that defines the position property of
# instances of the class using pyqtProperty.

class SlamBoard(QGraphicsView):
    def __init__(self, parent):
        super().__init__()
        self.scene = None
        self.rect: Optional[QGraphicsRectItem] = None
        self.initializeView()
        self.parent = parent

    def initializeView(self):
        """
        Initialize the graphics view and display its contents
        to the screen.
        """
        self.setGeometry(100, 100, 1700, 1450)
        # self.createObjects()
        self.setMouseTracking(True)
        self.createScene()
        self.show()

    def mouseMoveEvent(self, event):
        pos = event.pos()
        self.rect.setX(pos.x())
        self.rect.setY(pos.y())
        # print(pos.x(), pos.y())

    def createScene(self):
        """
        Create the graphics scene and add Objects instances
        to the scene.
        """
        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(0, 0, 4000, 4000)
        self.rect = QGraphicsRectItem(0, 0, 120, 120)
        test_text = QGraphicsTextItem("Testing this is one")
        test_text.setParentItem(self.rect)
        test_text.setTextWidth(120)
        self.rect.setX(2000)
        self.rect.setY(2000)
        self.scene.addItem(self.rect)
        self.setScene(self.scene)


class mainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SlamBoard")
        self.slamboard = SlamBoard(self)

        # Create toolbar
        tb = self.addToolBar("Toolbar")

        # Create exit button from standard icon
        exit_pixmap = getattr(QStyle, "SP_DialogCancelButton")
        exit_icon = self.style().standardIcon(exit_pixmap)
        exit_action = QAction(exit_icon, "red", self)
        exit_action.setIcon(exit_icon)
        tb.addAction(exit_action)
        exit_action.triggered.connect(qApp.quit)

        tb.addSeparator()

        # Create some color icons to make them easy to select
        red_pixmap = QPixmap(40, 40)
        red_pixmap.fill(QColor("red"))
        red_icon = QIcon(red_pixmap)

        red_action = QAction(red_icon, "red", self)
        red_action.setIcon(red_icon)
        tb.addAction(red_action)
        red_action.triggered.connect(self.color_action)

        # Create an empty QWidget to fill out the space so the
        # coordinates show on the right
        filler = QWidget()
        filler.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        tb.addWidget(filler)

        # Create a couple of labels to hold x/y coordinates
        self.label_x = QLabel("X:", self)
        self.label_y = QLabel("Y:", self)

        tb.addSeparator()
        tb.addWidget(self.label_x)
        tb.addWidget(self.label_y)

        self.setCentralWidget(self.slamboard)
        self.showMaximized()
        self.show()

    def update_coords(self, x, y):
        self.labelx

    def color_action(self):
        # who sent the signal
        target = self.sender()
        color = target.text()
        print("Color:", color)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = mainWindow()
    sys.exit(app.exec_())

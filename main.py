# Import necessary modules
import sys
from typing import Optional

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QColor, QIcon, QPen
from PyQt5.QtWidgets import (QApplication, QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsTextItem,
                             QMainWindow, QAction, QStyle, QLabel, QWidget, QSizePolicy, qApp)


# Create Objects class that defines the position property of
# instances of the class using pyqtProperty.

class SlamBoard(QGraphicsView):
    def __init__(self, parent):
        super().__init__()
        self.scene = None
        self.rect: Optional[QGraphicsRectItem] = None
        self.rect_width = 1
        self.rect_color = "black"
        self.initializeView()
        self.parent = parent

    def initializeView(self):
        """
        Initialize the graphics view and display its contents
        to the screen.
        """
        self.setGeometry(100, 100, 1700, 1450)
        self.setMouseTracking(True)
        self.createScene()
        self.show()

    def mouseMoveEvent(self, event):
        pos = event.pos()
        # Convert coordinates to scene
        new_pos = self.mapToScene(pos)
        x, y = new_pos.x(), new_pos.y()
        self.parent.update_coords(x, y)
        self.rect.setX(x)
        self.rect.setY(y)
        # print(pos.x(), pos.y())

    def update_rect_pen(self):
        pen = QPen(QColor(self.rect_color))
        pen.setWidth(self.rect_width)
        self.rect.setPen(pen)

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_W:
            self.rect_width += 1
            if self.rect_width > 10:
                self.rect_width = 1
            self.update_rect_pen()

        print("Key:", event.key())

    def color_action(self, color):
        self.rect_color = color
        self.update_rect_pen()

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
        exit_action = QAction(exit_icon, "exit", self)
        exit_action.setIcon(exit_icon)
        tb.addAction(exit_action)
        exit_action.triggered.connect(qApp.exit)

        tb.addSeparator()

        # Create some color icons to make them easy to select
        # First, create a red Icon
        red_pixmap = QPixmap(40, 40)
        red_pixmap.fill(QColor("red"))
        red_icon = QIcon(red_pixmap)
        # This is a blue icon
        blue_pixmap = QPixmap(40, 40)
        blue_pixmap.fill(QColor("blue"))
        blue_icon = QIcon(blue_pixmap)

        # Attach the new icon to the red action.  The
        # text for the action is pulled to actually set the
        # color.
        red_action = QAction(red_icon, "red", self)
        red_action.setIcon(red_icon)
        tb.addAction(red_action)
        red_action.triggered.connect(self.color_action)

        # Blue action
        blue_action = QAction(blue_icon, "blue", self)
        blue_action.setIcon(blue_icon)
        tb.addSeparator()
        tb.addAction(blue_action)
        blue_action.triggered.connect(self.color_action)

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
        tb.addSeparator()
        tb.addWidget(self.label_y)

        self.setCentralWidget(self.slamboard)
        self.showMaximized()
        self.show()

    def update_coords(self, x, y):
        self.label_x.setText(f"X: {x}")
        self.label_y.setText(f"Y: {y}")

    def color_action(self):
        # who sent the signal
        target = self.sender()
        color = target.text()
        self.slamboard.color_action(color)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = mainWindow()
    sys.exit(app.exec_())

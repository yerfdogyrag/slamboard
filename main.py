# Import necessary modules
import sys
from typing import Optional

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPixmap, QColor, QIcon, QPen
from PyQt5.QtWidgets import (QApplication, QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsTextItem,
                             QMainWindow, QAction, QStyle, QLabel, QWidget, QSizePolicy, qApp)


class SlamBoard(QGraphicsView):
    def __init__(self, parent):
        super().__init__()
        self.scene = None
        self.rect: Optional[QGraphicsRectItem] = None
        self.rect_width = 1
        self.rect_color = "black"
        self.initializeView()
        self.dragging = None
        self.rect_save = None
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
        modifiers = QtWidgets.QApplication.keyboardModifiers()
        if modifiers & Qt.ShiftModifier:
            if self.dragging is None:
                # Save off the rectangle as absolute coordinates in the scene
                off_x = self.rect.x()
                off_y = self.rect.y()
                self.rect_save = self.rect.rect().adjusted(off_x, off_y, off_x, off_y)

            # We're dragging the upper left-hand corner around, leaving
            # the bottom right in the same place.  This gets real funky
            # when the coordinates go negative, so it's easiest to convert
            # to x1,y1,x2,y2 rather than x,y,width,height
            # The "normalize" function makes sure that x1 < x2 and y1 < y2
            x1, y1, x2, y2 = self.rect_save.getCoords()
            x1 = new_pos.x()
            y1 = new_pos.y()
            new_rect = QRectF()
            new_rect.setCoords(x1, y1, x2, y2)
            final_rect = new_rect.normalized()

            # Note: the setX sets the rectangle's location in the scene space.  The actual
            #       rectangle has an upper-left hand corner of 0,0 and so we're just adjusting
            #       the location and the width/height.
            self.rect.setX(final_rect.x())
            self.rect.setY(final_rect.y())
            self.rect.setRect(0, 0, final_rect.width(), final_rect.height())
            # Set the width of children (assumed to be text)
            width = final_rect.width()
            for child in self.rect.childItems():
                child.setTextWidth(width)

        else:
            self.dragging = None
            self.rect.setX(x)
            self.rect.setY(y)
            # print(pos.x(), pos.y())
        # Update labels at the upper right
        self.parent.update_coords(x, y)

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
        if key == Qt.Key_S:
            self.rect_width -= 1
            if self.rect_width < 1:
                self.rect_width = 10
            self.update_rect_pen()
        elif key == Qt.Key_B:
            self.rect = QGraphicsRectItem(0, 0, 120, 120)
            self.rect.setParentItem(self.rect)
            self.scene.addItem(self.rect)

        # print("Key:", event.key())

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

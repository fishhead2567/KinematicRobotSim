from PyQt5 import QtCore, QtGui, QtWidgets, QtOpenGL
from KinematicViewOnly_qt import Ui_MainWindow

from random import randint, shuffle
import time

# Create a class for our main window

# first random from https://ralsina.me/stories/BBS53.html
class RandomGui(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)

        # This is always the same
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)

        # From here until the end of this method is
        # the only interesting part!

        # Since the UI is a QGraphicsView, I create a Scene
        # so it has something to show
        self.scene=QtWidgets.QGraphicsScene()
        self.ui.view.setScene(self.scene)


        self.scene.setSceneRect(0,0,600,400)

        # This makes the view OpenGL-accelerated. Usually makes
        # things much faster, but it *is* optional.

        self.ui.view.setViewport(QtOpenGL.QGLWidget())

        # populate fills the scene with interesting stuff.

        self.entities = []
        self.animations = []

        self.populate()

        # Make it bigger
        self.setWindowState(QtCore.Qt.WindowMaximized)

        # Well... it's going to have an animation, ok?

        # So, I set a timer to 1 second
        self.animator=QtCore.QTimer()

        # And when it triggers, it calls the animate method
        self.animator.timeout.connect(self.animate)

        # And I animate it once manually.
        self.animate()


    def populate(self):

        # create a set of items
        rectangle = QtWidgets.QGraphicsRectItem(
            0,0,50,100
        )

        # create an ellipse under it
        ellipse = QtWidgets.QGraphicsEllipseItem(
            0,0,50,50,
            rectangle
        )

        rectangle.setPos(200,200)

        self.entities.append(rectangle)
        self.rect = rectangle
        self.scene.addItem(rectangle)
        print(rectangle.childItems())
        i= rectangle.childItems()

    def animate(self):


        animation = QtCore.QPropertyAnimation(
            self.rect, b"pos")
        animation.setDuration(800)
        animation.setEndValue(QtCore.QPoint(randint(-100, 500), randint(-250, 250)))
        self.animations.append(animation)

        [animation.start() for animation in self.animations if type(animation) != int]

        self.animator.start(1000)

def main():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = RandomGui()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

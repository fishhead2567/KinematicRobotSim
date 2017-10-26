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
        self.digits = []
        self.animations = []

        # This is just a nice font, use any font you like, or none
        font = QtGui.QFont('White Rabbit')
        font.setPointSize(120)

        # Create three ":" and place them in our scene
        self.dot1 = QtWidgets.QGraphicsTextItem(':')
        self.dot1.setFont(font)
        self.dot1.setPos(140, 0)
        self.scene.addItem(self.dot1)
        self.dot2 = QtWidgets.QGraphicsTextItem(':')
        self.dot2.setFont(font)
        self.dot2.setPos(410, 0)
        self.scene.addItem(self.dot2)

        # Create 6 sets of 0-9 digits
        for i in range(60):
            l = QtWidgets.QGraphicsTextItem(str(i % 10))
            l.setFont(font)
            # The zvalue is what controls what appears "on top" of what.
            # Send them to "the bottom" of the scene.
            l.setZValue(-100)

            # Place them anywhere
            l.setPos(randint(0, 500), randint(150, 300))

            # Make them semi-transparent
            l.setOpacity(.3)

            # Put them in the scene
            self.scene.addItem(l)

            # Keep a reference for internal purposes
            self.digits.append(l)

    def animate(self):
        # Just a list with 60 positions
        self.animations = list(range(0, 60))


        # Ok, I confess it, this part is a mess, but... a little
        # mistery is good for you. Read this carefully, and tell
        # me if you can do it better. Or try to something nicer!

        offsets = list(range(6))
        shuffle(offsets)

        # Some items, animate with purpose
        h1, h2 = map(int, '%02d' % time.localtime().tm_hour)
        h1 += offsets[0] * 10
        h2 += offsets[1] * 10

        animation = QtCore.QPropertyAnimation(self.digits[h1], b"pos")
        animation.setDuration(800)
        animation.setEndValue(QtCore.QPoint(-40,0))
        self.animations.append(animation)

        animation = QtCore.QPropertyAnimation(self.digits[h2], b"pos")
        animation.setDuration(800)
        animation.setEndValue(QtCore.QPoint(50, 0))
        self.animations.append(animation)

        m1, m2 = map(int, '%02d' % time.localtime().tm_min)
        m1 += offsets[2] * 10
        m2 += offsets[3] * 10

        animation = QtCore.QPropertyAnimation(self.digits[m1], b"pos")
        animation.setDuration(800)
        animation.setEndValue(QtCore.QPoint(230, 0))
        self.animations.append(animation)

        animation = QtCore.QPropertyAnimation(self.digits[m2], b"pos")
        animation.setDuration(800)
        animation.setEndValue(QtCore.QPoint(320, 0))
        self.animations.append(animation)


        s1, s2 = map(int, '%02d' % time.localtime().tm_sec)
        s1 += offsets[4] * 10
        s2 += offsets[5] * 10

        animation = QtCore.QPropertyAnimation(self.digits[s1], b"pos")
        animation.setDuration(800)
        animation.setEndValue(QtCore.QPoint(500, 0))
        self.animations.append(animation)

        animation = QtCore.QPropertyAnimation(self.digits[s2], b"pos")
        animation.setDuration(800)
        animation.setEndValue(QtCore.QPoint(590, 0))
        self.animations.append(animation)

        # Other items, animate randomly
        for i in range(60):
            l = self.digits[i]
            if i in [h1, h2, m1, m2, s1, s2]:
                l.setOpacity(1)
                continue
            l.setOpacity(.3)
            animation = QtCore.QPropertyAnimation(l, b"pos")
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
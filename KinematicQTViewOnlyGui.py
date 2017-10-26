from PyQt5 import QtCore, QtGui, QtWidgets, QtOpenGL, Qt
from KinematicViewOnly_qt import Ui_MainWindow
import numpy as np

from QtMobileModel import QtOmniModel, QtBicycleModel
from random import randint, shuffle
import time

# Create a class for our main window

# first random from https://ralsina.me/stories/BBS53.html
class KinematicViewOnlyGui(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)

        # This is always the same
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)

        #default values
        self.ppm = 100.0
        self.centerPx = np.array((320,200))

        self.control_input = np.zeros(20)

    def SetupScene(self, entities, timestep):
        # setup the simulation scene

        # Since the UI is a QGraphicsView, I create a Scene
        # so it has something to show
        self.scene=QtWidgets.QGraphicsScene()
        self.ui.view.setScene(self.scene)


        self.scene.setSceneRect(0,0,600,400)

        # This makes the view OpenGL-accelerated. Usually makes
        # things much faster, but it *is* optional.

        self.ui.view.setViewport(QtOpenGL.QGLWidget())

        # setup basic sim data
        self.entities = entities
        self.timestep = timestep

        # Make the window big
        self.setWindowState(QtCore.Qt.WindowMaximized)


        # populate the scene
        for entity in self.entities:
            entity.CreateGraphicsItems(self.centerPx, self.ppm)
            for item in entity.graphics_items:
                self.scene.addItem(item)


        # setup the keyboard event filter
        self.ui.view.installEventFilter(self)


        # So, I set a timer to 1 second
        self.step_timer=QtCore.QTimer()

        # And when it triggers, it calls the animate method
        self.step_timer.timeout.connect(self.SimStep)
        self.step_timer.start(self.timestep)

    def SimStep(self):

        for entity in self.entities:
            entity.ApplyControls(self.control_input)
            entity.Tick(self.timestep / 1000.0) # ms to s
            entity.UpdateGraphicsItems()


        self.step_timer.start(self.timestep)

    # handle input
    def eventFilter(self, widget, event):
        if event.type() == QtCore.QEvent.KeyPress:
            # do some stuff ...

            # detect which key
            if event.key() == QtCore.Qt.Key_Q:
                self.control_input[0] = 1.0
            elif event.key() == QtCore.Qt.Key_A:
                self.control_input[0] = -1.0
            elif event.key() == QtCore.Qt.Key_W:
                self.control_input[1] = 1.0
            elif event.key() == QtCore.Qt.Key_S:
                self.control_input[1] = -1.0

            return True

        elif event.type() == QtCore.QEvent.KeyRelease:
            if event.key() == QtCore.Qt.Key_Q:
                self.control_input[0] = 0
            elif event.key() == QtCore.Qt.Key_A:
                self.control_input[0] =0
            elif event.key() == QtCore.Qt.Key_W:
                self.control_input[1] = 0
            elif event.key() == QtCore.Qt.Key_S:
                self.control_input[1] = 0

            return True # means stop event propagation
        else:
            return super(KinematicViewOnlyGui, self).eventFilter(widget, event)

def main():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = KinematicViewOnlyGui()

    models = []

    ppm = 50.0
    centerPx = np.array((320,200))

    #om = QtOmniModel(1)
    #models.append(om)

    by = QtBicycleModel(1, .5)
    models.append(by)

    for model in models:
        print("Info:", model.BasicInfoStr())

    # timestep in ms
    delta_t = 10
    window.SetupScene(models, delta_t)

    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

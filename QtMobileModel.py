from PyQt5 import QtCore, QtGui, QtWidgets, QtOpenGL

from MobileModel import *

class QtMobileModelMixin:
    def CreateGraphicsItems(self, centerPx, ppm):
        self.graphics_items = []
        self.centerPx = centerPx
        self.ppm = ppm


    def UpdateGraphicsItems(self):
        pass

    def PointMtoPx(self, point):
        return (point) * self.ppm + self.centerPx


class QtOmniModel(OmniModel, QtMobileModelMixin):

    def __init__(self, uid):
        super(QtOmniModel, self).__init__(uid)

    def CreateGraphicsItems(self, centerPx, ppm):
        super(QtOmniModel, self).CreateGraphicsItems(centerPx, ppm)

        # add a circle for this model
        ellipse = QtWidgets.QGraphicsEllipseItem(
            0,0,50,50
        )


        self.graphics_items.append(ellipse)
        self.ellipse = ellipse

        posPx = self.PointMtoPx(self.config[:2])
        self.ellipse.setPos(posPx[0], posPx[1])

        pass

    def UpdateGraphicsItems(self):
        super(QtOmniModel, self).UpdateGraphicsItems()

        #update the ellipse pos
        posPx = self.PointMtoPx(self.config[:2])
        self.ellipse.setPos(posPx[0], posPx[1])

class QtBicycleModel(BicycleModel, QtMobileModelMixin):
    def __init__(self, uid, length, max_steering=np.deg2rad(30)):
        super(QtBicycleModel, self).__init__(
            uid, length, max_steering)

    def CreateGraphicsItems(self, centerPx, ppm):
        super(QtBicycleModel, self).CreateGraphicsItems(centerPx, ppm)

        self.width = .15

        widthPx = self.width * self.ppm
        lengthPx = self.length * self.ppm

        # add a rectangle fot the body,
        rect = QtWidgets.QGraphicsRectItem(
            0, -widthPx / 2.0,
            lengthPx, widthPx
        )

        # front wheel
        wheelLength = 0.15 * self.ppm
        wheelWidth = 0.05 * self.ppm

        ellipse = QtWidgets.QGraphicsEllipseItem(
            lengthPx - wheelLength / 2.0,
            -wheelWidth / 2.0,
            wheelLength,
            wheelWidth,
            rect
        )
        self.front_wheel = ellipse
        #self.front_wheel.setTransformOriginPoint()

        # back wheel
        ellipse = QtWidgets.QGraphicsEllipseItem(
            -wheelLength /2.0,
            -wheelWidth / 2.0,
            wheelLength,
            wheelWidth,
            rect
        )

        self.graphics_items.append(rect)
        self.body = rect
        posPx = self.PointMtoPx(self.config[:2])
        self.body.setPos(posPx[0], posPx[1])


        axes = QtWidgets.QGraphicsRectItem(
            320, 200,
            320,1
        )
        self.graphics_items.append(axes)

        axes = QtWidgets.QGraphicsRectItem(
            320, 200,
            1,200
        )
        self.graphics_items.append(axes)

        pass

    def UpdateGraphicsItems(self):
        super(QtBicycleModel, self).UpdateGraphicsItems()

        # update the ellipse pos
        posPx = self.PointMtoPx(self.config[:2])
        self.body.setPos(posPx[0], posPx[1])
        self.body.setRotation(
            np.rad2deg(self.config[2])
        )
        pos = self.front_wheel.pos()

        """
        front_wheel_matrix = self.front_wheel.transform()
        new_matrix = front_wheel_matrix
        new_matrix.reset()
        new_matrix.rotateRadians(self.control[1])
        new_matrix.translate(self.front_wheel.pos().x(),
                             self.front_wheel.pos().y())
        self.front_wheel.setTransform(new_matrix)
        """
        #self.front_wheel.setPos(0,0)
        #self.front_wheel.setRotation(-np.rad2deg(
        #       self.control[1]
        #   ) )
        #self.front_wheel.setPos(pos)


        # reset the wheel position to get its orientation
        # wheelPos = self.front_wheel.getScenePos()
        # self.front_wheel.setPos(0,0)

        # self.front_wheel.setPos(wheelPos[0],wheelPos[1])

from PyQt5 import QtCore, QtGui, QtWidgets, QtOpenGL

from Util.Vector2 import  Vector2

from MobileModel import *

class SubItem(object):
    def __init__(self, item, offset, rotation):
        self.item = item
        self.offset = offset
        self.rotation = rotation


def RotatePt(pt,angle):
    return [
        pt[0] * np.cos(angle) - pt[1] * np.sin(angle),
        pt[0] * np.sin(angle) + pt[1] * np.cos(angle)
    ]

class QtMobileModelMixin:
    def CreateGraphicsItems(self, centerPx, ppm, config_orient=None):
        self.base_shape = None
        self.sub_shapes = []
        self.centerPx = centerPx
        self.ppm = ppm
        self.CONFIG_ORIENT = config_orient


    def UpdateGraphicsItems(self):
        # if there are subitems, update them to match their offset from the parent item
        if self.base_shape is None:
            return

        elif len(self.sub_shapes) == 0:
            return

        # in qt, rotations are clockwise. In most math packages, they aren't. So, invert here.
        base_pos = self.base_shape.pos()
        base_pos = [base_pos.x(), base_pos.y()]
        base_orient = -np.deg2rad(self.base_shape.rotation())

        for sub in self.sub_shapes:
            print(sub.item.parentItem())
            sub_pos =  RotatePt(sub.offset, -base_orient)
            sub_pos = [sub_pos[0] + base_pos[0], sub_pos[1] + base_pos[1]]
            sub_rotation = sub.rotation + base_orient
            sub.item.setPos(sub_pos[0], sub_pos[1])
            sub.item.setRotation(np.rad2deg(-sub_rotation))




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


        self.base_shape = ellipse

        posPx = self.PointMtoPx(self.config[:2])
        self.base_shape.setPos(posPx[0], posPx[1])

        pass

    def UpdateGraphicsItems(self):
        super(QtOmniModel, self).UpdateGraphicsItems()

        #update the ellipse pos
        posPx = self.PointMtoPx(self.config[:2])
        self.base_shape.setPos(posPx[0], posPx[1])

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
        self.base_shape = rect

        # front wheel
        wheelLength = 0.15 * self.ppm
        wheelWidth = 0.05 * self.ppm

        # create the ellipse at the origin, let the sub-relationship move it when it needs to
        ellipse = QtWidgets.QGraphicsEllipseItem(
            -wheelLength /2.0,
            -wheelWidth / 2.0,
            wheelLength,
            wheelWidth,
        )

        ellipse.setTransformOriginPoint(0, 0)

        ellipse_item = SubItem(
            ellipse,
            [lengthPx, 0],
            0.0
        )
        self.sub_shapes.append(ellipse_item)
        self.front_wheel = ellipse_item

        # back wheel
        ellipse = QtWidgets.QGraphicsEllipseItem(
            -wheelLength /2.0,
            -wheelWidth / 2.0,
            wheelLength,
            wheelWidth
        )

        ellipse.setTransformOriginPoint(0, 0)
        ellipse_item = SubItem(
            ellipse,
            [0, 0],
            0.0
        )
        self.sub_shapes.append(ellipse_item)

        posPx = self.PointMtoPx(self.config[:2])
        self.base_shape.setPos(posPx[0], posPx[1])


        """
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
        """
        pass

    def UpdateGraphicsItems(self):
        super(QtBicycleModel, self).UpdateGraphicsItems()

        # update the ellipse pos
        posPx = self.PointMtoPx(self.config[:2])
        self.base_shape.setPos(posPx[0], posPx[1])
        self.base_shape.setRotation(
            np.rad2deg(self.config[2])
        )

        self.front_wheel.rotation = -self.control[1] * self.max_steering

        super(QtBicycleModel, self).UpdateGraphicsItems()

if __name__ == "__main__":

    ppm = 50.0
    centerPx = np.array((320,200))

    #om = QtOmniModel(1)
    #models.append(om)

    omni = QtOmniModel(1)
    omni.CreateGraphicsItems(centerPx, ppm)
    omni.UpdateGraphicsItems()


    bicycle = QtBicycleModel(1, .5)
    bicycle.CreateGraphicsItems(centerPx, ppm)
    bicycle.UpdateGraphicsItems()
    bicycle.ApplyControl(1,1.0)
    bicycle.UpdateGraphicsItems()

# ##HPanda Library
# Input related classes

from direct.showbase.ShowBase import ShowBase
from panda3d.core import Vec3, WindowProperties


class HMouseLook():
    def __init__(self, showBase, xFact=500, yFact=500, applyH=True, applyP=True):
        self.Base = showBase
        self.xFact = xFact
        self.yFact = yFact
        self.centerMouse()
        self.setTask()
        self.centerX = base.win.getXSize() / 2
        self.centerY = base.win.getXSize() / 2
        self.dH = 0
        self.dP = 0
        self.applyH = applyH
        self.applyP = applyP
        self.hideMouse()

    def hideMouse(self, value=True):
        prop = WindowProperties()
        prop.setCursorHidden(value)
        base.win.requestProperties(prop)

    def disable(self):
        self.Base.removeTask("updateTask")

    def enable(self):
        self.setTask()

    def setTask(self):
        # if base.mouseWatcherNode.hasMouse():
        self.Base.addTask(self.updateTask, "updateTask")
        print "Task Added"

    def updateTask(self, task):
        try:
            x = base.mouseWatcherNode.getMouseX()
            y = base.mouseWatcherNode.getMouseY()
        except:
            self.centerMouse()
            return task.cont
        if x == 0:
            self.dH = 0
        if y == 0:
            self.dP = 0
            self.centerMouse()
        if x == 0 and y == 0:
            return task.cont
        else:
            dt = globalClock.getDt()
            self.dH = -x * self.xFact * dt
            self.dP = y * self.xFact * dt
            if self.applyH:
                self.Base.camera.setH(self.Base.camera, self.dH)
            if self.applyP:
                self.Base.camera.setP(self.Base.camera, self.dP)
            self.Base.camera.setR(self.Base.render, 0)
            self.centerMouse()
            return task.cont

    def centerMouse(self):
        base.win.movePointer(0, base.win.getXSize() / 2, base.win.getYSize() / 2)
# ##HPanda3D
# ##HGameObject

from direct.actor.Actor import Actor

from HUtils import *
from panda3d.bullet import BulletCharacterControllerNode, BulletRigidBodyNode, BulletGhostNode
from panda3d.bullet import BulletClosestHitSweepResult
from panda3d.core import TransformState, BitMask32, VBase3,Point3,Vec3, NodePath

physicsTypes = {"static": 0, "character": 1, "dynamic": 2, "None": 3, "ghost": 4}


class HBulletRigidBodyNode(BulletRigidBodyNode):
    def __init__(self, name):
        BulletRigidBodyNode.__init__(self, name)
        self.customData = {"name": name}


class HGameObject():
    def __init__(self, name, level, visualMeshEgg, parent, physicsType, physicsShapeEgg=None, shapeMargin=0.04,
                 animable=False, animationsDict=None, stepHeight=0.5, x=0, y=0, z=0, mass=0, perpixelShading=False):
        """

        :type name: str
        :type level: HLevel
        :type visualMeshEgg: str
        :type parent: panda3d.core.NodePath
        :type physicsType: int
        :type physicsShapeEgg: str
        :type shapeMargin: float
        :type animable: bool
        :type animationsDict: dict
        :type stepHeight: float
        :type x: float
        :type y: float
        :type z: float
        :type mass: float
        :type perpixelShading: bool
        """
        self.name = name
        self.level = level
        if visualMeshEgg is not None:
            if animable:
                if animationsDict is not None:
                    self.vMesh = Actor(visualMeshEgg, animationsDict)
                    self.vMesh.setBlend(frameBlend=True)

                else:
                    self.vMesh = Actor(visualMeshEgg)
                    self.vMesh.setBlend(frameBlend=True)
            else:
                self.vMesh = level.Base.loader.loadModel(visualMeshEgg)
        else:
            self.vMesh = None
        if physicsType == physicsTypes["character"]:
            print name + " is a character"
            self.shapeModel = self.level.loadEgg(physicsShapeEgg)
            self.shape = modelToConvex(self.shapeModel)[0]
            self.shape.setMargin(shapeMargin)
            self.body = BulletCharacterControllerNode(self.shape, stepHeight, name)
            self.bodyNP = parent.attachNewNode(self.body)
            if visualMeshEgg is not None:
                self.vMesh.reparentTo(self.bodyNP)
            self.level.world.attachCharacter(self.body)
            self.bodyNP.setPos(x, y, z)
            self.body.setPythonTag("name", name)
        elif physicsType == physicsTypes["dynamic"]:
            self.shapeModel = self.level.loadEgg(physicsShapeEgg)
            self.shape = modelToConvex(self.shapeModel)[0]
            self.shape.setMargin(shapeMargin)
            self.body = BulletRigidBodyNode(name)
            self.body.setMass(mass)
            self.body.addShape(self.shape)
            self.bodyNP = parent.attachNewNode(self.body)
            if visualMeshEgg is not None:
                self.vMesh.reparentTo(self.bodyNP)
            self.level.world.attachRigidBody(self.body)
            self.bodyNP.setPos(x, y, z)
            self.body.setPythonTag("name", name)
        elif physicsType == physicsTypes["ghost"]:
            self.shapeModel = self.level.loadEgg(physicsShapeEgg)
            self.shape = modelToConvex(self.shapeModel)[0]
            self.shape.setMargin(shapeMargin)
            self.body = BulletGhostNode(name)
            # self.body.setMass(mass)
            self.body.addShape(self.shape)
            self.bodyNP = parent.attachNewNode(self.body)
            if visualMeshEgg is not None:
                self.vMesh.reparentTo(self.bodyNP)
            self.level.world.attachGhost(self.body)
            self.bodyNP.setPos(x, y, z)
            self.body.setPythonTag("name", name)
        else:
            pass

            # ###3Events
            # self.level.Base.taskMgr.add(self.onFrame,"onFrame")
        self.shaders = perpixelShading
        if self.vMesh is not None and not self.shaders:
            self.level.Base.taskMgr.add(self.clearShaderTask, name + "_clearShader")
        #self.level.Base.taskMgr.add(self._calcVel,self.name+"_calcVelTask")
        self._lastPos=Point3()
        self.velocity=Vec3()

    def _calcVel(self,t):
        if self.level.pause is False:
            try:
                n=self.bodyNP.getPos()
                self.velocity=(n-self._lastPos)/globalClock.getDt()
                self._lastPos=n
            except:
                #print self.velocity
                pass
        return t.cont

    def clearShaderTask(self, t):
        self.vMesh.clearShader()
        print "Shader clear_", self.name

    def onFrame(self, task):
        pass

    def doRelativeSweepTest(self, relativePoint, BitMask=None, height=0.1):
        globalPoint = self.level.Base.render.getRelativePoint(self.bodyNP, relativePoint)
        fromT = TransformState.makePos(self.bodyNP.getPos(self.level.Base.render) + VBase3(0, 0, height))
        toT = TransformState.makePos(globalPoint + VBase3(0, 0, height))
        if BitMask != None:
            r = self.level.world.sweepTestClosest(self.shape, fromT, toT, BitMask)
        else:
            r = self.level.world.sweepTestClosest(self.shape, fromT, toT)
        if r.getNode() == self.body:
            return BulletClosestHitSweepResult.empty()
        else:
            return r

    def willCollide(self, relativePoint, bitMask=None, height=0.1):
        r = self.doRelativeSweepTest(relativePoint, bitMask, height)
        if r.getNode() == self.body:
            return False
        else:
            return r.hasHit()

    def doInverseRelativeSweepTest(self, relativePoint, bitMask=None, height=0.1):
        globalPoint = self.level.Base.render.getRelativePoint(self.bodyNP, relativePoint)
        fromT = TransformState.makePos(self.bodyNP.getPos(self.level.Base.render) + VBase3(0, 0, height))
        toT = TransformState.makePos(globalPoint + VBase3(0, 0, height))
        if bitMask != None:
            r = self.level.world.sweepTestClosest(self.shape, toT, fromT, bitMask)
        else:
            r = self.level.world.sweepTestClosest(self.shape, toT, fromT)
        if r.getNode() == self.body:
            return BulletClosestHitSweepResult.empty()
        else:
            return r

    def inverseWillCollide(self, relativePoint, bitMask=None, height=0.1):
        r = self.doRelativeSweepTest(relativePoint, bitMask, height)
        if r.getNode() == self:
            return False
        else:
            return r.hasHit()

    def destroy(self):
        if "Character" in str(self.body):
            self.level.world.removeCharacter(self.body)
        elif "Rigid" in str(self.body):
            self.level.world.removeRigidBody(self.body)
        elif "Ghost" in str(self.body):
            self.level.world.removeGhost(self.body)
        self.bodyNP.removeNode()
        try:
            self.vMesh.removeNode()
        except:
            pass
    def isOnGround(self):
        r=self.willCollide(Point3(0,0,-0.1),self.body.getIntoCollideMask(),0)
        print r
        return r

    def setVelocity(self,v):
        globalV=self.level.Base.render.getRelativeVector(self.bodyNP,v)
        self.body.setLinearVelocity(globalV)
    def applyForce(self,v):
        globalV=self.level.Base.render.getRelativeVector(self.bodyNP,v)
        self.body.applyCentralForce(globalV)


class HInteractiveObject(HGameObject):
    def __init__(self, level, name0, visualEgg, collisionEgg, mass, x0=0, y0=0, z0=0, margin=0.04,
                 sound=None, perpixelShading=True, CCD=False, CCDradius=0.05):
        HGameObject.__init__(self, name0, level, visualEgg, level.Base.render, 2, collisionEgg, margin, False, None,
                             0, x0, y0, z0, mass, perpixelShading)
        self.level.Base.taskMgr.add(self.testCollision, self.name + "_testCollisionTask")
        if CCD:
            self.body.setCcdMotionThreshold(0.01)
            self.body.setCcdSweptSphereRadius(CCDradius)

    def onContact(self, bodyList):
        "Play sound"

    def testCollision(self, task):
        result = self.level.world.contactTest(self.body)
        if result.getNumContacts() > 0:
            self.onContact(result)
        else:
            pass
        # if self.bodyNP.getZ(self.level.Base.render)<50: self.destroy()
        return task.cont

    def destroy(self):
        self.level.world.removeRigidBody(self.body)
        self.vMesh.removeNode()
        self.bodyNP.removeNode()
        self.level.Base.taskMgr.remove(self.name + "_testCollisionTask")
        print self.name, "_destroyed"

class HDynamicObject(NodePath):
    def __init__(self,name,level,visibleEgg,collisionEgg=None,x0=0,y0=0,z0=0,parent=None,margin=0.05,mass=0,directRender=True,convex=True):
        self.name=name
        self.level=level
        NodePath.__init__(self,self.level.loadEgg(visibleEgg))
        self.body= BulletRigidBodyNode(self.name+"_RigidBody")
        self.attachNewNode(self.body)
        if collisionEgg != None:
            m = self.level.Base.loader.loadModel(collisionEgg)
            if convex:
                sTuple=modelToConvex(m)
            else:
                sTuple = modelToShape(m)
            sTuple[0].setMargin(margin)
            self.body.addShape(sTuple[0], sTuple[1])
            self.body.setMass(mass)
            self.body.setPythonTag("name",self.name+"_RigidBody")
            self.level.world.attachRigidBody(self.body)
        self.setPos(x0,y0,z0)
        if directRender:
            self.reparentTo(self.level.Base.render)
        elif parent != None:
            self.reparentTo(parent)

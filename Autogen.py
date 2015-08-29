import argparse, os

# main file name
# firstScene name
#generate test floor

main_file_string = """
from HPanda.HGame import HGame
import Scene1


class MainGame(HGame):
    def __init__(self):
        HGame.__init__(self, title="Your Title")

    def setup(self):
        self.currentScene = Scene1.Scene(self)


if __name__ == "__main__":
    Game = MainGame()
    Game.run()
"""

run_bat_string = """
ppython main.py
pause"""

default_scene_str = """
from HPanda.HScene import HScene
from HPanda.HGameObject import HNewGameObject

# #################
from panda3d.core import loadPrcFileData

assets = "3d/"
windowTitle = "Scene Title"
windowX = 640
windowY = 480
perpixelShading = False
showFPS = True
debugPhysics = False
debugView = False
debugLights = False
pauseKey = "p"
filters = False
bulletSteps = 10
pystats = False

# ####Preferences#####
loadPrcFileData("", "win-size " + str(windowX) + " " + str(windowY))
loadPrcFileData("", "window-title " + windowTitle)
loadPrcFileData("", "allow-incomplete-render 1")
# loadPrcFileData("", "bullet-solver-iterations " + str(bulletSteps))
if showFPS:
    loadPrcFileData("", "show-frame-rate-meter #t")
if pystats:
    loadPrcFileData("", "want-pstats 1")
    loadPrcFileData("", "task-timer-verbose 1")
    loadPrcFileData("", "pstats-tasks 1")

#####################

class Scene(HScene):
    def __init__(self, base):
        HScene.__init__(self, base)
        self.debugDrawing = debugPhysics
        self.setPhysics()
        self.setStatics()
        self.setCamera()
        self.n = 0
        self.Base.taskMgr.add(self._loop, "Scene1_loop")

    def _loop(self, t):
        #Your per scene loop here
        return t.cont

    def setCamera(self):
        #Camera setup
        self.Base.camLens.setNearFar(1, 110)

    def setStatics(self):
        #Setup static objects here
        self.defaultGround = HNewGameObject("DefaultGround", self, "HPanda/defaultGround.egg",
                                            physicsMesh="HPanda/defaultGround.egg", physicsType="rigid",
                                            shapeMargin=0.02)
"""
if __name__ == "__main__":
    os.chdir("..")
    main_file = open("main.py", "wt")
    main_file.write(main_file_string)
    main_file.close()
    run_bat_file = open("Run.bat", "wt")
    run_bat_file.write(run_bat_string)
    run_bat_file.close()
    default_scene_file = open("Scene1.py", "wt")
    default_scene_file.write(default_scene_str)
    default_scene_file.close()
    print "Done!"
	
	

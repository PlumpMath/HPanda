from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties, Filename


class HGame(ShowBase):
    def __init__(self, sizeX=640, sizeY=480, title="Title", particles=True, fixedSize=True, cursorHide=False,
                 icon="None", cursorFile="None",posX=150,posY=50):
        ShowBase.__init__(self)
        if particles:
            base.enableParticles()
        self.propierties = WindowProperties()
        self.propierties.setSize(sizeX, sizeY)
        self.propierties.setTitle(title)
        self.propierties.setFixedSize(fixedSize)
        self.propierties.setCursorHidden(cursorHide)
        if icon != "None":
            self.propierties.setIconFilename(Filename(icon))
        if cursorFile != "None":
            self.propierties.setCursorFilename(Filename(cursorFile))
        self.propierties.setOrigin(posX,posY)
        base.win.requestProperties(self.propierties)
        self.setup()

    def setup(self):
        pass

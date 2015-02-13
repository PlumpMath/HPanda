from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties, Filename


class HGame(ShowBase):
    def __init__(self, sizeX=640, sizeY=480, title="Title", particles=True, fixedSize=True, cursorHide=False,
                 icon="None", cursorFile="None",posX=300,posY=50):
        """

        :param sizeX: Window horizontal size in pixels
        :param sizeY: Window vertical size i pixels
        :param title: Window's title bar text
        :param particles: Enable particles
        :param fixedSize: Window can be resized
        :param cursorHide: Hide cursor
        :param icon: filepath to window icon
        :param cursorFile: filepath to window cursor icon
        :param posX: window initial X position
        :param posY: window initial Y position
        """
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

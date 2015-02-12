# ##HPanda Library
# Input related classes
#import pygame
#from direct.showbase import DirectObject

#import os

class HJoystickSensor():
    def __init__(self,joystickId=0):
        #print os.getcwd()
        import pygame #pygame must be in the Main.py directory
        pygame.init()
        pygame.joystick.init()
        if pygame.joystick.get_count()>0:
            self.id=joystickId
            self.object=pygame.joystick.Joystick(self.id)
            self.numButtons=self.object.get_numbuttons()
            self.numAxes=self.object.get_numaxes()
            base.taskMgr.add(self.handler,"taskForJoystick_"+self.id)
        else:
            print "No Joystick connected"
    def handler(self,t):
        for b in range(self.numButtons):
            if self.object.get_button(b):
                messenger.send("Joystick_Button_"+str(b))
        for a in range(self.numAxes):
            axis=self.object.get_axis(a)
            if axis!=0:
                messenger.send("Joystick_Axis_"+str(a),sentArgs[a])
        return t.cont
        ##Hats y otras cosas que no uso ahorita
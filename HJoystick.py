#from direct.showbase import DirectObject
import pygame #pygame must be in the Main.py directory
#THIS FILE MUST BE IN THE MAIN.PY DIRECTORY BECAUSE SON PATH ISSUES


class HJoystickSensor():
    def __init__(self,joystickId=0):
        #print os.getcwd()
        pygame.init()
        pygame.joystick.init()
        c=pygame.joystick.get_count()
        if c>0:
            self.id=joystickId
            self.object=pygame.joystick.Joystick(self.id)
            self.numButtons=self.object.get_numbuttons()
            self.numAxes=self.object.get_numaxes()
            base.taskMgr.add(self._task,"taskForJoystick_"+self.id)
        else:
            print "No Joystick"

    def _task(self,t):
        pygame.event.pump()
        for b in range(self.numButtons):
            if self.object.get_button(b):
                messenger.send("Joystick_Button_"+str(b))
        for a in range(self.numAxes):
            axis=self.object.get_axis(a)
            if axis!=0:
                messenger.send("Joystick_Axis_"+str(a),sentArgs[a])
        return t.cont
        ##Hats y otras cosas que no uso ahorita

if __name__=="__main__":
    a=HJoystickSensor()
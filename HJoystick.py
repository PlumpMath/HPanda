# from direct.showbase import DirectObject
import pygame  # ********  pygame must be in the Main.py directory
# THIS FILE MUST BE IN THE MAIN.PY DIRECTORY BECAUSE SON PATH ISSUES


class HJoystickSensor():
    def __init__(self, joystickId=0):
        # print os.getcwd()
        pygame.init()
        pygame.joystick.init()
        c = pygame.joystick.get_count()
        self.id=0
        if c > 0:
            self.id = joystickId
            self.joy = pygame.joystick.Joystick(self.id)
            self.numButtons = self.joy.get_numbuttons()
            self.numAxes = self.joy.get_numaxes()
            self.eventName = "Joystick_" + str(self.id) + "_"
            self.buttonEventName = self.eventName + "button_"
            self.axisEventName = self.eventName + "axis_"
            base.taskMgr.add(self._task, "taskForJoystick_" +str(self.id))
        else:
            print "No Joystick"

    def _task(self, t):
        pygame.event.pump()
        for b in range(self.numButtons):
            if self.joy.get_button(b):
                messenger.send(self.buttonEventName + str(b))
        for a in range(self.numAxes):
            axisValue = self.joy.get_axis(a)
            if axisValue != 0:
                messenger.send(self.axisEventName + str(a), sentArgs[axisValue])
        return t.cont
        # #Hats y otras cosas que no uso ahorita

mappingDict = {"axes": [["a", "d"], ["s", "w"]],
               "buttons": ["z", "x"]}
#mappingDict={"axis":[axis0List[neg,pos],axis1List[neg,pos]....],
            # "buttons":[button0,button1...]}

class HJoyKeySensor(HJoystickSensor):
    def __init__(self, mappingDict, joystickId=0):
        HJoystickSensor.__init__(self, joystickId)
        self.eventName = "JoyKey_" + str(self.id) + "_"
        self.buttonEventName = self.eventName + "button_"
        self.axisEventName = self.eventName + "axis_"
        self.mapping = mappingDict
        self.keyStates = []
        self.axesKeyStates=[]
        for i in range(len(self.mapping["buttons"])):
            base.accept(self.mapping["buttons"][i], self._setKey,
                        extraArgs=[i])  # #Will send to _setButton the pressed button number
            base.accept(self.mapping["buttons"][i] + "-up", self._unsetKey,
                        extraArgs=[i])  # #Will send to _setButton the unpressed button number
            self.keyStates.append(False)
            print "Event handler for ",self.mapping["buttons"][i]
        for o in range(len(self.mapping["axes"])):
            self.axesKeyStates.append(list())
            for p in range(len(self.mapping["axes"][o])):
                base.accept(self.mapping["axes"][o][p],self._setArrow,extraArgs=[o,p])
                base.accept(self.mapping["axes"][o][p]+"-up",self._unsetArrow,extraArgs=[o,p])
                self.axesKeyStates[o].append(False)
        base.taskMgr.add(self._task, "taskForJoystick_" + str(self.id))
        print "Axes state keys:",self.axesKeyStates

    def _setArrow(self,o,p):
        self.axesKeyStates[o][p]=True
        #print "Pressed axis:",self.mapping["axes"][o][p]

    def _unsetArrow(self,o,p):
        self.axesKeyStates[o][p]=False
        #print "Freed:",self.mapping["axes"][o][p]

    def _setKey(self, k):
        self.keyStates[k] = True
        #print "Pressed key:",k

    def _unsetKey(self, k):
        self.keyStates[k] = False
        #print "Freed key: ",k

    def _task(self, t):
        pygame.event.pump()
        for nb in range(len(self.mapping["buttons"])):
            try:
                joyButtonValue = self.joy.get_button(nb)
                if self.keyStates[nb] or joyButtonValue:
                    messenger.send(self.buttonEventName + str(nb))
            except:
                if self.keyStates[nb]:
                    messenger.send(self.buttonEventName+str(nb))
                    #print self.mapping["buttons"][nb], "- pressed"
        for na in range(len(self.mapping["axes"])):
            try:
                axisValue=self.joy.get_axis(na)
                if axisValue !=0:
                    messenger.send(self.axisEventName+str(na),sentArgs=[axisValue])
            except:
                if self.mapping["axes"][na][0]:
                    messenger.send(self.axisEventName+str(na),sentArgs=[-1])
                elif self.mapping["axes"][na][1]:
                    messenger.send(self.axisEventName+str(na),sentArgs=[1])
        return t.cont
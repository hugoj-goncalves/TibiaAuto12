from Core.GUIManager import Disable, Enable, ExecGUITrigger
from Core.HookWindow import LocateCenterImage, LocateImageAlphaChannel 
from Conf.Hotkeys import Hotkey

from Core.GUI import *
from Core.GUISetter import GUISetter
from Core.ThreadManager import AllThreads, ThreadManager

GUIChanges = []

EnabledFoodEater = False

class FoodEater:
    def ScanFoodEater(self, wait):
        if self.UseFoodFromContainersCheck.get():
            X, Y = LocateImageAlphaChannel('images/Items/None/Foods/Container/DragonHam.png', Precision=0.95, Debug=False)
            # X, Y = LocateCenterImage('images/Items/None/Foods/Container/DragonHam.png', Precision=0.7, Debug=False)
            if X != 0 and Y != 0:
                print("Right Clicked at ", X, ", ", Y, " To Eat Food")
                self.SendToClient.RightClick(X, Y + 20)
                wait(4*60)
        else:
            self.SendToClient.Press(self.HotkeyFoodEater.get())
            print("Pressed ", self.HotkeyFoodEater.get(), " To Eat Food")
            wait(4*60)

    def __init__(self, MOUSE_OPTION):
        self.FoodEater = GUI('FoodEater', 'Module: Food Eater')
        self.FoodEater.DefaultWindow('AutoHeal2', [306, 372], [1.2, 2.29])
        self.Setter = GUISetter("FoodEaterLoader")
        self.SendToClient = Hotkey(MOUSE_OPTION)

        self.AllThreads = AllThreads()
        self.ThreadName = 'ThreadFoodEater'
        if not self.AllThreads.ExistsThread(self.ThreadName):
            self.ThreadManager = ThreadManager(self.ThreadName, Managed=True, Func=self.ScanFoodEater)

        self.HotkeyFoodEater, self.InitiatedHotkeyFoodEater = self.Setter.Variables.Str('HotkeyFoodEater')
        self.UseFoodFromContainersCheck, InitiatedUseFoodFromContainersCheck = self.Setter.Variables.Bool(
            'UseFoodFromContainers')

        def SetFoodEater():
            global EnabledFoodEater
            if not EnabledFoodEater:
                EnabledFoodEater = True
                ButtonEnabled.configure(text='FoodEater: ON', relief=SUNKEN, bg=rgb((158, 46, 34)))
                Checking()
                self.AllThreads.UnPauseThreads(self.ThreadName)
            else:
                EnabledFoodEater = False
                ButtonEnabled.configure(text='FoodEater: OFF', relief=RAISED, bg=rgb((127, 17, 8)))
                Checking()
                self.AllThreads.PauseThreads(self.ThreadName)

        def Checking():
            if EnabledFoodEater:
                Disable(HotkeyOption)
                Disable(UseFoodFromContainers)
            else:
                Enable(HotkeyOption)
                Enable(UseFoodFromContainers)
            if self.UseFoodFromContainersCheck.get():
                Disable(HotkeyOption)
            ExecGUITrigger()

        def CheckingGUI(Init, Get, Name):
            if Get != Init:
                GUIChanges.append((Name, Get))

        def Destroy():
            print('FoodEater Destroy called!')
            CheckingGUI(self.InitiatedHotkeyFoodEater, self.HotkeyFoodEater.get(), 'HotkeyFoodEater')
            CheckingGUI(InitiatedUseFoodFromContainersCheck, self.UseFoodFromContainersCheck.get(), 'UseFoodFromContainers')

            if len(GUIChanges) != 0:
                for EachChange in range(len(GUIChanges)):
                    self.Setter.SetVariables.SetVar(
                        GUIChanges[EachChange][0], GUIChanges[EachChange][1])

            self.FoodEater.destroyWindow()

        self.FoodEater.addButton('Ok', Destroy, [73, 21], [115, 340])

        HotkeyOption = self.FoodEater.addOption(self.HotkeyFoodEater, self.SendToClient.Hotkeys, [17, 80], 10)

        UseFoodFromContainers = self.FoodEater.addCheck(self.UseFoodFromContainersCheck, [
                                          17, 55], InitiatedUseFoodFromContainersCheck, "Use food from containers instead", cb=Checking)

        global EnabledFoodEater
        if not EnabledFoodEater:
            ButtonEnabled = self.FoodEater.addButton('FoodEater: OFF', SetFoodEater, [328, 29, 12, 469],
                                                       [5, 310, 8])
        else:
            ButtonEnabled = self.FoodEater.addButton('FoodEater: ON', SetFoodEater, [328, 29, 12, 469],
                                                       [5, 310, 8])
            ButtonEnabled.configure(relief=SUNKEN, bg=rgb((158, 46, 34)))

        Checking()

        self.FoodEater.Protocol(Destroy)
        self.FoodEater.loop()


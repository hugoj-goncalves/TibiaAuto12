import time

from Conf.Hotkeys import Hotkey

from Core.GUI import *
from Core.GUISetter import GUISetter
from Core.ThreadManager import ThreadManager

GUIChanges = []

EnabledFoodEater = False
ThreadStarted = False

class FoodEater:
    def __init__(self, root, MOUSE_OPTION):
        self.FoodEater = GUI('FoodEater', 'Module: Food Eater')
        self.FoodEater.DefaultWindow('AutoHeal2', [306, 372], [1.2, 2.29])
        self.Setter = GUISetter("FoodEaterLoader")
        self.SendToClient = Hotkey(MOUSE_OPTION)
        self.ThreadManager = ThreadManager("ThreadFoodEater")

        HotkeyFoodEater, InitiatedHotkeyFoodEater = self.Setter.Variables.Str('HotkeyFoodEater')

        def SetFoodEater():
            global EnabledFoodEater
            global ThreadStarted
            if not EnabledFoodEater:
                EnabledFoodEater = True
                ButtonEnabled.configure(text='FoodEater: ON')
                Checking()
                if not ThreadStarted:
                    ThreadStarted = True
                    self.ThreadManager.NewThread(ScanFoodEater)
                else:
                    self.ThreadManager.UnPauseThread()
            else:
                EnabledFoodEater = False
                ButtonEnabled.configure(text='FoodEater: OFF')
                Checking()
                self.ThreadManager.PauseThread()


        def ScanFoodEater():
            while EnabledFoodEater:
                self.SendToClient.Press(HotkeyFoodEater.get())
                print("Pressed ", HotkeyFoodEater.get(), " To Eat Food")
                time.sleep(4*60)

        def Checking():
            HotkeyOption = self.FoodEater.addOption(HotkeyFoodEater, self.SendToClient.Hotkeys, [145, 170], 10)
            if EnabledFoodEater:
                HotkeyOption.configure(state='disabled')
            else:
                HotkeyOption.configure(state='normal')

        def CheckingGUI(Init, Get, Name):
            if Get != Init:
                GUIChanges.append((Name, Get))

        def Destroy():
            print('FoodEater Destroy called!')
            CheckingGUI(InitiatedHotkeyFoodEater, HotkeyFoodEater.get(), 'HotkeyFoodEater')

            self.FoodEater.destroyWindow()

        self.FoodEater.addButton('Ok', Destroy, [84, 29, 130, 504], [5, 50, 8])

        global EnabledFoodEater
        if not EnabledFoodEater:
            ButtonEnabled = self.FoodEater.addButton('FoodEater: OFF', SetFoodEater, [328, 29, 12, 469],
                                                       [5, 17, 8])
        else:
            ButtonEnabled = self.FoodEater.addButton('FoodEater: ON', SetFoodEater, [328, 29, 12, 469],
                                                       [5, 17, 8])

        Checking()

        self.FoodEater.Protocol(Destroy)
        self.FoodEater.loop()


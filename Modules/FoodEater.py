import time

from Conf.Hotkeys import Hotkey

from Core.GUI import *
from Core.GUISetter import GUISetter
from Core.ThreadManager import AllThreads, ThreadManager

GUIChanges = []

EnabledFoodEater = False

class FoodEater:
    def ScanFoodEater(self, wait):
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

        def SetFoodEater():
            global EnabledFoodEater
            if not EnabledFoodEater:
                EnabledFoodEater = True
                ButtonEnabled.configure(text='FoodEater: ON')
                Checking()
                self.AllThreads.UnPauseThreads(self.ThreadName)
            else:
                EnabledFoodEater = False
                ButtonEnabled.configure(text='FoodEater: OFF')
                Checking()
                self.AllThreads.PauseThreads(self.ThreadName)

        def Checking():
            HotkeyOption = self.FoodEater.addOption(self.HotkeyFoodEater, self.SendToClient.Hotkeys, [145, 170], 10)
            if EnabledFoodEater:
                HotkeyOption.configure(state='disabled')
            else:
                HotkeyOption.configure(state='normal')

        def CheckingGUI(Init, Get, Name):
            if Get != Init:
                GUIChanges.append((Name, Get))

        def Destroy():
            print('FoodEater Destroy called!')
            CheckingGUI(self.InitiatedHotkeyFoodEater, self.HotkeyFoodEater.get(), 'HotkeyFoodEater')

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


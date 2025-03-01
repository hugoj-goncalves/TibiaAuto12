from Conf.Hotkeys import Hotkey
from Conf.Constants import ManaColor, ManaColorFull, Percentage

from Core.GUI import *
from Core.GUIManager import *
from Core.GUISetter import GUISetter
from Core.ThreadManager import AllThreads, ThreadManager

from Engine.ScanStages import ScanStages

GUIChanges = []

EnabledAutoMana = False

class AutoMana:
    def ScanAutoMana(self, wait):
        Mana = self.Scan.ScanStages(self.ManaLocation, ManaColor, ManaColorFull)

        if Mana is None:
            Mana = 0

        if self.ManaCheckStageTwo.get():
            stage_two = self.ManaPercentageStageTwo.get()
            if stage_two > Mana or stage_two == Mana:
                self.SendToClient.Press(self.ManaHotkeyStageTwo.get())
                print("Pressed ", self.ManaHotkeyStageTwo.get())
                wait(.1)
        elif self.ManaCheckStageOne.get():
            stage_one = self.ManaPercentageStageOne.get()
            if stage_one > Mana or stage_one == Mana:
                self.SendToClient.Press(self.ManaHotkeyStageOne.get())
                print("Pressed ", self.ManaHotkeyStageOne.get())
                wait(.1)
        else:
            print("Modulo Not Configured")
            wait(1)

    def __init__(self, ManaLocation, MOUSE_OPTION):
        self.AutoMana = GUI('AutoMana', 'Module: Auto Mana')
        self.AutoMana.DefaultWindow('AutoMana', [306, 272], [1.2, 2.29])
        self.Setter = GUISetter("ManaLoader")
        self.SendToClient = Hotkey(MOUSE_OPTION)
        self.Scan = ScanStages('Mana')
        self.ManaLocation = ManaLocation

        self.AllThreads = AllThreads()
        self.ThreadName = 'ThreadAutoMana'
        if not self.AllThreads.ExistsThread(self.ThreadName):
            self.ThreadManager = ThreadManager(self.ThreadName, Managed=True, Func=self.ScanAutoMana)

        self.ManaCheckStageOne, InitiatedManaCheckStageOne = self.Setter.Variables.Bool('ManaCheckStageOne')
        self.ManaCheckStageTwo, InitiatedManaCheckStageTwo = self.Setter.Variables.Bool('ManaCheckStageTwo')

        self.ManaPercentageStageOne, InitiatedManaPercentageStageOne = self.Setter.Variables.Int('ManaPercentageStageOne')
        self.ManaHotkeyStageOne, InitiatedManaHotkeyStageOne = self.Setter.Variables.Str('ManaHotkeyStageOne')

        self.ManaPercentageStageTwo, InitiatedManaPercentageStageTwo = self.Setter.Variables.Int('ManaPercentageStageTwo')
        self.ManaHotkeyStageTwo, InitiatedManaHotkeyStageTwo = self.Setter.Variables.Str('ManaHotkeyStageTwo')

        def SetAutoMana():
            global EnabledAutoMana
            if not EnabledAutoMana:
                ButtonEnabled.configure(text='AutoMana: ON', relief=SUNKEN, bg=rgb((158, 46, 34)))
                print("AutoMana: ON")
                EnabledAutoMana = True
                CheckingButtons()
                self.AllThreads.UnPauseThreads(self.ThreadName)
            else:
                print("AutoMana: OFF")
                EnabledAutoMana = False
                CheckingButtons()
                ButtonEnabled.configure(text='AutoMana: OFF', relief=RAISED, bg=rgb((127, 17, 8)))
                self.AllThreads.PauseThreads(self.ThreadName)

        VarCheckPrint, InitiatedCheckPrint = self.Setter.Variables.Bool('CheckPrint')
        VarCheckBuff, InitiatedCheckBuff = self.Setter.Variables.Bool('CheckBuff')

        def CheckingGUI(Init, Get, Name):
            if Get != Init:
                GUIChanges.append((Name, Get))

        def Destroy():
            CheckingGUI(InitiatedCheckPrint, VarCheckPrint.get(), 'CheckPrint')
            CheckingGUI(InitiatedCheckBuff, VarCheckBuff.get(), 'CheckBuff')
            CheckingGUI(InitiatedManaCheckStageOne, self.ManaCheckStageOne.get(), 'ManaCheckStageOne')
            CheckingGUI(InitiatedManaCheckStageTwo, self.ManaCheckStageTwo.get(), 'ManaCheckStageTwo')
            CheckingGUI(InitiatedManaPercentageStageOne, self.ManaPercentageStageOne.get(), 'ManaPercentageStageOne')
            CheckingGUI(InitiatedManaHotkeyStageOne, self.ManaHotkeyStageOne.get(), 'ManaHotkeyStageOne')
            CheckingGUI(InitiatedManaPercentageStageTwo, self.ManaPercentageStageTwo.get(), 'ManaPercentageStageTwo')
            CheckingGUI(InitiatedManaHotkeyStageTwo, self.ManaHotkeyStageTwo.get(), 'ManaHotkeyStageTwo')

            if len(GUIChanges) != 0:
                for EachChange in range(len(GUIChanges)):
                    self.Setter.SetVariables.SetVar(GUIChanges[EachChange][0], GUIChanges[EachChange][1])

            self.AutoMana.destroyWindow()

        self.AutoMana.addButton('Ok', Destroy, [73, 21], [115, 240])

        ''' button enable healing '''

        global EnabledAutoMana
        if not EnabledAutoMana:
            ButtonEnabled = self.AutoMana.addButton('AutoMana: OFF', SetAutoMana, [287, 23], [11, 211])
        else:
            ButtonEnabled = self.AutoMana.addButton('AutoMana: ON', SetAutoMana, [287, 23], [11, 211])
            ButtonEnabled.configure(relief=SUNKEN, bg=rgb((158, 46, 34)))

        LabelPercentage = self.AutoMana.addLabel('% Percentage', [145, 24])
        LabelHotkey = self.AutoMana.addLabel('HotKey', [230, 24])

        CheckPrint = self.AutoMana.addCheck(VarCheckPrint, [11, 160], InitiatedCheckPrint, "Print on Tibia's screen")
        CheckPrint.configure(bg=rgb((114, 94, 48)), activebackground=rgb((114, 94, 48)), selectcolor=rgb((114, 94, 48)))
        CheckBuff = self.AutoMana.addCheck(VarCheckBuff, [11, 180], InitiatedCheckBuff, "Don't Buff")
        CheckBuff.configure(bg=rgb((114, 94, 48)), activebackground=rgb((114, 94, 48)), selectcolor=rgb((114, 94, 48)))

        StageOne = self.AutoMana.addCheck(self.ManaCheckStageOne, [17, 55], InitiatedManaCheckStageOne, "Enable Stage One")
        StageTwo = self.AutoMana.addCheck(self.ManaCheckStageTwo, [17, 105], InitiatedManaCheckStageTwo, "Enable Stage Two")

        PercentageStageOne = self.AutoMana.addOption(self.ManaPercentageStageOne, Percentage, [148, 54])
        HotkeyStageOne = self.AutoMana.addOption(self.ManaHotkeyStageOne, self.SendToClient.Hotkeys, [223, 54])

        PercentageStageTwo = self.AutoMana.addOption(self.ManaPercentageStageTwo, Percentage, [148, 104])
        HotkeyStageTwo = self.AutoMana.addOption(self.ManaHotkeyStageTwo, self.SendToClient.Hotkeys, [223, 104])

        def CheckingButtons():
            if EnabledAutoMana:
                Disable(CheckPrint)
                Disable(CheckBuff)
                Disable(StageOne)
                Disable(StageTwo)
                Disable(PercentageStageOne)
                Disable(HotkeyStageOne)
                Disable(PercentageStageTwo)
                Disable(HotkeyStageTwo)
                Disable(LabelPercentage)
                Disable(LabelHotkey)
            else:
                Enable(CheckPrint)
                Enable(CheckBuff)
                Enable(StageOne)
                Enable(StageTwo)
                Enable(PercentageStageOne)
                Enable(HotkeyStageOne)
                Enable(PercentageStageTwo)
                Enable(HotkeyStageTwo)
                Enable(LabelPercentage)
                Enable(LabelHotkey)
            ExecGUITrigger()

        CheckingButtons()

        self.AutoMana.Protocol(Destroy)
        self.AutoMana.loop()

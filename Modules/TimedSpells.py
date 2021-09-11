from time import time
from Engine.ScanStages import ScanStages
from Core.ThreadManager import AllThreads, ThreadManager
from Core.GUISetter import GUISetter
from Core.GUIManager import *
from Core.GUI import *
from Conf.Constants import ManaColor, ManaColorFull, Percentage
from Conf.Hotkeys import Hotkey


GUIChanges = []

EnabledTimedSpells = False

class TimedSpells:
    def ScanTimedSpells(self, wait):
        Mana = self.Scan.ScanStages(
            self.ManaLocation, ManaColor, ManaColorFull)

        if Mana is None:
            Mana = 0

        if self.ManaCheckStageOne.get():
            stage_one = self.ManaPercentageStageOne.get()
            if stage_one <= Mana:
                self.SendToClient.Press(self.ManaHotkeyStageOne.get())
                print("Pressed ", self.ManaHotkeyStageOne.get())
                wait(.1)

        if self.ManaCheckStageTwo.get():
            if time() - self.LastExecutionTimeStageTwo > int(self.ManaTimedStageTwo.get()):
                stage_two = self.ManaPercentageStageTwo.get()
                if stage_two <= Mana:
                    self.SendToClient.Press(self.ManaHotkeyStageTwo.get())
                    self.LastExecutionTimeStageTwo = time()
                    print("Pressed ", self.ManaHotkeyStageTwo.get())
                    wait(.1)

        if not self.ManaCheckStageOne.get() and not self.ManaCheckStageTwo.get():
            print("Modulo Not Configured")
            wait(1)

    def __init__(self, ManaLocation, MOUSE_OPTION):
        self.TimedSpells = GUI('TimedSpells', 'Module: Timed Spells')
        self.TimedSpells.DefaultWindow('TimedSpells', [306, 272], [1.2, 2.29])
        self.Setter = GUISetter("TimedSpellsLoader")
        self.SendToClient = Hotkey(MOUSE_OPTION)
        self.Scan = ScanStages('Mana')
        self.ManaLocation = ManaLocation

        self.LastExecutionTimeStageTwo = time()

        self.AllThreads = AllThreads()
        self.ThreadName = 'ThreadTimedSpells'
        if not self.AllThreads.ExistsThread(self.ThreadName):
            self.ThreadManager = ThreadManager(
                self.ThreadName, Managed=True, Func=self.ScanTimedSpells)

        self.ManaCheckStageOne, InitiatedManaCheckStageOne = self.Setter.Variables.Bool(
            'ManaCheckStageOne')
        self.ManaCheckStageTwo, InitiatedManaCheckStageTwo = self.Setter.Variables.Bool(
            'ManaCheckStageTwo')

        self.ManaPercentageStageOne, InitiatedManaPercentageStageOne = self.Setter.Variables.Int(
            'ManaPercentageStageOne')
        self.ManaHotkeyStageOne, InitiatedManaHotkeyStageOne = self.Setter.Variables.Str(
            'ManaHotkeyStageOne')

        self.ManaPercentageStageTwo, InitiatedManaPercentageStageTwo = self.Setter.Variables.Int(
            'ManaPercentageStageTwo')
        self.ManaTimedStageTwo, InitiatedManaTimedStageTwo = self.Setter.Variables.Str(
            'ManaTimedStageTwo')
        self.ManaHotkeyStageTwo, InitiatedManaHotkeyStageTwo = self.Setter.Variables.Str(
            'ManaHotkeyStageTwo')

        def SetTimedSpells():
            global EnabledTimedSpells
            if not EnabledTimedSpells:
                ButtonEnabled.configure(
                    text='TimedSpells: ON', relief=SUNKEN, bg=rgb((158, 46, 34)))
                print("TimedSpells: ON")
                EnabledTimedSpells = True
                CheckingButtons()
                self.AllThreads.UnPauseThreads(self.ThreadName)
            else:
                print("TimedSpells: OFF")
                EnabledTimedSpells = False
                CheckingButtons()
                ButtonEnabled.configure(
                    text='TimedSpells: OFF', relief=RAISED, bg=rgb((127, 17, 8)))
                self.AllThreads.PauseThreads(self.ThreadName)

        VarCheckPrint, InitiatedCheckPrint = self.Setter.Variables.Bool(
            'CheckPrint')
        VarCheckBuff, InitiatedCheckBuff = self.Setter.Variables.Bool(
            'CheckBuff')

        def CheckingGUI(Init, Get, Name):
            if Get != Init:
                GUIChanges.append((Name, Get))

        def Destroy():
            CheckingGUI(InitiatedCheckPrint, VarCheckPrint.get(), 'CheckPrint')
            CheckingGUI(InitiatedCheckBuff, VarCheckBuff.get(), 'CheckBuff')
            CheckingGUI(InitiatedManaCheckStageOne,
                        self.ManaCheckStageOne.get(), 'ManaCheckStageOne')
            CheckingGUI(InitiatedManaCheckStageTwo,
                        self.ManaCheckStageTwo.get(), 'ManaCheckStageTwo')
            CheckingGUI(InitiatedManaPercentageStageOne,
                        self.ManaPercentageStageOne.get(), 'ManaPercentageStageOne')
            CheckingGUI(InitiatedManaHotkeyStageOne,
                        self.ManaHotkeyStageOne.get(), 'ManaHotkeyStageOne')
            CheckingGUI(InitiatedManaPercentageStageTwo,
                        self.ManaPercentageStageTwo.get(), 'ManaPercentageStageTwo')
            CheckingGUI(InitiatedManaTimedStageTwo,
                        self.ManaTimedStageTwo.get(), 'ManaTimedStageTwo')
            CheckingGUI(InitiatedManaHotkeyStageTwo,
                        self.ManaHotkeyStageTwo.get(), 'ManaHotkeyStageTwo')

            if len(GUIChanges) != 0:
                for EachChange in range(len(GUIChanges)):
                    self.Setter.SetVariables.SetVar(
                        GUIChanges[EachChange][0], GUIChanges[EachChange][1])

            self.TimedSpells.destroyWindow()

        self.TimedSpells.addButton('Ok', Destroy, [73, 21], [115, 240])

        ''' button enable healing '''

        global EnabledTimedSpells
        if not EnabledTimedSpells:
            ButtonEnabled = self.TimedSpells.addButton(
                'TimedSpells: OFF', SetTimedSpells, [287, 23], [11, 211])
        else:
            ButtonEnabled = self.TimedSpells.addButton(
                'TimedSpells: ON', SetTimedSpells, [287, 23], [11, 211])
            ButtonEnabled.configure(relief=SUNKEN, bg=rgb((158, 46, 34)))

        LabelPercentage = self.TimedSpells.addLabel('% Percentage', [145, 24])
        LabelHotkey = self.TimedSpells.addLabel('HotKey', [230, 24])

        CheckPrint = self.TimedSpells.addCheck(
            VarCheckPrint, [11, 160], InitiatedCheckPrint, "Print on Tibia's screen")
        CheckPrint.configure(bg=rgb((114, 94, 48)), activebackground=rgb(
            (114, 94, 48)), selectcolor=rgb((114, 94, 48)))
        CheckBuff = self.TimedSpells.addCheck(
            VarCheckBuff, [11, 180], InitiatedCheckBuff, "Don't Buff")
        CheckBuff.configure(bg=rgb((114, 94, 48)), activebackground=rgb(
            (114, 94, 48)), selectcolor=rgb((114, 94, 48)))

        StageOne = self.TimedSpells.addCheck(self.ManaCheckStageOne, [
                                          17, 55], InitiatedManaCheckStageOne, "Enable")
        StageTwo = self.TimedSpells.addCheck(self.ManaCheckStageTwo, [
                                          17, 105], InitiatedManaCheckStageTwo, "Enable Timed")
        StageTwoTimer = self.TimedSpells.addEntry([115, 105], self.ManaTimedStageTwo, 4)

        PercentageStageOne = self.TimedSpells.addOption(
            self.ManaPercentageStageOne, Percentage, [148, 54])
        HotkeyStageOne = self.TimedSpells.addOption(
            self.ManaHotkeyStageOne, self.SendToClient.Hotkeys, [223, 54])

        PercentageStageTwo = self.TimedSpells.addOption(
            self.ManaPercentageStageTwo, Percentage, [148, 104])
        HotkeyStageTwo = self.TimedSpells.addOption(
            self.ManaHotkeyStageTwo, self.SendToClient.Hotkeys, [223, 104])

        def CheckingButtons():
            if EnabledTimedSpells:
                Disable(CheckPrint)
                Disable(CheckBuff)
                Disable(StageOne)
                Disable(StageTwo)
                Disable(PercentageStageOne)
                Disable(HotkeyStageOne)
                Disable(PercentageStageTwo)
                Disable(StageTwoTimer)
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
                Enable(StageTwoTimer)
                Enable(HotkeyStageTwo)
                Enable(LabelPercentage)
                Enable(LabelHotkey)
            ExecGUITrigger()

        CheckingButtons()

        self.TimedSpells.Protocol(Destroy)
        self.TimedSpells.loop()

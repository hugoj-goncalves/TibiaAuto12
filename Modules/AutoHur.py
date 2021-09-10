from Conf.Hotkeys import Hotkey

from Core.GUI import *
from Core.GUIManager import *
from Core.GUISetter import GUISetter
from Core.ThreadManager import AllThreads, ThreadManager

from Engine.ScanHur import ScanHur

GUIChanges = []

EnabledAutoHur = False

class AutoHur:
    def ScanAutoHur(self, wait):
        try:
            NeedHur = ScanHur(self.StatsPositions)
        except Exception:
            NeedHur = False
            pass
        if NeedHur:
            self.SendToClient.Press(self.VarHotkeyHur.get())
            print("Hur Pressed ", self.VarHotkeyHur.get())
            wait(10)
        wait(.15)

    def __init__(self, StatsPositions, MOUSE_OPTION):
        self.StatsPositions = StatsPositions

        self.AutoHur = GUI('AutoHur', 'Module: Auto Hur')
        self.AutoHur.DefaultWindow('AutoHur', [224, 258], [1.2, 2.29])
        self.Setter = GUISetter("HurLoader")
        self.SendToClient = Hotkey(MOUSE_OPTION)

        self.AllThreads = AllThreads()
        self.ThreadName = 'ThreadAutoHur'
        if not self.AllThreads.ExistsThread(self.ThreadName):
            self.ThreadManager = ThreadManager(self.ThreadName, Managed=True, Func=self.ScanAutoHur)

        self.VarHotkeyHur, self.InitiatedHotkeyHur = self.Setter.Variables.Str('HotkeyHur')
        VarCheckPrint, InitiatedCheckPrint = self.Setter.Variables.Bool('CheckPrint')
        VarCheckBuff, InitiatedCheckBuff = self.Setter.Variables.Bool('CheckBuff')
        CheckLowMana, InitiatedCheckLowMana = self.Setter.Variables.Bool('CheckLowMana')

        def SetAutoHur():
            global EnabledAutoHur
            if not EnabledAutoHur:
                EnabledAutoHur = True
                ButtonEnabled.configure(text='AutoHur: ON', relief=SUNKEN, bg=rgb((158, 46, 34)))
                print("AutoHur: ON")
                CheckingButtons()
                self.AllThreads.UnPauseThreads(self.ThreadName)
            else:
                EnabledAutoHur = False
                CheckingButtons()
                print("AutoHur: OFF")
                ButtonEnabled.configure(text='AutoHur: OFF', relief=RAISED, bg=rgb((127, 17, 8)))
                self.AllThreads.PauseThreads(self.ThreadName)

        def Recapture():
            print("recapture")

        def CheckingGUI(Init, Get, Name):
            if Get != Init:
                GUIChanges.append((Name, Get))

        def Destroy():
            CheckingGUI(InitiatedCheckPrint, VarCheckPrint.get(), 'CheckPrint')
            CheckingGUI(InitiatedCheckBuff, VarCheckBuff.get(), 'CheckBuff')
            CheckingGUI(self.InitiatedHotkeyHur, self.VarHotkeyHur.get(), 'HotkeyHur')
            CheckingGUI(InitiatedCheckLowMana, CheckLowMana.get(), 'CheckLowMana')

            if len(GUIChanges) != 0:
                for EachChange in range(len(GUIChanges)):
                    self.Setter.SetVariables.SetVar(GUIChanges[EachChange][0], GUIChanges[EachChange][1])

            self.AutoHur.destroyWindow()

        self.AutoHur.addButton('Ok', Destroy, [73, 21], [75, 225])

        global EnabledAutoHur
        if not EnabledAutoHur:
            ButtonEnabled = self.AutoHur.addButton('AutoHur: OFF', SetAutoHur, [203, 23], [11, 195])
        else:
            ButtonEnabled = self.AutoHur.addButton('AutoHur: ON', SetAutoHur, [203, 23], [11, 195])
            ButtonEnabled.configure(relief=SUNKEN, bg=rgb((158, 46, 34)))

        CheckPrint = self.AutoHur.addCheck(VarCheckPrint, [11, 150], InitiatedCheckPrint, "Print on Tibia's screen")
        CheckPrint.configure(bg=rgb((114, 94, 48)), activebackground=rgb((114, 94, 48)), selectcolor=rgb((114, 94, 48)))
        CheckBuff = self.AutoHur.addCheck(VarCheckBuff, [11, 170], InitiatedCheckBuff, "Don't Buff")
        CheckBuff.configure(bg=rgb((114, 94, 48)), activebackground=rgb((114, 94, 48)), selectcolor=rgb((114, 94, 48)))

        ImgHur = 'images/PlayerStats/Hur.png'
        ImageID = self.AutoHur.openImage(ImgHur, [64, 64])

        ImgLabel = self.AutoHur.addLabel('Image To Search', [16, 14])
        LabelImage = self.AutoHur.addImage(ImageID, [28, 33])

        LabelHotkey = self.AutoHur.addLabel('Hotkey', [135, 48])
        HotkeyHur = self.AutoHur.addOption(self.VarHotkeyHur, self.SendToClient.Hotkeys, [113, 72], 8)

        ButtonRecapture = self.AutoHur.addButton('Recapture', Recapture, [85, 24], [20, 111])

        CheckBoxLowMana = self.AutoHur.addCheck(CheckLowMana, [118, 103], InitiatedCheckLowMana, 'Stop With\nLowMana')

        def CheckingButtons():
            if EnabledAutoHur:
                Disable(CheckPrint)
                Disable(CheckBuff)

                Disable(LabelImage)
                Disable(ImgLabel)

                Disable(ButtonRecapture)
                Disable(CheckBoxLowMana)
                Disable(LabelHotkey)
                Disable(HotkeyHur)
            else:
                Enable(CheckPrint)
                Enable(CheckBuff)

                Enable(LabelImage)
                Enable(ImgLabel)

                Enable(ButtonRecapture)
                Enable(CheckBoxLowMana)
                Enable(LabelHotkey)
                Enable(HotkeyHur)
            ExecGUITrigger()

        CheckingButtons()

        self.AutoHur.Protocol(Destroy)
        self.AutoHur.loop()


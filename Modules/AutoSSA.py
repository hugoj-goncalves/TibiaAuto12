import time
import keyboard
import pygetwindow

from Conf.Hotkeys import Hotkey
from Conf.Constants import LifeColor, LifeColorFull, Percentage, Amulets

from Core.GUI import *
from Core.GUIManager import *
from Core.GUISetter import GUISetter
from Core.ThreadManager import AllThreads, ThreadManager

from Engine.ScanAmulet import ScanAmulet

GUIChanges = []

FoundedImg = False
EnabledAutoSSA = False
WaitingForClick = False

Amulet = 'StoneSkinAmulet'
AmuletLocate = [0, 0]
MaxLen = 4

class AutoSSA:
    def ScanAutoAmulet(self, wait):
        global Amulet
        Amulet = self.NameAmulet.get()
        if self.CheckLifeBellowThan.get():
            BellowThan = self.LifeBellowThan.get()
            from Modules.AutoHeal import EnabledAutoHeal
            if EnabledAutoHeal:
                while EnabledAutoSSA and EnabledAutoHeal:
                    NoHasAmulet = ScanAmulet(self.AmuletPositions, Amulet, Amulets[Amulet]["Precision"])

                    from Modules.AutoHeal import Life
                    if NoHasAmulet and Life <= BellowThan:
                        self.Execute(wait)
            else:
                from Engine.ScanStages import ScanStages
                while EnabledAutoSSA:
                    Life = ScanStages('Life From AutoAmulet').ScanStages(self.HealthLocation, LifeColor, LifeColorFull)

                    if Life is None:
                        Life = 0

                    NoHasAmulet = ScanAmulet(self.AmuletPositions, Amulet, Amulets[Amulet]["Precision"])

                    if NoHasAmulet and Life < BellowThan:
                        self.Execute(wait)
        elif not self.CheckLifeBellowThan.get():
            while EnabledAutoSSA:
                NoHasAmulet = ScanAmulet(self.AmuletPositions, Amulet, Amulets[Amulet]["Precision"])

                if NoHasAmulet:
                    self.Execute(wait)

    def Execute(self, wait):
        if self.RadioButton.get() == 0:
            self.SendToClient.Press(self.HotkeyAmulet.get())
            print("Pressed ", self.HotkeyAmulet.get(), " To Reallocated Your Amulet")
            wait(1)
        elif self.RadioButton.get() == 1:
            try:
                X = int(self.TextEntryX.get())
                Y = int(self.TextEntryY.get())
            except:
                X = None
                Y = None
                print("Error To Get Type Of Position")
                wait(1)
            if X and Y is not None:
                if X < self.WidthScreen and Y < self.HeightScreen:
                    if self.MOUSE_OPTION == 1:
                        MousePosition = self.SendToClient.Position()
                    else:
                        MousePosition = [0, 0]

                    self.SendToClient.DragTo([X, Y], [self.AmuletPositions[0] + 16, self.AmuletPositions[1] + 16])

                    if self.MOUSE_OPTION == 1:
                        self.SendToClient.MoveTo(MousePosition[0], MousePosition[1])

                    print("Amulet Reallocated On: X =", self.AmuletPositions[0] + 16, "Y =", self.AmuletPositions[1] + 16,
                            "From: X =",
                            X, "Y =", Y)
                    wait(0.3)
                else:
                    print("Lower Resolution Than Entered")
                    wait(1)

    def __init__(self, AmuletPositions, HealthLocation, MOUSE_OPTION, ItemsPath):
        self.AutoSSA = GUI('AutoSSA', 'Module: Auto SSA')
        self.AutoSSA.DefaultWindow('AutoAmulet', [306, 397], [1.2, 2.29])
        self.Setter = GUISetter("AmuletLoader")
        self.SendToClient = Hotkey(MOUSE_OPTION)
        self.AmuletPositions = AmuletPositions
        self.HealthLocation = HealthLocation
        self.MOUSE_OPTION = MOUSE_OPTION

        self.AllThreads = AllThreads()
        self.ThreadName = 'ThreadAutoAmulet'
        if not self.AllThreads.ExistsThread(self.ThreadName):
            self.ThreadManager = ThreadManager(self.ThreadName, Managed=True, Func=self.ScanAutoMana)

        def SetAutoAmulet():
            global EnabledAutoSSA
            if not EnabledAutoSSA:
                EnabledAutoSSA = True
                ButtonEnabled.configure(text='AutoSSA: ON', relief=SUNKEN, bg=rgb((158, 46, 34)))
                print("AutoSSA: ON")
                global Amulet
                Amulet = self.NameAmulet.get()
                Checking()
                CheckingButtons()
                self.AllThreads.UnPauseThreads(self.ThreadName)
            else:
                EnabledAutoSSA = False
                ButtonEnabled.configure(text='AutoSSA: OFF', relief=RAISED, bg=rgb((127, 17, 8)))
                print("AutoSSA: OFF")
                Checking()
                CheckingButtons()
                self.AllThreads.PauseThreads(self.ThreadName)

        def Recapture():
            global WaitingForClick, Amulet
            WaitingForClick = True
            Amulet = self.NameAmulet.get()
            AutoSSAWindow = pygetwindow.getWindowsWithTitle("Module: Auto SSA")[0]
            TibiaAuto = pygetwindow.getWindowsWithTitle("TibiaAuto V12")[0]
            AutoSSAWindowX = self.AutoSSA.PositionOfWindow('X')
            AutoSSAWindowY = self.AutoSSA.PositionOfWindow('Y')
            time.sleep(0.1)
            TibiaAuto.minimize()
            AutoSSAWindow.minimize()
            Invisible = GUI('InvisibleWindow', 'InvisibleWindow')
            Invisible.InvisibleWindow('Recapture')
            while WaitingForClick:
                X, Y = GetPosition()
                if keyboard.is_pressed("c"):
                    sX, sY = GetPosition()
                    time.sleep(0.03)
                    from Core.HookWindow import SaveImage
                    SaveImage(ItemsPath + 'Amulets/' + Amulet + '.png', Region=(sX - 6, sY - 28, sX + 6, sY - 16))
                    WaitingForClick = False
                    Invisible.destroyWindow()
                    TibiaAuto.maximize()
                    time.sleep(0.04)
                    AutoSSAWindow.maximize()
                    AutoSSAWindow.moveTo(AutoSSAWindowX, AutoSSAWindowY)
                    break
                Invisible.UpdateWindow(X, Y)

        def AddNewAmulet():
            print('Option In Development...')

        def CheckClick():
            Checking()

        def ReturnGetPosition():
            global WaitingForClick
            WaitingForClick = True
            AutoSSAWindow = pygetwindow.getWindowsWithTitle("Module: Auto SSA")[0]
            TibiaAuto = pygetwindow.getWindowsWithTitle("TibiaAuto V12")[0]
            AutoSSAWindowX = self.AutoSSA.PositionOfWindow('X')
            AutoSSAWindowY = self.AutoSSA.PositionOfWindow('Y')
            time.sleep(0.1)
            TibiaAuto.minimize()
            AutoSSAWindow.minimize()
            Invisible = GUI('InvisibleWindow', 'InvisibleWindow')
            Invisible.InvisibleWindow('GetPosition')
            while WaitingForClick:
                X, Y = GetPosition()
                if keyboard.is_pressed("c"):
                    X, Y = GetPosition()
                    WaitingForClick = False
                    print(f"Your Click Is Located In: [X: {X}, Y: {Y}]")
                    self.TextEntryX.set(X)
                    self.TextEntryY.set(Y)
                    Invisible.destroyWindow()
                    TibiaAuto.maximize()
                    time.sleep(0.08)
                    AutoSSAWindow.maximize()
                    AutoSSAWindow.moveTo(AutoSSAWindowX, AutoSSAWindowY)
                    break
                Invisible.UpdateWindow(X, Y)

        def ValidateEntryX(*args):
            s = self.TextEntryX.get()
            if len(s) > MaxLen:
                if not s[-1].isdigit():
                    self.TextEntryX.set(s[:-1])
                else:
                    self.TextEntryX.set(s[:MaxLen])

        def ValidateEntryY(*args):
            s = self.TextEntryY.get()
            if len(s) > MaxLen:
                if not s[-1].isdigit():
                    self.TextEntryY.set(s[:-1])
                else:
                    self.TextEntryY.set(s[:MaxLen])

        self.WidthScreen, self.HeightScreen = pyautogui.size()

        VarCheckPrint, InitiatedCheckPrint = self.Setter.Variables.Bool('CheckPrint')
        VarCheckBuff, InitiatedCheckBuff = self.Setter.Variables.Bool('CheckBuff')

        self.RadioButton, InitiatedRadioButton = self.Setter.Variables.Int('RadioButton')

        self.NameAmulet, InitiatedNameAmulet = self.Setter.Variables.Str('NameAmulet')
        self.HotkeyAmulet, InitiatedHotkeyAmulet = self.Setter.Variables.Str('HotkeyAmulet')

        self.TextEntryX, InitiatedTextEntryX = self.Setter.Variables.Str('TextEntryX')
        self.TextEntryY, InitiatedTextEntryY = self.Setter.Variables.Str('TextEntryY')

        self.CheckLifeBellowThan, InitiatedLifeBellowThan = self.Setter.Variables.Bool('LifeBellowThan')
        self.LifeBellowThan, InitiatedBellowThan = self.Setter.Variables.Int('BellowThan')

        def CheckingGUI(Init, Get, Name):
            if Get != Init:
                GUIChanges.append((Name, Get))

        def Destroy():
            CheckingGUI(InitiatedCheckPrint, VarCheckPrint.get(), 'CheckPrint')
            CheckingGUI(InitiatedCheckBuff, VarCheckBuff.get(), 'CheckBuff')
            CheckingGUI(InitiatedRadioButton, self.RadioButton.get(), 'RadioButton')
            CheckingGUI(InitiatedNameAmulet, self.NameAmulet.get(), 'NameAmulet')
            CheckingGUI(InitiatedHotkeyAmulet, self.HotkeyAmulet.get(), 'HotkeyAmulet')
            CheckingGUI(InitiatedTextEntryX, self.TextEntryX.get(), 'TextEntryX')
            CheckingGUI(InitiatedTextEntryY, self.TextEntryY.get(), 'TextEntryY')
            CheckingGUI(InitiatedLifeBellowThan, self.CheckLifeBellowThan.get(), 'LifeBellowThan')
            CheckingGUI(InitiatedBellowThan, self.LifeBellowThan.get(), 'BellowThan')

            if len(GUIChanges) != 0:
                for EachChange in range(len(GUIChanges)):
                    self.Setter.SetVariables.SetVar(GUIChanges[EachChange][0], GUIChanges[EachChange][1])

            self.AutoSSA.destroyWindow()

        self.AutoSSA.addButton('Ok', Destroy, [73, 21], [115, 365])

        global EnabledAutoSSA
        if not EnabledAutoSSA:
            ButtonEnabled = self.AutoSSA.addButton('AutoSSA: OFF', SetAutoAmulet, [287, 23], [11, 336])
        else:
            ButtonEnabled = self.AutoSSA.addButton('AutoSSA: ON', SetAutoAmulet, [287, 23], [11, 336])
            ButtonEnabled.configure(relief=SUNKEN, bg=rgb((158, 46, 34)))

        CheckPrint = self.AutoSSA.addCheck(VarCheckPrint, [11, 285], InitiatedCheckPrint, "Print on Tibia's screen")
        CheckPrint.configure(bg=rgb((114, 94, 48)), activebackground=rgb((114, 94, 48)), selectcolor=rgb((114, 94, 48)))
        CheckBuff = self.AutoSSA.addCheck(VarCheckBuff, [11, 305], InitiatedCheckBuff, "Don't Buff")
        CheckBuff.configure(bg=rgb((114, 94, 48)), activebackground=rgb((114, 94, 48)), selectcolor=rgb((114, 94, 48)))

        BackImage = 'images/Fundo.png'
        Back = self.AutoSSA.openImage(BackImage, [150, 45])

        AmuletImages = []
        AmuletName = []
        for NameOfCurrentAmulet in Amulets:
            CurrentAmuletName = ItemsPath + 'Amulets/' + NameOfCurrentAmulet + '.png'
            CurrentAmuletImage = self.AutoSSA.openImage(CurrentAmuletName, [64, 64])

            AmuletImages.append(CurrentAmuletImage)
            AmuletName.append(NameOfCurrentAmulet)

        ImgLabel = self.AutoSSA.addLabel('Image To Search', [16, 22])

        def UpdateImg():
            for XAmulet in Amulets:
                if self.NameAmulet.get() == XAmulet:
                    self.AutoSSA.addImage(AmuletImages[AmuletName.index(XAmulet)], [28, 43])

            global Amulet
            Amulet = self.NameAmulet.get()

        UpdateImg()

        self.WidthScreen, self.HeightScreen = self.SendToClient.MainWindowSize()

        AmuletLabel = self.AutoSSA.addLabel('Select Name Of Amulet', [135, 55])
        OptionNameAmulet = self.AutoSSA.addOption(self.NameAmulet, Amulets, [120, 80], width=21)

        ButtonAddNewAmulet = self.AutoSSA.addButton('Add New Amulet', AddNewAmulet, [167, 24], [120, 115])

        ButtonRecapture = self.AutoSSA.addButton('Recapture', Recapture, [88, 24], [22, 115])

        DescLabel = self.AutoSSA.addLabel('', [150, 140])

        RButton1 = self.AutoSSA.addRadio('Hotkey', self.RadioButton, 0, [22, 155], CheckClick)
        RButton2 = self.AutoSSA.addRadio('Position', self.RadioButton, 1, [22, 175], CheckClick)

        CheckBoxLifeBellowThan = self.AutoSSA.addCheck(self.CheckLifeBellowThan, [60, 210], InitiatedLifeBellowThan,
                                                       'Use Only If Life Is Bellow Than')
        LabelLifeBellowThan = self.AutoSSA.addLabel('Life <= ', [90, 245])
        PercentageLifeBellowThan = self.AutoSSA.addOption(self.LifeBellowThan, Percentage, [140, 240])

        def Checking():
            global FoundedImg, Amulet
            if self.RadioButton.get() == 0:
                DescLabel.configure(text='Hotkey To Press')
                self.AutoSSA.addImage(Back, [130, 165])
                FoundedImg = False
                HotkeyOption = self.AutoSSA.addOption(self.HotkeyAmulet, self.SendToClient.Hotkeys, [145, 170], 10)
                if EnabledAutoSSA:
                    HotkeyOption.configure(state='disabled')
                else:
                    HotkeyOption.configure(state='normal')
            elif self.RadioButton.get() == 1:
                DescLabel.configure(text='Position To Search')
                self.AutoSSA.addImage(Back, [120, 165])
                FoundedImg = False

                ButtonGetPosition = self.AutoSSA.addButton('GetPosition', ReturnGetPosition, [80, 29], [195, 173])

                LabelX = self.AutoSSA.addLabel('X:', [135, 165])
                EntryX = self.AutoSSA.addEntry([150, 165], self.TextEntryX, width=4)
                self.TextEntryX.trace("w", ValidateEntryX)
                LabelY = self.AutoSSA.addLabel('Y:', [135, 185])
                EntryY = self.AutoSSA.addEntry([150, 185], self.TextEntryY, width=4)
                self.TextEntryY.trace("w", ValidateEntryY)
                if EnabledAutoSSA:
                    ButtonGetPosition.configure(state='disabled')

                    LabelX.configure(state='disabled')
                    EntryX.configure(state='disabled')
                    LabelY.configure(state='disabled')
                    EntryY.configure(state='disabled')
                else:
                    ButtonGetPosition.configure(state='normal')

                    LabelX.configure(state='normal')
                    EntryX.configure(state='normal')
                    LabelY.configure(state='normal')
                    EntryY.configure(state='normal')
            if not self.CheckLifeBellowThan.get():
                LabelLifeBellowThan.configure(state='disabled')
                PercentageLifeBellowThan.configure(state='disabled')
            elif self.CheckLifeBellowThan.get():
                LabelLifeBellowThan.configure(state='normal')
                PercentageLifeBellowThan.configure(state='normal')

        def CheckingButtons():
            if EnabledAutoSSA:
                Disable(CheckPrint)
                Disable(CheckBuff)

                Disable(DescLabel)
                Disable(ImgLabel)
                Disable(ButtonRecapture)
                Disable(ButtonAddNewAmulet)

                Disable(RButton1)
                Disable(RButton2)
                Disable(AmuletLabel)
                Disable(OptionNameAmulet)

                Disable(CheckBoxLifeBellowThan)
                Disable(LabelLifeBellowThan)
                Disable(PercentageLifeBellowThan)
            else:
                Enable(CheckPrint)
                Enable(CheckBuff)

                Enable(DescLabel)
                Enable(ImgLabel)
                Enable(ButtonRecapture)
                Enable(ButtonAddNewAmulet)

                Enable(RButton1)
                Enable(RButton2)
                Enable(AmuletLabel)
                Enable(OptionNameAmulet)

                Enable(CheckBoxLifeBellowThan)

                if not self.CheckLifeBellowThan.get():
                    Disable(LabelLifeBellowThan)
                    Disable(PercentageLifeBellowThan)
                elif self.CheckLifeBellowThan.get():
                    Enable(LabelLifeBellowThan)
                    Enable(PercentageLifeBellowThan)
            ExecGUITrigger()

        def ConstantVerify():
            if not EnabledAutoSSA:
                if not self.CheckLifeBellowThan.get():
                    Disable(LabelLifeBellowThan)
                    Disable(PercentageLifeBellowThan)
                elif self.CheckLifeBellowThan.get():
                    Enable(LabelLifeBellowThan)
                    Enable(PercentageLifeBellowThan)

                if self.NameAmulet.get() != Amulet:
                    UpdateImg()

                ExecGUITrigger()

            self.AutoSSA.After(200, ConstantVerify)

        Checking()
        CheckingButtons()

        ConstantVerify()

        self.AutoSSA.Protocol(Destroy)
        self.AutoSSA.loop()

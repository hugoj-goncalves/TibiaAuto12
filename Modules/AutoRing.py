import time
import keyboard
import pygetwindow

from Conf.Hotkeys import Hotkey
from Conf.Constants import LifeColor, LifeColorFull, Percentage, Rings

from Core.GUI import *
from Core.GUIManager import *
from Core.GUISetter import GUISetter
from Core.ThreadManager import AllThreads, ThreadManager

from Engine.ScanRing import ScanRing

GUIChanges = []

FoundedImg = False
EnabledAutoRing = False
WaitingForClick = False

Ring = 'MightRing'
RingLocate = [0, 0]
MaxLen = 4
RingsPath = None

class AutoRing:
    def ScanAutoRing(self, wait):
        global Ring
        Ring = self.NameRing.get()
        if self.CheckLifeBellowThan.get():
            BellowThan = self.LifeBellowThan.get()
            from Modules.AutoHeal import EnabledAutoHeal
            if EnabledAutoHeal:
                while EnabledAutoRing and EnabledAutoHeal:
                    NoHasRing = ScanRing(self.RingPositions)

                    from Modules.AutoHeal import Life
                    if NoHasRing and Life <= BellowThan:
                        self.Execute(wait)
            else:
                from Engine.ScanStages import ScanStages
                while EnabledAutoRing:
                    Life = ScanStages('Life From AutoRing').ScanStages(self.HealthLocation, LifeColor, LifeColorFull)

                    if Life is None:
                        Life = 0

                    NoHasRing = ScanRing(self.RingPositions)

                    if NoHasRing and Life < BellowThan:
                        self.Execute(wait)
        else:
            while EnabledAutoRing:
                NoHasRing = ScanRing(self.RingPositions)

                if NoHasRing:
                    self.Execute(wait)

    def Execute(self, wait):
        if self.RadioButton.get() == 0:
            self.SendToClient.Press(self.HotkeyRing.get())
            print("Pressed ", self.HotkeyRing.get(), " To Reallocated Your Ring")
            wait(1)
        elif self.RadioButton.get() == 1:
            try:
                X = int(self.TextEntryX.get())
                Y = int(self.TextEntryY.get())
            except Exception:
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

                    self.SendToClient.DragTo([X, Y], [self.RingPositions[0] + 16, self.RingPositions[1] + 16])

                    if self.MOUSE_OPTION == 1:
                        self.SendToClient.MoveTo(MousePosition[0], MousePosition[1])

                    print("Ring Reallocated On: X =", self.RingPositions[0] + 16, "Y =", self.RingPositions[1] + 16,
                            "From: X =",
                            X, "Y =", Y)
                    wait(0.3)
                else:
                    print("Lower Resolution Than Entered")
                    wait(1)


    def __init__(self, RingPositions, HealthLocation, MOUSE_OPTION, ItemsPath):
        self.AutoRing = GUI('AutoRing', 'Module: Auto Ring')
        self.AutoRing.DefaultWindow('AutoRing', [306, 397], [1.2, 2.29])
        self.Setter = GUISetter("RingLoader")
        self.SendToClient = Hotkey(MOUSE_OPTION)
        self.RingPositions = RingPositions
        self.HealthLocation = HealthLocation
        self.MOUSE_OPTION = MOUSE_OPTION

        self.AllThreads = AllThreads()
        self.ThreadName = 'ThreadAutoRing'
        if not self.AllThreads.ExistsThread(self.ThreadName):
            self.ThreadManager = ThreadManager(self.ThreadName, Managed=True, Func=self.ScanAutoRing)

        def SetAutoRing():
            global EnabledAutoRing
            if not EnabledAutoRing:
                EnabledAutoRing = True
                ButtonEnabled.configure(text='AutoRing: ON', relief=SUNKEN, bg=rgb((158, 46, 34)))
                print("AutoRing: ON")
                global Ring
                Ring = self.NameRing.get()
                Checking()
                CheckingButtons()
                self.AllThreads.UnPauseThreads(self.ThreadName)
            else:
                EnabledAutoRing = False
                print('AutoRing: OFF')
                ButtonEnabled.configure(text='AutoRing: OFF', relief=RAISED, bg=rgb((127, 17, 8)))
                Checking()
                CheckingButtons()
                self.AllThreads.PauseThreads(self.ThreadName)

        def Recapture():
            global WaitingForClick, Ring
            WaitingForClick = True
            Ring = self.NameRing.get()
            AutoRingWindow = pygetwindow.getWindowsWithTitle("Module: Auto Ring")[0]
            TibiaAuto = pygetwindow.getWindowsWithTitle("TibiaAuto V12")[0]
            AutoRingWindowX = self.AutoRing.PositionOfWindow('X')
            AutoRingWindowY = self.AutoRing.PositionOfWindow('Y')
            time.sleep(0.1)
            TibiaAuto.minimize()
            AutoRingWindow.minimize()
            Invisible = GUI('InvisibleWindow', 'InvisibleWindow')
            Invisible.InvisibleWindow('Recapture')
            while WaitingForClick:
                X, Y = GetPosition()
                if keyboard.is_pressed("c"):
                    sX, sY = GetPosition()
                    time.sleep(0.03)
                    from Core.HookWindow import SaveImage
                    SaveImage(ItemsPath + 'Rings/' + Ring + '.png', Region=(sX - 6, sY - 28, sX + 6, sY - 16))
                    WaitingForClick = False
                    Invisible.destroyWindow()
                    TibiaAuto.maximize()
                    time.sleep(0.04)
                    AutoRingWindow.maximize()
                    AutoRingWindow.moveTo(AutoRingWindowX, AutoRingWindowY)

                    UpdateImg()
                    break
                Invisible.UpdateWindow(X, Y)

        def AddNewAmulet():
            print('Option In Development...')

        def CheckClick():
            Checking()

        def ReturnGetPosition():
            global WaitingForClick
            WaitingForClick = True
            AutoRingWindow = pygetwindow.getWindowsWithTitle("Module: Auto Ring")[0]
            TibiaAuto = pygetwindow.getWindowsWithTitle("TibiaAuto V12")[0]
            AutoRingWindowX = self.AutoRing.PositionOfWindow('X')
            AutoRingWindowY = self.AutoRing.PositionOfWindow('Y')
            time.sleep(0.1)
            TibiaAuto.minimize()
            AutoRingWindow.minimize()
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
                    AutoRingWindow.maximize()
                    AutoRingWindow.moveTo(AutoRingWindowX, AutoRingWindowY)
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

        VarCheckPrint, InitiatedCheckPrint = self.Setter.Variables.Bool('CheckPrint')
        VarCheckBuff, InitiatedCheckBuff = self.Setter.Variables.Bool('CheckBuff')

        self.RadioButton, InitiatedRadioButton = self.Setter.Variables.Int('RadioButton')

        self.NameRing, InitiatedNameRing = self.Setter.Variables.Str('NameRing')
        self.HotkeyRing, InitiatedHotkeyRing = self.Setter.Variables.Str('HotkeyRing')

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
            CheckingGUI(InitiatedNameRing, self.NameRing.get(), 'NameRing')
            CheckingGUI(InitiatedHotkeyRing, self.HotkeyRing.get(), 'HotkeyRing')
            CheckingGUI(InitiatedTextEntryX, self.TextEntryX.get(), 'TextEntryX')
            CheckingGUI(InitiatedTextEntryY, self.TextEntryY.get(), 'TextEntryY')
            CheckingGUI(InitiatedLifeBellowThan, self.CheckLifeBellowThan.get(), 'LifeBellowThan')
            CheckingGUI(InitiatedBellowThan, self.LifeBellowThan.get(), 'BellowThan')

            if len(GUIChanges) != 0:
                for EachChange in range(len(GUIChanges)):
                    self.Setter.SetVariables.SetVar(GUIChanges[EachChange][0], GUIChanges[EachChange][1])

            self.AutoRing.destroyWindow()

        self.AutoRing.addButton('Ok', Destroy, [73, 21], [115, 365])

        global EnabledAutoRing
        if not EnabledAutoRing:
            ButtonEnabled = self.AutoRing.addButton('AutoRing: OFF', SetAutoRing, [287, 23], [11, 336])
        else:
            ButtonEnabled = self.AutoRing.addButton('AutoRing: ON', SetAutoRing, [287, 23], [11, 336])
            ButtonEnabled.configure(relief=SUNKEN, bg=rgb((158, 46, 34)))

        CheckPrint = self.AutoRing.addCheck(VarCheckPrint, [11, 285], InitiatedCheckPrint, "Print on Tibia's screen")
        CheckPrint.configure(bg=rgb((114, 94, 48)), activebackground=rgb((114, 94, 48)), selectcolor=rgb((114, 94, 48)))
        CheckBuff = self.AutoRing.addCheck(VarCheckBuff, [11, 305], InitiatedCheckBuff, "Don't Buff")
        CheckBuff.configure(bg=rgb((114, 94, 48)), activebackground=rgb((114, 94, 48)), selectcolor=rgb((114, 94, 48)))

        BackImage = 'images/Fundo.png'
        Back = self.AutoRing.openImage(BackImage, [150, 45])

        RingImages = []
        RingName = []
        for NameOfCurrentRing in Rings:
            CurrentRingName = ItemsPath + 'Rings/' + NameOfCurrentRing + '.png'
            CurrentRingImage = self.AutoRing.openImage(CurrentRingName, [64, 64])

            RingImages.append(CurrentRingImage)
            RingName.append(NameOfCurrentRing)

        ImgLabel = self.AutoRing.addLabel('Image To Search', [16, 22])

        def UpdateImg():
            for XRing in Rings:
                if self.NameRing.get() == XRing:
                    self.AutoRing.addImage(RingImages[RingName.index(XRing)], [28, 43])

            global Ring
            Ring = self.NameRing.get()

        UpdateImg()

        self.WidthScreen, self.HeightScreen = self.SendToClient.MainWindowSize()

        RingLabel = self.AutoRing.addLabel('Select Name Of Ring', [135, 55])
        OptionNameRing = self.AutoRing.addOption(self.NameRing, Rings, [120, 80], width=21)

        ButtonAddNewRing = self.AutoRing.addButton('Add New Ring', AddNewAmulet, [167, 24], [120, 115])

        ButtonRecapture = self.AutoRing.addButton('Recapture', Recapture, [88, 24], [22, 115])

        DescLabel = self.AutoRing.addLabel('', [150, 140])

        RButton1 = self.AutoRing.addRadio('Hotkey', self.RadioButton, 0, [22, 155], CheckClick)
        RButton2 = self.AutoRing.addRadio('Position', self.RadioButton, 1, [22, 175], CheckClick)

        CheckBoxLifeBellowThan = self.AutoRing.addCheck(self.CheckLifeBellowThan, [60, 210], InitiatedLifeBellowThan,
                                                        'Use Only If Life Is Bellow Than')
        LabelLifeBellowThan = self.AutoRing.addLabel('Life <= ', [90, 245])
        PercentageLifeBellowThan = self.AutoRing.addOption(self.LifeBellowThan, Percentage, [140, 240])

        def Checking():
            global FoundedImg, Ring
            if self.RadioButton.get() == 0:
                DescLabel.configure(text='Hotkey To Press')
                self.AutoRing.addImage(Back, [130, 165])
                FoundedImg = False
                HotkeyOption = self.AutoRing.addOption(self.HotkeyRing, self.SendToClient.Hotkeys, [145, 170], 10)
                if EnabledAutoRing:
                    Disable(HotkeyOption)
                else:
                    Enable(HotkeyOption)
            elif self.RadioButton.get() == 1:
                DescLabel.configure(text='Position To Search')
                self.AutoRing.addImage(Back, [120, 165])
                FoundedImg = False

                ButtonGetPosition = self.AutoRing.addButton('GetPosition', ReturnGetPosition, [80, 29], [195, 173])

                LabelX = self.AutoRing.addLabel('X:', [135, 165])
                EntryX = self.AutoRing.addEntry([150, 165], self.TextEntryX, width=4)
                self.TextEntryX.trace("w", ValidateEntryX)
                LabelY = self.AutoRing.addLabel('Y:', [135, 185])
                EntryY = self.AutoRing.addEntry([150, 185], self.TextEntryY, width=4)
                self.TextEntryY.trace("w", ValidateEntryY)
                if EnabledAutoRing:
                    Disable(ButtonGetPosition)

                    Disable(LabelX)
                    Disable(EntryX)
                    Disable(LabelY)
                    Disable(EntryY)
                else:
                    Enable(ButtonGetPosition)

                    Enable(LabelX)
                    Enable(EntryX)
                    Enable(LabelY)
                    Enable(EntryY)
            if not self.CheckLifeBellowThan.get():
                Disable(LabelLifeBellowThan)
                Disable(PercentageLifeBellowThan)
            elif self.CheckLifeBellowThan.get():
                Enable(LabelLifeBellowThan)
                Enable(PercentageLifeBellowThan)
            ExecGUITrigger()

        def CheckingButtons():
            if EnabledAutoRing:
                Disable(CheckPrint)
                Disable(CheckBuff)

                Disable(DescLabel)
                Disable(ImgLabel)
                Disable(ButtonRecapture)
                Disable(ButtonAddNewRing)

                Disable(RButton1)
                Disable(RButton2)
                Disable(RingLabel)
                Disable(OptionNameRing)

                Disable(CheckBoxLifeBellowThan)
                Disable(LabelLifeBellowThan)
                Disable(PercentageLifeBellowThan)
            else:
                Enable(CheckPrint)
                Enable(CheckBuff)

                Enable(DescLabel)
                Enable(ImgLabel)
                Enable(ButtonRecapture)
                Enable(ButtonAddNewRing)

                Enable(RButton1)
                Enable(RButton2)
                Enable(RingLabel)
                Enable(OptionNameRing)

                Enable(CheckBoxLifeBellowThan)

                if not self.CheckLifeBellowThan.get():
                    Disable(LabelLifeBellowThan)
                    Disable(PercentageLifeBellowThan)
                elif self.CheckLifeBellowThan.get():
                    Enable(LabelLifeBellowThan)
                    Enable(PercentageLifeBellowThan)
            ExecGUITrigger()

        def ConstantVerify():
            if not EnabledAutoRing:
                if not self.CheckLifeBellowThan.get():
                    Disable(LabelLifeBellowThan)
                    Disable(PercentageLifeBellowThan)
                elif self.CheckLifeBellowThan.get():
                    Enable(LabelLifeBellowThan)
                    Enable(PercentageLifeBellowThan)

                if self.NameRing.get() != Ring:
                    UpdateImg()

                ExecGUITrigger()

            self.AutoRing.After(200, ConstantVerify)

        Checking()
        CheckingButtons()

        ConstantVerify()

        self.AutoRing.Protocol(Destroy)
        self.AutoRing.loop()

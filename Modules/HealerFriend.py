from Conf.Hotkeys import Hotkey

from Core.GUI import *
from Core.GUISetter import GUISetter
from Core.ThreadManager import AllThreads, ThreadManager
from Core.HookWindow import LocateCenterImage, SaveImage

from Engine.ScanStages import ScanStages

GUIChanges = []

EnabledHealerFriend = False

class HealerFriend:
    def ScanTarget(self, BattlePosition, Target):
        HasTarget = [0, 0]

        HasTarget[0], HasTarget[1] = LocateCenterImage('images/Targets/Players/Names/' + Target + '.png', Precision=0.86, LeftHandle=True, Region=(
            BattlePosition[0], BattlePosition[1], BattlePosition[2], BattlePosition[3]))

        if HasTarget[0] != 0 and HasTarget[1] != 0:
            if HasTarget[0] < BattlePosition[0]:
                return (BattlePosition[0] - 30) + HasTarget[0] + 1, HasTarget[1] + BattlePosition[1] + 1
            else:
                return (BattlePosition[0] - 40) + HasTarget[0] + 1, HasTarget[1] + BattlePosition[1] + 1
        else:
            return 0, 0

    def ScanHealerFriend(self, wait):
        Target = self.ScanTarget(self.BattlePosition, "Tartaruga")
        # print("Target: ", Target[0], " - ", Target[1])
        if Target[0] != 0 and Target[1] != 0:
            # SaveImage('images/Tests/TestMaior.png', Region=(Target[0] + 29, Target[1] - 4, Target[0] + 159, Target[1] + 13))
            
            Target = [Target[0] + 29, Target[1] + 8]

            # SaveImage('images/Tests/Test.png', Region=(Target[0], Target[1], Target[0] + 130, Target[1] + 3))
            # SaveImage('images/Tests/Test2.png', Region=(Target[0], Target[1], Target[0] + 129, Target[1] + 3))
            # SaveImage('images/Tests/Test3.png', Region=(Target[0], Target[1] - 1, Target[0] + 130, Target[1] + 2))

            Life = self.Scan.ScanStagesBattle(Target, 130)
            if Life is None:
                Life = 0

            # print('Life: ', Life)
            if Life > 0:
                if Life < 80:
                    print("Pressed ", self.HotkeyHealerFriend.get(), " To Heal Friend from: ", Life)
                    self.SendToClient.Press(self.HotkeyHealerFriend.get())
                    wait(1)
                    return
        wait(.15)

    def __init__(self, MOUSE_OPTION, BattlePosition):
        self.HealerFriend = GUI('HealerFriend', 'Module: Healer Friend')
        self.HealerFriend.DefaultWindow('AutoHeal2', [306, 372], [1.2, 2.29])
        self.Setter = GUISetter("HealerFriendLoader")
        self.Scan = ScanStages('Life')
        self.SendToClient = Hotkey(MOUSE_OPTION)

        self.AllThreads = AllThreads()
        self.ThreadName = 'ThreadHealerFriend'
        if not self.AllThreads.ExistsThread(self.ThreadName):
            self.ThreadManager = ThreadManager(self.ThreadName, Managed=True, Func=self.ScanHealerFriend)

        self.BattlePosition = BattlePosition
        self.HotkeyHealerFriend, self.InitiatedHotkeyHealerFriend = self.Setter.Variables.Str('HotkeyHealerFriend')

        def SetHealerFriend():
            global EnabledHealerFriend
            if not EnabledHealerFriend:
                EnabledHealerFriend = True
                ButtonEnabled.configure(text='HealerFriend: ON')
                Checking()
                self.AllThreads.UnPauseThreads(self.ThreadName)
            else:
                EnabledHealerFriend = False
                ButtonEnabled.configure(text='HealerFriend: OFF')
                Checking()
                self.AllThreads.PauseThreads(self.ThreadName)


        def Checking():
            HotkeyOption = self.HealerFriend.addOption(
                self.HotkeyHealerFriend, self.SendToClient.Hotkeys, [145, 170], 10)
            if EnabledHealerFriend:
                HotkeyOption.configure(state='disabled')
            else:
                HotkeyOption.configure(state='normal')

        def CheckingGUI(Init, Get, Name):
            if Get != Init:
                GUIChanges.append((Name, Get))

        def Destroy():
            CheckingGUI(self.InitiatedHotkeyHealerFriend,
                        self.HotkeyHealerFriend.get(), 'HotkeyHealerFriend')

            self.HealerFriend.destroyWindow()

        self.HealerFriend.addButton('Ok', Destroy, [84, 29, 130, 504], [5, 50, 8])

        global EnabledHealerFriend
        if not EnabledHealerFriend:
            ButtonEnabled = self.HealerFriend.addButton('HealerFriend: OFF', SetHealerFriend, [328, 29, 12, 469],
                                                     [5, 17, 8])
        else:
            ButtonEnabled = self.HealerFriend.addButton('HealerFriend: ON', SetHealerFriend, [328, 29, 12, 469],
                                                     [5, 17, 8])

        Checking()

        self.HealerFriend.Protocol(Destroy)
        self.HealerFriend.loop()

import time

from Conf.Hotkeys import Hotkey
from Conf.Constants import LifeColor, LifeColorFull, LifeColorEmptyBattle

from Core.GUI import *
from Core.GUISetter import GUISetter
from Core.ThreadManager import ThreadManager
from Core.HookWindow import LocateCenterImage, SaveImage

from Engine.ScanStages import ScanStages

GUIChanges = []

EnabledHealerFriend = False
ThreadStarted = False

class HealerFriend:
    def __init__(self, root, MOUSE_OPTION, BattlePosition):
        self.HealerFriend = GUI('HealerFriend', 'Module: Healer Friend')
        self.HealerFriend.DefaultWindow('AutoHeal2', [306, 372], [1.2, 2.29])
        self.Setter = GUISetter("HealerFriendLoader")
        self.Scan = ScanStages('Life')
        self.SendToClient = Hotkey(MOUSE_OPTION)
        self.ThreadManager = ThreadManager("ThreadHealerFriend")

        HotkeyHealerFriend, InitiatedHotkeyHealerFriend = self.Setter.Variables.Str(
            'HotkeyHealerFriend')

        def SetHealerFriend():
            global EnabledHealerFriend
            global ThreadStarted
            if not EnabledHealerFriend:
                EnabledHealerFriend = True
                ButtonEnabled.configure(text='HealerFriend: ON')
                Checking()
                if not ThreadStarted:
                    ThreadStarted = True
                    self.ThreadManager.NewThread(ScanHealerFriend)
                else:
                    self.ThreadManager.UnPauseThread()
            else:
                EnabledHealerFriend = False
                ButtonEnabled.configure(text='HealerFriend: OFF')
                Checking()
                self.ThreadManager.PauseThread()


        def ScanTarget(BattlePosition, Target):
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

        def ScanHealerFriend():
            while EnabledHealerFriend:
                Target = ScanTarget(BattlePosition, "Tataruga")
                # print("Target: ", Target[0], " - ", Target[1])
                if Target[0] != 0 and Target[1] != 0:
                    # SaveImage('images/Tests/TestMaior.png', Region=(Target[0] + 29, Target[1] - 4, Target[0] + 159, Target[1] + 13))
                    # SaveImage('images/Tests/Test.png', Region=(Target[0] + 29, Target[1] + 8, Target[0] + 30, Target[1] + 11))
                    
                    Target = [Target[0] + 29, Target[1] + 8]
                    Life = self.Scan.ScanStagesBattle(Target, LifeColorEmptyBattle, 130)
                    if Life is None:
                        Life = 0

                    # print('Life: ', Life)
                    if Life > 0:
                        if Life < 70:
                            print("Pressed ", HotkeyHealerFriend.get(), " To Heal Friend from: ", Life)
                            self.SendToClient.Press(HotkeyHealerFriend.get())
                            time.sleep(1)
                            continue
                time.sleep(.2)

        def Checking():
            HotkeyOption = self.HealerFriend.addOption(
                HotkeyHealerFriend, self.SendToClient.Hotkeys, [145, 170], 10)
            if EnabledHealerFriend:
                HotkeyOption.configure(state='disabled')
            else:
                HotkeyOption.configure(state='normal')

        def CheckingGUI(Init, Get, Name):
            if Get != Init:
                GUIChanges.append((Name, Get))

        def Destroy():
            CheckingGUI(InitiatedHotkeyHealerFriend,
                        HotkeyHealerFriend.get(), 'HotkeyHealerFriend')

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

from Core.HookWindow import PixelMatchesColor, GetPixelColor
from Conf.Constants import LifeColorGreenBattle, LifeColorGreenBattle2, LifeColorYellowBattle, LifeColorRedBattle, LifeColorRedBattle2


class ScanStages:
    LifeColorGreenBattleRgb = (LifeColorGreenBattle[0], LifeColorGreenBattle[1], LifeColorGreenBattle[2])
    LifeColorGreenBattleRgb2 = (LifeColorGreenBattle2[0], LifeColorGreenBattle2[1], LifeColorGreenBattle2[2])
    LifeColorYellowBattleRgb = (LifeColorYellowBattle[0], LifeColorYellowBattle[1], LifeColorYellowBattle[2])
    LifeColorRedBattleRgb = (LifeColorRedBattle[0], LifeColorRedBattle[1], LifeColorRedBattle[2])
    LifeColorRedBattleRgb2 = (LifeColorRedBattle2[0], LifeColorRedBattle2[1], LifeColorRedBattle2[2])

    def __init__(self, name):
        self.stage = 0
        self.name = name

    def ScanStages(self, Localization, color, colorFull):
        if PixelMatchesColor(Localization[0] + 100, Localization[1],
                             (colorFull[0], colorFull[1], colorFull[2])):
            self.stage = 100
            # print(f"Get {self.name}: {self.stage}%")
            return self.stage
        else:
            for i in range(95, 5, -5):
                if PixelMatchesColor(Localization[0] + i, Localization[1], (color[0], color[1], color[2])):
                    self.stage = i
                    # print(f"Get {self.name}: {self.stage}%")
                    return self.stage

    def ScanStagesBattle(self, Localization, size):
        if PixelMatchesColor(Localization[0] + size - 1, Localization[1],
                             (LifeColorGreenBattle[0], LifeColorGreenBattle[1], LifeColorGreenBattle[2])):
            self.stage = 100
            # print(f"Get {self.name}: {self.stage}%")
            return self.stage
        else:
            for i in range(size - 5, 0, -5):
                rgb = GetPixelColor(Localization[0] + i, Localization[1])
                # print(rgb, LifeColorGreenBattle, LifeColorYellowBattle, LifeColorRedBattle, i)
                if rgb == self.LifeColorGreenBattleRgb or rgb == self.LifeColorGreenBattleRgb2 or rgb == self.LifeColorYellowBattleRgb or rgb == self.LifeColorRedBattleRgb or rgb == self.LifeColorRedBattleRgb2:
                    self.stage = i * 100 / size
                    # print(f"Get {self.name}: {self.stage}%")
                    return self.stage

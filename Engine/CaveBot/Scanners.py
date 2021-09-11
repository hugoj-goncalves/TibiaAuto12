import time
import cv2
import numpy as np

from Core.HookWindow import LocateAllImages, LocateCenterImage, LocateImage, SaveImage, TakeImage


def NumberOfTargets(BattlePosition, Monster):
    Number = LocateAllImages('images/Targets/Names/' + Monster + '.png', Precision=0.8, Region=(
        BattlePosition[0], BattlePosition[1], BattlePosition[2], BattlePosition[3]))

    if Number > 0:
        return Number
    else:
        return 0


def ScanTarget(BattlePosition, Monster):
    HasTarget = [0, 0]

    HasTarget[0], HasTarget[1] = LocateCenterImage('images/Targets/Names/' + Monster + '.png', Precision=0.86, Region=(
        BattlePosition[0], BattlePosition[1], BattlePosition[2], BattlePosition[3]))

    if HasTarget[0] != 0 and HasTarget[1] != 0:
        if HasTarget[0] < BattlePosition[0]:
            return (BattlePosition[0] - 30) + HasTarget[0] + 1, HasTarget[1] + BattlePosition[1] + 1
        else:
            return (BattlePosition[0] - 40) + HasTarget[0] + 1, HasTarget[1] + BattlePosition[1] + 1
    else:
        return 0, 0


def CheckWaypoint(image, map_positions):
    wpt = [0, 0]
    middle_start = (map_positions[0] + 48, map_positions[1] + 48)
    middle_end = (map_positions[2] - 48, map_positions[3] - 48)

    wpt[0], wpt[1] = LocateImage('images/MapSettings/' + image + '.png', Precision=0.7, Region=(middle_start[0], middle_start[1], middle_end[0], middle_end[1]))

    if wpt[0] != 0 and wpt[1] != 0:
        print("Arrived At Mark:", image)
        return True
    else:
        print("Didn't Arrived At Mark:", image)
        return False


def IsAttacking(BattlePosition):
    ImagesAttacking = {
        "FullRed": False,
        # "FullBlackRed": False,

        # "LeftRed": False,
        # "TopRed": False,
        # "RightRed": False,
        # "BottomRed": False,

        # "LeftBlackRed": False,
        # "TopBlackRed": False,
        # "RightBlackRed": False,
        # "BottomBlackRed": False,

        # "LeftPink": False,
        # "TopPink": False,
        # "RightPink": False,
        # "BottomPink": False,

        # "LeftBlackPink": False,
        # "TopBlackPink": False,
        # "RightBlackPink": False,
        # "BottomBlackPink": False
    }

    TakedImage = TakeImage(Region=(
        BattlePosition[0] + 1, BattlePosition[1], BattlePosition[0] + 25, BattlePosition[3]))
    # TakedImage.save('images/Tests/TestScanner.png')

    img_rgb = np.array(TakedImage, dtype='uint8')
    # cv2.imshow("window_name RGB", img_rgb)
    # cv2.waitKey(0)
    # img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    img_rgb_cv2 = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2RGBA)
    # cv2.imshow("window_name Gray", img_gray)
    # cv2.waitKey(1000*60)

    def ScannerAttack(image, Precision=0.9):
        def findImgthres(template_path, mask=False, method=1, thres=.95):
            img = img_rgb_cv2
            tem = cv2.imread(template_path, cv2.IMREAD_UNCHANGED)

            # Match template with and without mask
            if mask and img.shape[2] == 4:
                # print('has mask!')
                alpha_channel = np.array(cv2.split(tem)[3])
                result = cv2.matchTemplate(img, tem, method, mask=alpha_channel)
            else:
                result = cv2.matchTemplate(img, tem, method)

            # Nomrmalize result data to percent (0-1)
            # # result = cv2.normalize(result, None, 0, 1, cv2.NORM_MINMAX, -1)

            # Invert Image to work similar across all methods!
            if method == 0 or method == 1:
                result = (1 - result)

            result_list = np.argwhere(result > thres)
            return result, result_list

        mask_result = findImgthres(image, mask=True, thres=Precision)
        matchLoc = mask_result[1]
        if matchLoc is not None and matchLoc.size > 0:
            # Debug
            # print(matchLoc)
            # tmp_tem = cv2.imread(image, cv2.IMREAD_UNCHANGED)
            # for loc in matchLoc:
            #     cv2.rectangle(img_rgb_cv2, tuple(loc)[
            #                 ::-1], (loc[1] + tmp_tem.shape[1], loc[0] + tmp_tem.shape[0]), (0, 0, 0), 1)
            # cv2.imshow('output', img_rgb_cv2)
            # cv2.waitKey(0)
            # DebugEnd
            return True
        return False

        # template = cv2.imread(image, 0)
        # res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)

        # # w, h = template.shape[::-1]
        # # loc = np.where(res >= Precision)
        # # for pt in zip(*loc[::-1]):
        # #     cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
        # # cv2.imshow('output', img_rgb)
        # # cv2.waitKey(0)

        # min_val, LocatedPrecision, min_loc, Position = cv2.minMaxLoc(res)
        # print('Located Precision: ', LocatedPrecision, ' image: ', image)
        # if LocatedPrecision > Precision:
        #     # # Draw the rectangle:
        #     # # Extract the coordinates of our best match
        #     # MPx, MPy = min_loc
        #     # # Step 2: Get the size of the template. This is the same size as the match.
        #     # trows, tcols = template.shape[:2]
        #     # # Step 3: Draw the rectangle on large_image
        #     # cv2.rectangle(img_gray, (MPx, MPy),
        #     #               (MPx+tcols, MPy+trows), (0, 0, 255), 2)
        #     # # Display the original image with the rectangle around the match.
        #     # cv2.imshow('output', img_gray)
        #     # # The image is only displayed if we call this
        #     # cv2.waitKey(0)
        #     return True
        # return False

    for Image in ImagesAttacking:
        ImagesAttacking[Image] = False
        if ScannerAttack('images/MonstersAttack/' + Image + '.png'):
            ImagesAttacking[Image] = True

    if ImagesAttacking['FullRed']:
        # print('attacking true: red')
        return True
    # elif ImagesAttacking['LeftRed'] and ImagesAttacking['TopRed'] and ImagesAttacking['RightRed'] and ImagesAttacking['BottomRed']:
    #     print('attacking true: red')
    #     return True
    # elif ImagesAttacking['LeftBlackRed'] and ImagesAttacking['TopBlackRed'] and ImagesAttacking['RightBlackRed'] and ImagesAttacking['BottomBlackRed']:
    #     print('attacking true: black red')
    #     return True
    # elif ImagesAttacking['LeftPink'] and ImagesAttacking['TopPink'] and ImagesAttacking['RightPink'] and ImagesAttacking['BottomPink']:
    #     print('attacking true: pink')
    #     return True
    # elif ImagesAttacking['LeftBlackPink'] and ImagesAttacking['TopBlackPink'] and ImagesAttacking['RightBlackPink'] and ImagesAttacking['BottomBlackPink']:
    #     print('attacking true: black pink')
    #     return True
    else:
        return False


'''X, Y = LocateCenterImage('images/MonstersAttack/top.png', Precision=0.85, Region=(
    BattlePosition[0], BattlePosition[1], BattlePosition[2], BattlePosition[3]))
if X != 0 and Y != 0:
    return True
else:
    X, Y = LocateCenterImage('images/MonstersAttack/right.png', Precision=0.85, Region=(
        BattlePosition[0], BattlePosition[1], BattlePosition[2], BattlePosition[3]))
    if X != 0 and Y != 0:
        return True
    else:
        X, Y = LocateCenterImage('images/MonstersAttack/left.png', Precision=0.85, Region=(
            BattlePosition[0], BattlePosition[1], BattlePosition[2], BattlePosition[3]))
        if X != 0 and Y != 0:
            return True
        else:
            X, Y = LocateCenterImage('images/MonstersAttack/bottom.png', Precision=0.85, Region=(
                BattlePosition[0], BattlePosition[1], BattlePosition[2], BattlePosition[3]))
            if X != 0 and Y != 0:
                return True
            else:
                return False'''


def NeedFollow():
    X, Y = LocateImage('images/TibiaSettings/Idle.png', Precision=0.7)
    if X != 0 and Y != 0:
        return True
    else:
        return False


def NeedIdle():
    X, Y = LocateImage('images/TibiaSettings/Following.png', Precision=0.7)
    if X != 0 and Y != 0:
        return True
    else:
        return False

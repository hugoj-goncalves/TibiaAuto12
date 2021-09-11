import win32gui
import pygetwindow as gw


def GetHWND(Title):
    try:
        a = gw.getWindowsWithTitle(Title)
        a = str(a)
        b = a.split('=', 1)
        b = b[1].split(')', 1)
        hwnd = int(b[0])
        print(f">>> OBS's Window Located")
        return hwnd
    except Exception as Ex:
        print("From GetHWND.py: ", Ex)
        print(f">>> Window Not Located: '{Title}', Trying Again")
        return 0


def ListWindowNames():
    def winEnumHandler(hwnd, ctx):
        if win32gui.IsWindowVisible(hwnd):
            print(hex(hwnd), '"' + win32gui.GetWindowText(hwnd) + '"')
    win32gui.EnumWindows(winEnumHandler, None)


def GetInnerWindows(whndl):
    def callback(hwnd, hwnds):
        if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
            hwnds[win32gui.GetClassName(hwnd)] = hwnd
        return True
    hwnds = {}
    win32gui.EnumChildWindows(whndl, callback, hwnds)
    return hwnds

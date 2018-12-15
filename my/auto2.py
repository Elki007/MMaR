import ctypes
import win32gui
import win32con
import win32api
from time import sleep

EnumWindows = ctypes.windll.user32.EnumWindows
EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
GetWindowText = ctypes.windll.user32.GetWindowTextW
GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
IsWindowVisible = ctypes.windll.user32.IsWindowVisible

titles = []
def foreach_window(hwnd, lParam):
    if IsWindowVisible(hwnd):
        length = GetWindowTextLength(hwnd)
        buff = ctypes.create_unicode_buffer(length + 1)
        GetWindowText(hwnd, buff, length + 1)
        titles.append(buff.value)
    return True

EnumWindows(EnumWindowsProc(foreach_window), 0)

#print(titles)
i=""
hwnd=""
for i in titles:
    if "BLACK" in i:
        hwnd=i

hwndMain = win32gui.FindWindow(None, hwnd)
print(hwndMain) #you can use this to see main/parent Unique IDsaa

while(True):
    temp = win32api.SendMessage(hwndMain, win32con.WM_IME_KEYDOWN, 0x52, 0) #press r
    #temp = win32api.PostMessage(hwndMain, win32con.WM_CHAR, 0x52, 0) #press r
    sleep(1)
    temp = win32api.PostMessage(hwndMain, win32con.WM_IME_KEYUP, 0x52, 0)  # press r
    #prrrint(temp)
    sleep(1)
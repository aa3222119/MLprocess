# ===========================================
# @Time    : 2019/3/27 17:10
# @Author  : antony
# @Email   : 502202879@qq.com
# @File    : win32kb_auto.py
# @Software: PyCharm
# ===========================================
import pyautogui as pag
import pyperclip
import time
screenWidth, screenHeight = pag.size()
pag.PAUSE = .5


def typing_root(*args):
    print(args, '控制键盘输入密码并确认')
    pag.click()
    pyperclip.copy("sssudo sssu - ")
    pag.click(button='sright')
    pag.hotkey('menters')
    pyperclip.copy("k4BBbi1234321..")
    pag.click(button='sright')
    pag.hotkey('senters')


def hmove_to(x, y):
    x, y = int(x), int(y)
    for i in range(5):
        pag.moveTo(x, y, duration=0.1)
        print(x, y, pag.position())
        if pag.position() == (x, y):
            break


def waitforpicshowup(pic, times=20, gap=0.1):
    res2 = None
    for i in range(times):
        res2 = pag.locateOnScreen(pic, confidence=0.95)
        if res2 is not None:
            break
        time.sleep(gap)
    return res2


def waitforpicsshowup(pics, times=20, gap=0.1):
    res = None
    if type(pics) is list:
        for i in range(times):
            for pic in pics:
                res = pag.locateOnScreen(pic, confidence=0.95)
                if res is not None:
                    return res
                time.sleep(gap)
    return res


def dobbsblogin(*args):
    print(*args, __name__,)
    res = pag.locateOnScreen('F:\python_pro\MLprocess\ie.png', confidence=0.9)
    if res:
        # x, y = int(res[0]+.5*res[2]), int(res[1]+.5*res[3])
        # win32api.SetCursorPos((x, y))
        hmove_to(res[0]+.5*res[2], res[1]+.5*res[3])
        pag.click(button='left')
    else:
        return -1
    urls = ['F:\python_pro\MLprocess\\url.png', 'F:\python_pro\MLprocess\\url1.png']
    res1 = waitforpicsshowup(urls, 50)
    # res1 = pag.locateOnScreen('F:\python_pro\MLprocess\\url.png', confidence=0.9)
    if res1:
        hmove_to(res1[0] + 150, res1[1] + .5 * res1[3])
        # x, y = int(res1[0] - 150), int(res1[1] + .5 * res1[3])
        # win32api.SetCursorPos((x, y))
        pag.mouseDown()
        pag.mouseUp()
        pyperclip.copy("https://sfok4rts.simnk4opk4ec.com/iam/login.jsp")
        pag.hotkey('ctrl', 'v')
        # pag.typewrite("https://sfok4rts.simnk4opk4ec.com/iam/login.jsp", 0.1)
        pag.hotkey('enter')
    else:
        return -1
    res2 = waitforpicsshowup(['F:\python_pro\MLprocess\jnta_ready.png'], 50)
    print(res2)
    res3 = waitforpicsshowup(['F:\python_pro\MLprocess\yhmc.png'])
    if res3:
        print(res3)
        hmove_to(res3[0] + 1.5 * res3[2], res3[1] + 1.5 * res3[3])
        pag.click(button='left')
        # pag.typewrite("hxc.bbsb", 0.1)
        pyperclip.copy("hxc.bbsb")
        pag.hotkey('ctrl', 'v')
        pag.hotkey('tab')
    else:
        return -1
    res3 = waitforpicsshowup(['F:\python_pro\MLprocess\ykl.png'])
    if res3:
        print(res3)
        hmove_to(res3[0] + 1.5 * res3[2], res3[1] + 1.5 * res3[3])
        pag.click(button='left')
        # pag.typewrite("Zz313249172", 0.1)
        pyperclip.copy("Zz313249172")
        pag.hotkey('ctrl', 'v')
        pag.hotkey('enter')
    else:
        return -1
    res4 = waitforpicsshowup(['F:\python_pro\MLprocess\grgw.png'])
    if res4:
        print(res4)
        hmove_to(res4[0] + 0.5 * res4[2], res4[1] + 0.5 * res4[3])
        pag.click(button='left')
    else:
        return -1
    return 0


if __name__ == '__main__':
    dobbsblogin()

import pyautogui as pag
import time

import ctypes
import threading


# pag.screenshot('foo.png')
# screenimg = pag.screenshot()
#
# time.sleep(2)
# img = pag.screenshot(region=(605, 555, 142, 42))
# img.save('button.png')

for i in range(100000):
    time.sleep(5)
    res = pag.locateOnScreen('F:\python_pro\MLprocess\goon.png')
    if res:
        pag.click(res[0]+.5*res[2], res[1]+.5*res[3], 2)


pag.moveTo(1300, 300, 0.6)
pag.typewrite("Hello cark1 !!!~.~", 0.2)
pag.confirm('sure?')
time.sleep(200)
pag.hotkey('ctrl', 'shift', 'n')

# -------------------------------------------------------
import requests, json
r = requests.get('http://apis.juhe.cn/oil/region?key=b17d61a3d33c0cf5b38dc04f51d6ad5d&city=襄阳市')
res = json.loads(r.text)

# ----------------------------------------------------------------------------------------------------------------
import os
cmd_win = 'dir G:\\KuGou /b /a /s | find ".mp4"'
out_dir = 'G:\\KuGou\\tmp\\'
# out_dir = '此电脑\Redmi 5 Plus\内部存储设备\data\\'
cmd_cp = 'xcopy /h /fy "%s" ' + out_dir
file_list = os.popen(cmd_win).read().strip().split('\n')
import random
for i in range(16):
    x = random.choice(file_list)
    mp = x.split('\\')[-1]
    cmd_ = cmd_cp % (x,)
    print(cmd_,)
    print(os.popen(cmd_))
##
import os, time
import cv2


def devide_v(ss, t, file, postfix='.wmv'):
    cmd = 'ffmpeg -ss %s -t %s -accurate_seek -i "%s" -codec copy "%s"'
    input_f = file + postfix
    output_f = file + 'cut' + time.strftime('%Y%m%d_%H%M%S') + postfix
    print(os.popen(cmd %(ss, t, input_f, output_f)).read())
    # os.popen(output_f).read()
    return output_f


os.chdir('I:\番剧相关')
fname = '''Re.Zero.kara.Hajimeru.Isekai.Seikatsu.Memory.Snow.2018.OVA.BDrip.1080p.CHS.AVC.AAC-Mabors'''
of = devide_v('00:08:15.03', 60*2, fname, '.mp4')
cap = cv2.VideoCapture(of)
cv2.namedWindow("frame", 0)
# cv2.resizeWindow("frame", 640, 480)
ret = True
while (ret):
    ret, frame = cap.read()
    cv2.imshow('frame', frame)  # 一个窗口用以显示原视频
    cv2.resizeWindow("enhanced", 640, 480)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()

# ----------------------------------------------------------------------------------------------------------------
import cv2,time
import numpy as np
cap = cv2.VideoCapture(0)
# fourcc = cv2.cv.CV_FOURCC(*'XVID')
#opencv3的话用:fourcc = cv2.VideoWriter_fourcc(*'XVID')
# out = cv2.VideoWriter('output.avi',fourcc,20.0,(640,480))#保存视频
while True:
    ret, frame = cap.read()
    cv2.imshow('frame', frame)  # 一个窗口用以显示原视频
    time.sleep(0.1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
# out.release()
cv2.destroyAllWindows()
from exam.cark_funcs import *
# import pyautogui as pag
#
# import ctypes
# import threading
#
#
# # pag.screenshot('foo.png')
# # screenimg = pag.screenshot()
# #
# # time.sleep(2)
# # img = pag.screenshot(region=(605, 555, 142, 42))
# # img.save('button.png')
#
# for i in range(100000):
#     time.sleep(5)
#     res = pag.locateOnScreen('F:\python_pro\MLprocess\goon.png')
#     if res:
#         pag.click(res[0]+.5*res[2], res[1]+.5*res[3], 2)
#
#
# pag.moveTo(1300, 300, 0.6)
# pag.typewrite("Hello cark1 !!!~.~", 0.2)
# pag.confirm('sure?')
# time.sleep(200)
# pag.hotkey('ctrl', 'shift', 'n')

# cark playground

gen_dev_v2('335599.xyz FSDSS-549.mp4', '012855', dev_secs=59, f_dir="/Users/hanxuechen/Downloads/need_to_move")
gen_dev_v('2-1Q123222322', '000726', dev_secs=60, f_dir="C:\\迅雷下载\\16278482\\cut2")

# mv_concat2("C:\\迅雷下载\\16278482\\cut2", mv_nums=5)
mv_concat3("Z:\\process_area", mv_nums=78, ts_dir='C:\\迅雷下载\\ts\\')

# -------------------------------------------------------
import requests, json
r = requests.get('http://apis.juhe.cn/oil/region?key=b17d61a3d33c0cf5b38dc04f51d6ad5d&city=襄阳市')
res = json.loads(r.text)

# ----------------------------------------------------------------------------------------------------------------

source_dir = 'Z:\\process_area\\'
format_ = 'mp4'
import os
cmd_win = f'dir {source_dir} /b /a /s | find ".{format_}"'
out_dir = 'C:\\迅雷下载\\16278482\\11'
# out_dir = '此电脑\Redmi 5 Plus\内部存储设备\data\\'
cmd_cp = 'xcopy /h /fy "%s" ' + out_dir
file_list = os.popen(cmd_win).read().strip().split('\n')

for i in range(16):
    x = random.choice(file_list)
    mp = x.split('\\')[-1]
    cmd_ = cmd_cp % (x,)
    print(cmd_,)
    print(os.popen(cmd_))
##



import cv2
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
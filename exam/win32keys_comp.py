# ===========================================
# @Time    : 2019/3/27 14:10
# @Author  : antony
# @Email   : 502202879@qq.com
# @File    : win32kb_auto.py
# @Software: PyCharm
# ===========================================
import win32api
import win32con
import win32clipboard as w3c
import ctypes
import threading


def set_clipboard(astring):  # 写入剪切板  目前这方法有bug
    w3c.OpenClipboard()
    w3c.EmptyClipboard()
    w3c.SetClipboardData(win32con.CF_TEXT, astring)
    w3c.CloseClipboard()


class Hotkey:

    def __init__(self):
        self.stop_flag = False  # 置为True时终止热键进程
        self.keys ={
            10: win32con.VK_F10,
            98: (win32con.VK_F10, win32con.MOD_CONTROL),
            99: (win32con.VK_F10, win32con.MOD_CONTROL, win32con.MOD_ALT)}
        self.callbacks = {
            10: self.print_test,
            98: self.print_test,
            99: self.print_test}
        self.args = {
            10: (),
            98: ('token to run out ~',),
            99: ('token to run out ~', '额外信息测试 id:99')}  # 一般默认的传参都是 () 特定传参需要注册

    def add(self, des_list):
        # des_list = [10, (win32con.VK_F10, win32con.MOD_CONTROL), hotkey_print_test, *()]
        # 4个元素 分别是 id 热键 回调函数 和 回调函数的参数
        if des_list[0] in self.keys:
            print(f'key_id: {des_list[0]} is already used')
            return -1
        else:
            id, key, callback, *args = des_list
            self.keys.update({id: key})
            self.callbacks.update({id: callback})
            self.args.update({id: args if args else ()})

    def __iter__(self):
        return iter([(i, self.keys[i], self.callbacks[i], self.args[i]) for i in self.keys])

    def print_test(self, x='this is a hotkey run test~', *args):
        print(x, *args)
        if x == 'token to run out ~':
            self.stop_flag = True
            print('  >> 热键监控到此为止~!!')


class HotkeyThread(threading.Thread):  # 创建一个Thread.threading的扩展类
    user32 = ctypes.windll.user32  # 加载user32.dll

    def __init__(self, hotkey_configs):
        super(HotkeyThread, self).__init__()
        self.useable = True
        if type(hotkey_configs) is not Hotkey:
            print('hotkey_configs type error')
            self.useable = False
        self.hotkey_configs = hotkey_configs

    def run(self):
        if not self.useable:
            return -1
        for id, key, callback, args in self.hotkey_configs:
            if type(key) is not int and len(key) > 1:
                mod, vk = eval('|'.join([str(x) for x in key[1:]])), key[0]  # 辅助按键的特殊处理例子
            else:
                mod, vk = 0, key
            # 注册快捷键mod是辅助按键，vk是像F10这样的按键
            if not self.user32.RegisterHotKey(None, id, mod, vk):
                print("Unable to register id", id)  # 返回一个错误信息
            else:
                print(f'成功注册热键：mod({mod}) vk({vk})')
        try:
            # 以下为检测热键是否被按下，并在最后释放快捷键
            msg = ctypes.wintypes.MSG()
            while True and not self.hotkey_configs.stop_flag:
                if self.user32.GetMessageA(ctypes.byref(msg), None, 0, 0) != 0:
                    if msg.message == win32con.WM_HOTKEY:
                        # print(msg.message, msg.wParam)
                        if msg.wParam in self.hotkey_configs.keys:
                            func = self.hotkey_configs.callbacks[msg.wParam]
                            args = self.hotkey_configs.args[msg.wParam]
                            if args:
                                res = func(*args)
                            else:
                                res = func()
                    self.user32.TranslateMessage(ctypes.byref(msg))
                    self.user32.DispatchMessageA(ctypes.byref(msg))
        finally:
            # 必须得释放热键，否则下次就会注册失败，所以当程序异常退出，没有释放热键，
            # 那么下次很可能就没办法注册成功了，这时可以换一个热键测试
            for id, key, callback, args in self.hotkey_configs:
                self.user32.UnregisterHotKey(None, id)


if __name__ == '__main__':
    # 一个通过热键触发自动root登录(通过pyautogui)的实例
    hot = Hotkey()
    # 增加自己真正需要配置的热键
    from win32kb_auto import typing_root, dobjsylogin
    # 68 对应D键
    hot.add([11, (67, win32con.MOD_CONTROL, win32con.MOD_ALT), dobjsylogin, ()])  #
    hot.add([12, (68, win32con.MOD_CONTROL, win32con.MOD_ALT), typing_root, ()])  #
    p = HotkeyThread(hot)
    p.start()

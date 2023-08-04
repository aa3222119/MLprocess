import os
import zipfile
import pyzipper
import random
import time
import numpy as np

# 94\
_charset = ['`', '~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '=', '+', '[', ']', '{', '}', ';',
            ':', "'", '"', '\\', '|', ',', '<', '.', '>', '/', '?', 'a', 'A', 'b', 'B', 'c', 'C', 'd', 'D', 'e', 'E',
            'f', 'F', 'g', 'G', 'h', 'H', 'i', 'I', 'j', 'J', 'k', 'K', 'l', 'L', 'm', 'M', 'n', 'N', 'o', 'O', 'p',
            'P', 'q', 'Q', 'r', 'R', 's', 'S', 't', 'T', 'u', 'U', 'v', 'V', 'w', 'W', 'x', 'X', 'y', 'Y', 'z', 'Z',
            '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

_charset1 = ['a', 'A', 'b', 'B', 'c', 'C', 'd', 'D', 'e', 'E',
             'f', 'F', 'g', 'G', 'h', 'H', 'i', 'I', 'j', 'J', 'k', 'K', 'l', 'L', 'm', 'M', 'n', 'N', 'o', 'O', 'p',
             'P', 'q', 'Q', 'r', 'R', 's', 'S', 't', 'T', 'u', 'U', 'v', 'V', 'w', 'W', 'x', 'X', 'y', 'Y', 'z', 'Z',
             '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']


def gPwd(chST, lgth, rgth):
    while True:
        pl = int(np.random.random() * 100)
        if pl >= lgth and pl <= rgth:
            break

    pwd = ""

    chStLen = len(chST)

    for i in range(0, pl):
        while True:
            idx = int(np.random.random() * 100)
            if idx >= 0 and idx < chStLen:
                break
        pwd += chST[idx]

    return pwd


def dcryp(fileName, lLen, rLen, chST):
    fp = zipfile.ZipFile(fileName)

    count = 0

    while True:
        pwd = gPwd(chST, lLen, rLen)
        count += 1
        try:
            for file in fp.namelist():
                fp.extract(file, pwd=pwd.encode())
                os.rename(file, file.encode('cp437').decode('gbk'))
            print("%d Success! The password is %s" % (count, pwd))
            break
        except Exception as err:
            print(f"{err=} {pwd=} {count=}")


def factorial(n):
    ret_ = 1
    for i in range(1, n + 1):
        ret_ *= i
    return ret_


class StrGen:

    def __init__(self, s_='abc', per=0.11):
        self.s = s_
        self.s_li = list(s_)
        self.s_li_use = self.s_li[:]
        self.l_ = len(s_)
        self.cnt_limit = factorial(self.l_)
        if self.l_ > 4:
            self.cnt_limit = int(per * self.cnt_limit) + 1

    def random_iters(self):
        for i in range(self.cnt_limit):
            random.shuffle(self.s_li_use)
            yield ''.join(self.s_li_use)

    def speedup_random_iters(self):
        for i in range(self.cnt_limit):
            x = random.randint(0, self.l_ - 1)
            y = random.randint(0, self.l_ - 1)
            self.s_li_use[x], self.s_li_use[y] = self.s_li_use[y], self.s_li_use[x]
            yield ''.join(self.s_li_use)


class ZipHandler:

    def __init__(self, f_name):
        assert zipfile.is_zipfile(f_name), f'file input error: not is_zipfile {f_name=}'
        file_path_li = f_name.split(os.sep)
        self.cur_dir = os.sep.join(file_path_li[:-1])
        self.f_name_ful = file_path_li[-1]
        self.f_name_ = self.f_name_ful.split('.')[0]
        self.default_dir = os.sep.join([self.cur_dir, self.f_name_])
        self.fh_ = zipfile.ZipFile(f_name)
        self.namelist = self.fh_.namelist()
        self.fir_name = self.namelist[0]
        self.infolist = self.fh_.infolist()
        self.fir_flag_bits = self.fir_info.flag_bits
        self.cro_flag = self.fir_flag_bits & 0x01
        self.aes_flag = self.fir_info.compress_type in [99]  # todo
        if self.aes_flag:
            self.fh_aes = pyzipper.AESZipFile(f_name)
        else:
            self.fh_aes = None
        self.right_pwd = ''
        self.cra_cnt = 0

    @property
    def fir_info(self):
        return self.infolist[0]

    def extractall(self, dir_=None):
        pass

    def try_ex_a_pwd(self, pwd_=''):
        try:
            self.fh_aes.extract(member=self.fir_name, path=self.default_dir, pwd=pwd_.encode())
            # if self.aes_flag:
            #     # self.fh_aes.pwd = pwd_.encode()
            #     # self.fh_aes.extractall(self.default_dir)
            #     self.fh_aes.extract(member=self.fir_name, path=self.default_dir, pwd=pwd_.encode())
            #     return 1, pwd_
            # else:
            #     # self.fh_.extractall(self.default_dir, pwd=pwd_.encode())
            #     self.fh_.extract(member=self.fir_name, path=self.default_dir, pwd=pwd_.encode())
            #     return 1, pwd_
        except RuntimeError as err:
            # print(f'0 {err=} {err.args=}')
            return 0, err
        except Exception as err:
            # print(f'1 {err=} {err.args=}')
            return -1, err

    def crack_until(self, charset=None, limit_len=16):
        assert self.cro_flag, 'warning: no need to crack'
        if charset is None:
            charset = _charset1
        l_set = len(charset)

        tic = time.time()
        for cra_len in range(1, limit_len):
            the_lim = l_set ** cra_len  # 理论上限
            if cra_len > 3:
                the_lim = int(0.05 * the_lim)
            c_cnt_l = 0
            # random.shuffle(charset)
            sg_times = 0
            print(f'> crack at {cra_len=} {the_lim=}')
            while c_cnt_l <= the_lim:
                sg = StrGen(''.join(random.choices(charset, k=cra_len)))
                sg_times += 1
                # print(f'   * {sg.s=} {sg.cnt_limit=}')
                for pwd_ in sg.random_iters():
                    self.cra_cnt += 1
                    _sig, _er = self.try_ex_a_pwd(pwd_=pwd_)
                    if _sig == 1:
                        self.right_pwd = pwd_
                        print(f' crack success {self.cra_cnt=} {self.right_pwd=}')
                        return
                else:
                    c_cnt_l += sg.cnt_limit
            dt = time.time() - tic
            a_cra_taken = dt / c_cnt_l
            print(f' <finished cause:{c_cnt_l=}>{the_lim}; {sg_times=} {dt=:.5f} {a_cra_taken=:}.')

    def __del__(self):
        self.fh_.close()
        if self.fh_aes:
            self.fh_aes.close()


# -- use demo
file_name = os.sep.join(['compress_file', 'testing', "uz5.zip"])
zh5 = ZipHandler(file_name)

file_name = os.sep.join(['compress_file', 'testing', "uz3.zip"])
zh3 = ZipHandler(file_name)

zh1 = ZipHandler(os.sep.join(['compress_file', 'testing', "uz1.zip"]))
zh2 = ZipHandler(os.sep.join(['compress_file', 'testing', "uz2.zip"]))
zh6 = ZipHandler(os.sep.join(['compress_file', 'testing', "uz6.zip"]))

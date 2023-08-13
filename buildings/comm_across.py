# 跨平台实用方法

import os
import time
import datetime
import uuid
import hashlib
import logging
import re
import pickle
import sys

# 最好还是用python3.6

running_dir = os.getcwd()  # 多数情形下即是项目目录


def goto_script_dir(full_script_name=sys.argv[0]):
    exec_dir = os.path.dirname(full_script_name)
    print(f'切换当前目录(os.chdir): go to =>({exec_dir})', os.chdir(exec_dir))


def print_wf(ss):
    """
    print with flush
    :param ss:
    :return:
    """
    sys.stdout.write('\r' + ss)
    sys.stdout.flush()


def general_console_safe(funcs_li):
    console_li = [f.__name__ for f in funcs_li]
    print(day_forpast(0, ss='%Y-%m-%d %H:%M:%S'), 'hello console %s' % sys.path[0], sys.argv)
    print('use cons to start, standby tasks are :', console_li)
    if len(sys.argv) >= 2:
        if sys.argv[1] == 'cons' and sys.argv[2:]:
            assert sys.argv[2] in console_li, f'{sys.argv[2]} not in standby funcs'
            # 适应调度框架: 去掉 --开头的参数
            args_li = [x for x in sys.argv[3:] if '--' not in x]
            return f"{sys.argv[2]}({', '.join(args_li)})"
        else:
            print('please use keyword cons, and have expression after that~')
    print(day_forpast(0, ss='%Y-%m-%d %H:%M:%S'), 'done')


def general_console(funcs_li):
    console_li = [f.__name__ for f in funcs_li]
    print(day_forpast(0, ss='%Y-%m-%d %H:%M:%S'), 'hello console %s' % sys.path[0], sys.argv)
    print('use cons|eval to start, standby tasks are :', console_li)
    if len(sys.argv) >= 2:
        if sys.argv[1] == 'cons' and sys.argv[2:]:
            assert sys.argv[2] in console_li, f'{sys.argv[2]} not in standby funcs'
            return f'{sys.argv[2]}()'
        elif sys.argv[1] == 'eval' and sys.argv[2:]:
            assert '(' in sys.argv[2], f'please make sure {sys.argv[2]} is the expression can eval'
            return sys.argv[2]
        else:
            print('please use keyword cons|eval, and have expression after that~')
    print(day_forpast(0, ss='%Y-%m-%d %H:%M:%S'), 'done')


def iter_mkdir(path):
    """
        能够迭代的建立文件夹 path = /A/B/C/ 则会用迭代的方式先保证/A/B/存在 ;
        最好以/结尾 若path = /A/B/C/asdf 则只新建文件夹到/A/B/C/
        2019年10月16日11:54:15 : 更新 /被替换为 os.sep 兼容win下
        :param path:
        :return:
    """
    # path = re.match('(.*)/+', path).group(1)
    # path = re.match('(.*)' + os.sep + '+', path).group(1)
    path = os.sep.join(path.split(os.sep)[:-1])
    if path:
        try:
            os.mkdir(path)
            print('successful mkdir (%s)' % path)
        except Exception as err:
            print(err)
            if err.args[0] == 2:
                iter_mkdir(path)
                os.mkdir(path)
            else:
                print('no need to (iter)mkdir~')


def text2file(text_, file_name):
    iter_mkdir(file_name)
    with open(file_name, "w") as f:
        f.write(text_)


class VHolder:

    def __init__(self, va=''):
        self.values = va

    def store(self, path):
        try:
            pickle.dump(self.values, open(path, 'wb'))
        except Exception as err:
            print(err)
            iter_mkdir(path)
            pickle.dump(self.values, open(path, 'wb'))
        return self

    def pickup(self, path):
        try:
            self.values = pickle.load(open(path, 'rb'))
        except Exception as err:
            # iter_mkdir(path)
            print(err, path)
        return self.values


class Logger:

    def __init__(self, name):
        # super(Logger, self).__init__()
        self.logger = logging.getLogger(name)
        self.logger.setLevel(20)
        self.file_handler = None
        self.formatter_ = None
        self.with_date = '0'
        self.filename = name

    def set_format(self, format_ss):
        self.formatter_ = logging.Formatter(format_ss)
        return self

    def set_file(self, ):
        if self.file_handler:
            self.logger.removeHandler(self.file_handler)
        filename = '%s_%s' % (self.filename, self.with_date)
        try:
            self.file_handler = logging.FileHandler(filename)
            self.file_handler.formatter = self.formatter_
            # self.file_handler.setFormatter(self.formatter_)
            self.logger.addHandler(self.file_handler)
            return self
        except FileNotFoundError as err:
            print(err)
            iter_mkdir(filename)
            return self.set_file()

    def set_date(self, date_now):
        if date_now == self.with_date:
            pass
        else:
            self.with_date = date_now
            self.set_file()
        return self

    def set_level_info(self):
        pass

    def do_info(self, content):
        self.logger.info(content)
        return self


def datetime_format(a_datetime, ss="%Y%m%d"):
    if ss == 'stamp':
        return time.mktime(a_datetime.timetuple())
    elif ss == 'Timestamp':
        return a_datetime
    else:
        return a_datetime.strftime(ss)


def day_forpast(d=0, h=0, ss="%Y%m%d", curr_time=None):
    """
    平移时间，写forpast是老代码遗留问题，也可找未来，缺点是datetime.timedelta的参数不能用month
    :param d:
    :param h:
    :param ss:
    :param curr_time: 需要 datetime.datetime 结构
    :return:
    """
    if curr_time is None:
        curr_time = datetime.datetime.now()
    t1 = curr_time + datetime.timedelta(days=d, hours=h)
    return datetime_format(t1, ss)


# 任意置换curr_time的特定位置 curr_time不传时为当前时间
# rep_dict使用如下格式{'year':2020,'month':5,'day':31,'hour':23,'minute':59,'second':59}
def time_replace(rep_dict=None, ss='stamp', curr_time=None):
    if rep_dict is None:
        rep_dict = {}
    curr_time = curr_time if curr_time else datetime.datetime.now()
    re_curr = curr_time.replace(**rep_dict)
    return datetime_format(re_curr, ss)


# 某月的(倒数)第-n天 ym_dict 不传表示当前月
def lastnday_of_month(ym_dict=None, n=0, ss='%Y%m%d'):
    import calendar
    if ym_dict is None:
        ym_dict = {}
    now = datetime.datetime.now()
    c_year = ym_dict['year'] if 'year' in ym_dict else now.year
    c_month = ym_dict['month'] if 'month' in ym_dict else now.month
    days = calendar.monthrange(c_year, c_month)
    ym_dict.update({'day': days[-1] + n})
    return time_replace(ym_dict, ss)


def last_nd_of_month(curr_time=None, n=0, ss='%Y%m%d'):
    """
    时间替换成一个月的倒数n天的时间，默认最后一天
    :param curr_time: 需要 datetime.datetime 结构
    :param n: -1 表示倒数第1天再减一天
    :param ss:
    :return:
    """
    import calendar
    if curr_time is None:
        curr_time = datetime.datetime.now()
    days = calendar.monthrange(curr_time.year, curr_time.month)
    return time_replace({'day': days[-1] + n}, ss, curr_time)


# 获取curr_time的上月最后一天的一种方法 curr_time不传时为当前时间
def last_month_last_day(ss='%Y-%m-%d', curr_time=None):
    this_month_first_day = time_replace({'day': 1}, ss='Timestamp', curr_time=curr_time)
    last_month_last_day_ = this_month_first_day - datetime.timedelta(days=1)
    return datetime_format(last_month_last_day_, ss)


class Timer:
    def __init__(self, num=1):
        self.num = num
        self.extradata = []
        self.tictoc = []
        self.alltoc = []
        self.initpoint = time.time()
        self.ticpoint = time.time()
        self.stopoint = -1

    def tic(self):
        self.ticpoint = time.time()
        return self

    def toc(self, withinittic=False):
        self.tictoc.append(time.time() - self.ticpoint)
        self.alltoc.append(time.time() - self.initpoint)
        if withinittic:
            self.tic()
        return self

    def add_exd(self, exd):
        if type(exd) is list:
            self.extradata += exd
        else:
            self.extradata.append(exd)

    def stop(self):
        self.stopoint = time.time()

    def sleep(self, n=0.1):
        time.sleep(n)
        return self

    def runtime_delay(self, delta_second=1):
        if delta_second < 0:
            print(day_forpast(0, ss='%Y-%m-%d %H:%M:%S'), '需要等待%s秒以继续....' % (-delta_second), )
            self.sleep(-delta_second)
        return self


def try_cmd(cmd):
    return os.popen(cmd).read()


def findall_in_list(self, content):
    """
    从列表中找出所有包含content的元素
    :param self: 列表本身
    :param content: 查找内容
    :return res_li: list 包含content的列表
    """
    try:
        content = str(content)
    except Exception as err:
        print('string failed !', err)
    res_li = []
    for x in self:
        try:
            if content in str(x):
                res_li.append(x)
        finally:
            pass
    return res_li


# list.findall_in_list = findall_in_list  # TypeError: can't set attributes of built-in/extension type 'list'


def findall_in_dir(content, path=running_dir, include_dir=True) -> list:
    """

    :param content: 查找内容
    :param path: 查找的根文件夹
    :param include_dir: 是否返回包含纯文件夹的结果
    :return res_li: list 包含content的列表:
    """
    res_li = []
    for ro, dirs, files in os.walk(path):
        if include_dir:
            res_li += findall_in_list([ro + os.sep + d for d in dirs], content)
        res_li += findall_in_list([ro + os.sep + f for f in files], content)
    return res_li


def content_walker(content, path=running_dir, include_dir=True):
    """

    :param content: 查找内容
    :param path: 查找的根文件夹
    :param include_dir: 是否返回包含纯文件夹的结果
    :return : generator 和 os.walk 输出模式一致
    """
    if include_dir:
        for ro, dirs, files in os.walk(path):
            if content in ro:
                yield ro, dirs, files
            else:
                dirs_with_content = findall_in_list([d for d in dirs], content)
                files_with_content = findall_in_list([f for f in files], content)
                if dirs_with_content + files_with_content:
                    yield ro, dirs_with_content, files_with_content
    else:
        for ro, dirs, files in os.walk(path):
            if content in ro:
                yield ro, files
            else:
                files_with_content = findall_in_list([f for f in files], content)
                if files_with_content:
                    yield ro, files_with_content


def generate_sl_general_id():
    return str(uuid.uuid4()).replace('-', '')


def sha2str(str_, hash_func=hashlib.sha256):
    encoded_str = str(str_).encode()
    return hash_func(encoded_str).hexdigest()


def bit_judge(int_num, lower_bit=0, higher_bit=0):
    """
    位标识的判断，输出原始值，比如
       8 被第3bit判断结果为1 bit_judge(8, 3) = 1
       7 被12bit判断结果为3 bit_judge(7, 1, 2) = 3
       7 单独被1/2bit判断结果都1 bit_judge(7, 1, 1) = 1； bit_judge(7, 2) = 1
    :param int_num: 待判断的int输入
    :param lower_bit: 连续的开关位低位界
    :param higher_bit: 连续的开关位高位界
    :return:
    """
    higher_bit = lower_bit if higher_bit == 0 else higher_bit  # 高位不传默认和低位一样
    re_int = 0
    for i_ in range(lower_bit, higher_bit + 1):
        re_int += int_num & (2 ** i_)
    return re_int >> lower_bit


def bit_judge_raw(int_num, judge_bit=0b001):
    """
    位标识的判断，输出原始值，比如 8 & 0b1001 输出为8
    :param int_num: 待判断的int输入
    :param judge_bit: 开关位/关注位
    :return:
    """
    return int_num & judge_bit


if __name__ == '__main__':
    list(content_walker('.py'))
    findall_in_dir('.py')
    findall_in_dir('py', os.path.dirname(running_dir), include_dir=False)

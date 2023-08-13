
from buildings.comm_across import *
from compress_file.dec_zip import *


def run_test():
    # p_ = try_cmd("D:\Programs\Python\Python39\python.exe E:/simulate_area/MLprocess/console_inner_sc.py")
    zh6.crack_until()


if __name__ == "__main__":
    ava_jobs_li = [
        run_test
    ]
    e_str = general_console_safe(ava_jobs_li)
    print(e_str)
    if e_str:
        eval(e_str)
    run_test()


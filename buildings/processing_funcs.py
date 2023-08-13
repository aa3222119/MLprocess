import multiprocessing
import time
# import cloudpickle


def always_dec(dt=60):
    """通用轮询
    """

    def wrapper(func):
        def _wrapper(*args, **k_args):
            while 1:
                func(*args, **k_args)
                time.sleep(dt)

        return _wrapper

    return wrapper


def polling_dec(dt=60, times=10 ** 66):
    """通用轮询
    """
    def wrapper(func):
        def _wrapper(*args, ):
            # 不传入times时几乎相当于无限循环，其实只被丢到后台做一次的时候就很实用了
            for i in range(times):
                p = multiprocessing.Process(target=func, args=(*args,), )
                p.start()
                time.sleep(dt)
                p.join()

        return _wrapper

    return wrapper


# def polling_dec_win10(dt=60, times=10 ** 66):
#     def wrapper(func):
#         def _wrapper(*args, ):
#             # 不传入times时几乎相当于无限循环，其实只被丢到后台做一次的时候就很实用了
#             _func_ = cloudpickle.loads(cloudpickle.dumps(func))
#             for i in range(times):
#                 p = multiprocessing.get_context('spawn').Process(target=_func_, args=(*args,), )
#                 p.start()
#                 time.sleep(dt)
#                 p.join()
#         return _wrapper
#     return wrapper


def general_bgp(func, args=(), **k_args):
    """
    通用版后端进程bgp background process, 只有一个进程去做这个任务，间隔时间是任务结束到下次开始的间隔
    :param func:
    :param args:
    :param k_args:
    :return:
    """
    if 'dt' not in k_args:
        k_args['dt'] = 300

    @always_dec(k_args['dt'])
    def continue_do_sth(*args_, **k_args_):
        # print(args_, k_args_)
        func(*args_, **k_args_)

    p = multiprocessing.Process(target=continue_do_sth, args=args, )
    p.start()
    return p


def general_bgp2(func, args=(), **k_args):
    """
    通用版后端进程bgp background process, 每次用新的进程来执行，间隔时间是任务开始到开始的间隔
    更通用的应该是这个
    :param func: 
    :param args: 
    :param k_args: dt 间隔的秒数  times 执行的次数
    :return: 
    """
    # if 'dt' not in k_args:
    #     k_args['dt'] = 300
    func_ = polling_dec(**k_args)(func)
    # print(args)
    return multiprocessing.Process(target=func_, args=args, ).start()


# def general_bgp2_win10(func, args=(), **k_args):
#     func_ = polling_dec(**k_args)(func)
#     d_func_ = cloudpickle.loads(cloudpickle.dumps(func_))
#     return multiprocessing.get_context('spawn').Process(target=d_func_, args=args, ).start()


def test_doing(glo, words):
    glo['test'] = words
    print(glo)


if __name__ == "__main__":
    print(f'这里是功能包被直接调用时,,,,')
    general_bgp2(test_doing, ({}, '测试亿下polling_dec装饰器否成功'), dt=5, times=2)
    # general_bgp2_win10(test_doing, ({}, 'win10下，测试polling_dec装饰器否成功'), dt=5, times=2)

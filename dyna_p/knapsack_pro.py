import numpy as np

np.set_printoptions(linewidth=100)


class KnapsackPro:

    def __init__(self, kv_li, kw_li):
        self._n = len(kv_li)
        assert self._n == len(kw_li), f'length error'
        self.v_li = kv_li
        self.w_li = kw_li
        # ret_ 背包问题的状态空间解，解释为前i个物体，体积为j时的最大价值
        self.ret_01 = np.zeros((self._n + 1, 1))  # 0-1 means 单背包问题
        self.ret_0_inf = np.zeros((self._n + 1, 1))  # 0-infinity means 无限背包问题

    def get_res_01(self, l_, v_):
        if v_ < 0:
            return - np.inf
        elif l_ < 0:
            return 0
        else:
            return self.ret_01[l_, v_]

    def solve_01(self, v_):
        v = v_ + 1
        solved_v = self.ret_01.shape[1]
        if solved_v < v:  # cache 机制
            _los = v - solved_v
            # print(f'{self.ret_01=}')
            self.ret_01 = np.concatenate([self.ret_01, np.zeros((self._n + 1, _los))], 1)
            we_li = [0] + self.w_li
            vo_li = [0] + self.v_li
            for j in range(solved_v - 1, v):
                for i in range(self._n + 1):
                    # 1.
                    without_i = self.get_res_01(i - 1, j)  # self.ret_01[i - 1, j]
                    with_i = self.get_res_01(i - 1, j - vo_li[i]) + we_li[i]  #
                    # # 2. also can
                    # if i > 0:
                    #     without_i = self.ret_01[i - 1, j]
                    #     if j < vo_li[i]:
                    #         with_i = - np.inf
                    #     else:
                    #         with_i = self.ret_01[i - 1, j - vo_li[i]] + we_li[i]
                    # else:
                    #     without_i = with_i = 0
                    # print(f'{j, i} {without_i=} {with_i=}')
                    self.ret_01[i, j] = max(without_i, with_i)
            print(f'{self.ret_01}')
        return self.ret_01

    def get_res_0_inf(self, l_, v_):
        if v_ < 0:
            return - np.inf
        elif l_ < 0:
            return 0
        else:
            return self.ret_0_inf[l_, v_]

    def solve_0_inf(self, v_):
        v = v_ + 1
        solved_v = self.ret_0_inf.shape[1]
        if solved_v < v:  # cache 机制
            _los = v - solved_v
            self.ret_0_inf = np.concatenate([self.ret_0_inf, np.zeros((self._n + 1, _los))], 1)
            we_li = [0] + self.w_li
            vo_li = [0] + self.v_li
            for j in range(solved_v - 1, v):
                for i in range(self._n + 1):
                    if i > 0:
                        without_i = self.get_res_0_inf(i - 1, j)
                        max_k = j // vo_li[i]
                        candi = [self.get_res_0_inf(i - 1, j - k * vo_li[i]) + k * we_li[i] for k in
                                 range(1, max_k + 1)]
                        print(f'{i=} {max_k=} {candi=}')
                        with_i = max(candi + [0])
                        self.ret_0_inf[i, j] = max(without_i, with_i)
                    else:
                        self.ret_0_inf[i, j] = 0
                print(f'{j=} {self.ret_0_inf}')
        return self.ret_0_inf

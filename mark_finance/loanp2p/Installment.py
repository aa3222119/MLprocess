# ===========================================
# @Time    : 2019/7/2 15:37
# @project : MLprocess
# @Author  : antony
# @Email   : 502202879@qq.com
# @File    : Installment
# @Software: PyCharm
# ===========================================

from sympy import solve
from sympy import abc


class MonthInstallment:
    """
    按月的分期付款计算，按月息为计息周期，一般常用的方式有等额本金和等额本息
    """
    def __init__(self, corpus, periods, y_rate, first_period_rate=1.0):
        """
        .   @param corpus 本金.
        .   @param periods 期数 即还款一共分期几个月.
        .   @param y_rate 年化利率 我们一般以年化来讨论.
        .   @param first_period_rate 第一个周期月的倍率，恰好为整月时是1.
        """
        self.m_rate = y_rate/12                          # 月利率
        self.corpus = corpus                             # 本金
        self.periods = periods                           # 期数
        self.first_period_rate = first_period_rate       # 第一周期月的倍率
        self.m_corpus_return = corpus/periods            # 每期应还本金
        self.return_li = []                              # 应还列表


    def equal_corpus(self):
        """
        等额本金
        """
        return_interest_li, left_ = [], self.corpus
        for i in range(self.periods):
            return_interest_li += [left_ * self.m_rate]
            left_ -= self.m_corpus_return
        return_interest_li[0] *= self.first_period_rate  # 对第一个月的应还利息做first_period_rate的修正
        self.return_li = [x + self.m_corpus_return for x in return_interest_li]
        return self.return_li

    def equal_corpus_interest(self):
        """
        等额本息
        """
        left_ = self.corpus * (1 + self.m_rate) ** self.first_period_rate - abc.x  # 第一个月的剩余
        for i in range(1, self.periods):
            left_ = left_ * (1 + self.m_rate) - abc.x
        return_x = solve(left_, [abc.x])  # 解方程剩余应还金额为0，求得未知数abc.x
        self.return_li = [return_x[0] for x in range(self.periods)]
        return self.return_li


if __name__ == '__main__':
    print(__name__)
    # from mark_finance.loanp2p.Installment import *
    mo = MonthInstallment(30000,6,0.07,1.13)
    mo.equal_corpus()
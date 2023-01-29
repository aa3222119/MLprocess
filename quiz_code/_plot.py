# ===========================================
# @Time    : 2019/7/17 19:57
# @project : MLprocess
# @Author  : antony
# @Email   : 502202879@qq.com
# @File    : _plot
# @Software: PyCharm
# ===========================================

import seaborn as sn
import pandas as pd
import matplotlib
import time

plt = matplotlib.pyplot

plt.rcParams['font.sans-serif'] = ['KaiTi']  # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题


def shift_time2h(ss):
    if type(ss) is str:
        t1 = time.strptime(ss, "%Y-%m-%d %H:%M:%S.0")
        return t1.tm_hour + t1.tm_min/60
    else:
        return 0


df = pd.read_csv('quiz_code\\testplotdata.txt', sep='\t' , encoding='gbk')


fig = plt.figure(figsize=(16, 9))  # figsize=(10,6)
pl = fig.add_subplot('111')
# x_ = df.query('dt_minutes<60')['dt_minutes']
x_ = df.loc[df['申请动用时间'].notnull(), '申请动用时间'].map(shift_time2h)
sn.distplot(x_, color="#988CBE", bins=24, rug=True, ax=pl)
x__ = x_.mean()

pl.plot([0, 0], [0, .1], color='#000000')
pl.plot([x__, x__], [0, .1], color='#009890', label='mean')
ybound = pl.properties()['ybound']
pl.annotate('mean of h:%2.2f \n count: %d' % (x__, x_.__len__()), xy=(x__, 0),
            xytext=(x__, 0.6 * ybound[1]),
            bbox=dict(boxstyle='sawtooth', fc="w"),
            arrowprops=dict(arrowstyle="-|>", connectionstyle="arc,rad=0.5", fc='r'))  # "-|>"代表箭头头上是实心的
pl.set_title(u'plot distributing: delta_d of uid=%s' )
pl.set_xlabel('h', fontsize=16, )
pl.set_ylabel('试试', fontsize=16)
pl.grid(True)
pl.axis([-1, x_.max() + 1] + list(ybound))

plt.tick_params(labelsize=18)  # 坐标轴数字标签大小
fig.show()
# ===========================================
# @Time    : 2018/11/29 14:44
# @Author  : antony
# @Email   : 502202879@qq.com
# @File    : hlearn.py
# @Software: PyCharm Community Edition
# ===========================================
import tensorflow as tf
import numpy as np


def add_layer(inputs, out_size, activation_function=None, name='', with_scope=False):
    # add one more layer and return the output of this layer
    # 可以加任意的层数 为DL打好基础
    in_size = int(inputs.shape[-1])  # inputs的最后一维
    if with_scope:
        # 大部件，定义层 layer，里面有 小部件 with定义的部件可以在tensorbord里看到
        with tf.name_scope('layer'):
            # 区别：小部件
            with tf.name_scope('weights'):
                weights = tf.Variable(tf.random_normal([in_size, out_size]), name='W'+name)
            with tf.name_scope('biases'):
                biases = tf.Variable(tf.zeros([1, out_size]) + 0.2, name='b'+name)
            # with tf.name_scope('wx_plus_b'):
    else:
        weights = tf.Variable(tf.random_normal([in_size, out_size]), name='W'+name)
        biases = tf.Variable(tf.zeros([1, out_size]) + 0.2, name='b'+name)

    wx_plus_b = tf.add(tf.matmul(inputs, weights), biases)
    if activation_function is None:
        outputs = wx_plus_b
    else:
        outputs = activation_function(wx_plus_b, )
    return weights, biases, outputs


# 第三维度下平行扩展添加层，
# 第三维度代表层，同层依然是全连接，层与层之间无连接
# 低三维度的层数由inputs的第三维度大小决定  inputs.shape[2] 没有则退化为add_layer
def parallel3_add_layer(inputs, out_size, activation_function=None, with_scope=False):
    in_size = int(inputs.shape[1])
    if len(inputs.shape) == 3 and inputs.shape[2]:
        parallel_size = int(inputs.shape[2])
        if with_scope:
            with tf.name_scope('layer'):
                weights = tf.Variable(tf.random_normal([in_size, out_size, parallel_size]), name='W_')
                biases = tf.Variable(tf.zeros([1, out_size, parallel_size]) + 0.1, name='b_')
        else:
            weights = tf.Variable(tf.random_normal([in_size, out_size, parallel_size]), name='W_')
            biases = tf.Variable(tf.zeros([1, out_size, parallel_size]) + 0.1, name='b_')
        out_li = [tf.add(tf.matmul(inputs[:, :, i], weights[:, :, i]), biases[:, :, i]) for i in range(parallel_size)]
        wx_plus_b = tf.stack(out_li, 2)
        if activation_function is None:
            outputs = wx_plus_b
        else:
            outputs = activation_function(wx_plus_b, )
        return weights, biases, outputs
    else:
        return add_layer(inputs, out_size, activation_function, '', with_scope=with_scope)


def nd_inx_li(nd_shape):  # 任意维度的shape下的所有索引的组合, 输出列表可直接迭代
    iter_li = ['for x%s in range(%s)' % (ix, nd_shape[ix]) for ix in range(len(nd_shape))]
    iter_ss = ' '.join(iter_li)
    tuple_ss = '(%s,)' % ','.join(['x%s' % ix for ix in range(len(nd_shape))])
    return eval('[%s %s]' % (tuple_ss, iter_ss))  # pix 索引的-1维度的位置


class SortedArrayHot:

    def __init__(self, li):  # li=[-1, 0, 1]
        arr = np.array(li)
        self.arr = arr
        self.status = 1
        self.lengt = len(arr)-1 # lengt 实际长度-1 index的最大值
        for i in range(1, self.lengt + 1):
            if arr[i] <= arr[i-1]:
                self.status = 0
                print('Not Positive sequence arrangement!! baded status')

    def inx_arr(self, x):
        if self.arr[0] >= x:
            return 0, 1
        if x >= self.arr[-1]:
            return self.lengt-1, 0
        for i in range(0, self.lengt):
            if x < self.arr[i+1]:
                return i, 1 - (x-self.arr[i])/(self.arr[i+1]-self.arr[i])

    def arr2hot(self, input_arr):
        hot_shape = input_arr.shape + self.arr.shape
        hot_ = np.zeros(hot_shape)
        # iter_li = ['for x%s in range(%s)' % (ix, input_arr.shape[ix]) for ix in range(len())]
        # iter_ss = ' '.join(iter_li)
        # tuple_ss = '(%s)' % ','.join(['x%s' % ix for ix in range(len(input_arr.shape))])
        # pix_zip = eval('[%s %s]' %(tuple_ss, iter_ss)) # pix 索引的-1维度的位置
        for pix in nd_inx_li(input_arr.shape):
            x = input_arr[pix]
            inx, val = self.inx_arr(x)
            hot_[pix + (inx,)] = val
            hot_[pix + (inx+1,)] = 1 - val
        return hot_

    def hot2arr(self, input_hot):
        if input_hot.shape[-1] == self.lengt + 1:
            arr_ = np.zeros(input_hot.shape[:-1])
            for pix in nd_inx_li(input_hot.shape[:-1]):
                arr_[pix] = (self.arr * input_hot[pix]).sum()
            return arr_
        else:
            print("iput_hot's last demension not suit !! right is ", self.lengt + 1)


class ConfusionMatrix:

    def __init__(self, y_label, y_pre):
        self.label = y_label.copy()
        self.pre = y_pre.copy()
        self.label.shape = (self.label.shape[0],)
        self.pre.shape = (self.pre.shape[0],)
        if self.label.shape[0] != self.pre.shape[0]:
            print('length problem')

    def acc(self, th=0.5):  # 精确率、准确率 Accuracy
        y_l = np.zeros(self.label.shape)
        y_l[self.pre > th] = 1
        return self.label[self.label == y_l].shape[0]/self.label.shape[0]

    def precision(self, th=0.5):  # 精准率、查准率
        y_l = np.zeros(self.label.shape)
        y_l[self.pre > th] = 1
        return self.label[(self.label == y_l) & (y_l == 1)].shape[0] / self.label[y_l == 1].shape[0]

    def tpr(self, th=0.5):   # 真正例率 所有正样本中 也是常说的召回率
        y_l = np.zeros(self.label.shape)
        y_l[self.pre > th] = 1
        return self.label[(self.label == y_l) & (self.label == 1)].shape[0] / self.label[self.label == 1].shape[0]

    def tnr(self, th=0.5):  # 真负例率 所有负样本中
        y_l = np.zeros(self.label.shape)
        y_l[self.pre > th] = 1
        return self.label[(self.label == y_l) & (self.label == 0)].shape[0] / self.label[self.label == 0].shape[0]

    def fpr(self, th=0.5):   # 假正例率 所有负样本中
        return 1 - self.tnr(th)

    def fb_score(self, th=0.5, beta=1):  # balanced F Score 默认beta=1为f1_score
        prec = self.precision(th)  # Accuracy
        rec = self.tpr(th)  # recall
        b2 = beta**2  #
        return (1 + b2)*prec*rec/(rec + b2*prec)

    def auc(self):  # 一种AUC的计算方式
        sorted_ind = np.argsort(self.pre)[::-1]
        auc_value, positive_pool = 1, 0
        positive_len, samples_len = self.label[self.label == 1].shape[0], self.label.shape[0]
        negative_len = samples_len - positive_len
        positive_part, negative_part = 1/positive_len, 1/negative_len
        for inx in sorted_ind:
            if self.label[inx] == 1:
                positive_pool += positive_part
            else:
                auc_value -= negative_part*(1-positive_pool)
        return auc_value

    def status_p(self):
        return f'''Accuracy:{self.acc()}| precision:{self.precision()}| recall:{self.tpr()}| fpr:{self.fpr()}
        fb_score:{self.fb_score()}| AUC:{self.auc()}'''


if __name__ == '__main__':
    harr = SortedArrayHot([-1, 0, 1])
    input_array = np.array([.4, -.6, 1, -1])
    # 也可以兼容一般意义上的 onehot
    # harr = SortedArrayHot([1, 2, 3, 4])  # 关键在于hot边界的选取 第一行
    # input_array = np.array([3, 1, 1, 2, 4, 2.6])   # 取值不为整数的时候 可以转成hot编码  最后一个取值2.6
    # hot_ = harr.arr2hot(input_array)
    # harr.hot2arr(hot_)
    #
    # # 它还可以适用于N维到N+1维
    # harr = SortedArrayHot([-1, 0, 1])
    # input_array = np.array([[.4, -.6, .1],[1, -.3, .8]])
    # hot_ = harr.arr2hot(input_array)
    # harr.hot2arr(hot_)


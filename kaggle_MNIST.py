# ===========================================
# @Time    : 2018/8/21 11:39
# @Author  : antony
# @Email   : 502202879@qq.com
# @File    : kaggle_MNIST.py
# @Software: PyCharm Community Edition
# ===========================================

import numpy as np
import struct
import matplotlib.pyplot as plt
from functools import reduce
from time import time


def idxtomat(filename, ints='>IIII'):
    binfile = open(filename, 'rb')
    buf = binfile.read()
    magic, *dims = struct.unpack_from(ints, buf)

    index = struct.calcsize(ints)
    BS = reduce(lambda x, y: x * y, dims)

    ims = struct.unpack_from('>%sB' % BS, buf, index)
    print(index, dims, BS)
    ims = np.array(ims)
    ims = ims.reshape(tuple(dims))
    return ims


def showimg(mat, title='手写数字'):
    plt.figure()
    plt.imshow(mat, cmap='gray')
    plt.title(title)
    plt.show()
    return plt


filename = ['train-images.idx3-ubyte', 'train-labels.idx1-ubyte', 't10k-images.idx3-ubyte', 't10k-labels.idx1-ubyte']


tr_imgs=idxtomat('datasets/' + filename[0])
tr_labs=idxtomat('datasets/' + filename[1], '>II')
t10_imgs=idxtomat('datasets/' + filename[2])
t10_labs=idxtomat('datasets/' + filename[3], '>II')


judge_imgs = np.zeros((10,28,28))


for i in range(0, 10):
    print(tr_labs[tr_labs == i].shape)
    judge_imgs[i] = tr_imgs[tr_labs == i].mean(0)
    showimg(judge_imgs[i])


# showimg(tr_imgs[2])
# print(tr_imgs.shape,tr_labs.shape,t10_imgs.shape,t10_labs.shape,tr_labs[2])
# print(tr_imgs[2])

test_num = 10000
t10_labs = t10_labs[:test_num]

ones = np.ones(test_num)
K = 5  #
candi_ = np.ones(K) * -1

labs_ = ones * -1
t1 = time()
tr_imgs_used = tr_imgs[:60000]
for x in range(test_num):
    t10_img = t10_imgs[x]
    # s = np.tile(0, 10)
    # for i in range(10):
    #    dis=t10_img-judge_imgs[i]
    #   diss=dis**2
    #   s[i]=diss.sum()
    # s[i]=sdi**0.5
    # s = ((np.tile(t10_img, (60000, 1, 1)) - tr_imgs) ** 2).sum((1, 2))
    s = ((t10_img - tr_imgs_used) ** 2).sum((1, 2))

    # # labs_[x] = tr_labs[list(s).index(s.min())]
    # labs_[x] = tr_labs[s.argmin()]
    for k in range(K):
        min_index = s.argmin()
        candi_[k] = int(tr_labs[min_index])
        s[min_index] = 999999999
    labs_[x] = np.argmax(np.bincount(candi_.astype(int)))

    # print(s,s.min(),list(s).index(s.min()))
    # showimg(t10_img)

print(f'K={K},耗时{time()-t1}秒, 训练样本数量:{len(tr_imgs_used)}, 准确率{ones[labs_ == t10_labs].sum() / ones.sum()}')


# 彩蛋
xx = np.argwhere(t10_labs == 1)
for x in xx[:100:9]:
    x = int(x)
    showimg(t10_imgs[x], 't10 index:  %d' % x)



plt.figure()
plt.imshow(t10_imgs[2] - t10_imgs[145])
plt.show()

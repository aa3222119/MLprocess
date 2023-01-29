# ===========================================
# @Time    : 2019/7/23 20:54
# @project : MLprocess
# @Author  : antony
# @Email   : 502202879@qq.com
# @File    : Recursion_Cellular_
# @Software: PyCharm
# ===========================================
from tf_comm import *
import os
import pandas as pd
import numpy as np

data_dir = f'D:\chrome_download{os.sep}'

# --


import cv2


def showing_img_(img_arr, img_name='shuai', dur=5000):
    cv2.imshow(img_name, img_arr)
    cv2.waitKey(dur)
    cv2.destroyAllWindows()


class ImgHandle:

    def __init__(self, df, tp='train'):
        self.df_t__ = df
        self.tp = tp
        self.s1_channel_li = [f'_s{i}_w{j}' for i in [1] for j in range(1, 7)]
        self.s2_channel_li = [f'_s{i}_w{j}' for i in [2] for j in range(1, 7)]
        self.train_x, self.train_y, self.cor = None, None, 0
        self.batch_size = 200

    def get_img_by_id(self, ind):
        # e_p_w = self.df_t__.loc[ind, "id_code"].replace('_', '\\')
        experiment = self.df_t__.loc[ind, "experiment"]
        plate = self.df_t__.loc[ind, "plate"]
        well = self.df_t__.loc[ind, "well"]
        e_p_w = f'{experiment}{os.sep}Plate{plate}{os.sep}{well}'
        # print(f'{data_dir}{self.tp}{os.sep}{e_p_w}')
        img_s1_li, img_s2_li = [], []
        df_ind = df_pixel_stats_idx.loc[ind, :]
        # astype(np.int16) 之后相减才有负数
        for w in range(1, 7):
            df_ind_s1 = df_ind.query(f'site=={1}&channel=={w}')
            img_s1 = cv2.imread(f'{data_dir}{self.tp}{os.sep}{e_p_w}_s{1}_w{w}.png')[:, :, 0:1].astype(np.int16)
            df_ind_s2 = df_ind.query(f'site=={2}&channel=={w}')
            img_s2 = cv2.imread(f'{data_dir}{self.tp}{os.sep}{e_p_w}_s{2}_w{w}.png')[:, :, 0:1].astype(np.int16)
            img_s1_li.append(img_s1 - int(df_ind_s1['mean']))
            img_s2_li.append(img_s2 - int(df_ind_s2['mean']))

        # img_s1_li = [cv2.imread(f'{data_dir}{self.tp}{os.sep}{e_p_w}_s{s}_w{w}.png')[:, :, 0:1].astype(np.int16) -
        #              int(df_pixel_stats_idx.loc[ind, :].query(f'site=={s}&channel=={w}')['mean'])
        #              for s in [1] for w in range(1, 7)]
        img_s1_com = np.concatenate(img_s1_li, 2)
        # img_s2_li = [cv2.imread(f'{data_dir}{self.tp}{os.sep}{e_p_w}_s{s}_w{w}.png')[:, :, 0:1].astype(np.int16) -
        #              int(df_pixel_stats_idx.loc[ind, :].query(f'site=={s}&channel=={w}')['mean'])
        #              for s in [2] for w in range(1, 7)]
        img_s2_com = np.concatenate(img_s2_li, 2)
        return img_s1_com, img_s2_com

    def gen_train_xy(self, ids_li=None):
        if ids_li is None:
            ids_li = self.df_t__.index[:500]
        train_x_li = []
        train_y = np.zeros((len(ids_li), 1111))
        for i in range(len(ids_li)):
            id = ids_li[i]
            target = self.df_t__.loc[id, "sirna"]
            train_y[i, target] = 1
            # 不妨先只看 s1
            img = self.get_img_by_id(id)[0]
            train_x_li.append(img[np.newaxis, :, :, :])
        train_x = np.concatenate(train_x_li, axis=0)
        return train_x, train_y

    def exchange_xy(self):
        if self.train_x is None:
            self.train_x, self.train_y = self.gen_train_xy(self.df_t__.index[:self.batch_size])
            self.cor = self.batch_size
        else:
            half_size = int(.5*self.batch_size)
            self.train_x, self.train_y = self.train_x[half_size:], self.train_y[half_size:]
            train_x, train_y = self.gen_train_xy(self.df_t__.index[self.cor: self.cor + half_size])
            self.train_x = np.concatenate([self.train_x, train_x], 0)
            self.train_y = np.concatenate([self.train_y, train_y], 0)
            self.cor += half_size
            if self.cor > len(self.df_t__):
                self.cor = 0
        # print(self.train_x.sum())


df_pixel_stats = pd.read_csv(f'{data_dir}pixel_stats.csv')
df_pixel_stats_idx = df_pixel_stats.set_index('id_code')
# df_pixel_stats_idx.loc['HEPG2-01_1_B02', ].query('site==1&channel==1')

df_train = pd.read_csv(f'{data_dir}train.csv', index_col='id_code')
df_train_con = pd.read_csv(f'{data_dir}train_controls.csv', index_col='id_code')
df_test = pd.read_csv(f'{data_dir}test.csv', index_col='id_code')
df_test_con = pd.read_csv(f'{data_dir}test_controls.csv', index_col='id_code')
df_res = pd.read_csv(f'{data_dir}sample_submission.csv', index_col='id_code')

img_t = ImgHandle(df_train, 'train')
# img_s1, img_s2 = img_t.get_img_by_id('HEPG2-01_1_B11')
# train_x, train_y = img_t.gen_train_xy(df_train.index[1000:1500])
img_t.exchange_xy()
samples, height, width, channels = img_t.train_x.shape
_, y_len = img_t.train_y.shape

img_input = tf.compat.v1.placeholder(tf.float32, [None, height, width, channels], name='img_input')
y_input = tf.compat.v1.placeholder(tf.float32, [None, y_len], name='y_input')

conv1_1 = add_conv_layer(img_input, [3, 3], 32, [1, 3, 3, 1], padding='VALID', name='conv1_1')
conv1_2 = add_conv_layer(conv1_1, [3, 3], 32, [1, 3, 3, 1], padding='SAME', name='conv1_2')
conv1_3 = add_conv_layer(conv1_2, [2, 2], 64, [1, 2, 2, 1], padding='SAME', name='conv1_2')
poo11 = add_pooling(conv1_3, [1,3,3,1], [1,2,2,1])
conv2_1 = add_conv_layer(poo11, [3, 3], 128, [1, 3, 3, 1], padding='SAME', name='conv2_1')
conv2_2 = add_conv_layer(conv2_1, [2, 2], 256, [1, 2, 2, 1], padding='SAME', name='conv2_2')
poo12 = add_pooling(conv2_2, [1,3,3,1], [1,2,2,1], pooling_func=tf.nn.avg_pool2d)
conv3_1 = add_conv_layer(poo12, [2, 2], 512, [1, 2, 2, 1], padding='SAME', name='conv3_1')
conv3_2 = add_conv_layer(conv3_1, [2, 2], 1024, [1, 2, 2, 1], padding='SAME', name='conv3_2')
# conv3_3 = add_conv_layer(conv3_2, [2, 2], 1024, [1, 1, 1, 1], padding='VALID', name='conv3_3')
# poo13 = add_pooling(conv3_2, [1,2,2,1], [1,1,1,1], pooling_func=tf.nn.avg_pool2d)

feature_nums = int(conv3_2.shape[1]) * int(conv3_2.shape[2]) * int(conv3_2.shape[3])
flatten = tf.reshape(conv3_2, [-1, feature_nums])
print(flatten.shape)
weight, b, dense1 = add_layer(flatten, 1024, tf.nn.relu, name='1')
weight1, b1, label_out = add_layer(dense1, y_len, None, name='o')  #
# loss_c = tf.reduce_mean(tf.pow(tf.subtract(label_out, y_input), 2), name='loss_c')
E2 = tf.nn.softmax_cross_entropy_with_logits_v2(labels=y_input, logits=label_out)
loss_c = tf.reduce_mean(E2, name='loss_c')
train_step_c = tf.compat.v1.train.AdamOptimizer(learning_rate=0.002).minimize(loss_c)

sess = tf.compat.v1.Session()
sess.run(tf.compat.v1.global_variables_initializer())

# 简易训练控制
loss, task_num = 1, 1
while loss > 0.5 and task_num < 777:

    step_size = img_t.batch_size - 70
    loss = sess.run(loss_c, feed_dict={img_input: img_t.train_x, y_input: img_t.train_y})
    print(f'task_{task_num}  do_:{img_t.batch_size}  cursor:{img_t.cor}  loss:{loss:#.4f}', end=' || ')

    for i in range(18):
        # if task_num % 10 == 1 and i % 3 == 0:
        #     loss = sess.run(loss_c, feed_dict={img_input: img_t.train_x, y_input: img_t.train_y})
        #     print(i, loss)
        batch_st = 14 * (i // 3)  # 对应剩下的分5次分别训练
        batch_ed = batch_st + step_size
        sess.run(train_step_c, feed_dict={img_input: img_t.train_x[batch_st: batch_ed],
                                          y_input: img_t.train_y[batch_st: batch_ed]})
    loss = sess.run(loss_c, feed_dict={img_input: img_t.train_x, y_input: img_t.train_y})
    print(f'loss_after:{loss:#.4f}')
    img_t.exchange_xy()
    task_num += 1


img_test = ImgHandle(df_test, 'test')
df_test['sirna'] = 911
for id in df_test.index:
    img_, img_s2_ = img_test.get_img_by_id(id)
    label_hot = sess.run(label_out, feed_dict={img_input: img_[np.newaxis, :, :, :]})
    df_test.loc[id, 'sirna'] =  label_hot.argmax()

print(df_test.head())
print(len(df_test.query('sirna>911')), len(df_test.query('sirna<911')))

# def predict_img(id):
#     img_, img_s2 = img_test.get_img_by_id(id)
#     label_hot = sess.run(label_out, feed_dict={img_input: img_[np.newaxis, :, :, :]})
#     label_hot.argmax()
#
#

# --

df_test.loc[:, ['sirna']].reset_index().to_csv(f'{data_dir}{os.sep}submission1.csv', index=False)




import tensorflow as tf
import numpy as np

def softmax(x):
    sum_raw = np.sum(np.exp(x),axis=-1)
    x1 = np.ones(np.shape(x))
    for i in range(np.shape(x)[0]):
        x1[i] = np.exp(x[i])/sum_raw[i]
    return x1

# y = np.array([[1,0,0],[0,1,0],[0,0,1],[1,0,0],[0,1,0]])# 每一行只有一个1
# logits =np.array([[12,3,2],[3,10,1],[1,2,5],[4,6.5,1.2],[3,6,1]])
y = np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0],[1,0,0,0],[0,1,0,1]])# 每一行只有一个1
logits =np.ones(y.shape)
# 按计算公式计算
y_pred =softmax(logits)
E1 = -np.sum(y*np.log(y_pred),-1)
print(E1)
# 按封装方法计算
sess = tf.compat.v1.Session()
y = np.array(y).astype(np.float64)
E2 = sess.run(tf.nn.softmax_cross_entropy_with_logits(labels=y,logits=logits))
print(E2)

if E1.all() == E2.all():
    print("True")
else:
    print("False")
# 输出的E1，E2结果相同
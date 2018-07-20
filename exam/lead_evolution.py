import numpy as np
import random
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")
with open('exam/sjc/sjc4b.txt') as file:
# with open('exam/cpmp01-20/cpmp20.txt') as file:
    data = file.readlines()

sample_size, clusters_size = (int(x) for x in data.pop(0).strip().split())
all_ = set(range(sample_size))  # 所有点的集合
data_list =[[int(i) for i in x.strip().split()] for x in data]
data_matrix = np.matrix(data_list)
masss = data_matrix[:, 3]

sample_size = data_matrix.shape[0] if data_matrix.shape[0] == sample_size else data_matrix.shape[0]
all_dis = np.hstack([np.power(np.power(data_matrix[i, :2] - data_matrix[:, :2], 2).sum(1), 0.5) for i in range(sample_size)])
mean_dis = all_dis.mean()
last_slove = all_dis.sum(0).min()  # 最终求解目标,点的距离和。  --------> 所有的进化之为此
all_dis_inf = all_dis.copy()
all_dis_inf[all_dis_inf == 0] = np.inf


# np.random.randint(sample_size)  #


def randind_by_value(arr):
    # if type(arr) is list:
    arr = np.array(arr)
    # if type(arr) == np.matrixlib.defmatrix.matrix and arr.shape[1] == 1:   # 化成一行
    #     arr = arr.T
    #     L = arr.shape[1]
    L = arr.shape[0]
    arr_uni = arr / arr.sum()
    p = np.random.rand()
    for i in range(L):
        p -= arr_uni[i]
        if p <= 0:
            return i


class Gaze():
    count = 0
    mass_list = masss.T.tolist()[0]
    Mass = masss.sum()                     # 所有样本总质量
    region_max = data_matrix[:, 2].max()   # 区域最大质量约束
    saturation = Mass / clusters_size / region_max  # 饱和度
    stat_usenum = np.zeros(sample_size)
    point_rev_index = [set() for i in range(sample_size)]  # 全局的所有点在哪些个Clus中的倒排索引

    def show_status(self):
        print('Gaze status\nClus num::', self.count)


class OneClus(Gaze):
    def __init__(self, sample_size):
        Gaze.count += 1
        self.cid = Gaze.count  # cluster的id 类似数据库的自增
        self.center = np.random.randint(sample_size)  # 中心点序号
        self.pnum_set = {self.center}                # 类的序号集合
        self.score = 0
        self.outload_tries = 0                       # 尝试的超重次数
        self.dis_1d = all_dis_inf.copy()[:, self.center]        # 该类中心到其他点的距离一维，进入类的对应位置变成inf
        self.dis_1d_list = all_dis[self.center, :].tolist()[0]     # 保留原始值
        self.sum_dis = 0                           # 该类的距离和
        self.total_mass = Gaze.mass_list[self.center]  # 该类的质量和
        # self.totally_full = False   # 当前连最小的样本也装不上了
        self.fit = 1  # 该类的存活率

    @property
    def std0(self):
        arrx = all_dis[list(self.pnum_set), self.center]
        return arrx[arrx>0].std()

    def __checkcenter(self):
        pass

    def delpoint(self, pnum):
        if pnum in self.pnum_set:
            Gaze.point_rev_index[pnum] -= {self.cid}
            self.pnum_set -= {pnum}
            self.sum_dis -= self.dis_1d_list[pnum]
            self.total_mass -= Gaze.mass_list[pnum]
            self.dis_1d[pnum] = self.dis_1d_list[pnum]
        else:
            print('can not del')
            return 0

    def addpoint(self, pnum):  # 添加点编号为pnum的点
        if pnum in self.pnum_set:
            print('already in , can not add')
            return 0
        else:
            new_mass = self.total_mass + Gaze.mass_list[pnum]
            if new_mass < Gaze.region_max:
                self.pnum_set.update({pnum})
                self.sum_dis += self.dis_1d_list[pnum]
                self.dis_1d[pnum] = np.inf
                self.total_mass = new_mass
                self.__checkcenter()
                return 1
            else:
                self.outload_tries += 1
                return 0

    def gain_onestep(self, compare_size=1):
        gain_candidate = [randind_by_value(np.power(self.dis_1d, -4)) for i in range(compare_size)]  # 距离越近越可能成为候选进入的点candidate, 已近进入Clus的因为距离为inf不会具备进入的概率
        for e in gain_candidate:
            P1 = 0.6*((mean_dis - self.dis_1d[e])/mean_dis + 1) + 0.2  # 进一步缩小距离过于远的概率
            # print(P1)
            if random.random() < P1:
                res = self.addpoint(e)
                if res:
                    return 1     # 该方法成功添加一个既停止
        return 0

    def change_mcenter(self):
        # 寻找最好中心，一般发生在修剪完点之后。如果执行此方法后再delpoint,则不能保证依然是最好中心了。
        for n in self.pnum_set:
            sum_dis_candi = all_dis[list(self.pnum_set), n].sum()
            if sum_dis_candi < self.sum_dis:
                print('更好的中心减少距离%s' %(self.sum_dis-sum_dis_candi), '新的中心：', n)
                self.center = n
                self.sum_dis = sum_dis_candi
        # 更换中心后需要随即更换下面俩
        self.dis_1d = all_dis_inf.copy()[:, self.center]  # 该类中心到其他点的距离一维，进入类的对应位置变成inf
        for n in self.pnum_set:
            self.dis_1d[n] = np.inf
        self.dis_1d_list = all_dis[self.center, :].tolist()[0]  # 保留原始值

    def show_status(self):
        print(self.center, '==>', self.pnum_set)
        print('all dis::', self.sum_dis, ';  in all mass::', self.total_mass)
        print('cid::', self.cid, 'outload_tries::', self.outload_tries)

    def __del__(self):
        print('del cluster cid=%s' % self.cid)
        for pnum in self.pnum_set:
            Gaze.point_rev_index[pnum] -= {self.cid}


class ClusCsize():
    # 一个此类需要构成一个解
    def __init__(self):  # 初始化时顺便加入第一个类
        self.stat_usenum = np.zeros(sample_size)
        self.cid_set = set()  # 解中cid,最后长度需要等于clusters_size
        self.pnum_set = set()  # 解的clus集合中所有点的登记,最后长度需要等于sample_size
        self.center_set = set()  # 解中所有中心的集合
        self.total_dis = 0
        self.point_rev_index = [set() for i in range(sample_size)]  # 一个ClusCsize构成的解中所有点在哪些个Clus中的倒排索引

    @property
    def stdarr(self):
        arrx = np.array([clus_pool[cid].std0 for cid in self.cid_set])
        return arrx

    def addclus(self, clus_id):
        if len(self.cid_set) < clusters_size and clus_id not in self.cid_set:
            self.cid_set |= {clus_id}
            self.pnum_set |= clus_pool[clus_id].pnum_set
            self.center_set |= {clus_pool[clus_id].center}
            for n in clus_pool[clus_id].pnum_set:
                self.stat_usenum[n] += 1
                self.point_rev_index[n] |= {clus_id}
            self.total_dis += clus_pool[clus_id].sum_dis
            return 1
        else:
            return 0

    def all_changecenter(self):
        for cid in list(self.cid_set):
            clus_pool[cid].change_mcenter()

    def all_alter_point(self):
        for n in range(sample_size):
            candi_cids = list(self.point_rev_index[n])  # set 无法索引 ; 转成list
            while int(self.stat_usenum[n]) > 1:
                if all_dis[clus_pool[candi_cids[0]].center, n] < all_dis[clus_pool[candi_cids[1]].center, n]:
                    del_cid = candi_cids.pop(1)  # 需要删掉点n的cid
                else:
                    del_cid = candi_cids.pop(0)
                print(n, candi_cids, del_cid)
                clus_pool[del_cid].delpoint(n)
                self.point_rev_index[n] -= {del_cid}
                self.stat_usenum[n] -= 1
            # for i in range(int(self.stat_usenum[n]-1)):
            #     this_cid = candi_cids[i]
            #     that_cid = candi_cids[i+1]
            #     if all_dis[clus_pool[this_cid].center,n] < all_dis[clus_pool[that_cid].center,n]:
            #         del_cid = that_cid  # 需要删掉点n的cid
            #     else:
            #         del_cid = this_cid
            #     print(n, candi_cids, del_cid)
            #     clus_pool[del_cid].delpoint(n)
            #     self.point_rev_index[n] -= {del_cid}
            # self.stat_usenum[n] = 1

    def rand_optimiza(self):
        pass

    @property
    def slove_stat(self):
        cids_dis = [clus_pool[cid].sum_dis for cid in self.cid_set]
        return np.array(cids_dis).sum()

    def natural_selection(self):  # 外层各自更新Oneclus.fit 依据其的一次自然选择
        for cid in self.cid_set:
            p = random.random()
            print(cid, '存活率:', clus_pool[cid].fit, p)
            if p > clus_pool[cid].fit:
                del clus_pool[cid]

    def plot_status(self):
        plt.figure(figsize=(14, 8))
        for i in range(sample_size):
            plt.scatter(data_matrix[i, 0], data_matrix[i, 1], marker='.', color='r', s=data_matrix[i, 3])
        for cid in list(self.cid_set):
            color = hex(random.randint(1111111, 7777777)).replace('0x', '#')
            for i in clus_pool[cid].pnum_set:
                x0 = data_matrix[i, 0]
                x1 = data_matrix[i, 1]
                c_x0 = data_matrix[clus_pool[cid].center, 0]
                c_x1 = data_matrix[clus_pool[cid].center, 1]
                plt.text(x0, x1, str(i), color=color, fontdict={'weight': 'bold', 'size': 8})
                plt.plot([x0, c_x0], [x1, c_x1], color)
        plt.title("generation={:d},FO={:.5f}".format(1, self.slove_stat))


def add_cluspool(num=clusters_size*100):
    # alls = set()
    for i in range(num):
        Clus = OneClus(sample_size)
        for j in range(999):
            Clus.gain_onestep(3)
            if Clus.outload_tries > 3:
                break

        Clus.show_status()
        clus_pool[GM.count] = Clus
        # 添加point_rev_index
        for n in Clus.pnum_set:
            GM.point_rev_index[n] |= {Clus.cid}

        # alls |= Clus.pnum_set
        # if len(all_ - alls)==0:
        #     print(clus_pool.__len__())
        #     break


# ============= 预留的关键进化点1, 如何选择合并的步伐
def gener_slove():
    slo = ClusCsize()
    i = 0
    for i in range(1000):
        # point_num = randind_by_value(np.power(slo.stat_usenum+1, -1))
        needpoints = np.where(slo.stat_usenum == slo.stat_usenum.min())[0]  # 被需要的points
        needpoints_set = set(needpoints)
        if len(needpoints_set) < 20:  # 最后的时候 组合需要一定的目的性
            candi_cid_list = []   # 至少能包含一个所需cid列表
            for point in needpoints_set:
                candi_cid_list += list(GM.point_rev_index[point])
            rand_cid = random.choice(candi_cid_list)
        else:
            rand_cid = random.choice(list(clus_pool.keys()))  # 候选的cid
        cid_have_needpoints = clus_pool[rand_cid].pnum_set & needpoints_set  # cid有的被需要的ponits
        cid_have_needpoints_num = len(cid_have_needpoints)
        p = round(random.random(), 3)
        pth = round(0.4*(1-2**(-cid_have_needpoints_num)) + 0.1*int(cid_have_needpoints_num/4) + 0.2*int(len(slo.cid_set)/10), 3)
        print(cid_have_needpoints_num, pth, p, end='|> ')
        if p < pth and float(cid_have_needpoints_num) > (sample_size-len(slo.pnum_set))/(clusters_size-len(slo.cid_set)):
            slo.addclus(rand_cid)
            print(len(slo.cid_set),len(slo.pnum_set))
        # cids_set = all_.copy()
        # for i in range(5):
        #     point_num = points[i]
        #     cids_set &= GM.point_rev_index[point_num]
        #     print(cids_set)
        # point_num = random.choice()
        # print(i, slo.addclus(GM.point_rev_index[point_num].copy().pop()))
        if len(slo.cid_set) == clusters_size:
            break
    return i < 999, slo

GM = Gaze()
clus_pool = {}

add_cluspool(clusters_size*20)
while clus_pool.__len__() > 1000:
    success_flag,slo = gener_slove()
    if success_flag:
        slo.all_alter_point()
        # slo.plot_status()
        slo.all_changecenter()
        slo.plot_status()
        print(slo.slove_stat)
    else:
        stds_mean = slo.stdarr.mean()
        for cid in slo.cid_set:
            clus_pool[cid].fit -= clus_pool[cid].std0/stds_mean/clusters_size  # 更新存活率
    slo.natural_selection()







# ----------------解的可视化---------------------

plt.figure(figsize=(14, 8))
for i in range(sample_size):
    plt.scatter(data_matrix[i, 0], data_matrix[i, 1], marker='.', color='r', s=data_matrix[i, 3])
for cid in list(slo.cid_set):
    color = hex(random.randint(1111111, 7777777)).replace('0x', '#')
    print(color)
    for i in clus_pool[cid].pnum_set:
        x0 = data_matrix[i, 0]
        x1 = data_matrix[i, 1]
        c_x0 = data_matrix[clus_pool[cid].center, 0]
        c_x1 = data_matrix[clus_pool[cid].center, 1]
        plt.text(x0, x1, str(i), color=color, fontdict={'weight': 'bold', 'size': 8})
        plt.plot([x0, c_x0], [x1, c_x1], color)




# if __name__ == '__main__':
#     filename1 = "D:/psocpmp/2017年终版/最终版/最终版/result_sjc4b-局部.txt"
#     # logfile=open("D:/psocpmp/PSO0522/PSO0522/result4a.txt","r")
#     filename = 'D:/psocpmp/cpmp0727/CPMP/CPMP/sjc4b.txt'  # txt文件和当前脚本在同一目录下，所以不用写具体路径
#     f = open(filename, 'r')
#     logfile = open(filename1, 'r')
#     x = []
#     y = []
#     q = []
#     data = []
#     Efield = []
#     for line in f.readlines():
#         data.append(list(map(int, line.split())))
#
#     f.close()
#     n_number = data[0][0]
#     p_number = data[0][1]
#
#     labels = []
#     len = 0
#     for line in logfile.readlines():
#         labels.append(list(map(float, line.split())))
#         len = len + 1
#     # print(data)
#     # print(len(labels[0]),len(labels[1]),len(labels[2]),len(labels[3]))
#     # print(set(labels[0]))
#     logfile.close()
#     # print(labels[0][n_number])
#     plt.figure(figsize=(8, 8))
#     for i in range(len):
#         plt.clf()
#         # plt.scatter(data[:,0],data[:,1],marker='.',color = 'b', s = 25)
#         for j in range(1, n_number + 1):
#             x0 = data[j][0]
#             x1 = data[j][1]
#             plt.scatter(x0, x1, marker='.', color='r', s=25)
#             plt.text(x0, x1, str(j - 1), color='b', fontdict={'weight': 'bold', 'size': 8})
#             plt.plot([x0, data[int(labels[i][j - 1]) + 1][0]], [x1, data[int(labels[i][j - 1]) + 1][1]], 'r')
#         plt.title("generation={:d},FO={:.5f}".format(i, labels[i][n_number]))
#         plt.show()
#         # plt.pause(0.1)
#         # time.sleep(1.5)
#     i = len - 1
#     # print(data[50])
#     for j in range(1, n_number + 1):
#         x0 = data[j][0]
#         x1 = data[j][1]
#         # print(j,labels[i][j-1])
#         # plt.scatter(x0,x1)
#         plt.scatter(x0, x1, marker='.', color='b', s=25)
#         plt.text(x0, x1, str(j - 1), color='r', fontdict={'weight': 'bold', 'size': 8})
#         plt.title("generation={:d},FO={:.5f}".format(i, labels[i][j]))
#         plt.plot([x0, data[int(labels[i][j - 1]) + 1][0]], [x1, data[int(labels[i][j - 1]) + 1][1]])

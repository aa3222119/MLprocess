# ===========================================
# @Time    : 2018/7/11 17:47
# @Author  : antony
# @Email   : 502202879@qq.com
# @File    : main.py
# @Software: PyCharm Community Edition
# ===========================================

import os
import pandas as pd
import numpy as np
from copy import deepcopy
from random import choice, randint, random
from time import time


os.chdir(os.getcwd()+'\\alibabaqqddsfds'+'\data')

mac_keys = ['machine_id', 'cpu', 'mem', 'disk', 'P', 'M', 'PM']

data_path = os.sep.join(['..', 'data', ''])
output_path = os.sep.join(['..', 'submit', ''])
# 加载约束 interference
df_app_interference = pd.read_csv(data_path + 'scheduling_preliminary_app_interference_20180606.csv'
                                  , names=['app_a', 'app_b', 'k']).set_index('app_a')
# 加载app 和 instance_deploy
df_app_resources = pd.read_csv(data_path + 'scheduling_preliminary_app_resources_20180606.csv',
                               names=['app_id', 'cpu_', 'mem_', 'disk', 'P', 'M', 'PM'])
apps_cpu_mat = np.matrix(np.vstack(tuple(df_app_resources['cpu_'].map(lambda x:np.array(x.split('|'), dtype=float)))))
apps_mem_mat = np.matrix(np.vstack(tuple(df_app_resources['mem_'].map(lambda x:np.array(x.split('|'), dtype=float)))))
df_instance_deploy = pd.read_csv(data_path + 'scheduling_preliminary_instance_deploy_20180606.csv',
                                 names=['id', 'app_id', 'machine_id'])
df_instance_deploy['app_index'] = df_instance_deploy['app_id'].str.replace('app_', '').astype(int)
df_instance_join_app = df_instance_deploy.join(df_app_resources.set_index('app_id'), on='app_id'
                                               , lsuffix='', rsuffix='_r')
# 加载 machine_resources
df_machine_resources = pd.read_csv(data_path + 'scheduling_preliminary_machine_resources_20180606.csv',
                                   names=mac_keys)
df_machine_resources['machine_index'] = df_machine_resources.machine_id.str.replace('machine_', '').astype(int)
df_machine_resources = df_machine_resources.set_index('machine_index')
mac_num = len(df_machine_resources)


class Machine:

    def __init__(self, machine_id, cpu, mem, disk, P, M, PM, **kargs):
        self.machine_id = machine_id
        self.cpu = cpu
        self.mem = mem
        self.disk = disk
        self.P = P
        self.M = M
        self.PM = PM
        self.instances_list = []  # 实例列表
        # self.app_set = set()  # app的集合
        self.app_list = []
        self.app_index_1_list = []   # app_index -1 的集合
        self.app_interference = {}  # {app_id: 还剩余能被添加的次数} 这台机器的实时interference约束
        # if all([x in kargs for x in mac_keys]):
        #     self.restrict_di = kargs
        #     self.instances_list = []
        # else:
        #     print('机器限制初始化有误'
        self.disk_taken = 0  # disk占用
        self.P_taken = 0
        self.M_taken = 0
        self.PM_taken = 0
        self.static_score = 0
        self.score_increase = 0   # 每次add之后变高的score
        self.potential = 2 * cpu + 2 * mem + disk + P + PM + M
        self.resource_high_rate = 0  # 资源占用率 以最严重的为主
        self.resource_high_rate = 0  # 资源平均占用评价

    @property
    def instances_num(self):
        return len(self.instances_list)

    # @property
    # def cpu_instances_arr(self):
    #     if self.instances_num:
    #         return np.vstack((x.cpu_time_taken for x in self.instances_list))
    #     else:
    #         return 0

    @property
    def cpu_instances_arr(self):
            return apps_cpu_mat[self.app_index_1_list, :]


    # @property
    # def mem_instances_arr(self):
    #     if self.instances_num:
    #         return np.vstack((x.mem_time_taken for x in self.instances_list))
    #     else:
    #         return 0

    @property
    def mem_instances_arr(self):
            return apps_mem_mat[self.app_index_1_list, :]

    # @property
    # def cpu_time_taken(self) -> np.array:
    #     if self.instances_num:
    #         return self.cpu_instances_arr.sum(0)/self.cpu
    #     else:
    #         return 0

    @property
    def cpu_time_taken(self):
        return self.cpu_instances_arr.sum(0)/self.cpu

    # @property
    # def mem_time_taken(self) -> np.array:
    #     if self.instances_num:
    #         return self.mem_instances_arr.sum(0)/self.mem
    #     else:
    #         return 0

    @property
    def mem_time_taken(self):
        return self.mem_instances_arr.sum(0)/self.mem

    @property
    def mac_status(self):
        if self.disk_taken > self.disk:
            return 1  # 不满足 disk
        if self.P_taken > self.P:
            return 2  # 不满足 P
        if self.M_taken > self.M:
            return 3  # 不满足 M
        if self.PM_taken > self.PM:
            return 4  # 不满足 PM
        return 0

    @property
    def score(self):
        if self.instances_num:
            if self.mac_status > 0 or (self.cpu_time_taken > 1).any() or (self.mem_time_taken > 1).any():
                return 10**9
            else:
                # return 1 + 10 * (np.e ** (self.cpu_time_taken - 0.5).clip(0, ) - 1).mean()
                return 1 + 10 * (np.exp((self.cpu_time_taken - 0.5).clip(0, )) - 1).mean()
        else:
            return 0

    def update_interference(self, row):  # row为add_instances所带来的新interference
        if row['app_b'] in self.app_interference and row['k'] > self.app_interference[row['app_b']]:
            pass
            # print('do nothing')
        else:
            self.app_interference.update({row['app_b']: row['k']})

    def add_instances(self, instance):
        if instance.id not in self.instances_list:
            if instance.app_id in self.app_interference:
                if self.app_interference[instance.app_id] < 1:
                    return 5  # 不满足 app_interference
                else:
                    self.app_interference[instance.app_id] -= 1

            if instance.app_id not in self.app_list:
                # 更新app_interference
                # self.app_set |= {instance.app_id}
                if instance.app_id in df_app_interference.index:
                    df_interference_tmp = df_app_interference.loc[instance.app_id, :]
                    if type(df_interference_tmp) is pd.Series:
                        self.update_interference(df_interference_tmp)
                    else:
                        for i in range(len(df_interference_tmp)):
                            self.update_interference(df_interference_tmp.iloc[i, :])
            self.app_list.append(instance.app_id)
            self.app_index_1_list.append(instance.app_index - 1)

            self.instances_list.append(instance.id)
            self.disk_taken += instance.disk   #
            self.P_taken += instance.P
            self.M_taken += instance.M
            self.PM_taken += instance.PM

            score_tmp = self.score
            self.score_increase = score_tmp - self.static_score
            self.static_score = score_tmp

            self.resource_high_rate = max(
                self.mem_time_taken.mean(), self.disk_taken/self.disk,
                self.P_taken / self.P,
                self.M_taken / self.M,
                self.PM_taken / self.PM,)

        else:
            return 6

    @property
    def status(self):
        return ('id:%s | 实例数量：%s | score：%s | score_increase：%s' %
                (self.machine_id, self.instances_num, self.static_score, self.score_increase))


# class Instance:
#
#     def __init__(self, id, app_id, cpu_, mem_, disk, P, M, PM, **kargs):
#         self.id = id
#         self.app_id = app_id
#         self.app_index = int(app_id.replace('app_', ''))
#         # self.cpu_time_taken = np.array(cpu_.split('|'), dtype=float)
#         # self.mem_time_taken = np.array(mem_.split('|'), dtype=float)
#         self.cpu_time_taken = apps_cpu_mat[self.app_index - 1, :]
#         self.mem_time_taken = apps_mem_mat[self.app_index - 1, :]
#         self.disk = disk
#         self.P = P
#         self.M = M
#         self.PM = PM
#         self.hard_degree = self.cpu_time_taken.mean() + self.mem_time_taken.mean() + self.disk/2


def choice_one_machine(ins, ranges=range(1, mac_num+1), times=7):
    print(ins.id, ins.app_id, ins.hard_degree,  end=':: ')
    for i in range(times):
        # rd_mac_index = randint(1, mac_num)  # 全平等随机取
        rd_mac_index = choice(ranges)
        mac_tmp = deepcopy(all_machine_resources[rd_mac_index])
        res = mac_tmp.add_instances(ins)
        if type(res) is int:
            print(res, end='|>')
            del mac_tmp
            continue
        if mac_tmp.mac_status > 0:
            print(mac_tmp.mac_status, end='|>')
            del mac_tmp
            continue
        p = random()
        if mac_tmp.score_increase > 1:
            del mac_tmp
            continue
        sc = 0.6 * mac_tmp.score_increase + 0.8 * mac_tmp.static_score
        threshold = .4 * sc + 0.15
        print('p:%.3f score+:%.3f th:%.3f'% (p, mac_tmp.score_increase, threshold), end='=>')
        if p > threshold:
            all_machine_resources[rd_mac_index] = mac_tmp
            #
            df_machine_resources.loc[rd_mac_index, 'score'] = all_machine_resources[rd_mac_index].static_score
            df_machine_resources.loc[rd_mac_index, 'instances_num'] = all_machine_resources[rd_mac_index].instances_num
            df_machine_resources.loc[rd_mac_index, 'cpu_avg'] = all_machine_resources[rd_mac_index].cpu_time_taken.mean()
            df_machine_resources.loc[rd_mac_index, 'resource_rate'] = mac_tmp.resource_high_rate
            print(i, '实例成功部署于%s, 直接作用于all_machine_resources' % rd_mac_index)
            return rd_mac_index
        else:
            print('继续寻找', end='||>')
            del mac_tmp
    print('||')


def output_csv():
    import datetime
    print(df_machine_resources.score.sum())
    name = 'submit_%s.csv' % datetime.datetime.now().strftime('%y%m%d_%H%M%S')
    df_instance_join_app.loc[:, ['id', 'machine_id']].to_csv(output_path + name, index=False, header=False)


df_machine_resources['instances_num'] = 0
df_machine_resources['score'] = 0
df_machine_resources['cpu_avg'] = 0
df_machine_resources['resource_rate'] = 0  # 资源占用的最高值


t1 = time()
print('加载all_machine_resources....', end='')
all_machine_resources = [Machine('空machine，只为对应index', 0, 0, 0, 0, 0, 0)]
for _, row in df_machine_resources.iterrows():
    all_machine_resources.append(Machine(**row.to_dict()))
df_machine_resources['potential'] = [mac.potential for mac in all_machine_resources[1:]]
potential_avg = df_machine_resources['potential'].mean()
potential_min = df_machine_resources['potential'].min()
t2 = time()
print('   time taken :%s' % (t2-t1))

print('加载all_instances....', end='')
all_instances = [None] * len(df_instance_join_app)
df_instance_join_app['hard_degree'] = 0

# 初始化所有，忽略已经部署的
df_instance_join_app['machine_id'] = 0
# df_instance_join_app['machine_id'] = df_instance_join_app['machine_id'].fillna(0)
df_instance_join_app['hard_degree'] = [row['disk']/2 + apps_cpu_mat[row['app_index'] - 1, :].mean()
                                       + apps_mem_mat[row['app_index'] - 1, :].mean()
                                       for i, row in df_instance_join_app.iterrows()]
# for i, row in df_instance_join_app.iterrows():
#     row_di = row.to_dict()
#     ins_tmp = Instance(**row_di)
#     df_instance_join_app.loc[i, 'hard_degree'] = ins_tmp.hard_degree
#     all_instances[i] = ins_tmp
#     # if type(row_di['machine_id']) is str:
#     #     machine_index = int(row_di['machine_id'][8:])
#     #     all_machine_resources[machine_index].add_instances(ins_tmp)
#     #     #
#     #     df_machine_resources.loc[machine_index, 'score'] = all_machine_resources[machine_index].static_score
#     #     df_machine_resources.loc[machine_index, 'instances_num'] = all_machine_resources[machine_index].instances_num
#     #     df_machine_resources.loc[machine_index, 'cpu_avg'] = all_machine_resources[machine_index].cpu_time_taken.mean()
#     #     df_machine_resources.loc[machine_index, 'resource_rate'] = all_machine_resources[machine_index].resource_high_rate
#     #     # print(i, '初始条件已部署', df_instance_join_app.loc[i, 'machine_id'], all_machine_resources[machine_index].status)
t3 = time()
print('   time taken :%s' % (t3-t2))


# 结果依据表 df_instance_join_app - 贪心
def greedy(handel_set, greedy_type, handel_batch):
    if greedy_type == 1:
        machines = df_machine_resources.query('score<=1&potential>=%s' % potential_avg).index
    elif greedy_type==2:
        machines = df_machine_resources.query('score==1').index
    elif greedy_type == 3:
        machines = df_machine_resources.query('score==1&cpu_avg<0.4').index
    elif greedy_type == 4:
        machines = df_machine_resources.query('score==1&resource_rate<0.9').index
    elif greedy_type==0:
        machines = df_machine_resources.query('score==0&potential>=%s' % potential_min).index
    elif type(greedy_type) is str:
        machines = df_machine_resources.query(greedy_type).index
    else:
        machines = range(1, mac_num+1)
    print('**'*34+'handel_set:', len(handel_set), ' 候选机器数量:', len(machines), ' handel_num:', handel_batch, '**'*34)
    success_handel_num = 0
    for i in handel_set[:handel_batch]:
        # row = df_instance_join_app.loc[i, :]
        # row_di = row.to_dict()
        # ins_tmp = all_instances[i]
        ins_tmp = df_instance_join_app.loc[i,:]
        machine_index = choice_one_machine(ins_tmp, machines)
        if machine_index:
            #
            df_instance_join_app.loc[i, 'machine_id'] = 'machine_' + str(machine_index)
            print('greedy_type(%s)添加了：' % greedy_type, i, df_instance_join_app.loc[i, 'machine_id'], all_machine_resources[machine_index].status)
            success_handel_num += 1
    return success_handel_num


def step_batch_greedy(greedy_type, times=500,  handel_num=100, out_rate=0.2):
    for i in range(times):
        handel_set = df_instance_join_app[df_instance_join_app['machine_id'] == 0].sort_values('hard_degree',ascending=False).index
        if greedy(handel_set, greedy_type, handel_num) / handel_num < out_rate:
            break
    return i


# 为了避免前面的被漏分 采用小碎步模式

step_batch_greedy(1)

step_batch_greedy(0, times=5)

step_batch_greedy('score==0', times=5)

step_batch_greedy(2)

step_batch_greedy(4)

step_batch_greedy(0, times=10)

step_batch_greedy(2, out_rate=0.1)

step_batch_greedy(3, out_rate=0.1)

step_batch_greedy(0, times=6)

step_batch_greedy('score==1&instances_num<11', out_rate=0.1)

step_batch_greedy('score>=1&score<1.1', out_rate=0.1)   # 为什么这一步花的时间很长



# df_machine_resources[df_machine_resources.score == df_machine_resources.score.max()]
# all_machine_resources[2304].instances_list[-1].disk   ## inst_43689




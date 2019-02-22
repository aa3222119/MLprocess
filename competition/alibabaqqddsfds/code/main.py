# ===========================================
# @Time    : 2018/7/11 17:47
# @Author  : antony
# @Email   : 502202879@qq.com
# @File    : main.py
# @Software: PyCharm Community Edition
# ===========================================


from copy import deepcopy
from random import choice, randint, random
from time import time, sleep
from component import *
import datetime

solution_step = []  # 解决方案操作步骤 由[ins_id, machine_id]构成的列表


def df_machine_resources_update(mac_index):
    #
    df_machine_resources.loc[mac_index, 'score'] = all_machine_resources[mac_index].static_score
    df_machine_resources.loc[mac_index, 'instances_num'] = len(all_machine_resources[mac_index])
    df_machine_resources.loc[mac_index, 'disk_rate'] = all_machine_resources[mac_index].disk_rate
    # df_machine_resources.loc[mac_index, 'mem_avg'] = all_machine_resources[mac_index].mem_time_taken.mean()
    df_machine_resources.loc[mac_index, 'full_loaded_score'] = all_machine_resources[mac_index].full_loaded_score
    all_machine_resources[mac_index].update_loaded_status()
    df_machine_resources.loc[mac_index, 'full_loaded_status'] = all_machine_resources[mac_index].full_loaded_status
    df_machine_resources.loc[mac_index, 'loaded_nice_score'] = all_machine_resources[mac_index].loaded_nice_score


def df_machine_resources_updates(mac_index_s=None):
    if mac_index_s is None:
        mac_index_s = range(1, mac_num+1)
    print(' df_machine_resources_updates||| ', len(mac_index_s))
    for mac_index in mac_index_s:
        df_machine_resources_update(mac_index)


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

print('初始化已经部署的instances....', end='')
# 初始化已经部署的instances....
for ind in df_instance_join_app_idx[~(df_instance_join_app_idx['machine_id'].isna())].index:
    ins_tmp = df_instance_join_app_idx.loc[ind, :]
    mac_index = ins_tmp['deployed_mac_index']
    res = all_machine_resources[mac_index].add_instances(ind)
    # df_machine_resources_update(mac_index)
df_machine_resources_updates()
t3 = time()
print('   time taken :%s' % (t3-t2))


# 更改解的步骤solution_step和df_instance_join_app
def update_deploy(ins_id, machine_id):
    df_instance_join_app_idx.loc[ins_id, 'machine_id'] = machine_id
    solution_step.append([ins_id, machine_id])


def choice_one_machine(ins_id, mac_ranges=range(1, mac_num+1), times=6):
    for i in range(times):
        # rd_mac_index = randint(1, mac_num)  # 全平等随机取
        rd_mac_index = choice(mac_ranges)
        mac_tmp = deepcopy(all_machine_resources[rd_mac_index])
        res = mac_tmp.add_instances_with_check(ins_id)
        if res > 0:
            print('束(%s)' % res, end='||> ')
            continue
        # if mac_tmp.score_increase > 1:
        #     continue
        # buff = mac_tmp.re_job_score()
        not_add_buff = mac_tmp.cpu_score_increase + mac_tmp.mem_score_increase
        p = random() - not_add_buff
        sc = 0.5 * mac_tmp.score_increase + 0.6 * mac_tmp.static_score
        threshold = .4 * sc + 0.1
        print('not_add_buff:\033%.3f\033 p:%.3f add_score:%.3f th:%.3f' % (not_add_buff, p, mac_tmp.score_increase, threshold), end='>')
        if p > threshold:
            all_machine_resources[rd_mac_index] = mac_tmp
            df_machine_resources_update(rd_mac_index)
            print('   %s==' % i, '%s成功部署于%s, 直接作用 ' % (ins_id, rd_mac_index))
            return rd_mac_index
        else:
            print('>>', end='>')
    print('||')
    return -1


def release_reload(rd_release_mac_index, mac_ranges, remove_num=1, times=6):
    df_machine_upd_set = set()
    for i in range(times):
        # rd_release_mac_index = choice(release_mac_ranges)
        continue_flag = False
        release_mac_tmp = deepcopy(all_machine_resources[rd_release_mac_index])
        release_app_index_li, rd_ins_id_li = [], []
        for num in range(remove_num):
            if len(release_mac_tmp) == 0:
                break
            rd_ = randint(0, len(release_mac_tmp) - 1)
            rd_ins_id_li.append(release_mac_tmp.instance_id_list[rd_])
            release_app_index_li.append(release_mac_tmp.remove_instance(rd_ins_id_li[-1], rd_))
        if len(rd_ins_id_li) < 1:
            # print('可移除实例为0', end='||> ')
            continue

        mac_tmp_li, rd_mac_index_li = [], []
        score_increase, buff = release_mac_tmp.score_increase, 0
        # not_release_buff = release_mac_tmp.app_job_score(release_app_index - 1)
        not_release_buff = release_mac_tmp.cpu_score_increase + release_mac_tmp.mem_score_increase
        buff -= not_release_buff
        print('not_release_buff:%.3f' % not_release_buff, end=' ')
        for release_app_index, rd_ins_id in zip(release_app_index_li, rd_ins_id_li):
            rd_mac_index = choice(mac_ranges)  # 挑选reload的主机
            mac_tmp = deepcopy(all_machine_resources[rd_mac_index])
            res = mac_tmp.add_instances_with_check(rd_ins_id)
            if res == 0:
                score_increase += mac_tmp.score_increase

                if score_increase < 2:

                    # add_buff = mac_tmp.re_job_score()
                    not_add_buff = mac_tmp.cpu_score_increase + mac_tmp.mem_score_increase
                    buff -= not_add_buff
                mac_tmp_li.append(mac_tmp)
                rd_mac_index_li.append(rd_mac_index)
                # print('buff:%.3f' % buff, end='> ')
            else:
                continue_flag = True
                # print('束(%s)' % res, end='||> ')
                break
        if continue_flag:
            continue

        threshold = 0.2 - score_increase + buff
        p = random()
        print('buff:\033%.3f\033 p:%.3f add_score:%.3f th:%.3f' % (buff, p, score_increase, threshold), end=' ')
        if p < threshold:
            all_machine_resources[rd_release_mac_index] = release_mac_tmp
            df_machine_upd_set.add(rd_release_mac_index)
            # df_machine_resources_update(rd_release_mac_index)
            # print('成功完成切换, 直接作用\n', all_machine_resources[rd_release_mac_index].status_print, end='::')
            for rd_ins_id, mac_tmp, rd_mac_index in zip(rd_ins_id_li, mac_tmp_li, rd_mac_index_li):
                all_machine_resources[rd_mac_index] = mac_tmp
                df_machine_upd_set.add(rd_mac_index)
                # df_machine_resources_update(rd_mac_index)
                print('   %s(%s)==>%s' % (rd_release_mac_index, rd_ins_id, rd_mac_index),
                      all_machine_resources[rd_mac_index].status_print)
            df_machine_resources_updates(df_machine_upd_set)
            return rd_ins_id_li, rd_mac_index_li
        else:
             print(i, end='>> ')
    print(' ||| ')
    return [], []


# 结果依据表 df_instance_join_app - 贪心
def greedy(handel_set, greedy_type, handel_batch):
    if greedy_type == 1:
        machines = df_machine_resources.query('score<=1&potential>=%s' % (0.9*potential_avg)).index
    elif greedy_type==2:
        machines = df_machine_resources.query('score==1').index
    elif greedy_type==0:
        machines = df_machine_resources.query('score==0').index
    elif type(greedy_type) is str:
        machines = df_machine_resources.query(greedy_type).index
    else:
        machines = range(1, mac_num+1)
    print('**'*34+'handel_set:', len(handel_set), ' 候选机器数量:', len(machines), ' handel_num:', handel_batch, '**'*66)
    success_handel_num = 0
    for ix in handel_set[:handel_batch]:
        # row = df_instance_join_app.loc[i, :]
        # row_di = row.to_dict()
        # ins_tmp = all_instances[i]
        ins_tmp = df_instance_join_app_idx.loc[ix, :]
        print(ix, ins_tmp.app_id, ins_tmp.hard_degree, end=':: ')
        machine_index = choice_one_machine(ix, machines)
        if machine_index > 0:
            #
            update_deploy(ix, 'machine_' + str(machine_index))
            print('greedy_type(%s)添加了：' % greedy_type, ix, df_instance_join_app_idx.loc[ix, 'machine_id'], all_machine_resources[machine_index].status_print)
            success_handel_num += 1
    return success_handel_num


def step_batch_greedy(greedy_type, times=500,  handel_num=100, out_rate=0.3):
    for i in range(times):
        handel_set = df_instance_join_app_idx[df_instance_join_app_idx['machine_id'] == 0].sort_values('hard_degree', ascending=False).index
        if greedy(handel_set, greedy_type, handel_num) / handel_num < out_rate:
            break


#  实例移除方法  , 初衷是置换分数太高的主机
def step_fix_(release_type='score > 1.1', greedy_type='score<=1', handel_num=200, out_rate=0.2, remove_num=1):
    handel_rate = 1.0
    while handel_rate > out_rate:
        release_mac_ranges = df_machine_resources.query(release_type).index
        if len(release_mac_ranges) == 0:
            break
        # release_mac_ranges = [1820]
        machines = df_machine_resources.query(greedy_type).index
        real_handel_num = 0
        print('**'*34, len(release_mac_ranges), len(machines), '**'*66)
        for ix in release_mac_ranges[:handel_num]:
            ins_id_li, machine_index_li = release_reload(ix, machines, remove_num=remove_num)
            for ins_id, machine_index in zip(ins_id_li, machine_index_li):
                update_deploy(ins_id, 'machine_' + str(machine_index))
                real_handel_num += 1
        handel_rate = real_handel_num/handel_num
        out_rate += 0.02
    # all_sc, max_sc = df_machine_resources.score.sum(), df_machine_resources.score.max()
    # print(all_sc, max_sc)
    return df_machine_resources.score.sum(), df_machine_resources.score.max()

df_instance_join_app_idx['machine_id'].fillna(0, inplace=True)
# 为了避免前面的被漏分 采用小碎步模式

step_batch_greedy(1, times=10)


step_batch_greedy(1)
step_fix_(release_type='score > 2', greedy_type='score==1', out_rate=0.4)
step_fix_(release_type='score > 2', greedy_type='score<2&full_loaded_status==0')
step_fix_(release_type='score > 1.5', greedy_type='score<1.5', remove_num=1)
step_fix_(release_type='score>=1&full_loaded_score<0.9', greedy_type='score<2',out_rate=0.4)

for i in range(99):
    step_fix_(release_type='score > 1.5', greedy_type='score<1.5&full_loaded_status==0')
    step_fix_(release_type='score > 1.4', greedy_type='score<1.3&full_loaded_status==0')
    step_fix_(release_type='score > 1.3', greedy_type='score<1.4&full_loaded_status==0')
    step_fix_(release_type='score > 1.2', greedy_type='score<1.3&full_loaded_status==0')
    step_fix_(release_type='score > 1.0', greedy_type='score<1.1&full_loaded_status==0')
    step_fix_(release_type='score > 1.2', greedy_type='score<1.9&full_loaded_status==0')
    step_fix_(release_type='full_loaded_score<0.85&full_loaded_status>0', greedy_type='score<2&full_loaded_status==0')
    step_fix_(release_type='full_loaded_score<0.8&full_loaded_status>0', greedy_type='score<2&full_loaded_status==0')
    step_fix_(release_type='loaded_nice_score>0.7&full_loaded_status>0', greedy_type='score<2&full_loaded_status==0')
    step_fix_(release_type='score > 1.0', greedy_type='score<1.1&full_loaded_status==0')
    step_fix_(release_type='score > 1.2', greedy_type='score<1.9&full_loaded_status==0')
    step_fix_(release_type='score > 1.5', greedy_type='score<1.5&full_loaded_status==0')
    step_fix_(release_type='score > 1.4', greedy_type='score<1.4&full_loaded_status==0')
    step_fix_(release_type='score > 1.3', greedy_type='score<1.4&full_loaded_status==0')
    step_fix_(release_type='score > 1.2', greedy_type='score<1.3&full_loaded_status==0')
    step_fix_(release_type='score > 1.1', greedy_type='score<1.1&full_loaded_status==0')
    step_fix_(release_type='instances_num>=6', greedy_type='score>=1&score<2&full_loaded_status==0', remove_num=2)
    step_fix_(release_type='instances_num==6', greedy_type='score>=1&score<2&full_loaded_status==0', remove_num=2)
    step_fix_(release_type='instances_num==5', greedy_type='score>=1&score<2&full_loaded_status==0', remove_num=2)
    step_fix_(release_type='instances_num==4', greedy_type='score>=1&score<2&full_loaded_status==0', remove_num=2)
    step_fix_(release_type='instances_num==3', greedy_type='score>=1&score<2&full_loaded_status==0')
    step_fix_(release_type='instances_num==3', greedy_type='score>=1&score<2&full_loaded_status==0', remove_num=2)
    step_fix_(release_type='instances_num==2', greedy_type='score>=1&score<2&full_loaded_status==0')
    step_fix_(release_type='instances_num==2', greedy_type='score>=1&score<2&full_loaded_status==0', remove_num=2)
    step_fix_(release_type='instances_num==1', greedy_type='score>=1&score<2&full_loaded_status==0')





step_batch_greedy(0, times=4)
step_batch_greedy('score==1', out_rate=0.2)

step_batch_greedy('score==0', times=4)
step_batch_greedy('score==1&disk_rate<0.92', out_rate=0.1)
step_batch_greedy('score==1&instances_num<11', out_rate=0.1)
step_batch_greedy('score>=1&score<1.2', out_rate=0.05)
step_fix_(release_type='score > 1.2', out_rate=0.2)

step_batch_greedy('score>=1&score<1.7&disk_rate<0.8', out_rate=0.05)
step_fix_(release_type='score > 1.4', greedy_type='score<1.4', out_rate=0.05)

step_batch_greedy(0, times=1, handel_num=50)

step_fix_(release_type='instances_num==1', greedy_type='score==1')
step_fix_(release_type='score > 1.5', greedy_type='score<1.4&potential>=%s' % (0.9*potential_avg), out_rate=0.1)
step_fix_(release_type='instances_num==2', greedy_type='score>=1', remove_num=2)


t = 0
sc_, ma_ = step_fix_(release_type='score > 1', greedy_type='score<1.4', out_rate=0.5)
while t<4:
    sc, ma = step_fix_(release_type='score > 1', greedy_type='score<1.4', out_rate=0.5)
    print(sc, ma)
    if sc == sc_:
        t += 1
    else:
        sc = sc_
        t = 0


def output_csv():
    print(df_machine_resources.score.sum())
    name = 'submit_%s.csv' % datetime.datetime.now().strftime('%y%m%d_%H%M%S')
    # df_instance_join_app_idx.sort_values('deployed_mac_index', ascending=False).loc[:, ['id', 'machine_id']].to_csv(output_path + name, index=False, header=False)
    pd.DataFrame(solution_step).to_csv(output_path + name, index=False, header=False)
    return output_path + name


def add_submit(path_name_a):
    path_name_b = output_csv()
    os.chdir('..\submit\\')
    name = 'submit_%s.csv' % datetime.datetime.now().strftime('%y%m%d_%H%M%S')
    os.popen('type %s >> %s' % (path_name_a, name))
    sleep(0.5)
    os.popen('(echo #) >> %s' % name)
    sleep(0.5)
    os.popen('type %s >> %s' % (path_name_b, name))



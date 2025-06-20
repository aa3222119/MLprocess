import pandas as pd


class FloydEMT:
    def __init__(self, city_graph):
        self.city_graph = city_graph
        # 提取所有节点并创建索引映射
        self.nodes = list(city_graph.keys())
        n = len(self.nodes)  # 节点总数
        self.n = n
        self.node_index = {node: idx for idx, node in enumerate(self.nodes)}  # 节点到索引的映射

        # 步骤：初始化邻接矩阵（n x n）
        min_dist = [[float('inf')] * self.n for _ in range(n)]
        for i in range(self.n):
            min_dist[i][i] = 0  # 自身到自身的距离为0
        
        next_node = [[None] * n for _ in range(n)]  # 记录i到j的直接后继节点
        # 填充直接连接的边（无向图，双向设置）
        for u in city_graph:
            u_idx = self.node_index[u]
            for v, w in city_graph[u].items():
                v_idx = self.node_index[v]
                if min_dist[u_idx][v_idx] > w:  # 避免重复边覆盖更短的（本题无此情况，但通用逻辑保留）
                    min_dist[u_idx][v_idx] = w
                    min_dist[v_idx][u_idx] = w
                    next_node[u_idx][v_idx] = v  # u→v的直接后继是v
                    next_node[v_idx][u_idx] = u  # v→u的直接后继是u
        self.next_node = next_node
        self.min_dist = min_dist
    
    def cul_dist(self):
        # 填充直接连接的边（无向图，双向设置）
        for u in self.city_graph:
            u_idx = self.node_index[u]
            for v, w in self.city_graph[u].items():
                v_idx = self.node_index[v]
                self.min_dist[u_idx][v_idx] = w  # 直接连接的距离
                self.min_dist[v_idx][u_idx] = w  # 无向图，反向距离相同

        # Floyd算法核心（三层循环更新最短路径
        n = self.n
        for k in range(n):  # 中间节点k
            for i in range(n):  # 起点i
                for j in range(n):  # 终点j
                    if self.min_dist[i][k] + self.min_dist[k][j] < self.min_dist[i][j]:
                        self.min_dist[i][j] = self.min_dist[i][k] + self.min_dist[k][j]
                        # 更新路径：i→k→j，因此i的直接后继是k（原i→j的后继被替换为i→k的后继）
                        self.next_node[i][j] = self.next_node[i][k]
        return self

    # 根据next_node生成i到j的具体路径
    def get_path(self, i, j):
        if self.next_node[i][j] is None:
            return []  # 不可达
        path = [self.nodes[i]]
        current = i
        while current != j:
            current = self.node_index[self.next_node[current][j]]  # 移动到下一个节点
            path.append(self.nodes[current])
        return path
    
    def get_df_res(self):
        return pd.DataFrame(self.min_dist, columns=self.nodes, index=self.nodes)

    def show_min_dis_and_path(self, i, j):
        print(f" {self.nodes[i]} => {self.nodes[j]}: 距离为 {self.min_dist[i][j]}, 路径为 {self.get_path(i, j)}")


# 输入的城市距离字典
city_graph = {
    '深圳': {'广州': 1.5, '东莞': 1.0},
    '广州': {'深圳': 1.5, '韶关': 2.5, '长沙': 5.5},
    '东莞': {'深圳': 1.0, '惠州': 1.2},
    '惠州': {'东莞': 1.2, '武汉': 8.0},
    '韶关': {'广州': 2.5, '长沙': 4.0},
    '长沙': {'韶关': 4.0, '武汉': 3.0, '郑州': 8.0},
    '武汉': {'惠州': 8.0, '长沙': 3.0, '郑州': 4.5, '西安': 10.0},
    '郑州': {'长沙': 8.0, '武汉': 4.5, '洛阳': 2.0},
    '洛阳': {'郑州': 2.0, '西安': 5.0},
    '西安': {'武汉': 10.0, '洛阳': 5.0}
}
# 计算所有点对的最短路径
fly_e = FloydEMT(city_graph)
df_min_dis = fly_e.cul_dist().get_df_res()
# 1. 深圳到西安的距离和路径为：
fly_e.show_min_dis_and_path(0, 9)
# >> 1.  深圳 => 西安: 距离为 20.0, 路径为 ['深圳', '广州', '长沙', '武汉', '西安']

# 2.  假定刚走到第二站广州时， 广州到长沙路断了需要修复， 即令 city_graph['广州']['长沙'] = 999  # 也不是修不好，需要花费很大才能通过的意思
city_graph['广州']['长沙'] = 999
fly_e2 = FloydEMT(city_graph).cul_dist()
print('深圳 => 广州 1.5,', end='再加上现在要从广州开始到西安： ')
fly_e2.show_min_dis_and_path(1, 9)
# >> 2. 深圳 => 广州 1.5,再加上现在要从广州开始到西安：  广州 => 西安: 距离为 19.5, 路径为 ['广州', '韶关', '长沙', '武汉', '西安']
# 结论：完成成就条条大路通西安。绕道韶关 总路程 多走了1

# 3.

# # 打印结果（格式化输出）
# for row in shortest_paths:
#     # 对齐显示，宽度设为8（可根据需求调整）
#     print(" | ".join(f"{item:^8}" for item in row))

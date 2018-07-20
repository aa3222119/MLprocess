#include <iostream>
using namespace std;
#define MaxVertexNum 10
#define INF 9999
int edges[MaxVertexNum][MaxVertexNum] = {{ 0, INF, 32, INF, INF, 5, INF, INF, INF, INF },
{ INF, 0, INF, INF, 13, INF, INF, INF, INF, INF },
{ 32, INF, 0, INF, 20, INF, INF, INF, INF, INF },
{ INF, INF, INF, 0, INF, INF, INF, 8, 7, INF },
{ INF, 13, 20, INF, 0, INF, INF, INF, INF, INF },
{ 5, INF, INF, INF, INF, 0, INF, INF, INF, INF },
{ INF, INF, INF, INF, INF, INF, 0, INF, INF, 3 },
{ INF, INF, INF, 8, INF, INF, INF, 0, INF, INF },
{ INF, INF, INF, 7, INF, INF, INF, INF, 0, INF },
{ INF, INF, INF, INF, INF, INF, 3, INF, INF, 0 } };
int Interchan[MaxVertexNum][MaxVertexNum] = {{ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
	{ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
	{ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
	{ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
	{ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
	{ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
	{ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
	{ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
	{ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
	{ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 } };
int Pa[MaxVertexNum] =  { -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 } ;
int flag = 0;

void Ipath(int i, int j)
{
	int k,jj;
	k=Interchan[Pa[i]][Pa[j]];
	if (k != -1)
	{
		for (jj = MaxVertexNum; jj > j; jj--)
		{
			Pa[jj] = Pa[jj - 1];
		}
		Pa[j] = k;
		Ipath(j, j+1);
		Ipath(i, j);
	}
}
void Epath(int Vi, int Vj)
{
	int k,tem;
	for (k = 0; k < MaxVertexNum; k++)
	{
		tem = edges[Vi][k] + edges[k][Vj];
		if (tem < edges[Vi][Vj])
		{
			edges[Vi][Vj] = tem;
			Interchan[Vi][Vj] = k;
			flag = 1;
		}
	}
	//return flag;
}

void Sprint(int m, int n, int SS[][MaxVertexNum])
{
	int i, j;
	for (i = 0; i < m; i++)
	{
		for (j = 0; j < n; j++)
		{
			printf("%-6d", SS[i][j]);
		}
		printf("\n");
	}
	printf("\n");
}

void main()
{
	
	printf("，，，#￥%……环仔一切因你而始￥%……&，，，\n原始权值图：\n");
	Sprint(MaxVertexNum, MaxVertexNum, edges);
	int i, j;
	flag = 1;
	while (flag==1)
	{
		flag = 0;
		for (i = 0; i < MaxVertexNum; i++)
		{
			for (j = 0; j < MaxVertexNum; j++)
			{
				Epath(i, j);
			}
		}	
	}
	printf("用floyd寻求最优路径和后权值图：\n");
	Sprint(MaxVertexNum, MaxVertexNum, edges);
	printf("中转节点序号（-1表示不需要中转）：\n");
	Sprint(MaxVertexNum, MaxVertexNum, Interchan);
	cin >> Pa[0] >> Pa[1];
	//I = 1; J = 2;//选择起点和终点
	//Pa[0] = 3; Pa[1] = 4;
	printf("%d点到%d点的距离是%d,路径是：", Pa[0], Pa[1], edges[Pa[0]][Pa[1]]);
	Ipath(0, 1);
	for (i = 0; Pa[i] != -1; i++)
	{
		printf("%2d", Pa[i]);
	}
	printf("\n", Pa[i]);


	/*for (i = 0; i < MaxVertexNum; i++)
	{
		for (j = 0; j < MaxVertexNum; j++)
		{
			Epath(i, j);
		}
	}
	printf("用floyd寻求最优路径和后权值图：\n");
	Sprint(MaxVertexNum, MaxVertexNum, edges);
	printf("中转节点序号（-1表示不需要中转）：\n");
	Sprint(MaxVertexNum, MaxVertexNum, Interchan);*/ //要判断结束啊

	
}
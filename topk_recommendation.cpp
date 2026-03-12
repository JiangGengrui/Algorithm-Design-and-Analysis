#include <iostream>      // 输入输出库
#include <vector>        // 向量容器
#include <cmath>         // 数学函数，例如 sqrt()
#include <algorithm>     // 排序函数 sort()
#include <queue>         // 优先队列（堆）
#include <cstdlib>       // rand() 随机数
#include <ctime>         // time() 随机种子

using namespace std;

// 向量维度（实验要求为50维）
const int DIM = 50;

/*
    函数：cosineSimilarity
    功能：计算两个用户兴趣向量之间的余弦相似度
    参数：
        a - 用户A的兴趣向量
        b - 用户B的兴趣向量
    返回：
        两个向量之间的余弦相似度
*/
double cosineSimilarity(const vector<double>& a, const vector<double>& b) {

    double dot = 0;      // 向量点积
    double normA = 0;    // 向量A的模长平方
    double normB = 0;    // 向量B的模长平方

    // 遍历50维向量
    for(int i = 0; i < DIM; i++) {

        // 点积计算
        dot += a[i] * b[i];

        // 计算向量A的模
        normA += a[i] * a[i];

        // 计算向量B的模
        normB += b[i] * b[i];
    }

    // 返回余弦相似度公式
    return dot / (sqrt(normA) * sqrt(normB));
}


/*
    函数：generateUsers
    功能：生成n个用户的兴趣向量
    参数：
        n - 用户数量
    返回：
        用户兴趣向量集合
*/
vector<vector<double>> generateUsers(int n){

    // 创建n个用户，每个用户50维
    vector<vector<double>> users(n, vector<double>(DIM));

    // 随机生成用户兴趣数据
    for(int i = 0; i < n; i++){
        for(int j = 0; j < DIM; j++){

            // 生成0-1之间随机数
            users[i][j] = (double)rand() / RAND_MAX;
        }
    }

    return users;
}


/*
    方法一：基准算法（排序实现Top-K）
    思路：
        1. 计算所有用户与目标用户的相似度
        2. 将相似度排序
        3. 取前k个
*/
vector<int> topK_sort(vector<vector<double>>& users, vector<double>& target, int k){

    // 存储（相似度，用户编号）
    vector<pair<double,int>> sim;

    // 遍历所有用户
    for(int i = 0; i < users.size(); i++){

        // 计算相似度
        double s = cosineSimilarity(users[i], target);

        // 保存结果
        sim.push_back({s, i});
    }

    // 按相似度从大到小排序
    sort(sim.begin(), sim.end(), greater<pair<double,int>>());

    // 取前k个用户
    vector<int> result;

    for(int i = 0; i < k; i++){
        result.push_back(sim[i].second);
    }

    return result;
}


/*
    方法二：优化算法（最小堆实现Top-K）

    思路：
        维护一个大小为k的最小堆

        如果堆未满：
            直接插入

        如果堆已满：
            若当前相似度 > 堆顶
                删除堆顶
                插入新元素

    时间复杂度：
        O(n log k)
*/
vector<int> topK_heap(vector<vector<double>>& users, vector<double>& target, int k){

    // 定义最小堆
    priority_queue<
        pair<double,int>,
        vector<pair<double,int>>,
        greater<pair<double,int>>
    > pq;

    // 遍历所有用户
    for(int i = 0; i < users.size(); i++){

        // 计算相似度
        double s = cosineSimilarity(users[i], target);

        // 如果堆还没满
        if(pq.size() < k){

            pq.push({s, i});
        }

        // 如果堆满并且当前相似度更大
        else if(s > pq.top().first){

            // 删除最小元素
            pq.pop();

            // 插入新元素
            pq.push({s, i});
        }
    }

    // 提取结果
    vector<int> result;

    while(!pq.empty()){

        result.push_back(pq.top().second);
        pq.pop();
    }

    return result;
}


/*
    主函数
*/
int main(){

    // 设置随机种子
    srand(time(0));

    // 用户数量
    int n = 10000;

    // Top-K参数
    int k = 5;

    // 生成用户数据
    vector<vector<double>> users = generateUsers(n);

    // 生成目标用户兴趣向量
    vector<double> target(DIM);

    for(int i = 0; i < DIM; i++){
        target[i] = (double)rand() / RAND_MAX;
    }

    // 使用堆算法寻找Top-K用户
    vector<int> result = topK_heap(users, target, k);

    // 输出结果
    cout << "Top " << k << " similar users:" << endl;

    for(int id : result){
        cout << id << " ";
    }

    cout << endl;

    return 0;
}
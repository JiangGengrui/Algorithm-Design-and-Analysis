#include <iostream>
#include <vector>
#include <cmath>
#include <algorithm>
#include <queue>
#include <cstdlib>
#include <ctime>
#include <chrono>   // 用于计算程序运行时间

using namespace std;

const int DIM = 50;   // 向量维度

/*
    计算余弦相似度
*/
double cosineSimilarity(const vector<double>& a, const vector<double>& b){

    double dot = 0;
    double normA = 0;
    double normB = 0;

    for(int i = 0; i < DIM; i++){
        dot += a[i] * b[i];
        normA += a[i] * a[i];
        normB += b[i] * b[i];
    }

    return dot / (sqrt(normA) * sqrt(normB));
}

/*
    生成用户兴趣向量
*/
vector<vector<double>> generateUsers(int n){

    vector<vector<double>> users(n, vector<double>(DIM));

    for(int i = 0; i < n; i++){
        for(int j = 0; j < DIM; j++){
            users[i][j] = (double)rand() / RAND_MAX;
        }
    }

    return users;
}

/*
    方法1：排序寻找Top-K
*/
vector<int> topK_sort(vector<vector<double>>& users, vector<double>& target, int k){

    vector<pair<double,int>> sim;

    for(int i = 0; i < users.size(); i++){

        double s = cosineSimilarity(users[i], target);

        sim.push_back({s, i});
    }

    sort(sim.begin(), sim.end(), greater<pair<double,int>>());

    vector<int> result;

    for(int i = 0; i < k; i++){
        result.push_back(sim[i].second);
    }

    return result;
}

/*
    方法2：最小堆优化Top-K
*/
vector<int> topK_heap(vector<vector<double>>& users, vector<double>& target, int k){

    priority_queue<
        pair<double,int>,
        vector<pair<double,int>>,
        greater<pair<double,int>>
    > pq;

    for(int i = 0; i < users.size(); i++){

        double s = cosineSimilarity(users[i], target);

        if(pq.size() < k)
            pq.push({s, i});

        else if(s > pq.top().first){

            pq.pop();
            pq.push({s, i});
        }
    }

    vector<int> result;

    while(!pq.empty()){
        result.push_back(pq.top().second);
        pq.pop();
    }

    return result;
}

int main(){

    srand(time(0));

    // 不同用户规模
    vector<int> testSizes = {100, 500, 1000, 5000, 10000};

    int k = 5;

    cout << "用户数量\t排序算法时间(ms)\t堆优化时间(ms)" << endl;

    for(int n : testSizes){

        double sortTime = 0;
        double heapTime = 0;

        for(int t = 0; t < 20; t++){   // 每个规模运行20次

            vector<vector<double>> users = generateUsers(n);

            vector<double> target(DIM);

            for(int i = 0; i < DIM; i++){
                target[i] = (double)rand() / RAND_MAX;
            }

            // 记录排序算法时间
            auto start1 = chrono::high_resolution_clock::now();

            topK_sort(users, target, k);

            auto end1 = chrono::high_resolution_clock::now();

            sortTime += chrono::duration<double, milli>(end1 - start1).count();

            // 记录堆算法时间
            auto start2 = chrono::high_resolution_clock::now();

            topK_heap(users, target, k);

            auto end2 = chrono::high_resolution_clock::now();

            heapTime += chrono::duration<double, milli>(end2 - start2).count();
        }

        // 计算平均时间
        sortTime /= 20;
        heapTime /= 20;

        cout << n << "\t\t"
             << sortTime << "\t\t\t"
             << heapTime << endl;
    }

    return 0;
}
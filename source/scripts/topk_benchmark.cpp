#include <iostream>
#include <vector>
#include <queue>
#include <cstdlib>
#include <ctime>
#include <algorithm>
#include <cmath>
#include <fstream>
#include <chrono>

using namespace std;
using namespace chrono;

const int DIM = 50; // 向量维度

// 随机生成n个高维向量
vector<vector<double>> generateUsers(int n) {
    vector<vector<double>> users(n, vector<double>(DIM));
    for(int i = 0; i < n; ++i)
        for(int j = 0; j < DIM; ++j)
            users[i][j] = (double)rand() / RAND_MAX;
    return users;
}

// 计算余弦相似度
double cosineSimilarity(const vector<double>& a, const vector<double>& b){
    double dot=0, normA=0, normB=0;
    for(int i=0;i<DIM;i++){
        dot += a[i]*b[i];
        normA += a[i]*a[i];
        normB += b[i]*b[i];
    }
    return dot / (sqrt(normA) * sqrt(normB));
}

// 插入排序Top-K
vector<int> topK_insert(const vector<vector<double>>& users, const vector<double>& target, int k){
    vector<pair<double,int>> topK;
    for(int i=0;i<k;i++)
        topK.push_back({cosineSimilarity(users[i], target),i});
    sort(topK.begin(), topK.end(), greater<pair<double,int>>());
    for(int i=k;i<users.size();i++){
        double sim = cosineSimilarity(users[i], target);
        if(sim <= topK.back().first) continue;
        int pos = k-1;
        while(pos>0 && topK[pos-1].first < sim){
            topK[pos] = topK[pos-1];
            pos--;
        }
        topK[pos] = {sim,i};
    }
    vector<int> res;
    for(auto &p: topK) res.push_back(p.second);
    return res;
}

// 选择排序Top-K
vector<int> topK_selection(const vector<vector<double>>& users, const vector<double>& target, int k){
    int n = users.size();
    vector<pair<double,int>> sims(n);
    for(int i=0;i<n;i++)
        sims[i] = {cosineSimilarity(users[i], target), i};
    for(int i=0;i<k;i++){
        int max_idx = i;
        for(int j=i+1;j<n;j++)
            if(sims[j].first > sims[max_idx].first)
                max_idx = j;
        swap(sims[i], sims[max_idx]);
    }
    vector<int> res;
    for(int i=0;i<k;i++) res.push_back(sims[i].second);
    return res;
}

// 冒泡排序Top-K
vector<int> topK_bubble(const vector<vector<double>>& users, const vector<double>& target, int k){
    int n = users.size();
    vector<pair<double,int>> sims(n);
    for(int i=0;i<n;i++)
        sims[i] = {cosineSimilarity(users[i], target), i};
    for(int i=0;i<k;i++){
        for(int j=0;j<n-i-1;j++){
            if(sims[j].first < sims[j+1].first)
                swap(sims[j], sims[j+1]);
        }
    }
    vector<int> res;
    for(int i=0;i<k;i++) res.push_back(sims[i].second);
    return res;
}

// QuickSelect Top-K
int partition(vector<pair<double,int>>& arr, int left, int right){
    double pivot = arr[right].first;
    int i = left;
    for(int j=left;j<right;j++){
        if(arr[j].first >= pivot){
            swap(arr[i], arr[j]);
            i++;
        }
    }
    swap(arr[i], arr[right]);
    return i;
}
void quickSelect(vector<pair<double,int>>& arr, int left, int right, int k){
    if(left >= right) return;
    int pi = partition(arr, left, right);
    if(pi > k-1)
        quickSelect(arr, left, pi-1, k);
    else if(pi < k-1)
        quickSelect(arr, pi+1, right, k);
}
vector<int> topK_quickSelect(const vector<vector<double>>& users, const vector<double>& target, int k){
    int n = users.size();
    vector<pair<double,int>> sims(n);
    for(int i=0;i<n;i++)
        sims[i] = {cosineSimilarity(users[i], target), i};
    quickSelect(sims, 0, n-1, k);
    vector<int> res;
    for(int i=0;i<k;i++) res.push_back(sims[i].second);
    return res;
}

// 小顶堆Top-K
vector<int> topK_heap(const vector<vector<double>>& users, const vector<double>& target, int k){
    priority_queue<pair<double,int>, vector<pair<double,int>>, greater<pair<double,int>>> pq;
    for(int i=0;i<users.size();i++){
        double sim = cosineSimilarity(users[i], target);
        if(pq.size() < k) pq.push({sim,i});
        else if(sim > pq.top().first){
            pq.pop();
            pq.push({sim,i});
        }
    }
    vector<int> res;
    while(!pq.empty()){
        res.push_back(pq.top().second);
        pq.pop();
    }
    return res;
}

// 记录csv结果
void write_csv(const string& fname, const string& algoname, int n, int k, double ms) {
    ofstream fout(fname, ios::app);
    if (!fout.is_open()) {
        cerr << "Error: Cannot open file " << fname << " for writing!" << endl;
        return;
    }
    fout << algoname << "," << n << "," << k << "," << ms << "\n";
    fout.close();
}

int main(){
    srand(time(0));
    // ====== 实验参数区 ======
    vector<int> N_list = {100000, 500000, 1000000, 2000000, 3000000, 4000000, 5000000, 8000000, 10000000}; // 可增大
    int k = 10;
    string csv_file = "d:\\code\\Algorithm-Design-and-Analysis\\source\\data\\topk_benchmark.csv";

    // 删除旧文件（如果存在）并创建新文件
    remove(csv_file.c_str());
    {
        ofstream fout(csv_file);
        if (fout.is_open()) {
            fout << "algorithm,n,k,time_ms\n";
            fout.close();
        } else {
            cerr << "Error: Cannot create file " << csv_file << endl;
            cerr << "Please check if the file is open in another program." << endl;
            return 1;
        }
    }

    for (int n : N_list) {
        cout << "==== n = " << n << " ====" << endl;
        // 每个规模都新生成一次users和target，保证公平
        vector<vector<double>> users = generateUsers(n);
        vector<double> target(DIM);
        for(int i=0;i<DIM;i++)
            target[i] = (double)rand()/RAND_MAX;

        // 1. 插入排序Top-K
        auto t1 = high_resolution_clock::now();
        auto res1 = topK_insert(users, target, k);
        auto t2 = high_resolution_clock::now();
        double insert_ms = duration<double, milli>(t2-t1).count();
        cout << "InsertSort Top-K: " << insert_ms << " ms" << endl;
        write_csv(csv_file, "InsertSort_TopK", n, k, insert_ms);

        // 2. 选择排序Top-K
        t1 = high_resolution_clock::now();
        auto res2 = topK_selection(users, target, k);
        t2 = high_resolution_clock::now();
        double select_ms = duration<double, milli>(t2-t1).count();
        cout << "SelectionSort Top-K: " << select_ms << " ms" << endl;
        write_csv(csv_file, "SelectionSort_TopK", n, k, select_ms);

        // 3. 冒泡排序Top-K
        t1 = high_resolution_clock::now();
        auto res3 = topK_bubble(users, target, k);
        t2 = high_resolution_clock::now();
        double bubble_ms = duration<double, milli>(t2-t1).count();
        cout << "BubbleSort Top-K: " << bubble_ms << " ms" << endl;
        write_csv(csv_file, "BubbleSort_TopK", n, k, bubble_ms);

        // 4. QuickSelect Top-K
        t1 = high_resolution_clock::now();
        auto res4 = topK_quickSelect(users, target, k);
        t2 = high_resolution_clock::now();
        double quicksel_ms = duration<double, milli>(t2-t1).count();
        cout << "QuickSelect Top-K: " << quicksel_ms << " ms" << endl;
        write_csv(csv_file, "QuickSelect_TopK", n, k, quicksel_ms);

        // 5. 小顶堆Top-K
        t1 = high_resolution_clock::now();
        auto res5 = topK_heap(users, target, k);
        t2 = high_resolution_clock::now();
        double heap_ms = duration<double, milli>(t2-t1).count();
        cout << "MinHeap Top-K: " << heap_ms << " ms" << endl;
        write_csv(csv_file, "MinHeap_TopK", n, k, heap_ms);

        cout << "-----------" << endl;
    }

    cout << "数据已记录到 CSV 文件: " << csv_file << endl;
    return 0;
}

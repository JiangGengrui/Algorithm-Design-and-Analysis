#include <iostream>
#include <vector>
#include <utility>
#include <algorithm>
#include <cstdlib>
#include <ctime>
#include <fstream>
#include <chrono>
#include <cmath>

using namespace std;
using namespace chrono;

const int DIM = 50;       // 向量维度
const int FIXED_N = 10000;// 固定用户规模 n=10000
const int REPEAT = 20;   // 重复测试20次取平均

// ==== 随机数据生成 ====
vector<vector<double>> generateUsers(int n) {
    vector<vector<double>> users(n, vector<double>(DIM));
    for (int i = 0; i < n; ++i)
        for (int j = 0; j < DIM; ++j)
            users[i][j] = (double)rand() / RAND_MAX;
    return users;
}

// 余弦相似度计算
double cosineSimilarity(const vector<double>& a, const vector<double>& b) {
    double dot = 0, normA = 0, normB = 0;
    for (int i = 0; i < DIM; i++) {
        dot += a[i] * b[i];
        normA += a[i] * a[i];
        normB += b[i] * b[i];
    }
    return dot / (sqrt(normA) * sqrt(normB));
}

// ==== 插入排序 ====
vector<int> origin_insertsort(const vector<vector<double>>& users, const vector<double>& target, int k) {
    int n = users.size();
    vector<pair<double, int>> sims(n);
    for (int i = 0; i < n; ++i)
        sims[i] = {cosineSimilarity(users[i], target), i};
    // 插入排序（降序）
    for (int i = 1; i < n; ++i) {
        auto key = sims[i];
        int j = i - 1;
        while (j >= 0 && sims[j].first < key.first) {
            sims[j + 1] = sims[j];
            --j;
        }
        sims[j + 1] = key;
    }
    vector<int> res;
    for (int i = 0; i < k; ++i) res.push_back(sims[i].second);
    return res;
}

// ==== 冒泡排序 ====
vector<int> origin_bubblesort(const vector<vector<double>>& users, const vector<double>& target, int k) {
    int n = users.size();
    vector<pair<double, int>> sims(n);
    for (int i = 0; i < n; ++i)
        sims[i] = {cosineSimilarity(users[i], target), i};
    // 冒泡排序（降序）
    for (int i = 0; i < n - 1; ++i) {
        for (int j = 0; j < n - 1 - i; ++j) {
            if (sims[j].first < sims[j + 1].first)
                swap(sims[j], sims[j + 1]);
        }
    }
    vector<int> res;
    for (int i = 0; i < k; ++i) res.push_back(sims[i].second);
    return res;
}

// ==== 选择排序 ====
vector<int> origin_selectionsort(const vector<vector<double>>& users, const vector<double>& target, int k) {
    int n = users.size();
    vector<pair<double, int>> sims(n);
    for (int i = 0; i < n; ++i)
        sims[i] = {cosineSimilarity(users[i], target), i};
    // 选择排序（降序）
    for (int i = 0; i < n - 1; ++i) {
        int max_idx = i;
        for (int j = i + 1; j < n; ++j)
            if (sims[j].first > sims[max_idx].first)
                max_idx = j;
        swap(sims[i], sims[max_idx]);
    }
    vector<int> res;
    for (int i = 0; i < k; ++i) res.push_back(sims[i].second);
    return res;
}

// ==== 快速排序（降序） ====
int partition(vector<pair<double, int>>& arr, int left, int right) {
    double pivot = arr[left].first;
    int i = left, j = right;
    while (i < j) {
        while (i < j && arr[j].first <= pivot) j--;
        arr[i] = arr[j];
        while (i < j && arr[i].first >= pivot) i++;
        arr[j] = arr[i];
    }
    arr[i].first = pivot;
    return i;
}

void quicksort(vector<pair<double, int>>& arr, int left, int right) {
    if (left >= right) return;
    int pivot = partition(arr, left, right);
    quicksort(arr, left, pivot - 1);
    quicksort(arr, pivot + 1, right);
}

vector<int> origin_quicksort(const vector<vector<double>>& users, const vector<double>& target, int k) {
    int n = users.size();
    vector<pair<double, int>> sims(n);
    for (int i = 0; i < n; ++i)
        sims[i] = {cosineSimilarity(users[i], target), i};
    quicksort(sims, 0, n - 1);
    vector<int> res;
    for (int i = 0; i < k; ++i)
        res.push_back(sims[i].second);
    return res;
}

// ==== 写入CSV ====
void write_csv(const string& fname, const string& algoname, int n, int k, double ms) {
    ofstream fout(fname, ios::app);
    if (!fout.is_open()) {
        cerr << "文件打开失败！" << endl;
        return;
    }
    fout << algoname << "," << n << "," << k << "," << ms << "\n";
    fout.close();
}

int main() {
    srand(time(0));
    // 配置：固定n=10000，测试不同k值
    vector<int> k_list = {1,5,10,20,50,100,200,500,1000};
    // 修改为你的CSV保存路径
    string csv_file = "d:\\code\\Algorithm-Design-and-Analysis\\source\\data\\k_benchmark.csv";

    // 初始化CSV文件
    remove(csv_file.c_str());
    ofstream fout(csv_file);
    fout << "algorithm,n,k,time_ms\n";
    fout.close();

    // 固定n=10000，仅生成一次数据（提升效率）
    auto users = generateUsers(FIXED_N);
    vector<double> target(DIM);
    for (int i = 0; i < DIM; ++i)
        target[i] = (double)rand()/RAND_MAX;

    // 遍历所有k值，测试4种算法
    for (int k : k_list) {
        cout << "\n==== 测试 k = " << k << " , n = 10000 ====\n";

        // 1. 插入排序
        double ins_ms = 0;
        for(int i=0; i<REPEAT; i++){
            auto t1 = high_resolution_clock::now();
            origin_insertsort(users, target, k);
            auto t2 = high_resolution_clock::now();
            ins_ms += duration<double, milli>(t2 - t1).count();
        }
        ins_ms /= REPEAT;
        cout << "插入排序: " << ins_ms << " ms\n";
        write_csv(csv_file, "InsertSort", FIXED_N, k, ins_ms);

        // 2. 冒泡排序
        double bub_ms = 0;
        for(int i=0; i<REPEAT; i++){
            auto t1 = high_resolution_clock::now();
            origin_bubblesort(users, target, k);
            auto t2 = high_resolution_clock::now();
            bub_ms += duration<double, milli>(t2 - t1).count();
        }
        bub_ms /= REPEAT;
        cout << "冒泡排序: " << bub_ms << " ms\n";
        write_csv(csv_file, "BubbleSort", FIXED_N, k, bub_ms);

        // 3. 选择排序
        double sel_ms = 0;
        for(int i=0; i<REPEAT; i++){
            auto t1 = high_resolution_clock::now();
            origin_selectionsort(users, target, k);
            auto t2 = high_resolution_clock::now();
            sel_ms += duration<double, milli>(t2 - t1).count();
        }
        sel_ms /= REPEAT;
        cout << "选择排序: " << sel_ms << " ms\n";
        write_csv(csv_file, "SelectionSort", FIXED_N, k, sel_ms);

        // 4. 快速排序
        double qk_ms = 0;
        for(int i=0; i<REPEAT; i++){
            auto t1 = high_resolution_clock::now();
            origin_quicksort(users, target, k);
            auto t2 = high_resolution_clock::now();
            qk_ms += duration<double, milli>(t2 - t1).count();
        }
        qk_ms /= REPEAT;
        cout << "快速排序: " << qk_ms << " ms\n";
        write_csv(csv_file, "QuickSort", FIXED_N, k, qk_ms);
    }

    cout << "\n实验完成！数据已保存至: " << csv_file << endl;
    return 0;
}
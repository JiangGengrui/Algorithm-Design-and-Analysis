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

const int DIM = 50; // 向量维度

// ==== 随机数据生成 ====
vector<vector<double>> generateUsers(int n) {
    vector<vector<double>> users(n, vector<double>(DIM));
    for (int i = 0; i < n; ++i)
        for (int j = 0; j < DIM; ++j)
            users[i][j] = (double)rand() / RAND_MAX;
    return users;
}

double cosineSimilarity(const vector<double>& a, const vector<double>& b) {
    double dot = 0, normA = 0, normB = 0;
    for (int i = 0; i < DIM; i++) {
        dot += a[i] * b[i];
        normA += a[i] * a[i];
        normB += b[i] * b[i];
    }
    return dot / (sqrt(normA) * sqrt(normB));
}

// ==== 原始插入排序 ====
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

// ==== 原始冒泡排序 ====
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

// ==== 原始选择排序 ====
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

// ==== 原始快排（标准sort） ====
vector<int> origin_quicksort(const vector<vector<double>>& users, const vector<double>& target, int k) {
    int n = users.size();
    vector<pair<double, int>> sims(n);
    for (int i = 0; i < n; ++i)
        sims[i] = {cosineSimilarity(users[i], target), i};
    sort(sims.begin(), sims.end(), std::greater<pair<double, int>>());
    vector<int> res;
    for (int i = 0; i < k; ++i) res.push_back(sims[i].second);
    return res;
}

// ==== CSV写入 ====
void write_csv(const string& fname, const string& algoname, int n, int k, double ms) {
    ofstream fout(fname, ios::app);
    if (fout.tellp() == 0)
        fout << "algorithm,n,k,time_ms\n";
    fout << algoname << "," << n << "," << k << "," << ms << "\n";
    fout.close();
}

int main() {
    srand(time(0));
    // ====== 实验参数区 =====
    vector<int> N_list = {10000, 20000, 50000, 100000}; // 可改更大
    int k = 10;
    string csv_file = "original_fullsort_benchmark.csv";
    ofstream fout(csv_file, ios::trunc); fout.close(); // 清空csv

    for (int n : N_list) {
        cout << "\n==== n = " << n << " ====\n";
        auto users = generateUsers(n);
        vector<double> target(DIM);
        for (int i = 0; i < DIM; ++i)
            target[i] = (double)rand()/RAND_MAX;

        // 插入排序
        auto t1 = high_resolution_clock::now();
        auto res1 = origin_insertsort(users, target, k);
        auto t2 = high_resolution_clock::now();
        double ins_ms = duration<double, milli>(t2-t1).count();
        cout << "Origin_InsertSort_Full: " << ins_ms << " ms" << endl;
        write_csv(csv_file, "Origin_InsertSort_Full", n, k, ins_ms);

        // 冒泡排序
        t1 = high_resolution_clock::now();
        auto res2 = origin_bubblesort(users, target, k);
        t2 = high_resolution_clock::now();
        double bub_ms = duration<double, milli>(t2-t1).count();
        cout << "Origin_BubbleSort_Full: " << bub_ms << " ms" << endl;
        write_csv(csv_file, "Origin_BubbleSort_Full", n, k, bub_ms);

        // 选择排序
        t1 = high_resolution_clock::now();
        auto res3 = origin_selectionsort(users, target, k);
        t2 = high_resolution_clock::now();
        double sel_ms = duration<double, milli>(t2-t1).count();
        cout << "Origin_SelectionSort_Full: " << sel_ms << " ms" << endl;
        write_csv(csv_file, "Origin_SelectionSort_Full", n, k, sel_ms);

        // 快排（STL sort）
        t1 = high_resolution_clock::now();
        auto res4 = origin_quicksort(users, target, k);
        t2 = high_resolution_clock::now();
        double qk_ms = duration<double, milli>(t2-t1).count();
        cout << "Origin_QuickSort_Full: " << qk_ms << " ms" << endl;
        write_csv(csv_file, "Origin_QuickSort_Full", n, k, qk_ms);
    }
    cout << "\n原始全排序实验已完成,数据写入: " << csv_file << endl;
    return 0;
}
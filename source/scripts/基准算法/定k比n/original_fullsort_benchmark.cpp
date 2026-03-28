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

// ==== 手写快速排序（降序） ====
int partition(vector<pair<double, int>>& arr, int left, int right) {
    double pivot = arr[left].first;  // 选第一个为基准
    int i = left, j = right;

    while (i < j) {
        // 从右往左找比pivot大的
        while (i < j && arr[j].first <= pivot) j--;
        arr[i] = arr[j];

        // 从左往右找比pivot小的
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

// ==== 原始快排 ====
vector<int> origin_quicksort(const vector<vector<double>>& users, const vector<double>& target, int k) {
    int n = users.size();
    vector<pair<double, int>> sims(n);

    for (int i = 0; i < n; ++i)
        sims[i] = {cosineSimilarity(users[i], target), i};

    // 手写快排（降序）
    quicksort(sims, 0, n - 1);

    vector<int> res;
    for (int i = 0; i < k; ++i)
        res.push_back(sims[i].second);

    return res;
}

// ==== CSV写入 ====
void write_csv(const string& fname, const string& algoname, int n, int k, double ms) {
    ofstream fout(fname, ios::app);
    if (!fout.is_open()) {
        cerr << "Error: Cannot open file " << fname << " for writing!" << endl;
        return;
    }
    fout << algoname << "," << n << "," << k << "," << ms << "\n";
    fout.close();
}

int main() {
    srand(time(0));

    vector<int> N_list = {10000, 50000, 100000, 500000, 1000000, 5000000, 10000000};
    int k = 10;
    string csv_file = "d:\\code\\Algorithm-Design-and-Analysis\\source\\data\\original_Quicksort_benchmark.csv";

    remove(csv_file.c_str());
    {
        ofstream fout(csv_file);
        if (fout.is_open()) {
            fout << "algorithm,n,k,time_ms\n";
            fout.close();
        } else {
            cerr << "Error: Cannot create file " << csv_file << endl;
            return 1;
        }
    }

    const int REPEAT = 20; // 每个算法重复20次

    for (int n : N_list) {
        cout << "\n==== n = " << n << " ====\n";

        // 只生成一次数据
        auto users = generateUsers(n);

        vector<double> target(DIM);
        for (int i = 0; i < DIM; ++i)
            target[i] = (double)rand()/RAND_MAX;

        // ==== 插入排序 ====
        double ins_ms = 0;
        for (int i = 0; i < REPEAT; ++i) {
            auto t1 = high_resolution_clock::now();
            origin_insertsort(users, target, k);
            auto t2 = high_resolution_clock::now();
            ins_ms += duration<double, milli>(t2 - t1).count();
        }
        ins_ms /= REPEAT;
        cout << "Origin_InsertSort_Full: " << ins_ms << " ms\n";
        write_csv(csv_file, "Origin_InsertSort_Full", n, k, ins_ms);

        // ==== 冒泡排序 ====
        double bub_ms = 0;
        for (int i = 0; i < REPEAT; ++i) {
            auto t1 = high_resolution_clock::now();
            origin_bubblesort(users, target, k);
            auto t2 = high_resolution_clock::now();
            bub_ms += duration<double, milli>(t2 - t1).count();
        }
        bub_ms /= REPEAT;
        cout << "Origin_BubbleSort_Full: " << bub_ms << " ms\n";
        write_csv(csv_file, "Origin_BubbleSort_Full", n, k, bub_ms);

        // ==== 选择排序 ====
        double sel_ms = 0;
        for (int i = 0; i < REPEAT; ++i) {
            auto t1 = high_resolution_clock::now();
            origin_selectionsort(users, target, k);
            auto t2 = high_resolution_clock::now();
            sel_ms += duration<double, milli>(t2 - t1).count();
        }
        sel_ms /= REPEAT;
        cout << "Origin_SelectionSort_Full: " << sel_ms << " ms\n";
        write_csv(csv_file, "Origin_SelectionSort_Full", n, k, sel_ms);

        // ==== 快速排序 ====
        double qk_ms = 0;
        for (int i = 0; i < REPEAT; ++i) {
            auto t1 = high_resolution_clock::now();
            origin_quicksort(users, target, k);
            auto t2 = high_resolution_clock::now();
            qk_ms += duration<double, milli>(t2 - t1).count();
        }
        qk_ms /= REPEAT;
        cout << "Origin_QuickSort_Full: " << qk_ms << " ms\n";
        write_csv(csv_file, "Origin_QuickSort_Full", n, k, qk_ms);
    }

    cout << "\n实验完成，数据写入: " << csv_file << endl;
    return 0;
}
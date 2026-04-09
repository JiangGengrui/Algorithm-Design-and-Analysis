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

const int DIM = 50;
const int FIXED_N = 10000;  // 固定用户数 n=10000
const int REPEAT = 20;      // 重复测试20次取平均

// 内联优化：余弦相似度
inline double cosineSimilarity(const vector<double>& a, const vector<double>& b) {
    double dot = 0.0, normA = 0.0, normB = 0.0;
    for (int i = 0; i < DIM; ++i) {
        dot += a[i] * b[i];
        normA += a[i] * a[i];
        normB += b[i] * b[i];
    }
    return dot / sqrt(normA * normB);
}

// 随机向量生成
vector<vector<double>> generateUsers(int n) {
    vector<vector<double>> users(n, vector<double>(DIM));
    for (int i = 0; i < n; ++i)
        for (int j = 0; j < DIM; ++j)
            users[i][j] = (double)rand() / RAND_MAX;
    return users;
}

// 1. 插入排序 Top-K
vector<int> topK_insert(const vector<vector<double>>& users, const vector<double>& target, int k) {
    vector<pair<double, int>> topK;
    topK.reserve(k);

    for (int i = 0; i < k; ++i)
        topK.emplace_back(cosineSimilarity(users[i], target), i);

    sort(topK.begin(), topK.end(), greater<pair<double, int>>());

    for (int i = k; i < users.size(); ++i) {
        double sim = cosineSimilarity(users[i], target);
        if (sim <= topK.back().first) continue;

        int pos = k - 1;
        while (pos > 0 && topK[pos - 1].first < sim) {
            topK[pos] = topK[pos - 1];
            --pos;
        }
        topK[pos] = {sim, i};
    }

    vector<int> res;
    res.reserve(k);
    for (auto& p : topK) res.push_back(p.second);
    return res;
}

// 2. 选择排序 Top-K
vector<int> topK_selection(const vector<vector<double>>& users, const vector<double>& target, int k) {
    int n = users.size();
    vector<pair<double, int>> sims(n);

    for (int i = 0; i < n; ++i)
        sims[i] = {cosineSimilarity(users[i], target), i};

    for (int i = 0; i < k; ++i) {
        int max_idx = i;
        for (int j = i + 1; j < n; ++j)
            if (sims[j].first > sims[max_idx].first)
                max_idx = j;
        swap(sims[i], sims[max_idx]);
    }

    vector<int> res;
    res.reserve(k);
    for (int i = 0; i < k; ++i)
        res.push_back(sims[i].second);
    return res;
}

// 3. 冒泡排序 Top-K
vector<int> topK_bubble(const vector<vector<double>>& users, const vector<double>& target, int k) {
    int n = users.size();
    vector<pair<double, int>> sims(n);

    for (int i = 0; i < n; ++i)
        sims[i] = {cosineSimilarity(users[i], target), i};

    for (int i = 0; i < k; ++i)
        for (int j = 0; j < n - i - 1; ++j)
            if (sims[j].first < sims[j + 1].first)
                swap(sims[j], sims[j + 1]);

    vector<int> res;
    res.reserve(k);
    for (int i = 0; i < k; ++i)
        res.push_back(sims[i].second);
    return res;
}

// 4. QuickSelect Top-K
int partition(vector<pair<double, int>>& arr, int left, int right) {
    double pivot = arr[right].first;
    int i = left;
    for (int j = left; j < right; ++j) {
        if (arr[j].first >= pivot) {
            swap(arr[i], arr[j]);
            ++i;
        }
    }
    swap(arr[i], arr[right]);
    return i;
}

void quickSelect(vector<pair<double, int>>& arr, int left, int right, int k) {
    if (left >= right) return;
    int pi = partition(arr, left, right);
    if (pi > k - 1)
        quickSelect(arr, left, pi - 1, k);
    else if (pi < k - 1)
        quickSelect(arr, pi + 1, right, k);
}

vector<int> topK_quickSelect(const vector<vector<double>>& users, const vector<double>& target, int k) {
    int n = users.size();
    vector<pair<double, int>> sims(n);

    for (int i = 0; i < n; ++i)
        sims[i] = {cosineSimilarity(users[i], target), i};

    quickSelect(sims, 0, n - 1, k);

    vector<int> res;
    res.reserve(k);
    for (int i = 0; i < k; ++i)
        res.push_back(sims[i].second);
    return res;
}

// 5. 小顶堆 Top-K
vector<int> topK_heap(const vector<vector<double>>& users, const vector<double>& target, int k) {
    priority_queue<pair<double, int>, vector<pair<double, int>>, greater<pair<double, int>>> pq;

    for (int i = 0; i < users.size(); ++i) {
        double sim = cosineSimilarity(users[i], target);
        if (pq.size() < k)
            pq.emplace(sim, i);
        else if (sim > pq.top().first) {
            pq.pop();
            pq.emplace(sim, i);
        }
    }

    vector<int> res;
    res.reserve(k);
    while (!pq.empty()) {
        res.push_back(pq.top().second);
        pq.pop();
    }
    return res;
}

// 写入CSV
void write_csv(const string& fname, const string& algoname, int n, int k, double ms) {
    ofstream fout(fname, ios::app);
    fout << algoname << "," << n << "," << k << "," << ms << "\n";
}

// ==================== 主函数（固定n=10000，测试多组k）====================
int main() {
    srand(time(0));

    // 测试的k值列表
    vector<int> k_list = {1,5,10,20,50,100,200,500,1000};
    string csv_file = "d:\\code\\Algorithm-Design-and-Analysis\\source\\data\\k_topk.csv";  // CSV保存路径

    // 初始化CSV
    remove(csv_file.c_str());
    {
        ofstream fout(csv_file);
        fout << "algorithm,n,k,time_ms\n";
    }

    // 固定n=10000，仅生成一次数据（提升效率）
    cout << "正在生成 " << FIXED_N << " 个用户向量..." << endl;
    auto users = generateUsers(FIXED_N);
    vector<double> target(DIM);
    for (int i = 0; i < DIM; ++i)
        target[i] = (double)rand() / RAND_MAX;
    cout << "数据生成完成，开始测试多组k值..." << endl << endl;

    // 遍历所有k值
    for (int k : k_list) {
        cout << "==== 测试 n=" << FIXED_N << ", k=" << k << " ====" << endl;

        // 1. 插入排序 Top-K
        double t_insert = 0;
        for (int i = 0; i < REPEAT; ++i) {
            auto start = high_resolution_clock::now();
            topK_insert(users, target, k);
            auto end = high_resolution_clock::now();
            t_insert += duration<double, milli>(end - start).count();
        }
        t_insert /= REPEAT;
        cout << "InsertSort_TopK:   " << t_insert << " ms" << endl;
        write_csv(csv_file, "InsertSort_TopK", FIXED_N, k, t_insert);

        // 2. 选择排序 Top-K
        double t_selection = 0;
        for (int i = 0; i < REPEAT; ++i) {
            auto start = high_resolution_clock::now();
            topK_selection(users, target, k);
            auto end = high_resolution_clock::now();
            t_selection += duration<double, milli>(end - start).count();
        }
        t_selection /= REPEAT;
        cout << "SelectionSort_TopK:" << t_selection << " ms" << endl;
        write_csv(csv_file, "SelectionSort_TopK", FIXED_N, k, t_selection);

        // 3. 冒泡排序 Top-K
        double t_bubble = 0;
        for (int i = 0; i < REPEAT; ++i) {
            auto start = high_resolution_clock::now();
            topK_bubble(users, target, k);
            auto end = high_resolution_clock::now();
            t_bubble += duration<double, milli>(end - start).count();
        }
        t_bubble /= REPEAT;
        cout << "BubbleSort_TopK:   " << t_bubble << " ms" << endl;
        write_csv(csv_file, "BubbleSort_TopK", FIXED_N, k, t_bubble);

        // 4. QuickSelect Top-K
        double t_quick = 0;
        for (int i = 0; i < REPEAT; ++i) {
            auto start = high_resolution_clock::now();
            topK_quickSelect(users, target, k);
            auto end = high_resolution_clock::now();
            t_quick += duration<double, milli>(end - start).count();
        }
        t_quick /= REPEAT;
        cout << "QuickSelect_TopK:  " << t_quick << " ms" << endl;
        write_csv(csv_file, "QuickSelect_TopK", FIXED_N, k, t_quick);

        // 5. 小顶堆 Top-K
        double t_heap = 0;
        for (int i = 0; i < REPEAT; ++i) {
            auto start = high_resolution_clock::now();
            topK_heap(users, target, k);
            auto end = high_resolution_clock::now();
            t_heap += duration<double, milli>(end - start).count();
        }
        t_heap /= REPEAT;
        cout << "MinHeap_TopK:      " << t_heap << " ms" << endl;
        write_csv(csv_file, "MinHeap_TopK", FIXED_N, k, t_heap);

        cout << "-----------------------------------------" << endl;
    }

    cout << "\n✅ 全部实验完成！数据已保存到: " << csv_file << endl;
    return 0;
}
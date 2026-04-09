#include <chrono>
#include <iostream>
#include <vector>
#include <cstdlib>
#include <fstream>
#include "divideConquer.cpp"
#include "bruteForce.cpp"

using namespace std;
using namespace std::chrono;

// 写入csv文件
void writeCSV(const string& filename, const string& algo, int n, double time_ms)
{
    ofstream fout(filename, ios::app);
    fout << algo << "," << n << "," << time_ms << "\n";
    fout.close();
}

int main()
{
    srand(time(0));
    vector<int> N_list = {100000, 200000, 300000, 400000, 500000};
    const int REPEAT = 5;
    const int DATA_REPEAT = 3;

    string csvFile = "closest_pair.csv";

    // 清空文件写表头
    remove(csvFile.c_str());
    ofstream fout(csvFile);
    fout << "algorithm,n,time_ms\n";
    fout.close();

    for (int N : N_list)
    {
        cout << "\n====== N = " << N << " ======\n";

        double brute_total = 0;
        double divide_total = 0;

        // ===== 多组数据 =====
        for (int d = 0; d < DATA_REPEAT; ++d) {

            vector<pair<int, int>> points(N);
            for (int i = 0; i < N; ++i)
                points[i] = {rand() % 100000, rand() % 100000};

            double brute_time = 0;
            double divide_time = 0;

            // ===== 多次重复 =====
            for (int t = 0; t < REPEAT; ++t) {

                // 蛮力法
                auto t1 = chrono::high_resolution_clock::now();
                bruteForce(points);
                auto t2 = chrono::high_resolution_clock::now();
                brute_time += chrono::duration<double, milli>(t2 - t1).count();

                // 分治法
                t1 = chrono::high_resolution_clock::now();
                ClosestPair(points);
                t2 = chrono::high_resolution_clock::now();
                divide_time += chrono::duration<double, milli>(t2 - t1).count();
            }

            brute_total += brute_time / REPEAT;
            divide_total += divide_time / REPEAT;
        }

        // ===== 最终平均 =====
        double brute_avg = brute_total / DATA_REPEAT;
        double divide_avg = divide_total / DATA_REPEAT;

        cout << "BruteForce: " << brute_avg << " ms\n";
        cout << "DivideConquer: " << divide_avg << " ms\n";

        writeCSV(csvFile, "BruteForce", N, brute_avg);
        writeCSV(csvFile, "DivideConquer", N, divide_avg);
    }

    cout << "\n数据已写入 closest_pair.csv\n";
    return 0;
}

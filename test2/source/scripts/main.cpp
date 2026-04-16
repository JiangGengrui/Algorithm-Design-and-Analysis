#include <chrono>
#include <iostream>
#include <vector>
#include <cstdlib>
#include <fstream>
#include <ctime>   // 加了这个

using namespace std;
using namespace std::chrono;

// 声明外部函数（分文件编译不需要互相 include）
double bruteForce(const vector<pair<int, int>>& points);
double closestPair(vector<pair<int, int>> points);

void writeCSV(const string& filename, const string& algo, int n, double time_ms)
{
    ofstream fout(filename, ios::app);
    fout << algo << "," << n << "," << time_ms << "\n";
    fout.close();
}

int main()
{
    srand(time(0));

    vector<int> N_list = {1000, 5000, 10000, 20000, 50000, 100000};
    const int REPEAT = 5;
    const int DATA_REPEAT = 3;

    string csvFile = "closest_pair.csv";
    remove(csvFile.c_str());

    ofstream fout(csvFile);
    fout << "algorithm,n,time_ms\n";
    fout.close();

    for (int N : N_list)
    {
        cout << "\n====== N = " << N << " ======\n";

        double brute_total = 0;
        double divide_total = 0;

        for (int d = 0; d < DATA_REPEAT; ++d)
        {
            vector<pair<int, int>> points(N);
            for (int i = 0; i < N; ++i)
                points[i] = {rand() % 100000, rand() % 100000};

            double brute_time = 0;
            double divide_time = 0;

            for (int t = 0; t < REPEAT; ++t)
            {
                auto t1 = high_resolution_clock::now();
                bruteForce(points);
                auto t2 = high_resolution_clock::now();
                brute_time += duration<double, milli>(t2 - t1).count();

                t1 = high_resolution_clock::now();
                closestPair(points);
                t2 = high_resolution_clock::now();
                divide_time += duration<double, milli>(t2 - t1).count();
            }

            brute_total += brute_time / REPEAT;
            divide_total += divide_time / REPEAT;
        }

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
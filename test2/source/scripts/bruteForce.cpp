#include <iostream>
#include <vector>
#include <cmath>
#include <limits>

using namespace std;

// 计算两点之间的距离
double distance(const pair<int, int>& p1, const pair<int, int>& p2)
{
    return sqrt(pow(p2.first - p1.first, 2) + pow(p2.second - p1.second, 2));
}

// 蛮力法计算最近点对距离
double bruteForce(const vector<pair<int, int>>& points)
{
    double minDist = numeric_limits<double>::max();
    int n = points.size();
    for (int i = 0; i < n; i++)
    {
        for (int j = i + 1; j < n; j++)
        {
            double dist = distance(points[i], points[j]);
            minDist = min(minDist, dist);
        }
    }
    return minDist;
}
#include <iostream>
#include <vector>
#include <cmath>
#include <algorithm>
#include <limits>
#include "bruteForce.cpp"

using namespace std;

double distance(const pair<int, int>& p1, const pair<int, int>& p2)
{
    return sqrt(pow(p2.first - p1.first, 2) + pow(p2.second - p1.second, 2));
}

// 递归计算最近点对
double closestPair(vector<pair<int, int>>& pointsX, vector<pair<int, int>>& pointsY)
{
    int n = pointsX.size();
    if (n <= 3)
    {
        return bruteForce(pointsX);
    }

    int mid = n / 2;
    vector<pair<int, int>> leftX(mid), rightX(n - mid);
    vector<pair<int, int>> leftY, rightY;

    // 分割点集
    for (int i = 0; i < mid; i++) leftX[i] = pointsX[i];
    for (int i = mid; i < n; i++) rightX[i - mid] = pointsX[i];

    // 将Y排序，按y坐标排序
    for (const auto& point : pointsY)
    {
        if (point.first <= pointsX[mid].first) leftY.push_back(point);
        else rightY.push_back(point);
    }

    double leftDist = closestPair(leftX, leftY);
    double rightDist = closestPair(rightX, rightY);
    double minDist = min(leftDist, rightDist);

    // 合并步骤检查边界的点对
    vector<pair<int, int>> strip;
    for (const auto& point : pointsY)
    {
        if (abs(point.first - pointsX[mid].first) < minDist)
        {
            strip.push_back(point);
        }
    }

    for (int i = 0; i < strip.size(); i++)
    {
        for (int j = i + 1; j < strip.size() && (strip[j].second - strip[i].second) < minDist; j++)
        {
            double dist = distance(strip[i], strip[j]);
            minDist = min(minDist, dist);
        }
    }
    return minDist;
}

//主函数调用
double ClosestPair(vector<pair<int, int>>& points)
{
    vector<pair<int, int>> pointsX = points;
    vector<pair<int, int>> pointsY = points;

    // 按x坐标和y坐标分别排序
    sort(pointsX.begin(), pointsX.end(), [](const pair<int, int>& a, const pair<int, int>& b) {
        return a.first < b.first;
    });

    sort(pointsY.begin(), pointsY.end(), [](const pair<int, int>& a, const pair<int, int>& b) {
        return a.second < b.second;
    });

    return closestPair(pointsX, pointsY);
}
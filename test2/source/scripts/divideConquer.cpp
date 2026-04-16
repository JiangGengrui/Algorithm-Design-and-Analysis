#include <iostream>
#include <vector>
#include <cmath>
#include <algorithm>
#include <limits>

using namespace std;

// 声明外部函数，不再 #include 任何 cpp
double bruteForce(const vector<pair<int, int>>& points);

double distance(const pair<int, int>& p1, const pair<int, int>& p2)
{
    int dx = p2.first - p1.first;
    int dy = p2.second - p1.second;
    return sqrt(dx*dx + dy*dy);
}

double closestPairRecursive(vector<pair<int, int>>& pointsX, vector<pair<int, int>>& pointsY)
{
    int n = pointsX.size();
    if (n <= 3)
        return bruteForce(pointsX);

    int mid = n / 2;
    int midX = pointsX[mid].first; // 提前保存，避免错误

    vector<pair<int, int>> leftX(pointsX.begin(), pointsX.begin() + mid);
    vector<pair<int, int>> rightX(pointsX.begin() + mid, pointsX.end());

    vector<pair<int, int>> leftY, rightY;
    for (const auto& point : pointsY)
    {
        if (point.first <= midX)
            leftY.push_back(point);
        else
            rightY.push_back(point);
    }

    double dLeft = closestPairRecursive(leftX, leftY);
    double dRight = closestPairRecursive(rightX, rightY);
    double minDist = min(dLeft, dRight);

    vector<pair<int, int>> strip;
    for (const auto& point : pointsY)
    {
        if (abs(point.first - midX) < minDist)
            strip.push_back(point);
    }

    for (int i = 0; i < strip.size(); i++)
    {
        for (int j = i + 1; j < strip.size(); j++)
        {
            if (strip[j].second - strip[i].second >= minDist)
                break;

            double dist = distance(strip[i], strip[j]);
            if (dist < minDist)
                minDist = dist;
        }
    }
    return minDist;
}

// 统一入口
double closestPair(vector<pair<int, int>> points)
{
    vector<pair<int, int>> pointsX = points;
    vector<pair<int, int>> pointsY = points;

    sort(pointsX.begin(), pointsX.end(), [](const pair<int, int>& a, const pair<int, int>& b) {
        return a.first < b.first;
    });

    sort(pointsY.begin(), pointsY.end(), [](const pair<int, int>& a, const pair<int, int>& b) {
        return a.second < b.second;
    });

    return closestPairRecursive(pointsX, pointsY);
}
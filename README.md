# 算法设计与分析 - Top-K 优化算法实验

本项目包含两部分实验：原始全排序算法基准测试和 Top-K 优化算法基准测试。

## 项目结构

```
Algorithm-Design-and-Analysis/
├── source/
│   ├── scripts/           # 源代码
│   │   ├── original_fullsort_benchmark.cpp      # 原始全排序算法基准测试
│   │   ├── topk_benchmark.cpp                    # Top-K算法基准测试
│   │   ├── plot_original_fullsort.py            # 原始全排序数据可视化
│   │   └── plot_topk_benchmark.py               # Top-K数据可视化
│   ├── data/              # 实验数据
│   │   ├── original_fullsort_benchmark.csv      # 原始全排序实验数据
│   │   └── topk_benchmark.csv                   # Top-K实验数据
│   ├── origin/            # 原始全排序可视化图表
│   └── Topk/              # Top-K可视化图表
├── README.md
└── .gitignore
```

## 实验内容

### 1. 原始全排序算法
- 插入排序 (InsertSort) - O(n²)
- 冒泡排序 (BubbleSort) - O(n²)
- 选择排序 (SelectionSort) - O(n²)
- 快速排序 (QuickSort) - O(n log n)

### 2. Top-K 优化算法
- 插入排序 Top-K - O(nk)
- 选择排序 Top-K - O(nk)
- 冒泡排序 Top-K - O(nk)
- QuickSelect - O(n)
- 小顶堆 - O(n log k)

## 使用方法

### 编译并运行实验程序

```bash
# 编译原始全排序基准测试
g++ source/scripts/original_fullsort_benchmark.cpp -o origin_benchmark -O2
./origin_benchmark

# 编译Top-K基准测试
g++ source/scripts/topk_benchmark.cpp -o topk_benchmark -O2
./topk_benchmark
```

### 生成可视化图表

```bash
# 生成原始全排序图表
python source/scripts/plot_original_fullsort.py

# 生成Top-K图表
python source/scripts/plot_topk_benchmark.py
```

## 实验参数

### 原始全排序
- 数据规模 n: 10,000 ~ 100,000
- Top-K 值: 10
- 向量维度: 50

### Top-K 优化
- 数据规模 n: 100,000 ~ 10,000,000
- Top-K 值: 10
- 向量维度: 50

## 实验结论

1. 原始全排序算法在小规模数据下表现尚可，但随着数据规模增长，O(n²)算法性能急剧下降
2. Top-K优化显著提升了算法性能，尤其是数据规模较大时
3. Top-K优化将复杂度从O(n²)优化到O(n log k)，性能提升明显

# 算法设计与分析 - Top-K 优化算法实验

本项目包含两部分实验：原始全排序算法基准测试和 Top-K 优化算法基准测试。通过对比不同数据规模（n）和不同 K 值下的算法性能，验证 Top-K 优化的效果。

## 项目结构

```
Algorithm-Design-and-Analysis/
├── source/
│   ├── scripts/               # 源代码
│   │   ├── origin/           # 原始全排序算法实验
│   │   │   ├── set-K-compare-n/    # 固定K值，变化n
│   │   │   │   ├── original_fullsort_benchmark.cpp
│   │   │   │   └── plot_original_fullsort.py
│   │   │   └── set-n-compare-k/    # 固定n值，变化K
│   │   │       ├── origin_for_K.cpp
│   │   │       └── origin_for_K.py
│   │   └── TopK/             # Top-K优化算法实验
│   │       ├── set-k-compare-n/    # 固定k值，变化n
│   │       │   ├── topk_benchmark.cpp
│   │       │   └── plot_topk_benchmark.py
│   │       └── set-n-compare-k/    # 固定n值，变化k
│   │           ├── topk_for_K.cpp
│   │           └── topk_for_K.py
│   ├── data/                  # 实验数据
│   │   ├── original_fullsort_benchmark.csv    # 原始全排序数据
│   │   ├── topk_benchmark.csv                 # Top-K数据（固定k）
│   │   ├── k_benchmark.csv                     # Top-K数据（固定n）
│   │   └── k_topk.csv                          # 原始全排序数据（固定n）
│   ├── origin-image/                # 原始全排序可视化图表
│   └── Topk-image/                  # Top-K可视化图表
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

### 3. 实验维度
本实验通过两个维度对比算法性能：
- **维度一**：固定 K 值，变化数据规模 n（验证算法随 n 增长的性能变化）
- **维度二**：固定数据规模 n，变化 K 值（验证算法随 K 增长的性能变化）

## 使用方法

### 实验一：固定 K 值，变化数据规模 n

#### 原始全排序算法
```bash
# 编译并运行
g++ source/scripts/origin/set-K-compare-n/original_fullsort_benchmark.cpp -o origin_benchmark -O2
./origin_benchmark

# 生成图表
python source/scripts/origin/set-K-compare-n/plot_original_fullsort.py
```

#### Top-K 优化算法
```bash
# 编译并运行
g++ source/scripts/TopK/set-k-compare-n/topk_benchmark.cpp -o topk_benchmark -O2
./topk_benchmark

# 生成图表
python source/scripts/TopK/set-k-compare-n/plot_topk_benchmark.py
```

### 实验二：固定数据规模 n，变化 K 值

#### 原始全排序算法
```bash
# 编译并运行
g++ source/scripts/origin/set-n-compare-k/origin_for_K.cpp -o origin_k_benchmark -O2
./origin_k_benchmark

# 生成图表
python source/scripts/origin/set-n-compare-k/origin_for_K.py
```

#### Top-K 优化算法
```bash
# 编译并运行
g++ source/scripts/TopK/set-n-compare-k/topk_for_K.cpp -o topk_k_benchmark -O2
./topk_k_benchmark

# 生成图表
python source/scripts/TopK/set-n-compare-k/topk_for_K.py
```

## 实验参数

### 实验一：固定 K 值，变化数据规模 n
- **原始全排序**：n = 10,000 ~ 1,000,000，K = 10
- **Top-K 优化**：n = 100,000 ~ 10,000,000，k = 10
- **向量维度**：50

### 实验二：固定数据规模 n，变化 K 值
- **原始全排序**：n = 100,000，K = 5, 10, 20, 50, 100, 200, 500
- **Top-K 优化**：n = 1,000,000，k = 5, 10, 20, 50, 100, 200, 500
- **向量维度**：50

## 实验结论

1. **数据规模影响**
   - 原始全排序算法在小规模数据下表现尚可，但随着数据规模增长，O(n²)算法性能急剧下降
   - QuickSort（O(n log n)）在大规模数据下表现最优

2. **Top-K 优化效果**
   - Top-K优化显著提升了算法性能，尤其是数据规模较大时
   - 小顶堆和QuickSelect在Top-K问题中表现最优
   - 对于小K值，插入排序Top-K也有不错的性能

3. **K 值影响**
   - 当K值较小时（K < 100），Top-K优化优势明显
   - 当K值接近n时，Top-K算法退化为全排序，性能优势消失
   - 小顶堆和QuickSelect对K值变化不敏感，性能稳定

4. **复杂度对比**
   - 原始全排序：O(n²) → O(n log n)
   - Top-K 优化：O(nk) → O(n log k)
   - Top-K 优化将复杂度从O(n²)优化到O(n log k)，性能提升明显

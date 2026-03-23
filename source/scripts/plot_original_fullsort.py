import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

# 设置中文字体 + 支持LaTeX公式显示
plt.rcParams['font.sans-serif'] = ['SimHei']  # Windows
# plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']  # Mac
# plt.rcParams['font.sans-serif'] = ['WenQuanYi Micro Hei']  # Linux
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['text.usetex'] = False  # 关闭LaTeX（避免环境依赖）
plt.rcParams['mathtext.fontset'] = 'cm'  # 数学公式字体
plt.rcParams['figure.dpi'] = 150
plt.rcParams['savefig.dpi'] = 150

# ===== 优化：目录创建（兼容多系统）=====
save_dir = os.path.join("source", "origin")
os.makedirs(save_dir, exist_ok=True)
print(f"✅ 图片保存目录：{os.path.abspath(save_dir)}")

# 1. 读取并清洗原始CSV文件
csv_path = os.path.join("source", "data", "original_fullsort_benchmark.csv")
try:
    df = pd.read_csv(csv_path)
    required_cols = ['algorithm', 'n', 'k', 'time_ms']
    if not all(col in df.columns for col in required_cols):
        raise ValueError("CSV列名不匹配，尝试按无表头读取")
except:
    df_raw = pd.read_csv(csv_path, header=None, names=['algorithm', 'n', 'k', 'time_ms'])
    df = df_raw.copy()

# 数据清洗（彻底处理空值）
df['n'] = pd.to_numeric(df['n'], errors='coerce')
df['k'] = pd.to_numeric(df['k'], errors='coerce')
df['time_ms'] = pd.to_numeric(df['time_ms'], errors='coerce')
df = df.dropna(subset=['algorithm', 'n', 'k', 'time_ms'])
df['n'] = df['n'].astype(int)
df['k'] = df['k'].astype(int)
df['time_ms'] = df['time_ms'].astype(float)
print(f"✅ 数据加载完成，过滤空值后有效行数：{len(df)}")

# 实测点等距映射
n_actual_all = sorted(df['n'].unique())
n_to_idx = {n: idx for idx, n in enumerate(n_actual_all)}
df['n_idx'] = df['n'].map(n_to_idx)
print(f"✅ 实测n值：{n_actual_all} → 等距索引：{n_to_idx}")

# 2. 核心修正：无scipy的精准理论模型（加权平均法拟合C）
def get_complexity_model(algo_name, algo_data):
    """
    无scipy依赖，用加权平均法计算最优C：
    - 快排：T(n) = C * n * log₂n → C = 平均(t/(n*log₂n))
    - 其他排序：T(n) = C * n² → C = 平均(t/n²)
    """
    n_fit = algo_data['n'].values
    t_fit = algo_data['time_ms'].values

    if algo_name == 'Origin_QuickSort_Full':
        # 快排：以2为底的对数，加权平均计算C（避免单个点误差）
        log2_n = np.log2(n_fit)
        # 计算每个点的C值，取平均（加权）
        c_values = t_fit / (n_fit * log2_n)
        C = np.mean(c_values)  # 平均C值，综合所有点的信息
        # 精准公式标注（log₂n）
        formula = r'$T(n) = C \cdot n \log_2 n$ (O($n\log n$))'
        def calc_func(n_values):
            return C * n_values * np.log2(n_values)
    
    else:  # 插入/冒泡/选择排序：O(n²)
        # 计算每个点的C值，取平均
        c_values = t_fit / (n_fit **2)
        C = np.mean(c_values)
        formula = r'$T(n) = C \cdot n^2$ (O($n^2$))'
        def calc_func(n_values):
            return C * (n_values** 2)
    
    return formula, calc_func

# 3. 绘图逻辑（等距横坐标+精准理论曲线）
algorithms = df['algorithm'].unique()
for algo in algorithms:
    algo_data = df[df['algorithm'] == algo].sort_values(by='n')
    n_idx_actual = algo_data['n_idx'].values
    time_actual = algo_data['time_ms'].values
    n_actual = algo_data['n'].values

    # 获取精准的理论公式和拟合后的计算函数
    complexity_formula, calc_theory = get_complexity_model(algo, algo_data)
    
    # 生成理论曲线的连续坐标（适配等距横坐标）
    n_min, n_max = min(n_actual_all), max(n_actual_all)
    n_range = np.linspace(n_min, n_max, 200)
    time_theory = calc_theory(n_range)
    n_idx_range = np.linspace(n_to_idx[n_min], n_to_idx[n_max], 200)

    # 创建画布
    plt.figure(figsize=(10, 6))

    # 绘制实测折线（红色+圆点）
    plt.plot(n_idx_actual, time_actual, color='#e74c3c', marker='o', markersize=6,
             linewidth=2, label='实际运行时间（实测）', zorder=5)

    # 绘制修正后的理论曲线（蓝色虚线）
    plt.plot(n_idx_range, time_theory, color='#3498db', linewidth=2,
             linestyle='--', label=f'理论复杂度曲线: {complexity_formula}', zorder=3)

    # 等距横坐标设置
    plt.xticks(
        ticks=list(n_to_idx.values()),
        labels=[f"{n//10000}万" for n in n_actual_all],
        fontsize=10
    )
    plt.xlabel('数据规模 n（实测点等距分布）', fontsize=12)
    plt.ylabel('运行时间 (ms)', fontsize=12)
    plt.title(f'{algo.replace("Origin_", "").replace("_Full", "")} 时间复杂度对比', fontsize=14, pad=15)
    plt.legend(fontsize=11, loc='upper left')
    plt.grid(True, alpha=0.3, axis='y')
    plt.grid(True, alpha=0.1, axis='x')

    # 保存图片
    save_name = os.path.join(save_dir, f'{algo.replace("Origin_", "").replace("_Full", "")}_comparison.png')
    plt.tight_layout()
    plt.savefig(save_name, bbox_inches='tight')
    plt.close()

    print(f'✅ {algo.replace("Origin_", "").replace("_Full", "")} 图表已保存：{save_name}')

print('\n🎉 所有算法图表生成完成！快排理论曲线已精准修正（无scipy依赖）！')
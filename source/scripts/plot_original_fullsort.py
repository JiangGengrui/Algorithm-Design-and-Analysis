import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

# ================== 全局配置 ==================
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.dpi'] = 150
plt.rcParams['savefig.dpi'] = 150

# ================== 路径配置 ==================
save_dir = os.path.join("source", "origin")
os.makedirs(save_dir, exist_ok=True)
csv_path = os.path.join("source", "data", "original_fullsort_benchmark.csv")

print(f"📂 读取数据：{os.path.abspath(csv_path)}")

# ================== 读取数据 ==================
try:
    df = pd.read_csv(csv_path)
except:
    df = pd.read_csv(csv_path, header=None, names=['algorithm', 'n', 'k', 'time_ms'])

# ================== 数据清洗 ==================
df['n'] = pd.to_numeric(df['n'], errors='coerce')
df['k'] = pd.to_numeric(df['k'], errors='coerce')
df['time_ms'] = pd.to_numeric(df['time_ms'], errors='coerce')
df = df.dropna()
df['n'] = df['n'].astype(int)
df['time_ms'] = df['time_ms'].astype(float)
print(f"✅ 数据行数：{len(df)}")

# ================== 等距横坐标 ==================
n_actual_all = sorted(df['n'].unique())
n_to_idx = {n: i for i, n in enumerate(n_actual_all)}
df['n_idx'] = df['n'].map(n_to_idx)

# ================== 【核心】严格理论复杂度曲线（平滑） ==================
def get_smooth_theoretical_curve(algo_name, n_actual, t_actual):
    # 取第一个点为基准（你要求的）
    n0 = n_actual[0]
    t0 = t_actual[0]

    # 生成平滑的 n 序列（让曲线光滑）
    n_smooth = np.linspace(n_actual.min(), n_actual.max(), 500)

    if "QuickSort" in algo_name:
        # 严格 O(n log n) 平滑曲线
        base = n0 * np.log2(n0)
        t_smooth = t0 * (n_smooth * np.log2(n_smooth)) / base
        formula = r'$O(n\log_2 n)$'
    else:
        # 严格 O(n²) 平滑曲线
        t_smooth = t0 * (n_smooth ** 2) / (n0 ** 2)
        formula = r'$O(n^2)$'

    # 横坐标映射到等距 index，保证对齐
    x_smooth = np.array([n_to_idx[n] for n in n_actual_all])
    x_smooth = np.linspace(x_smooth.min(), x_smooth.max(), 500)

    return formula, x_smooth, t_smooth

# ================== 绘图 ==================
algorithms = df['algorithm'].unique()

for algo in algorithms:
    data = df[df['algorithm'] == algo].sort_values(by='n')
    n_idx = data['n_idx'].values
    n_actual = data['n'].values
    t_actual = data['time_ms'].values

    # 获取平滑理论曲线
    formula, x_theory, y_theory = get_smooth_theoretical_curve(algo, n_actual, t_actual)

    # 画图
    plt.figure(figsize=(10, 6))
    # 实测数据（完全不动）
    plt.plot(n_idx, t_actual, marker='o', linewidth=2, label='实际运行时间')
    # 理论平滑曲线（严格复杂度）
    plt.plot(x_theory, y_theory, '--', linewidth=3, color='red', label=f'理论曲线 {formula}')

    plt.xticks(ticks=list(n_to_idx.values()), labels=[f"{n//10000}万" for n in n_actual_all])
    title = algo.replace("Origin_", "").replace("_Full", "")
    plt.title(f"{title} 时间复杂度", fontsize=14)
    plt.xlabel("数据规模 n")
    plt.ylabel("时间 (ms)")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    save_path = os.path.join(save_dir, f"{title}.png")
    plt.savefig(save_path)
    plt.close()
    print(f"✅ 已生成：{save_path}")

print("\n🎉 完成！理论曲线现在是完美平滑的！")
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
df['time_ms'] = pd.to_numeric(df['time_ms'], errors='coerce')
df = df.dropna()

# ================== 等距横坐标 ==================
n_actual_all = sorted(df['n'].unique())
n_to_idx = {n: i for i, n in enumerate(n_actual_all)}
df['n_idx'] = df['n'].map(n_to_idx)

# ================== 公式计算 ==================
def get_theory_curve(algo, n_list, t0, n0):
    # 你的公式：c = 第一个点实测值 / 第一个点理论复杂度
    if "QuickSort" in algo:
        c = t0 / (n0 * np.log2(n0))
        theory = c * n_list * np.log2(n_list)
        formula = r'$T = c \cdot n\log_2 n$'
    else:
        c = t0 / (n0 ** 2)
        theory = c * (n_list ** 2)
        formula = r'$T = c \cdot n^2$'
    return theory, formula

# ================== 绘图 ==================
algorithms = df['algorithm'].unique()

for algo in algorithms:
    data = df[df['algorithm'] == algo].sort_values('n')
    n_actual = data['n'].values
    t_actual = data['time_ms'].values
    n_idx = data['n_idx'].values

    # 取第一个点作为基准
    n0 = n_actual[0]
    t0 = t_actual[0]

    # 生成平滑理论曲线
    n_smooth = np.linspace(n_actual.min(), n_actual.max(), 200)
    t_smooth, formula = get_theory_curve(algo, n_smooth, t0, n0)

    # 横坐标映射
    x_smooth = np.interp(n_smooth, n_actual_all, list(n_to_idx.values()))

    # 画图
    plt.figure(figsize=(10,6))
    plt.plot(n_idx, t_actual, 'o-', label='实测数据')
    plt.plot(x_smooth, t_smooth, '--', linewidth=2, label=f'理论曲线 {formula}')

    plt.xticks(list(n_to_idx.values()), [f'{n//10000}万' for n in n_actual_all])
    plt.title(algo.replace("Origin_","").replace("_Full",""))
    plt.xlabel("数据规模 n")
    plt.ylabel("时间 (ms)")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, f"{algo}.png"))
    plt.close()

print("理论曲线绘制完成，已保存到：", os.path.abspath(save_dir))
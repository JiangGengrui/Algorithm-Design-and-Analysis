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
    df = pd.read_csv(csv_path, header=None,
                     names=['algorithm', 'n', 'k', 'time_ms'])

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

# ================== 正确复杂度拟合 ==================
def get_complexity_model(algo_name, algo_data):
    n = algo_data['n'].values
    t = algo_data['time_ms'].values

    if "QuickSort" in algo_name:
        # T(n) = a*n log n + b*n
        X = np.vstack([n * np.log2(n), n]).T
        coeffs, _, _, _ = np.linalg.lstsq(X, t, rcond=None)
        a, b = coeffs

        formula = r'$T(n)=a\cdot n\log_2 n + b\cdot n$'

        def func(x):
            return a * x * np.log2(x) + b * x

    else:
        # T(n) = a*n^2 + b*n
        X = np.vstack([n**2, n]).T
        coeffs, _, _, _ = np.linalg.lstsq(X, t, rcond=None)
        a, b = coeffs

        formula = r'$T(n)=a\cdot n^2 + b\cdot n$'

        def func(x):
            return a * x**2 + b * x

    return formula, func

# ================== 绘图 ==================
algorithms = df['algorithm'].unique()

for algo in algorithms:
    data = df[df['algorithm'] == algo].sort_values(by='n')

    n_idx = data['n_idx'].values
    n_actual = data['n'].values
    t_actual = data['time_ms'].values

    # 获取理论模型
    formula, theory_func = get_complexity_model(algo, data)

    # 连续曲线
    n_min, n_max = min(n_actual_all), max(n_actual_all)
    n_smooth = np.linspace(n_min, n_max, 200)
    t_smooth = theory_func(n_smooth)

    n_idx_smooth = np.linspace(n_to_idx[n_min], n_to_idx[n_max], 200)

    # ================== 开始画图 ==================
    # ====== 用真实 n 作横轴 ======
    plt.figure(figsize=(10, 6))

    plt.plot(n_actual, t_actual,
         marker='o',
         linewidth=2,
         label='实际运行时间')

    plt.plot(n_smooth, t_smooth,
         linestyle='--',
         linewidth=2,
         label=f'理论模型 {formula}')

    plt.xlabel("数据规模 n")
    plt.ylabel("时间 (ms)")
    plt.title(f"{title} 时间复杂度拟合")
    plt.legend()
    plt.grid(alpha=0.3)

    # ================== 保存 ==================
    save_path = os.path.join(save_dir, f"{title}.png")
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

    print(f"✅ 已生成：{save_path}")

print("\n🎉 所有图生成完成（理论模型已修正）")
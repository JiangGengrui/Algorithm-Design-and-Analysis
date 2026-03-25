import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

# ===================== 全局设置（解决中文/公式乱码）=====================
plt.rcParams['font.sans-serif'] = ['SimHei']  # Windows
# plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']  # Mac
# plt.rcParams['font.sans-serif'] = ['WenQuanYi Micro Hei']  # Linux
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['mathtext.fontset'] = 'cm'  # 数学公式字体规范
plt.rcParams['figure.dpi'] = 150  # 高清图
plt.rcParams['savefig.dpi'] = 150

# ===================== 创建保存目录（source/Topk）=====================
def create_save_dir():
    save_dir = os.path.join("source", "Topk")
    os.makedirs(save_dir, exist_ok=True)
    print(f"✅ 目录：{save_dir}")
    return save_dir

# ===================== 1. 读取并清洗CSV数据 =====================
def load_data(csv_path="source/data/topk_benchmark.csv"):
    df = pd.read_csv(csv_path)
    df['n'] = df['n'].astype(int)
    df['k'] = df['k'].astype(int)
    df['time_ms'] = df['time_ms'].astype(float)
    df = df.sort_values(by=['algorithm', 'n']).reset_index(drop=True)

    n_actual_all = sorted(df['n'].unique())
    k_fixed = df['k'].unique()[0]
    n_to_idx = {n: idx for idx, n in enumerate(n_actual_all)}
    df['n_idx'] = df['n'].map(n_to_idx)

    print("\n✅ 数据加载完成，实验参数：")
    print(f"固定Top-K值 k = {k_fixed}")
    print(f"实测数据规模n：{n_actual_all}")
    print(f"算法列表：{df['algorithm'].unique().tolist()}")
    return df, n_actual_all, n_to_idx, k_fixed

# ===================== 【核心修改】完全按你的规则计算理论曲线 =====================
def get_algo_info(algo_name, df, n_actual_all, k_fixed):
    # 取第一个点作为基准
    n0 = n_actual_all[0]
    t0 = df[(df['algorithm'] == algo_name) & (df['n'] == n0)]['time_ms'].iloc[0]
    log_k = np.log2(k_fixed)

    if algo_name == "MinHeap_TopK":
        # 你的公式：c = t0 / (n0 * logk)
        c = t0 / (n0 * log_k)
        formula = rf'$T = c \cdot n\log_2 k$, k={k_fixed}'
        o_name = r'O($n\log k$)'
        def calc_theory(n):
            return c * n * log_k

    else:
        # 你的公式：c = t0 / n0
        c = t0 / n0
        formula = r'$T = c \cdot n$'
        o_name = r'O($n$)'
        def calc_theory(n):
            return c * n

    return f"{formula} {o_name}", calc_theory

# ===================== 2. 单个算法绘图（理论曲线完全按你的规则） =====================
def plot_algo(algo_name, df, n_actual_all, n_to_idx, k_fixed, save_dir):
    algo_data = df[df['algorithm'] == algo_name].copy()
    n_idx_actual = algo_data['n_idx'].values
    t_actual = algo_data['time_ms'].values

    complexity_formula, calc_theory = get_algo_info(algo_name, df, n_actual_all, k_fixed)

    # 平滑理论曲线 + 横坐标严格对齐
    n_smooth = np.linspace(min(n_actual_all), max(n_actual_all), 500)
    t_theory = calc_theory(n_smooth)
    x_theory = np.interp(n_smooth, n_actual_all, list(n_to_idx.values()))

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(n_idx_actual, t_actual, color='#e74c3c', marker='o', markersize=7, linewidth=2.5, label='实测运行时间', zorder=5)
    ax.plot(x_theory, t_theory, color='#3498db', linewidth=2, linestyle='--', label=f'理论曲线：{complexity_formula}', zorder=3)

    ax.set_xticks(list(n_to_idx.values()))
    ax.set_xticklabels([f"{n//10000}万" for n in n_actual_all], fontsize=10)
    ax.set_title(f'{algo_name} 时间复杂度对比（Top-K实验）', fontsize=14, pad=20)
    ax.set_xlabel('数据规模 n（实测点等距分布）', fontsize=12)
    ax.set_ylabel('运行时间（ms）', fontsize=12)
    ax.legend(fontsize=10, loc='upper left', framealpha=0.9)
    ax.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    save_path = os.path.join(save_dir, f"{algo_name}_topk.png")
    plt.savefig(save_path, bbox_inches='tight')
    plt.close()
    print(f"✅ 已保存：{save_path}")

# ===================== 3. 多算法对比图 =====================
def plot_all_algos(df, n_actual_all, n_to_idx, k_fixed, save_dir):
    fig, ax = plt.subplots(figsize=(14, 7))
    algo_style = {
        "InsertSort_TopK": {"color": "#e74c3c", "marker": "o"},
        "SelectionSort_TopK": {"color": "#f39c12", "marker": "s"},
        "BubbleSort_TopK": {"color": "#2ecc71", "marker": "^"},
        "QuickSelect_TopK": {"color": "#9b59b6", "marker": "D"},
        "MinHeap_TopK": {"color": "#3498db", "marker": "p"}
    }
    for algo in df['algorithm'].unique():
        algo_data = df[df['algorithm'] == algo]
        ax.plot(algo_data['n_idx'], algo_data['time_ms'],
                color=algo_style[algo]["color"], marker=algo_style[algo]["marker"],
                markersize=7, linewidth=2, label=algo)

    ax.set_xticks(list(n_to_idx.values()))
    ax.set_xticklabels([f"{n//10000}万" for n in n_actual_all], fontsize=10)
    ax.set_title(f'Top-K 算法对比（k={k_fixed}）', fontsize=15)
    ax.set_xlabel('数据规模 n', fontsize=12)
    ax.set_ylabel('运行时间（ms）', fontsize=12)
    ax.legend(fontsize=10)
    ax.grid(alpha=0.3)
    plt.tight_layout()
    save_path = os.path.join(save_dir, f"All_TopK.png")
    plt.savefig(save_path, bbox_inches='tight')
    plt.close()
    print(f"✅ 已保存：{save_path}")

# ===================== 主函数 =====================
if __name__ == "__main__":
    save_dir = create_save_dir()
    df, n_actual_all, n_to_idx, k_fixed = load_data("source/data/topk_benchmark.csv")
    print("\n📊 绘制单个算法图...")
    for algo in df['algorithm'].unique():
        plot_algo(algo, df, n_actual_all, n_to_idx, k_fixed, save_dir)
    print("\n📊 绘制多算法对比图...")
    plot_all_algos(df, n_actual_all, n_to_idx, k_fixed, save_dir)
    print(f"\n🎉 全部完成！理论曲线 100% 按你的规则计算！")
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
    """创建保存图片的目录：source/Topk（不存在则自动创建）"""
    save_dir = os.path.join("source", "Topk")
    os.makedirs(save_dir, exist_ok=True)
    print(f"✅ 目录：{save_dir}")
    return save_dir

# ===================== 1. 读取并清洗CSV数据 =====================
def load_data(csv_path="source/data/topk_benchmark.csv"):
    """读取Top-K基准测试数据，返回清洗后的DataFrame"""
    df = pd.read_csv(csv_path)
    # 数据类型转换+排序（按n升序，保证折线顺序正确）
    df['n'] = df['n'].astype(int)
    df['k'] = df['k'].astype(int)
    df['time_ms'] = df['time_ms'].astype(float)
    df = df.sort_values(by=['algorithm', 'n']).reset_index(drop=True)

    # 提取所有实测n值、固定k值（本次实验k=10）
    n_actual_all = sorted(df['n'].unique())
    k_fixed = df['k'].unique()[0]  # 从数据中提取固定k值，无需硬编码
    # 建立n值到等距坐标的映射（实测点等距核心）
    n_to_idx = {n: idx for idx, n in enumerate(n_actual_all)}
    df['n_idx'] = df['n'].map(n_to_idx)

    # 验证数据
    print("\n✅ 数据加载完成，实验参数：")
    print(f"固定Top-K值 k = {k_fixed}")
    print(f"实测数据规模n：{n_actual_all}")
    print(f"算法列表：{df['algorithm'].unique().tolist()}")
    return df, n_actual_all, n_to_idx, k_fixed

# ===================== 2. 精准定义各算法的理论复杂度（核心修正）=====================
def get_algo_info(algo_name, df, n_actual_all, k_fixed):
    """
    为每个算法返回**精准**的理论公式、大O表示、理论值计算函数
    单独区分小顶堆MinHeap_TopK的O(nlogk)与其他算法的O(n)
    """
    # 基准值：最小n的实测时间（保证理论曲线贴合实测）
    n_base = n_actual_all[0]
    t_base = df[(df['algorithm'] == algo_name) & (df['n'] == n_base)]['time_ms'].iloc[0]
    log_k = np.log2(k_fixed)  # 对数以2为底（算法复杂度中默认底为2）

    # 情况1：小顶堆MinHeap_TopK - 精准O(nlogk)
    if algo_name == "MinHeap_TopK":
        formula = rf'$T(n) = C \cdot n \cdot \log_2 k$ (k={k_fixed})'
        o_name = r'O($n\log k$)'
        # 拟合常数C：T = C·n·logk → C = t_base/(n_base·logk)
        C = t_base / (n_base * log_k)
        def calc_theory(n_values):
            return C * n_values * log_k  # 理论时间计算

    # 情况2：其余4种算法 - O(n)（Insert/Selection/Bubble为O(nk)，QuickSelect为O(n)，k固定均为O(n)）
    else:
        if algo_name in ["InsertSort_TopK", "SelectionSort_TopK", "BubbleSort_TopK"]:
            formula = rf'$T(n) = C \cdot n \cdot k$ (k={k_fixed})'
        else:  # QuickSelect_TopK
            formula = r'$T(n) = C \cdot n$'
        o_name = r'O($n$)'
        # 拟合常数C：T = C·n → C = t_base/n_base
        C = t_base / n_base
        def calc_theory(n_values):
            return C * n_values  # 理论时间计算

    return f"{formula} {o_name}", calc_theory

# ===================== 3. 单个算法绘图函数（实测点等距+精准理论）=====================
def plot_algo(algo_name, df, n_actual_all, n_to_idx, k_fixed, save_dir):
    """为单个算法绘制「实测折线+精准理论曲线」对比图"""
    # 筛选当前算法的实测数据
    algo_data = df[df['algorithm'] == algo_name].copy()
    n_idx_actual = algo_data['n_idx'].values
    t_actual = algo_data['time_ms'].values

    # 获取**精准**的理论公式和计算函数
    complexity_formula, calc_theory = get_algo_info(algo_name, df, n_actual_all, k_fixed)

    # 生成理论曲线的平滑坐标（和实测点等距对齐）
    n_min, n_max = min(n_actual_all), max(n_actual_all)
    n_range = np.linspace(n_min, n_max, 200)  # 连续n值
    t_theory = calc_theory(n_range)           # 精准理论时间
    n_idx_range = np.linspace(n_to_idx[n_min], n_to_idx[n_max], 200)  # 等距横坐标

    # 创建画布
    fig, ax = plt.subplots(figsize=(10, 6))

    # 绘制：实测值（红色实线+圆形标记，等距分布）
    ax.plot(n_idx_actual, t_actual, color='#e74c3c', marker='o', markersize=7,
            linewidth=2.5, label=f'实测运行时间', zorder=5)
    # 绘制：理论值（蓝色虚线，精准拟合）
    ax.plot(n_idx_range, t_theory, color='#3498db', linewidth=2,
            linestyle='--', label=f'理论复杂度：{complexity_formula}', zorder=3)

    # 等距横坐标设置（核心：实测点间隔完全均匀）
    ax.set_xticks(list(n_to_idx.values()))
    ax.set_xticklabels([f"{n//10000}万" for n in n_actual_all], fontsize=10)

    # 图表样式优化
    ax.set_title(f'{algo_name} 时间复杂度对比（Top-K实验）', fontsize=14, pad=20)
    ax.set_xlabel('数据规模 n（实测点等距分布）', fontsize=12)
    ax.set_ylabel('运行时间（ms）', fontsize=12)
    ax.legend(fontsize=10, loc='upper left', framealpha=0.9)
    ax.grid(True, alpha=0.3, axis='y')  # 纵向网格辅助对比
    ax.grid(True, alpha=0.1, axis='x')  # 横向网格弱化，突出等距点

    # 保存图片到source/Topk
    plt.tight_layout()
    save_filename = f"{algo_name}_topk_comparison_even.png"
    save_path = os.path.join(save_dir, save_filename)
    plt.savefig(save_path, bbox_inches='tight')
    plt.close()
    print(f"✅ 已保存：{save_path}")

# ===================== 4. 多算法同图对比（精准复杂度标注）=====================
def plot_all_algos(df, n_actual_all, n_to_idx, k_fixed, save_dir):
    """所有Top-K算法同图对比（实测点等距+各算法精准复杂度标注）"""
    fig, ax = plt.subplots(figsize=(14, 7))
    # 定义差异化颜色/标记（区分5种算法，小顶堆单独标记）
    algo_style = {
        "InsertSort_TopK": {"color": "#e74c3c", "marker": "o"},
        "SelectionSort_TopK": {"color": "#f39c12", "marker": "s"},
        "BubbleSort_TopK": {"color": "#2ecc71", "marker": "^"},
        "QuickSelect_TopK": {"color": "#9b59b6", "marker": "D"},
        "MinHeap_TopK": {"color": "#3498db", "marker": "p"}  # 小顶堆单独蓝色+五边形标记
    }
    algorithms = df['algorithm'].unique()

    # 绘制各算法实测曲线（等距分布）
    for algo in algorithms:
        algo_data = df[df['algorithm'] == algo]
        ax.plot(algo_data['n_idx'], algo_data['time_ms'],
                color=algo_style[algo]["color"], marker=algo_style[algo]["marker"],
                markersize=7, linewidth=2, label=algo, zorder=5)

    # 绘制理论参考线（以QuickSelect_TopK的O(n)为基准，最具代表性）
    ref_algo = "QuickSelect_TopK"
    _, calc_theory_ref = get_algo_info(ref_algo, df, n_actual_all, k_fixed)
    n_min, n_max = min(n_actual_all), max(n_actual_all)
    n_range = np.linspace(n_min, n_max, 200)
    t_theory_ref = calc_theory_ref(n_range)
    n_idx_range = np.linspace(n_to_idx[n_min], n_to_idx[n_max], 200)
    ax.plot(n_idx_range, t_theory_ref, color='black', linewidth=2,
            linestyle='--', label=f'理论参考（O(n)）', zorder=3)

    # 等距横坐标设置
    ax.set_xticks(list(n_to_idx.values()))
    ax.set_xticklabels([f"{n//10000}万" for n in n_actual_all], fontsize=10)

    # 图表样式
    ax.set_title(f'Top-K算法时间复杂度对比（k={k_fixed}，实测点等距分布）', fontsize=15, pad=20)
    ax.set_xlabel('数据规模 n', fontsize=12)
    ax.set_ylabel('运行时间（ms）', fontsize=12)
    ax.legend(fontsize=9, loc='upper left', framealpha=0.9)
    ax.grid(True, alpha=0.3, axis='y')
    ax.grid(True, alpha=0.1, axis='x')

    # 保存多算法对比图
    plt.tight_layout()
    save_filename = f"All_TopK_Algorithms_Comparison_k{k_fixed}.png"
    save_path = os.path.join(save_dir, save_filename)
    plt.savefig(save_path, bbox_inches='tight')
    plt.close()
    print(f"✅ 已保存：{save_path}")

# ===================== 5. 主函数：批量绘图 =====================
if __name__ == "__main__":
    # 1. 创建保存目录source/Topk
    save_dir = create_save_dir()
    # 2. 加载数据（自动提取k值，无需硬编码）
    df, n_actual_all, n_to_idx, k_fixed = load_data("source/data/topk_benchmark.csv")
    # 3. 遍历所有算法，绘制单个算法精准对比图
    print("\n📊 开始绘制单个算法精准对比图...")
    for algo in df['algorithm'].unique():
        plot_algo(algo, df, n_actual_all, n_to_idx, k_fixed, save_dir)
    # 4. 绘制多算法同图对比图
    print("\n📊 绘制多算法同图对比图...")
    plot_all_algos(df, n_actual_all, n_to_idx, k_fixed, save_dir)
    # 5. 完成提示
    print(f"\n🎉 所有图表绘制完成！图片均保存到：{os.path.abspath(save_dir)}")

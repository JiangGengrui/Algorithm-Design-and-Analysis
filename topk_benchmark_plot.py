import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# ===================== 全局设置（解决中文/公式乱码）=====================
plt.rcParams['font.sans-serif'] = ['SimHei']  # Windows
# plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']  # Mac
# plt.rcParams['font.sans-serif'] = ['WenQuanYi Micro Hei']  # Linux
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['mathtext.fontset'] = 'cm'  # 数学公式字体规范
plt.rcParams['figure.dpi'] = 150  # 高清图
plt.rcParams['savefig.dpi'] = 150

# ===================== 1. 读取并清洗CSV数据 =====================
def load_data(csv_path="topk_benchmark.csv"):
    """读取Top-K基准测试数据，返回清洗后的DataFrame"""
    df = pd.read_csv(csv_path)
    # 数据类型转换+排序（按n升序，保证折线顺序）
    df['n'] = df['n'].astype(int)
    df['k'] = df['k'].astype(int)
    df['time_ms'] = df['time_ms'].astype(float)
    df = df.sort_values(by=['algorithm', 'n']).reset_index(drop=True)
    # 验证数据
    print("✅ 数据加载完成，预览：")
    print(df.head(5))
    print(f"📊 算法列表：{df['algorithm'].unique().tolist()}")
    print(f"📈 数据规模n：{sorted(df['n'].unique())}")
    return df

# ===================== 2. 定义复杂度公式+理论值计算 =====================
def get_algo_info(algo_name, df):
    """
    返回算法的理论公式、大O表示、理论值计算函数
    :param algo_name: 算法名
    :param df: 清洗后的数据集
    :return: formula(公式), o_name(大O), calc_theory(计算理论值的函数)
    """
    # 基于**最小的n(100000)**的实测值计算拟合常数C（保证理论曲线贴合实测）
    n_base = 100000
    t_base = df[(df['algorithm'] == algo_name) & (df['n'] == n_base)]['time_ms'].iloc[0]
    C = t_base / n_base  # 所有算法均为O(n)，C = 实测时间 / 基准n
    
    # 统一理论公式：O(n)，因k固定为常数
    formula = r'$T(n) = C \cdot n$'
    o_name = r'O($n$)'
    
    # 定义理论值计算函数：输入n的数组，返回理论时间
    def calc_theory(n_values):
        return C * n_values
    
    return f"{formula} ({o_name})", calc_theory

# ===================== 3. 单个算法绘图函数 =====================
def plot_algo(algo_name, df, n_range_log):
    """为单个算法绘制「实测折线+理论曲线」对比图"""
    # 筛选当前算法的实测数据
    algo_data = df[df['algorithm'] == algo_name].copy()
    n_actual = algo_data['n'].values
    t_actual = algo_data['time_ms'].values
    
    # 获取理论公式和计算函数
    complexity_formula, calc_theory = get_algo_info(algo_name, df)
    t_theory = calc_theory(n_range_log)
    
    # 创建画布
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # 绘制：实测值（红色实线+圆形标记，突出数据点）
    ax.plot(n_actual, t_actual, color='#e74c3c', marker='o', markersize=7, 
            linewidth=2.5, label=f'实测运行时间', zorder=5)
    # 绘制：理论值（蓝色虚线，和实测区分）
    ax.plot(n_range_log, t_theory, color='#3498db', linewidth=2, 
            linestyle='--', label=f'理论复杂度：{complexity_formula}', zorder=3)
    
    # 横坐标：对数刻度（保证10万/1000万间隔均匀）
    ax.set_xscale('log')
    # 自定义横坐标刻度+标签（易读，替换科学计数法）
    n_ticks = [100000, 500000, 1000000, 5000000, 10000000]
    n_labels = ['10万', '50万', '100万', '500万', '1000万']
    ax.set_xticks(n_ticks)
    ax.set_xticklabels(n_labels, fontsize=10)
    
    # 坐标轴标签+标题
    ax.set_title(f'{algo_name} 时间复杂度对比（Top-K, k=10）', fontsize=14, pad=20)
    ax.set_xlabel('数据规模 n（对数刻度）', fontsize=12)
    ax.set_ylabel('运行时间（ms）', fontsize=12)
    
    # 图例+网格
    ax.legend(fontsize=11, loc='upper left', framealpha=0.9)
    ax.grid(True, alpha=0.3, which='both')  # 显示对数网格线，方便对比
    
    # 调整布局，防止公式/标签被裁剪
    plt.tight_layout()
    # 保存图片（算法名作为文件名，无特殊字符）
    save_path = f"{algo_name}_topk_comparison.png"
    plt.savefig(save_path, bbox_inches='tight')
    plt.close()
    print(f"✅ 已保存：{save_path}")

# ===================== 4. 主函数：批量绘图 =====================
if __name__ == "__main__":
    # 1. 加载数据
    df = load_data("topk_benchmark.csv")  # 若CSV在其他路径，修改此处
    # 2. 生成对数刻度的n序列（用于绘制平滑的理论曲线）
    n_min, n_max = df['n'].min(), df['n'].max()
    n_range_log = np.logspace(np.log10(n_min), np.log10(n_max), 200)
    # 3. 遍历所有算法，批量绘图
    algorithms = df['algorithm'].unique()
    print("\n📊 开始绘制图表...")
    for algo in algorithms:
        plot_algo(algo, df, n_range_log)
    # 4. 完成提示
    print("\n🎉 所有Top-K算法对比图绘制完成！")
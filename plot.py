import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# 设置中文字体 + 支持LaTeX公式显示
plt.rcParams['font.sans-serif'] = ['SimHei']  # Windows
# plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']  # Mac
# plt.rcParams['font.sans-serif'] = ['WenQuanYi Micro Hei']  # Linux
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['text.usetex'] = False  # 关闭LaTeX（避免环境依赖，用matplotlib原生支持）
plt.rcParams['mathtext.fontset'] = 'cm'  # 数学公式字体

# 1. 读取并清洗原始CSV文件
df_raw = pd.read_csv("original_fullsort_benchmark.csv", header=None, names=['algorithm', 'n', 'k', 'time_ms'])
df = df_raw[pd.to_numeric(df_raw['n'], errors='coerce').notna()].copy()
df['n'] = df['n'].astype(int)
df['k'] = df['k'].astype(int)
df['time_ms'] = df['time_ms'].astype(float)

# 2. 定义理论复杂度计算函数 + 公式映射
def get_complexity_info(algo_name):
    """返回算法的复杂度公式和计算函数"""
    if algo_name in ['Origin_InsertSort_Full', 'Origin_BubbleSort_Full', 'Origin_SelectionSort_Full']:
        # O(n²) 算法
        formula = r'$T(n) = C \cdot n^2$ (O($n^2$))'
        def calc_func(n_values):
            c_data = df[(df['algorithm'] == algo_name) & (df['n'] == 10000)]['time_ms'].iloc[0]
            C = c_data / (10000 **2)
            return C * (n_values** 2)
        return formula, calc_func
    elif algo_name == 'Origin_QuickSort_Full':
        # O(n log n) 算法
        formula = r'$T(n) = C \cdot n \log n$ (O($n \log n$))'
        def calc_func(n_values):
            c_data = df[(df['algorithm'] == algo_name) & (df['n'] == 10000)]['time_ms'].iloc[0]
            C = c_data / (10000 * np.log(10000))
            return C * n_values * np.log(n_values)
        return formula, calc_func
    else:
        return r'$T(n) = 0$', lambda x: np.zeros_like(x)

# 3. 为每个算法绘图（含公式标注）
algorithms = df['algorithm'].unique()
n_range_log = np.logspace(np.log10(10000), np.log10(100000), 100)

for algo in algorithms:
    # 筛选并排序实测数据
    algo_data = df[df['algorithm'] == algo].sort_values(by='n')
    n_actual = algo_data['n'].values
    time_actual = algo_data['time_ms'].values
    
    # 获取复杂度公式和理论值计算函数
    complexity_formula, calc_theory = get_complexity_info(algo)
    time_theory = calc_theory(n_range_log)
    
    # 创建画布
    plt.figure(figsize=(10, 6))
    
    # 绘制实测折线（红色+圆点）
    plt.plot(n_actual, time_actual, color='#e74c3c', marker='o', markersize=6, 
             linewidth=2, label='实际运行时间（实测）', zorder=5)
    
    # 绘制理论曲线（蓝色虚线）
    plt.plot(n_range_log, time_theory, color='#3498db', linewidth=2, 
             linestyle='--', label=f'理论复杂度曲线: {complexity_formula}', zorder=3)
    
    # 设置对数横坐标
    plt.xscale('log')
    plt.xticks(
        ticks=[10000, 20000, 50000, 100000],
        labels=['1万', '2万', '5万', '10万'],
        fontsize=10
    )
    
    # 图表样式
    algo_name_simplified = algo.replace('Origin_', '').replace('_Full', '')
    plt.title(f'{algo_name_simplified} 时间复杂度对比', fontsize=14, pad=15)
    plt.xlabel('数据规模 n（对数刻度）', fontsize=12)
    plt.ylabel('运行时间 (ms)', fontsize=12)
    plt.legend(fontsize=11, loc='upper left')  # 图例放在左上，避免遮挡曲线
    plt.grid(True, alpha=0.3, which='both')
    
    # 保存图片
    save_name = f'{algo_name_simplified}_comparison_with_formula.png'
    plt.tight_layout()
    plt.savefig(save_name, dpi=150, bbox_inches='tight')  # bbox_inches避免公式被裁剪
    plt.close()
    
    print(f'✅ {algo_name_simplified} 图表已保存：{save_name}')

print('\n🎉 所有带公式标注的图表生成完成！')
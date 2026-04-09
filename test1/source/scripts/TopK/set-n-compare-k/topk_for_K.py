import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

# ================== 全局配置（完全对齐你的模板） ==================
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.dpi'] = 150
plt.rcParams['savefig.dpi'] = 150

# ================== 路径配置 ==================
save_dir = os.path.join("source", "topk")
os.makedirs(save_dir, exist_ok=True)
csv_path = os.path.join("source", "data", "k_topk.csv")

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
df = df[df['n'] == 10000]  # 固定n=10000

# ================== 等距横坐标配置 ==================
k_actual_all = sorted(df['k'].unique())
k_to_idx = {k: i for i, k in enumerate(k_actual_all)}
df['k_idx'] = df['k'].map(k_to_idx)

# ================== 单张图绘制所有算法对比 ==================
plt.figure(figsize=(10,6))

# 算法中文名称映射（让图例更美观）
algo_name_map = {
    "InsertSort_TopK": "插入排序Top-K",
    "SelectionSort_TopK": "选择排序Top-K",
    "BubbleSort_TopK": "冒泡排序Top-K",
    "QuickSelect_TopK": "快速选择Top-K",
    "MinHeap_TopK": "小顶堆Top-K"
}

# 遍历所有算法，绘制到同一张图
algorithms = df['algorithm'].unique()
for algo in algorithms:
    data = df[df['algorithm'] == algo].sort_values('k')
    k_idx = data['k_idx'].values
    t_actual = data['time_ms'].values
    # 绘制实测曲线
    plt.plot(k_idx, t_actual, 'o-', linewidth=2, markersize=6, 
             label=algo_name_map.get(algo, algo))

# ================== 图表样式 ==================
# 🔥 修复错误：把 n_to_idx 改为 k_to_idx
plt.xticks(list(k_to_idx.values()), [f'{k}' for k in k_actual_all])
plt.title("n=10000 时不同Top-K算法在不同k值下的效率对比")
plt.xlabel("Top-K 值 k")
plt.ylabel("运行时间 (ms)")
plt.legend()  # 显示所有算法图例
plt.grid(alpha=0.3)
plt.tight_layout()

# ================== 保存图片 ==================
plt.savefig(os.path.join(save_dir, "TopK_All_Algorithm_Compare.png"))
plt.close()

print("✅ Top-K 多算法对比图绘制完成，已保存到：", os.path.abspath(save_dir))
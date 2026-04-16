import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.dpi'] = 150
plt.rcParams['savefig.dpi'] = 300

# ===================== 完全保留你的原样：从CSV读取 =====================
csv_path = "closest_pair.csv"
df = pd.read_csv(csv_path)

df['n'] = pd.to_numeric(df['n'], errors='coerce')
df['time_ms'] = pd.to_numeric(df['time_ms'], errors='coerce')
df = df.dropna()

divide = df[df["algorithm"] == "DivideConquer"].sort_values("n")
n_actual = divide["n"].values
t_actual = divide["time_ms"].values

# ===================== 【唯一修复】正确计算拟合系数 c =====================
# 原来：只使用第一个点
# 现在：使用所有数据取平均 → 理论曲线完美贴合实测
c_values = t_actual / (n_actual * np.log2(n_actual))
c = np.mean(c_values)

# ===================== 以下完全不动 =====================
n_smooth = np.linspace(n_actual.min(), n_actual.max(), 200)
t_smooth = c * n_smooth * np.log2(n_smooth)

plt.figure(figsize=(10, 6))
plt.plot(n_actual, t_actual, 's-b', label="实测数据")
plt.plot(n_smooth, t_smooth, '--m', linewidth=2, label=r"理论曲线 $T = c \cdot n\log_2 n$")

plt.title("分治法 - 最近点对 实测 vs 理论", fontsize=14)
plt.xlabel("数据规模 n")
plt.ylabel("运行时间 (ms)")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("divide_theory.png")
plt.close()

print("✅ 分治法理论图已生成（曲线已修复）")


# algorithm,n,time_ms
# DivideConquer,100000,26.8367
# DivideConquer,200000,55.5459
# DivideConquer,300000,90.1867
# DivideConquer,400000,116.241
# DivideConquer,500000,149.182
# DivideConquer,600000,180.359
# DivideConquer,700000,202.233
# DivideConquer,800000,226.875
# DivideConquer,900000,260.513
# DivideConquer,1000000,296.285

# DivideConquer,1000000,290.184
# DivideConquer,2000000,544.553
# DivideConquer,3000000,803.9
# DivideConquer,4000000,1063.09
# DivideConquer,5000000,1317.66
# DivideConquer,6000000,1557.64
# DivideConquer,7000000,1842.59
# DivideConquer,8000000,2083.9
# DivideConquer,9000000,2413.23
# DivideConquer,10000000,2613.81
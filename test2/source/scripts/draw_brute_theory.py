import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.dpi'] = 150
plt.rcParams['savefig.dpi'] = 300

csv_path = "closest_pair.csv"
df = pd.read_csv(csv_path)

df['n'] = pd.to_numeric(df['n'], errors='coerce')
df['time_ms'] = pd.to_numeric(df['time_ms'], errors='coerce')
df = df.dropna()

brute = df[df["algorithm"] == "BruteForce"].sort_values("n")
n_actual = brute["n"].values
t_actual = brute["time_ms"].values

n0 = n_actual[0]
t0 = t_actual[0]
c = t0 / (n0 ** 2)

n_smooth = np.linspace(n_actual.min(), n_actual.max(), 200)
t_smooth = c * (n_smooth ** 2)

plt.figure(figsize=(10, 6))
plt.plot(n_actual, t_actual, 'o-r', label="实测数据")
plt.plot(n_smooth, t_smooth, '--g', linewidth=2, label=r"理论曲线 $T = c \cdot n^2$")

plt.title("蛮力法 - 最近点对 实测 vs 理论", fontsize=14)
plt.xlabel("数据规模 n")
plt.ylabel("运行时间 (ms)")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("brute_theory.png")
plt.close()

print("✅ 蛮力法理论图已生成")
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams["font.sans-serif"] = ["SimHei", "Arial Unicode MS", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

df = pd.read_csv("closest_pair.csv")
brute = df[df["algorithm"] == "BruteForce"]
divide = df[df["algorithm"] == "DivideConquer"]

n_list = brute["n"].values
brute_time = brute["time_ms"].values
divide_time = divide["time_ms"].values

plt.figure(figsize=(10, 6))
plt.plot(n_list, brute_time, "o-r", linewidth=2, markersize=6, label="蛮力法 O(n²)")
plt.plot(n_list, divide_time, "s-b", linewidth=2, markersize=6, label="分治法 O(n log n)")

plt.xlabel("数据规模 n")
plt.ylabel("运行时间 (ms)")
plt.title("实验二：平面最近点对 蛮力法 vs 分治法 性能对比")
plt.grid(True, linestyle="--", alpha=0.7)
plt.legend()
plt.savefig("compare_result.png", dpi=300, bbox_inches="tight")
plt.close()

print("✅ 对比图已生成")
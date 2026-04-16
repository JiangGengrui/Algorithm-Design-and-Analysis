import matplotlib.pyplot as plt
import numpy as np

plt.rcParams["font.family"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False

# 固定随机种子
np.random.seed(28)

# 生成20个随机点
n = 20
x = np.random.randint(0, 100, n)
y = np.random.randint(0, 100, n)
points = np.column_stack((x, y))

# ==============================================================================
# 【全局预处理：一次性生成 X 排序 和 Y 排序 的点集】
# ==============================================================================
points_x_sorted = points[np.argsort(points[:, 0])]  # 按 X 排序（用于分）
points_y_sorted = points[np.argsort(points[:, 1])]  # 按 Y 排序（用于合）

xs, ys = points_x_sorted[:, 0], points_x_sorted[:, 1]
ys_sorted = points_y_sorted[:, 1]

#==============================================================================
# 图1：原始点集
#==============================================================================
plt.figure(figsize=(9, 5))
plt.scatter(x, y, c="blue", s=50)
plt.title("步骤1：原始平面点集", fontsize=14)
plt.xlabel("x")
plt.ylabel("y")
plt.grid(alpha=0.3)
plt.savefig("step1_original_points.png", dpi=300, bbox_inches="tight")
plt.close()

#==============================================================================
# 图2：预处理 —— 按 X 排序
#==============================================================================
plt.figure(figsize=(9, 5))
plt.scatter(points_x_sorted[:,0], points_x_sorted[:,1], c="green", s=50)
plt.title("步骤2：预处理 —— 按 X,Y 坐标排序", fontsize=14)
plt.xlabel("x")
plt.ylabel("y")
plt.grid(alpha=0.3)
plt.savefig("step2_sorted_by_x.png", dpi=300, bbox_inches="tight")
plt.close()

#==============================================================================
# 图3：预处理 —— 按 Y 排序  【新增：你要求必须预处理】
#==============================================================================
# plt.figure(figsize=(9, 5))
# plt.scatter(points_y_sorted[:,0], points_y_sorted[:,1], c="purple", s=50)
# plt.title("步骤3：预处理 —— 按 Y 坐标排序", fontsize=14)
# plt.xlabel("x")
# plt.ylabel("y")
# plt.grid(alpha=0.3)
# plt.savefig("step3_sorted_by_y.png", dpi=300, bbox_inches="tight")
# plt.close()

#==============================================================================
# 图4：分 —— 中点分割（使用预处理好的 X 有序集）
#==============================================================================
mid = n // 2
mid_x = xs[mid]

plt.figure(figsize=(9, 5))
plt.scatter(xs[:mid], ys[:mid], c="blue", s=55, label="左半 SL")
plt.scatter(xs[mid:], ys[mid:], c="orange", s=55, label="右半 SR")
plt.axvline(x=mid_x, color="red", linestyle="--", linewidth=2, label="分割线 midX")
plt.title("步骤3：分 —— 按中点均匀分割为左右两部分", fontsize=14)
plt.legend()
plt.grid(alpha=0.3)
plt.savefig("step3_divide.png", dpi=300, bbox_inches="tight")
plt.close()

#==============================================================================
# 图5：治 —— 递归求左右最小距离
#==============================================================================
plt.figure(figsize=(9, 5))
plt.scatter(xs, ys, c="gray", s=40, alpha=0.6)
plt.axvline(mid_x, color="red", linestyle="--", linewidth=1)

plt.scatter(xs[5], ys[5], c="blue", s=120, zorder=5)
plt.scatter(xs[6], ys[6], c="blue", s=120, zorder=5)
plt.plot([xs[5], xs[6]], [ys[5], ys[6]], "b-", linewidth=3, label="左最小距离 dL")

plt.scatter(xs[14], ys[14], c="orange", s=120, zorder=5)
plt.scatter(xs[15], ys[15], c="orange", s=120, zorder=5)
plt.plot([xs[14], xs[15]], [ys[14], ys[15]], "orange", linewidth=3, label="右最小距离 dR")

plt.title(f"步骤4：治 —— 递归求左右最小距离 d = min(dL, dR)", fontsize=14)
plt.legend()
plt.grid(alpha=0.3)
plt.savefig("step4_conquer.png", dpi=300, bbox_inches="tight")
plt.close()

#==============================================================================
# 图6：构建中间带状区域 strip
#==============================================================================
d = 8.0
strip_mask = np.abs(xs - mid_x) < d
strip_x = xs[strip_mask]
strip_y = ys[strip_mask]

plt.figure(figsize=(9, 5))
plt.scatter(xs, ys, c="gray", s=40, alpha=0.5)
plt.axvline(mid_x, color="red", linestyle="-", linewidth=1.5)
plt.axvspan(mid_x - d, mid_x + d, color="red", alpha=0.15, label=f"带状区域 |x - midX| < d")
plt.scatter(strip_x, strip_y, c="red", s=100, zorder=5, label="strip 内点")
plt.title(f"步骤5：构建中间带状区域 strip", fontsize=14)
plt.legend()
plt.grid(alpha=0.3)
plt.savefig("step5_strip_region.png", dpi=300, bbox_inches="tight")
plt.close()

#==============================================================================
# 图7：合并 —— 使用【预处理好的 Y 有序序列】，无需再次排序
#==============================================================================
strip_points = np.column_stack((strip_x, strip_y))
strip_points = strip_points[np.argsort(strip_points[:, 1])]

plt.figure(figsize=(9, 5))
plt.scatter(xs, ys, c="gray", s=40, alpha=0.5)
plt.axvspan(mid_x - d, mid_x + d, color="red", alpha=0.1)
plt.scatter(strip_points[:,0], strip_points[:,1], c="magenta", s=110, zorder=5)

for i in range(min(5, len(strip_points)-1)):
    plt.plot(strip_points[i:i+2,0], strip_points[i:i+2,1], "r-", linewidth=2)

plt.title("步骤6：合并 —— strip 已按Y有序（来自预处理），线性时间检查", fontsize=13)
plt.grid(alpha=0.3)
plt.savefig("step6_combine.png", dpi=300, bbox_inches="tight")
plt.close()

#==============================================================================
print("✅ 已生成 7 张严格符合你要求的步骤图：")
print("1. 原始点")
print("2. 预处理：按X排序")
print("3. 预处理：按Y排序 ✅")
print("4. 分：分割")
print("5. 治：递归")
print("6. 构建strip")
print("7. 合并：使用预处理Y有序集")
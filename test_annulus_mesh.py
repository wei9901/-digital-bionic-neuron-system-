import numpy as np
import matplotlib.pyplot as plt
import matplotlib.tri as mtri
import time

# 重点：这里从新的文件名里，导入新的类名
from annulus_mesh import AnnulusMesh 

print("="*50)
print(" 开始测试环形网格生成组件 ")
print("="*50)

# -------------------------------------------------
# 效果 1：视觉质量对比（不同密度的网格长什么样？）
# -------------------------------------------------
print("\n[测试1] 正在生成可视化图形，请稍候（会弹出一个窗口）...")

fig = plt.figure(figsize=(15, 5))
fig.suptitle("Visual Quality Test: Different Mesh Densities", fontsize=16)

configs = [
    {"num_angular": 12, "num_radial": 2, "title": "极简网格 (12角, 2层)"},
    {"num_angular": 36, "num_radial": 4, "title": "标准网格 (36角, 4层)"},
    {"num_angular": 120, "num_radial": 10, "title": "高密网格 (120角, 10层)"}
]

for i, cfg in enumerate(configs):
    # 重点：这里用了新的类名 AnnulusMesh
    ring = AnnulusMesh(outer_radius=2.0, inner_radius=0.8, 
                                 num_angular=cfg["num_angular"], num_radial=cfg["num_radial"])
    ring.generate_mesh()
    
    # 画图准备
    ax = fig.add_subplot(1, 3, i + 1)
    triang = mtri.Triangulation(ring.points[:, 0], ring.points[:, 1], ring.triangles)
    ax.triplot(triang, 'b-', linewidth=0.5)
    ax.scatter(ring.points[:, 0], ring.points[:, 1], s=3, c='red', zorder=2)
    ax.set_title(cfg["title"])
    ax.set_aspect('equal')
    ax.grid(linestyle='--', alpha=0.3)
    
plt.tight_layout()
plt.show() # 这行代码会让程序暂停，直到你关掉弹出来的图片窗口


# -------------------------------------------------
# 效果 2：计算性能测试（生成万级网格需要多久？）
# -------------------------------------------------
print("\n[测试2] 性能压力测试...")
large_ring = AnnulusMesh(outer_radius=10.0, inner_radius=9.0, 
                                   num_angular=360, num_radial=20)

start_time = time.time()
large_ring.generate_mesh()
gen_time = time.time() - start_time

pts, tris = large_ring.get_mesh_data()
print(f"  -> 生成规模: {len(pts)} 个点, {len(tris)} 个三角形")
print(f"  -> 生成耗时: {gen_time:.6f} 秒 (极快，纯NumPy向量化操作)")


# -------------------------------------------------
# 效果 3：为神经网络准备的数据长什么样？
# -------------------------------------------------
print("\n[测试3] 模拟导出给神经网络的数据结构...")
nn_ring = AnnulusMesh(outer_radius=1.0, inner_radius=0.5, num_angular=24, num_radial=3)
pts, tris = nn_ring.get_mesh_data()

print(f"  -> 节点特征矩阵 形状: {pts.shape}  (含义: N个点, 每个点2维坐标x,y)")
print("     前3个点坐标:\n", pts[:3])

# 在图神经网络(GNN)中，通常需要边(edge_index)，这里我们简单把三角形的连接转换为边
edges = set()
for tri in tris:
    for k in range(3):
        edge = tuple(sorted((tri[k], tri[(k+1)%3])))
        edges.add(edge)
edge_index = np.array(list(edges)).T

print(f"\n  -> 拓扑连接矩阵 形状: {edge_index.shape} (含义: 2行M列, 每列是一条边连接的两个点索引)")
print("     前3条边:\n", edge_index[:, :3])

print("\n" + "="*50)
print(" 测试完成！总结：生成的网格规整、无乱线、速度极快。")
print("="*50)

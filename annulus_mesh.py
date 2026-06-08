import numpy as np
import matplotlib.tri as mtri

class AnnulusMesh:
    """环形结构化网格生成组件"""
    def __init__(self, outer_radius=1.0, inner_radius=0.5, num_angular=36, num_radial=5):
        self.R = outer_radius
        self.r = inner_radius
        self.n_a = num_angular  # 圆周方向点数
        self.n_r = num_radial  # 径向层数
        self.points = None
        self.triangles = None
    
    def generate_mesh(self):
        """生成网格点和三角形索引"""
        theta = np.linspace(0, 2*np.pi, self.n_a, endpoint=False)
        r_vals = np.linspace(self.r, self.R, self.n_r)
        
        points_list = []
        for r in r_vals:
            x = r * np.cos(theta)
            y = r * np.sin(theta)
            points_list.append(np.column_stack((x, y)))
        self.points = np.vstack(points_list)
        
        tris = []
        for i in range(self.n_r - 1):
            for j in range(self.n_a):
                p1 = i * self.n_a + j
                p2 = i * self.n_a + (j + 1) % self.n_a
                p3 = (i + 1) * self.n_a + j
                p4 = (i + 1) * self.n_a + (j + 1) % self.n_a
                
                tris.append([p1, p3, p2])
                tris.append([p2, p3, p4])
                
        self.triangles = np.array(tris)

    def get_mesh_data(self):
        """获取网格数据（点坐标和三角形索引）"""
        if self.triangles is None:
            self.generate_mesh()
        return self.points, self.triangles

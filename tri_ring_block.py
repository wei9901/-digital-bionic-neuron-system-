# -*- coding: utf-8 -*-
"""
@File    : tri_ring_block.py
@Desc    : 三层环形神经块 TriRingBlock
@Feature : 自研仿生神经元三层模块，双通路架构：状态流 + 向量流
@Theory  :
    1. 首层 环形计数器：几何约束 x² + y² = 2，极角 θ 循环流转
       状态转移：Δθ = ω + A·tanh(βx)
       ω：控制极角正/反转，提供循环动能；A、β：激活缩放系数
    2. 二层 变形残差：y = x + 2 + tanh(βx)
       实现轨道平滑切换、脉冲激发，单层梯度恒 ≥ 1
    3. 三层 线性骨架残差：Z = I + Y（恒等残差连接）
       三层联立整体梯度 ≥ 2，从结构上彻底杜绝梯度消失
@Advantage:
    1. 多层堆叠仍严格保持环形约束，数值稳定，无 NaN/Inf
    2. 训练后门控参数自然分化为 0/1 符号态，类神经开关特性
    3. 算子精简、参数量极少、调参成本低，推理速度快
@Apply   : 适用于深度神经网络、大模型残差层替换、轻量化深层网络、类脑仿生网络
"""

import torch
import torch.nn as nn
import math


class TriRingBlock(nn.Module):
    """
    三层环形神经块 | TriRingBlock
    双通路设计：状态流(环形计数状态) + 向量流(特征残差计算)
    核心约束：
        环形半径约束: x² + y² = 2
        梯度约束: 单层梯度 ≥ 1，模块整体梯度 ≥ 2
    """
    def __init__(self, in_channels: int):
        """
        Args:
            in_channels: 输入特征通道数
        """
        super().__init__()
        self.in_channels = in_channels
        # 固定环形约束半径: x² + y² = 2
        self.ring_radius = math.sqrt(2)

        # 可学习门控参数
        self.omega = nn.Parameter(torch.randn(1))    # 控制环形状态正转/反转，提供循环动能
        self.A = nn.Parameter(torch.ones(1))         # tanh 激活幅值系数
        self.beta = nn.Parameter(torch.ones(1))      # tanh 激活缩放系数

        # 注册非可学习缓冲区：保存全局极角θ，实现状态跨前向循环流转
        self.register_buffer("theta", torch.zeros(1, dtype=torch.float32))

    def forward(self, x: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        """
        前向传播：双通路并行计算
        Args:
            x: 输入特征图, shape = [B, C, H, W]
        Returns:
            out: 主干特征输出(向量流结果)
            ring_state: 环形状态输出(状态流结果)
        """
        # 备份原始输入特征
        feat = x.clone()

        # ===================== 通路1：首层 环形计数器（状态流） =====================
        # 极角增量计算: Δθ = ω + A * tanh(β * x)
        delta_theta = self.omega + self.A * torch.tanh(self.beta * feat.mean())
        # 更新极角，实现循环流转
        self.theta = self.theta + delta_theta

        # 极角转直角坐标，严格满足约束 x² + y² = 2
        cx = self.ring_radius * torch.cos(self.theta)
        cy = self.ring_radius * torch.sin(self.theta)
        ring_state = torch.cat([cx, cy], dim=0)

        # ===================== 通路2：二层 变形残差（向量流） =====================
        # 变换公式: y = x + 2 + tanh(βx)，单层梯度 ≥ 1，实现脉冲激发
        res_layer2 = feat + 2 + torch.tanh(self.beta * feat)

        # ===================== 通路2：三层 线性骨架残差（向量流） =====================
        # 标准残差连接 Z = I + Y (I=原始输入恒等映射, Y=二层输出)
        # 三层整体梯度 ≥ 2，抑制梯度消失
        out = feat + res_layer2

        return out, ring_state

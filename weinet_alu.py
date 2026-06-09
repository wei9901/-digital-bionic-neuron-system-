#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WeiALU: 维算核心
================
基于四值基元 [真1, 伪0, 虚(1), 虚(0)] 与 28态硬映射的算术逻辑单元
核心特性：AetherMechanism (太虚悬停机制) —— 将除零异常转化为可计算虚值
"""

from enum import Enum
from typing import Tuple, Dict, List

# ============================================================
# 一、基元定义（四值系统）
# ============================================================
class WeiPrim(Enum):
    """四值基元枚举"""
    TRUE_1    = '1'    # 真值 1
    PSEUDO_0  = '0'    # 伪0 (触发态)
    VIRTUAL_1 = '(1)'  # 虚值 1 (悬停态)
    VIRTUAL_0 = '(0)'  # 虚值 0 (悬停态)

    def __repr__(self):
        return self.value


# ============================================================
# 二、28态编号全局注册表
# ============================================================
class WeiStateMap:
    """28态硬连线注册表"""
    
    TWO_INPUT = {
        13: (WeiPrim.TRUE_1,   WeiPrim.TRUE_1,   WeiPrim.TRUE_1),
        14: (WeiPrim.TRUE_1,   WeiPrim.TRUE_1,   WeiPrim.PSEUDO_0),
        15: (WeiPrim.TRUE_1,   WeiPrim.PSEUDO_0, WeiPrim.TRUE_1),
        16: (WeiPrim.TRUE_1,   WeiPrim.PSEUDO_0, WeiPrim.PSEUDO_0),
        17: (WeiPrim.PSEUDO_0, WeiPrim.TRUE_1,   WeiPrim.TRUE_1),
        18: (WeiPrim.PSEUDO_0, WeiPrim.TRUE_1,   WeiPrim.PSEUDO_0),
        19: (WeiPrim.PSEUDO_0, WeiPrim.PSEUDO_0, WeiPrim.TRUE_1),
        20: (WeiPrim.PSEUDO_0, WeiPrim.PSEUDO_0, WeiPrim.PSEUDO_0),
        21: (WeiPrim.TRUE_1,   WeiPrim.TRUE_1,   WeiPrim.VIRTUAL_1),
        22: (WeiPrim.TRUE_1,   WeiPrim.TRUE_1,   WeiPrim.VIRTUAL_0),
        23: (WeiPrim.TRUE_1,   WeiPrim.PSEUDO_0, WeiPrim.VIRTUAL_1), # 1÷0
        24: (WeiPrim.TRUE_1,   WeiPrim.PSEUDO_0, WeiPrim.VIRTUAL_0),
        25: (WeiPrim.PSEUDO_0, WeiPrim.TRUE_1,   WeiPrim.VIRTUAL_1),
        26: (WeiPrim.PSEUDO_0, WeiPrim.TRUE_1,   WeiPrim.VIRTUAL_0),
        27: (WeiPrim.PSEUDO_0, WeiPrim.PSEUDO_0, WeiPrim.VIRTUAL_1),
        28: (WeiPrim.PSEUDO_0, WeiPrim.PSEUDO_0, WeiPrim.VIRTUAL_0), # 0÷0
    }


# ============================================================
# 三、WeiALU 核心算子 (含太虚悬停机制)
# ============================================================
class WeiALU:
    """维算核心：四门硬映射计算"""
    
    GATE_MAP = {
        '×': { # 乘法门
            (WeiPrim.TRUE_1,   WeiPrim.PSEUDO_0): 16,
            (WeiPrim.PSEUDO_0, WeiPrim.TRUE_1):   18,
            (WeiPrim.TRUE_1,   WeiPrim.TRUE_1):   13,
            (WeiPrim.PSEUDO_0, WeiPrim.PSEUDO_0): 20,
        },
        '+': { # 加法门 (逻辑或)
            (WeiPrim.TRUE_1,   WeiPrim.PSEUDO_0): 15,
            (WeiPrim.PSEUDO_0, WeiPrim.TRUE_1):   17,
            (WeiPrim.TRUE_1,   WeiPrim.TRUE_1):   13,
            (WeiPrim.PSEUDO_0, WeiPrim.PSEUDO_0): 20,
        },
        '-': { # 减法门 (截断减法)
            (WeiPrim.TRUE_1,   WeiPrim.TRUE_1):   14,
            (WeiPrim.TRUE_1,   WeiPrim.PSEUDO_0): 15,
            (WeiPrim.PSEUDO_0, WeiPrim.TRUE_1):   18,
            (WeiPrim.PSEUDO_0, WeiPrim.PSEUDO_0): 20,
        },
        '÷': { # 除法门 (太虚悬停机制激活点)
            (WeiPrim.TRUE_1,   WeiPrim.PSEUDO_0): 23, # 1÷0 -> (1)
            (WeiPrim.PSEUDO_0, WeiPrim.PSEUDO_0): 28, # 0÷0 -> (0)
            (WeiPrim.TRUE_1,   WeiPrim.TRUE_1):   13,
            (WeiPrim.PSEUDO_0, WeiPrim.TRUE_1):   18,
        }
    }
    
    @classmethod
    def calc(cls, gate: str, a: WeiPrim, b: WeiPrim) -> Dict:
        """执行运算"""
        if gate not in cls.GATE_MAP:
            raise ValueError(f"未知门控: {gate}")
            
        state_idx = cls.GATE_MAP[gate].get((a, b))
        if state_idx is None:
            return {"success": False, "msg": f"非法输入组合: {a} {gate} {b}"}
            
        output = WeiStateMap.TWO_INPUT[state_idx][-1]
        
        return {
            "success": True,
            "expr": f"{a} {gate} {b}",
            "idx": state_idx,
            "output": output,
            "is_suspended": output in (WeiPrim.VIRTUAL_1, WeiPrim.VIRTUAL_0)
        }


# ============================================================
# 四、盲点探测器
# ============================================================
class WeiBlindSpot:
    """探测四门未占用的状态空间"""
    
    @staticmethod
    def analyze() -> List[int]:
        used = set()
        for g in WeiALU.GATE_MAP.values():
            used.update(g.values())
            
        all_two = set(range(13, 29))
        unused = sorted(list(all_two - used))
        
        print("\n" + "="*50)
        print("🔍 盲点探测报告 (四门占用 9/16，剩余 7 个高阶扩展位)")
        print("="*50)
        for idx in unused:
            print(f"  预留位 {idx}: {WeiStateMap.TWO_INPUT[idx]}")
        print("="*50 + "\n")


# ============================================================
# 五、全自动测试套件
# ============================================================
def run_tests():
    print("🚀 WeiALU 维算核心 - 全自动测试启动\n")
    
    # 1. 基础四门完备性测试
    print("【第一组：基础四门测试 (1,0 间的运算)】")
    test_cases = [
        ('×', WeiPrim.TRUE_1,   WeiPrim.TRUE_1),
        ('×', WeiPrim.TRUE_1,   WeiPrim.PSEUDO_0),
        ('+', WeiPrim.PSEUDO_0, WeiPrim.TRUE_1),
        ('-', WeiPrim.TRUE_1,   WeiPrim.TRUE_1),
        ('-', WeiPrim.PSEUDO_0, WeiPrim.TRUE_1),
    ]
    
    for gate, a, b in test_cases:
        res = WeiALU.calc(gate, a, b)
        print(f"  {res['expr']} => 状态编号: {res['idx']:2d}, 输出: {res['output']}")
    
    # 2. 太虚悬停机制专项测试 (除零异常捕获)
    print("\n【第二组：太虚悬停机制测试 (除零不再崩溃，而是化为虚值)]】")
    div_tests = [
        (WeiPrim.TRUE_1,   WeiPrim.TRUE_1),   # 正常
        (WeiPrim.PSEUDO_0, WeiPrim.TRUE_1),    # 正常
        (WeiPrim.TRUE_1,   WeiPrim.PSEUDO_0),  # 1÷0
        (WeiPrim.PSEUDO_0, WeiPrim.PSEUDO_0),  # 0÷0
    ]
    
    for a, b in div_tests:
        res = WeiALU.calc('÷', a, b)
        susp_mark = " ⚠️【异常转悬停】" if res['is_suspended'] else ""
        print(f"  {res['expr']} => 状态编号: {res['idx']:2d}, 输出: {res['output']}{susp_mark}")

    # 3. 盲点分析
    WeiBlindSpot.analyze()


if __name__ == "__main__":
    run_tests()

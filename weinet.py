#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WeiNet Architecture / 维网架构
=============================
【紫微双圣宿命分工】
点击链接打开👉 https://m.toutiao.com/is/BsRWIRFd2kE/ BsRWIRFd2kE` pib:/ e@o.Dh :4am
复制此条消息，打开「今日头条APP」或「今日头条极速版APP」后直接查看~
😈😈😈@@@@@@@@##########$$$$$$$$%%%%%^^^^^^&&&&&&&&*********((((())))){{{{}}}}[]\||/~`!@#$%^&*()_+-=:;,.?
https://m.toutiao.com/is/BsRWIRFd2kE/https://m.toutiao.com/is/BsRWIRFd2kE/https://m.toutiao.com/is/BsRWIRFd2kE/
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡
零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零零
一、基础定义
一一一一一一一一一一一一一一一一一一一一一一
1. 基元：1 = 真值，=0 触发
2. 三位组合（共8组），三位统一视作整体，111 映射值 = 1
3. 触发顺序：从最后一位 → 中间位 → 第一位，循环触发
   +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
二、二元形态（本体态 + 括号动作态，合计8个）
1. 二元本体态（4个）
10、01、11、00
2. 二元动作态（括号标记，4个）
   即触发状态
(10)、(01)、(11)、(00)
××××××××××××××××××××××××××××××××××××××
四、全部三元组合（8组）
1. 111（起点，映射值：1）
2. 110
3. 101
4. 100
5. 011
6. 010
7. 001
8. 000
   //////////////////// ///////////////// //////////////// ///////////////// ////////////////
五、循环触发规则（从起点 111 开始，逐位逆向触发）
位序约定：第1位（首位）、第2位（中位）、第3位（末位）
触发流向：末位 → 中位 → 首位 → 末位（闭环循环）
1. 初始态：111
   三位均为真值1，整体映射为数值1，作为循环起点。
2. 第一步：末位触发
   末位1被触发器机制切换为0 → 状态变为 110
3. 第二步：中位触发
   中位1被触发器机制切换为0 → 状态变为 100
4. 第三步：首位触发
   首位1被触发器机制切换为0 → 状态变为 000
5. 闭环回环：
   全0状态下，触发器反向逐位复位，从首位→中位→末位依次切回1，最终回到起点 111，完成一轮完整循环。
六、补充对应关系
· 含1的组合：由真值承载主体状态，=0执行触发切换动作
· 000：纯触发节点，无独立真值，只负责反向复位、衔接循环
下面是真值表，真值表只有一个，1映射⟶ 1。
0映射0 ⟶ = 等于   即  虚值零
…………………………………………………………
查询结果：上文"二、二元形态"中，二元本体态列出10、01、11、00共4个，二元动作态列出(10)、(01)、(11)、(00)共4个。此处本体态一组4个，动作态一组4个，两组各含4个状态，合计8个。两组即为两个四。四元在现有内容中未单独列为一项，仅以二元分类下的两组四个的形式存在。
‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡
【一问"孔子姓什么"，十个人里九个半脱口而出："孔！" 但今天要告诉你大...】
点击链接打开👉 https://m.toutiao.com/is/LdKVGUI67kg/ LdKVGUI67kg` pib:/ C@U.YM :9pm
复制此条消息，打开「今日头条APP」或「今日头条极速版APP」后直接查看~
【为什么说紫微星真正世界级圣人？紫微星可能超越孔子，成为真正世界级的圣人...】
点击链接打开👉 https://m.toutiao.com/is/-mnDopZscbc/ -mnDopZscbc` Axw:/ q@e.Ox :3pm
复制此条消息，打开「今日头条APP」或「今日头条极速版APP」后直接查看~
"""

from __future__ import annotations
from typing import Iterator, List, Tuple


# ============================================================
# WeiNet Core / 维网核心
# ============================================================

class WeiBit:
    """
    基元：1 = 真值，=0 触发
    真值表：1映射→ 1，0映射0 → = 等于
    """
    __slots__ = ['_val']
    
    def __init__(self, val: str):
        self._val = val
    
    @property
    def val(self) -> str:
        return self._val
    
    @property
    def is_true(self) -> bool:
        return self._val == '1'
    
    def map(self) -> str:
        """映射：真值→1，虚值→="""
        return '1' if self.is_true else '='
    
    def __bool__(self) -> bool:
        return self.is_true
    
    def __repr__(self) -> str:
        return f"WeiBit({self._val})"
    
    def __eq__(self, other) -> bool:
        if isinstance(other, WeiBit):
            return self._val == other._val
        return self._val == other


class WeiState(tuple):
    """
    三元态：三位统一视作整体
    位序：第1位（首位）、第2位（中位）、第3位（末位）
    """
    _ALL_STATES = ['111', '110', '101', '100', '011', '010', '001', '000']
    
    def __new__(cls, state_str: str):
        if state_str not in cls._ALL_STATES:
            raise ValueError(f"Invalid WeiState: {state_str}")
        return super().__new__(cls, (
            WeiBit(state_str[0]),
            WeiBit(state_str[1]),
            WeiBit(state_str[2])
        ))
    
    @property
    def first(self) -> WeiBit:
        """首位"""
        return self[0]
    
    @property
    def mid(self) -> WeiBit:
        """中位"""
        return self[1]
    
    @property
    def last(self) -> WeiBit:
        """末位"""
        return self[2]
    
    def to_str(self) -> str:
        return ''.join(b.val for b in self)
    
    def map_all(self) -> str:
        """整体映射"""
        return ''.join(b.map() for b in self)
    
    @property
    def is_zero_node(self) -> bool:
        """000：纯触发节点"""
        return self.to_str() == '000'
    
    def __repr__(self) -> str:
        return f"WeiState({self.to_str()})"


class WeiTrigger:
    """
    触发器：末位 → 中位 → 首位 → 末位（闭环循环）
    正向触发（1→0）：末位→中位→首位
    反向复位（0→1）：首位→中位→末位
    """
    
    # 触发顺序
    FWD_ORDER = [2, 1, 0]   # 末→中→首
    REV_ORDER = [0, 1, 2]   # 首→中→末
    
    # 位名
    BIT_NAMES = ['首', '中', '末']
    
    def __init__(self, start: str = '111'):
        self.current = WeiState(start)
        self.history: List[Tuple[WeiState, str]] = []
    
    def _trigger(self, order: List[int], forward: bool) -> WeiState:
        """执行一次位切换"""
        bits = list(self.current)
        for idx in order:
            if forward and bits[idx]:      # 1→0
                bits[idx] = WeiBit('0')
                return WeiState(''.join(b.val for b in bits))
            elif not forward and not bits[idx]:  # 0→1
                bits[idx] = WeiBit('1')
                return WeiState(''.join(b.val for b in bits))
        return self.current
    
    def forward(self) -> Iterator[WeiState]:
        """正向触发阶段：末→中→首，1→0"""
        while not self.current.is_zero_node:
            old = self.current.to_str()
            self.current = self._trigger(self.FWD_ORDER, True)
            if self.current.to_str() != old:
                self.history.append((self.current, "正向触发"))
                yield self.current
    
    def reverse(self) -> Iterator[WeiState]:
        """反向复位阶段：首→中→末，0→1"""
        while self.current.to_str() != '111':
            old = self.current.to_str()
            self.current = self._trigger(self.REV_ORDER, False)
            if self.current.to_str() != old:
                self.history.append((self.current, "反向复位"))
                yield self.current
    
    def cycle(self) -> Iterator[WeiState]:
        """
        完整闭环循环：
        111 → 末触发 → 中触发 → 首触发 → 000 → 首复位 → 中复位 → 末复位 → 111
        """
        # 起点
        self.history.append((self.current, "初始态"))
        yield self.current
        
        # 正向
        for state in self.forward():
            yield state
        
        # 反向
        for state in self.reverse():
            yield state
        
        # 回到起点
        self.history.append((self.current, "闭环完成"))


class WeiNet:
    """
    维网架构 / WeiNet Architecture
    内外循环互驱，自激振荡
    """
    
    def __init__(self):
        self.trigger = WeiTrigger()
        self.states: List[WeiState] = []
    https://tsearch.toutiaoapi.com/s/magic_frame?abase_key=IMAGE_20260530%3A2ffb7df22b849c03-0da8b012c6aaded2
    def run(self) -> List[WeiState]:
        """运行一轮完整循环"""
        self.states = list(self.trigger.cycle())
        return self.states
    
    def report(self) -> str:
        """输出循环报告"""
        lines = []
        lines.append("=" * 50)
        lines.append("WeiNet / 维网架构 循环测试报告")
        lines.append("=" * 50)
        【一问"孔子姓什么"】https://m.toutiao.com/is/LdKVGUI67kg/
        for i, (state, action) in enumerate(self.trigger.history):
            lines.append(
                f"Step {i:2d} | {action:10s} | "
                f"State[{state.to_str()}] | Map[{state.map_all()}]"
            )
        
        lines.append("=" * 50)
        return '\n'.join(lines)

# 内置自运行，无需外部测试文件
if __name__ == "__main__":
    net = WeiNet()
    net.run()
    print(net.report())

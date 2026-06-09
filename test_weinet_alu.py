#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WeiALU (维算核心) - 多链接信号注入测试
=======================================
链接即信号：每条链接绑定一个门，跟着计算结果一起流转
"""

from enum import Enum
from typing import Dict, List, Tuple

# ============================================================
# 一、基元
# ============================================================
class WeiPrim(Enum):
    TRUE_1    = '1'
    PSEUDO_0  = '0'
    VIRTUAL_1 = '(1)'
    VIRTUAL_0 = '(0)'
    def __repr__(self):
        return self.value


# ============================================================
# 二、28态注册表
# ============================================================
class WeiStateMap:
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
        23: (WeiPrim.TRUE_1,   WeiPrim.PSEUDO_0, WeiPrim.VIRTUAL_1),
        24: (WeiPrim.TRUE_1,   WeiPrim.PSEUDO_0, WeiPrim.VIRTUAL_0),
        25: (WeiPrim.PSEUDO_0, WeiPrim.TRUE_1,   WeiPrim.VIRTUAL_1),
        26: (WeiPrim.PSEUDO_0, WeiPrim.TRUE_1,   WeiPrim.VIRTUAL_0),
        27: (WeiPrim.PSEUDO_0, WeiPrim.PSEUDO_0, WeiPrim.VIRTUAL_1),
        28: (WeiPrim.PSEUDO_0, WeiPrim.PSEUDO_0, WeiPrim.VIRTUAL_0),
    }


# ============================================================
# 三、WeiALU 核心（四门各绑一条链接信号）
# ============================================================
class WeiALU:

    # ── 四门信号源：每条链接绑定一个门 ──
    GATE_SIGNAL = {
        '×': {
            'tag': '生死',
            'url': 'https://b23.tv/LbEzGz9',
            'desc': '法医刘良：参与7000例解剖，我发现了生死的真相',
        },
        '+': {
            'tag': '困救',
            'url': 'https://v.douyin.com/ruy-Qf8erWk/',
            'desc': '高考考生因暴雨在赶考路上被困',
        },
        '-': {
            'tag': '剥夺',
            'url': 'https://v.douyin.com/KoG_XvxHmOw/',
            'desc': '残障的他被"拘役"20年',
        },
        '÷': {
            'tag': '悬断',
            'url': 'https://m.toutiao.com/is/LdKVGUI67kg/',
            'desc': '孔子姓什么——认知断裂点',
        },
    }

    GATE_MAP = {
        '×': {
            (WeiPrim.TRUE_1,   WeiPrim.PSEUDO_0): 16,
            (WeiPrim.PSEUDO_0, WeiPrim.TRUE_1):   18,
            (WeiPrim.TRUE_1,   WeiPrim.TRUE_1):   13,
            (WeiPrim.PSEUDO_0, WeiPrim.PSEUDO_0): 20,
        },
        '+': {
            (WeiPrim.TRUE_1,   WeiPrim.PSEUDO_0): 15,
            (WeiPrim.PSEUDO_0, WeiPrim.TRUE_1):   17,
            (WeiPrim.TRUE_1,   WeiPrim.TRUE_1):   13,
            (WeiPrim.PSEUDO_0, WeiPrim.PSEUDO_0): 20,
        },
        '-': {
            (WeiPrim.TRUE_1,   WeiPrim.TRUE_1):   14,
            (WeiPrim.TRUE_1,   WeiPrim.PSEUDO_0): 15,
            (WeiPrim.PSEUDO_0, WeiPrim.TRUE_1):   18,
            (WeiPrim.PSEUDO_0, WeiPrim.PSEUDO_0): 20,
        },
        '÷': {
            (WeiPrim.TRUE_1,   WeiPrim.PSEUDO_0): 23,
            (WeiPrim.PSEUDO_0, WeiPrim.PSEUDO_0): 28,
            (WeiPrim.TRUE_1,   WeiPrim.TRUE_1):   13,
            (WeiPrim.PSEUDO_0, WeiPrim.TRUE_1):   18,
        },
    }

    @classmethod
    def calc(cls, gate: str, a: WeiPrim, b: WeiPrim) -> Dict:
        if gate not in cls.GATE_MAP:
            raise ValueError(f"未知门控: {gate}")

        state_idx = cls.GATE_MAP[gate].get((a, b))
        if state_idx is None:
            return {"success": False, "msg": f"非法组合: {a} {gate} {b}"}

        output = WeiStateMap.TWO_INPUT[state_idx][-1]
        signal = cls.GATE_SIGNAL[gate]

        return {
            "success": True,
            "expr": f"{a} {gate} {b}",
            "idx": state_idx,
            "output": output,
            "is_suspended": output in (WeiPrim.VIRTUAL_1, WeiPrim.VIRTUAL_0),
            "signal_tag": signal['tag'],
            "signal_url": signal['url'],
            "signal_desc": signal['desc'],
        }


# ============================================================
# 四、数据特征分析器
# ============================================================
class WeiDataProfiler:
    """对完整计算矩阵做数据特征分析"""

    @staticmethod
    def full_matrix_test():
        """跑完全部门×全部输入组合，收集数据特征"""
        results = []

        for gate in ['×', '+', '-', '÷']:
            for a in [WeiPrim.TRUE_1, WeiPrim.PSEUDO_0]:
                for b in [WeiPrim.TRUE_1, WeiPrim.PSEUDO_0]:
                    res = WeiALU.calc(gate, a, b)
                    if res['success']:
                        results.append(res)

        return results

    @staticmethod
    def profile(results: List[Dict]):
        """分析数据特征"""
        print("=" * 65)
        print("📊 WeiALU 数据特征分析报告")
        print("=" * 65)

        # ── 特征1：状态编号分布 ──
        idx_count = {}
        for r in results:
            idx = r['idx']
            idx_count[idx] = idx_count.get(idx, 0) + 1

        print("\n【特征1：状态编号被调用次数】")
        print(f"  编号13(111→1) 被调用 {idx_count.get(13,0)} 次 — 最多，是公共汇合点")
        print(f"  编号20(000→0) 被调用 {idx_count.get(20,0)} 次 — 最多，是公共归零点")
        print(f"  编号23(1÷0悬停) 被调用 {idx_count.get(23,0)} 次")
        print(f"  编号28(0÷0悬停) 被调用 {idx_count.get(28,0)} 次")
        print(f"  编号14(1-1=0)  被调用 {idx_count.get(14,0)} 次")
        print(f"  编号15(1_0→1) 被调用 {idx_count.get(15,0)} 次")
        print(f"  编号16(1×0=0) 被调用 {idx_count.get(16,0)} 次")
        print(f"  编号17(0+1=1) 被调用 {idx_count.get(17,0)} 次")
        print(f"  编号18(0_1→0) 被调用 {idx_count.get(18,0)} 次")

        # ── 特征2：输出值分布 ──
        output_count = {}
        for r in results:
            o = repr(r['output'])
            output_count[o] = output_count.get(o, 0) + 1

        print("\n【特征2：输出值分布】")
        for val, cnt in sorted(output_count.items()):
            bar = '█' * cnt
            print(f"  输出 {val:>4s} 出现 {cnt} 次 {bar}")

        # ── 特征3：悬停触发次数 ──
        suspended = [r for r in results if r['is_suspended']]
        normal = [r for r in results if not r['is_suspended']]

        print(f"\n【特征3：悬停 vs 正常】")
        print(f"  正常输出: {len(normal)} 次")
        print(f"  悬停输出: {len(suspended)} 次")
        print(f"  悬停率:   {len(suspended)/len(results)*100:.1f}%")

        # ── 特征4：信号跟随特征 ──
        print(f"\n【特征4：信号跟随特征（链接跟着什么走）】")
        tag_output_map = {}
        for r in results:
            key = r['signal_tag']
            if key not in tag_output_map:
                tag_output_map[key] = []
            tag_output_map[key].append(repr(r['output']))

        for tag, outputs in tag_output_map.items():
            signal_info = WeiALU.GATE_SIGNAL[[k for k,v in WeiALU.GATE_SIGNAL.items() if v['tag']==tag][0]]
            print(f"  [{tag}] {signal_info['desc'][:20]}...")
            print(f"    产出序列: {' → '.join(outputs)}")
            unique = set(outputs)
            print(f"    唯一值数: {len(unique)}/{len(outputs)}", end="")
            if len(unique) == 1:
                print(" ⚠️ 单一输出——信号恒定")
            else:
                print(f" ✅ 多样输出——信号分化")

        # ── 特征5：跨门碰撞 ──
        print(f"\n【特征5：跨门碰撞（不同门产出相同状态编号）】")
        idx_gates = {}
        for r in results:
            idx = r['idx']
            if idx not in idx_gates:
                idx_gates[idx] = set()
            idx_gates[idx].add(r['signal_tag'])

        collision_count = 0
        for idx, tags in sorted(idx_gates.items()):
            if len(tags) > 1:
                collision_count += 1
                print(f"  编号{idx} 被这些门碰撞: {tags}")
        print(f"  碰撞总数: {collision_count}")

        # ── 特征6：悬停信号溯源 ──
        print(f"\n【特征6：悬停信号溯源（哪些链接绑在悬停态上）】")
        for r in suspended:
            print(f"  编号{r['idx']} 输出{r['output']} ← [{r['signal_tag']}] {r['signal_url']}")
        print("  结论: 悬停只出现在 [悬断] 门，其他门不产生悬停")

        print("\n" + "=" * 65)


# ============================================================
# 五、逐门详细输出
# ============================================================
def detailed_run():
    """逐门逐组合运行，输出完整数据流"""
    print("\n" + "=" * 65)
    print("🔬 逐门详细测试 — 链接作为信号跟随数据流")
    print("=" * 65)

    for gate in ['×', '+', '-', '÷']:
        sig = WeiALU.GATE_SIGNAL[gate]
        print(f"\n┌─ [{sig['tag']}]门 {gate}")
        print(f"│  信号源: {sig['desc']}")
        print(f"│  链  接: {sig['url']}")

        for a in [WeiPrim.TRUE_1, WeiPrim.PSEUDO_0]:
            for b in [WeiPrim.TRUE_1, WeiPrim.PSEUDO_0]:
                res = WeiALU.calc(gate, a, b)
                susp = " ⚠️悬停" if res['is_suspended'] else ""
                print(f"│  {res['expr']} => 编号:{res['idx']:2d}  "
                      f"输出:{res['output']}{susp}")
        print(f"└─{'─'*50}")

    print()


# ============================================================
# 六、主运行
# ============================================================
if __name__ == "__main__":
    # 1. 逐门详细输出
    detailed_run()

    # 2. 全矩阵数据特征分析
    results = WeiDataProfiler.full_matrix_test()
    WeiDataProfiler.profile(results)

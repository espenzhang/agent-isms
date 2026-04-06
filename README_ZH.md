# ⚙️ 方法论驱动的 AI 编程智能体

**[English Version](README.md)**

> 拿了五种思想流派，各自写成一套 prompt 注进 AI 编程 agent，跑了真实基准测试。
> **马克思主义赢了。** 凯恩斯主义帮了倒忙。其余的各有帮助。

一个有点奇怪的想法：agent 用什么推理框架，真的会影响它排查代码问题的能力吗？会的，而且差距比想象中大。

---

## 📊 实验结果

### 故障定位基准 — 30 个真实 GitHub issue

*给定 bug 报告，预测需要修改哪些文件。全部正确文件出现在 top-5 里才算通过。*

```
🥇 马克思主义   ████████████████████████████████░░░░░░░░  50.0%  +6.7 分
   实用主义     ██████████████████████████████░░░░░░░░░░  46.7%  +3.3 分
   泰勒主义     ██████████████████████████████░░░░░░░░░░  46.7%  +3.3 分
   全方法组合   ██████████████████████████████░░░░░░░░░░  46.7%  +3.3 分
   ──────────────────────────────── 基线 ──────────────────
   基线（无方法）████████████████████████████░░░░░░░░░░░░  43.3%
   演化论       ████████████████████████████░░░░░░░░░░░░  43.3%
   凯恩斯主义   ████████████████████████░░░░░░░░░░░░░░░░  36.7%  -6.7 分
```

### 视觉数学推理 — 50 道题

```
🥇 马克思主义   █████████████████████████████████████████░  84.0%  +2.0 分
   基线         █████████████████████████████████████████   82.0%
   （其他）     █████████████████████████████████████████   82.0%
   演化论       ████████████████████████████████████████░   80.0%  -2.0 分
   泰勒主义     ████████████████████████████████████████░   80.0%  -2.0 分
```

马克思主义方法论是唯一在两个基准上**同时提升**的框架。

完整数据：[`benchmark/reports/summary.md`](benchmark/reports/summary.md)

---

## 🤔 为什么马克思主义方法论有效？

不是噱头。辩证唯物主义映射到代码排查流程上，出乎意料地贴切。

**核心规则：你不能凭记忆回答。**

其他方法允许智能体从自己已知的知识出发推理。马克思主义方法规定了一件必须做的事：*在给出任何预测之前，先检查这个具体的仓库*。跑 `find`，跑 `grep`，读实际的 import 链。然后再回答。

听起来是废话，但实际上不是——智能体默认会从训练数据里做模式匹配，结果就是路径错了、文件名错了、跑去了错误的子模块。

除此之外：

- **「现象与本质」** → 报错的文件 ≠ 需要修改的文件
- **「追踪普遍联系」** → 沿 import 双向追溯；检查基类（`generic.py`），而不只是报错的子类（`frame.py`）
- **「找到主要矛盾」** → 按因果关系排序，而不是按表面相关性排序

实用主义方法的提升幅度几乎一样大，靠的是一条具体规则：*优先选父类文件而不是子类文件*。简单、具体、有效。

---

## 📉 为什么凯恩斯主义方法论会把结果搞砸？

凯恩斯主义的「乘数效应」启发式——按被其他文件引用的次数来给文件排序——听起来很有道理。实际上不行。

一个被 50 个模块引用的工具文件，几乎不可能是某个具体 bug 的所在地。越「重要」的文件，越不可能是你要找的答案。凯恩斯主义方法论每次都系统性地把智能体指向了错误的地方。

---

## 🛠️ 五种方法论

每种方法论都是一个 `SKILL.md`——一份结构化的推理提示词，可以直接注入任何智能体。

| 方法论 | 核心思路 | Loc-Bench |
|-------|---------|-----------|
| [🏆 马克思主义](马克思/marxist-engineering-method/SKILL.md) | 物质条件优先，找主要矛盾，追踪普遍联系 | **+6.7 分** |
| [🔧 实用主义](实用主义/pragmatist-engineering/SKILL.md) | 主张转化为后果，优先选父类文件 | +3.3 分 |
| [📋 泰勒主义](泰勒主义/SKILL.md) | 先研究后行动，明确步骤分解 | +3.3 分 |
| [🧬 演化论](社会达尔文主义-演化/evolutionary-execution/SKILL.md) | 验证每个文件路径确实存在再纳入预测 | ±0 分 |
| [📉 凯恩斯主义](凯恩斯主义/keynesian-engineer/SKILL.md) | 按引用频率排序，刺激活动 | **-6.7 分** |

每个目录包含主 `SKILL.md` 和 `references/` 哲学参考文件夹。

---

## ⚡ 现在就用

### Claude Code

```bash
# 把最强方法论复制到你的项目里
cp 马克思/marxist-engineering-method/SKILL.md ./SKILL.md
```

在 `CLAUDE.md` 里加一行：
```
@./SKILL.md
```

### 其他智能体

`SKILL.md` 就是普通 Markdown。拼接到你的系统提示前面即可，没有任何依赖。

---

## 🔬 复现实验

依赖：Python 3.11+、[uv](https://github.com/astral-sh/uv)、环境变量 `ANTHROPIC_API_KEY`。

```bash
git clone https://github.com/espenzhang/agent-isms
cd agent-isms/benchmark
uv sync

# 跑故障定位（全部变体，API 费用约 $5–10）
uv run skill-bench run --config benchmark.locbench.toml --benchmark locbench

# 只跑一个变体
uv run skill-bench run --config benchmark.locbench.toml --benchmark locbench --variant marxist_only

# 生成报告
uv run skill-bench report --config benchmark.locbench.toml
```

中断后重新运行会从断点继续。

---

## 📂 仓库结构

```
agent-isms/
├── 马克思/marxist-engineering-method/   马克思主义方法论 + 哲学参考
├── 实用主义/pragmatist-engineering/     实用主义方法论
├── 凯恩斯主义/keynesian-engineer/       凯恩斯主义方法论
├── 社会达尔文主义-演化/                 演化论方法论
├── 泰勒主义/                           泰勒主义方法论
└── benchmark/
    ├── skill_bench/                    基准测试框架源码（Python）
    ├── benchmark.*.toml               配置文件
    ├── samples/                        每个基准 30–100 个采样任务
    └── reports/                        结果：summary.md、dashboard.html、leaderboard.csv
```

---

## 🙏 灵感来源

- [HughYau/qiushi-skill](https://github.com/HughYau/qiushi-skill) —— 最初的启发：经典方法论可以直接指导工程实践

---

*基准测试：[Loc-Bench V1](https://huggingface.co/datasets/czlll/Loc-Bench_V1) · [MathVista](https://huggingface.co/datasets/AI4Math/MathVista) · 智能体：[Claude Code](https://claude.ai/claude-code)*

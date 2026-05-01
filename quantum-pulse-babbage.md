# EquipMind AI - IT基础设施智能监控预测系统

## 概述
一个基于AI驱动的IT基础设施监控与状态预测CLI工具，支持实时监控、异常检测、故障预测和报告生成。

## 技术栈
- **语言**: Python 3.12+
- **CLI框架**: Click (命令行)
- **终端美化**: Rich (彩色输出、表格、进度条)
- **AI/ML**: scikit-learn (异常检测、预测模型)
- **数据处理**: pandas, numpy
- **可视化**: matplotlib + plotly (图表)
- **报告**: 自动生成HTML报告
- **存储**: SQLite (时序数据)
- **实时**: 内置WebSocket接口 (预留真实数据对接)

## 系统架构

```
equipmind/                      # 主包
├── cli/                        # CLI命令层
│   ├── __init__.py
│   ├── main.py                 # 入口 & 命令组
│   ├── monitor_cmd.py          # monitor命令
│   ├── predict_cmd.py          # predict命令
│   ├── device_cmd.py           # devices管理命令
│   ├── alert_cmd.py            # alerts管理命令
│   ├── report_cmd.py           # report生成命令
│   ├── simulate_cmd.py         # simulate数据模拟命令
│   ├── api_cmd.py              # api服务 (预留真实数据接口)
│   └── config_cmd.py           # config配置管理
├── monitor/                    # 监控引擎
│   ├── __init__.py
│   ├── engine.py               # 实时监控引擎 (轮询/流式)
│   └── collector.py            # 指标采集器 (含预留接口)
├── ai/                         # AI预测引擎
│   ├── __init__.py
│   ├── anomaly.py              # 异常检测 (Isolation Forest)
│   ├── forecaster.py           # 趋势预测 (时序预测)
│   ├── health.py               # 健康评分引擎
│   ├── failure.py              # 故障风险预测
│   └── trainer.py              # 模型训练/更新
├── data/                       # 数据层
│   ├── __init__.py
│   ├── database.py             # SQLite数据库管理
│   ├── models.py               # 数据模型定义
│   ├── repository.py           # 数据访问层
│   └── api_bridge.py           # 真实数据源API桥接 (预留)
├── reports/                    # 报告生成
│   ├── __init__.py
│   ├── html_report.py          # HTML报告渲染
│   └── charts.py               # 图表生成
├── simulator/                  # 数据模拟器 (演示用)
│   ├── __init__.py
│   └── generator.py            # 设备指标模拟生成
├── config/                     # 配置
│   ├── __init__.py
│   └── settings.py             # 全局配置管理
├── utils/                      # 工具函数
│   ├── __init__.py
│   └── helpers.py
└── main.py                     # 入口点 (console_scripts)
```

## 数据库设计 (SQLite)

### devices - 设备表
| 字段 | 类型 | 说明 |
|------|------|------|
| id | TEXT PK | 设备ID |
| name | TEXT | 设备名称 |
| type | TEXT | 类型 (server/network/storage/database) |
| ip | TEXT | IP地址 |
| status | TEXT | 状态 (online/offline/warning/critical) |
| health_score | REAL | 健康评分 0-100 |
| created_at | TIMESTAMP | 创建时间 |
| updated_at | TIMESTAMP | 更新时间 |

### metrics - 指标时序数据
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PK | 自增ID |
| device_id | TEXT FK | 设备ID |
| metric_name | TEXT | 指标名 (cpu/memory/disk/network) |
| value | REAL | 值 |
| unit | TEXT | 单位 (%) |
| timestamp | TIMESTAMP | 采集时间 |

### alerts - 告警记录
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PK | 自增ID |
| device_id | TEXT FK | 设备ID |
| type | TEXT | 告警类型 (anomaly/threshold/prediction) |
| severity | TEXT | 严重级别 (info/warning/critical) |
| message | TEXT | 告警消息 |
| ai_triggered | BOOLEAN | 是否AI触发 |
| resolved | BOOLEAN | 是否已解决 |
| created_at | TIMESTAMP | 创建时间 |

### predictions - AI预测结果
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PK | 自增ID |
| device_id | TEXT FK | 设备ID |
| prediction_type | TEXT | 预测类型 (failure/trend/health) |
| predicted_value | REAL | 预测值 |
| confidence | REAL | 置信度 0-1 |
| risk_level | TEXT | 风险等级 (low/medium/high/critical) |
| predicted_at | TIMESTAMP | 预测时间 |
| valid_until | TIMESTAMP | 有效期至 |

## AI模型设计

### 1. 异常检测 (AnomalyDetector)
- **算法**: Isolation Forest + 滑动窗口统计
- **输入**: 最近N个时间窗口的指标数据
- **输出**: 异常分数 + 是否异常
- **用途**: 实时检测CPU/内存/磁盘等指标的异常波动

### 2. 趋势预测 (TrendForecaster)
- **算法**: 线性回归 + 加权移动平均
- **输入**: 历史指标时序数据
- **输出**: 未来M个时间点的预测值
- **用途**: 预测资源使用趋势 (如磁盘何时满、内存何时不足)

### 3. 健康评分 (HealthScorer)
- **算法**: 加权多指标综合评分模型
- **权重**: CPU 25%, 内存 25%, 磁盘 20%, 网络 15%, 异常频率 15%
- **输出**: 0-100 健康分数 + 等级 (优秀/良好/一般/较差/危险)

### 4. 故障风险预测 (FailurePredictor)
- **算法**: 多维度综合评分 (阈值偏离度 + 趋势恶化度 + 异常频率)
- **输出**: 故障概率 + 风险等级 + 建议维护时间窗口
- **用途**: 提前预警可能的设备故障

## CLI命令设计

```
equipmind
├── monitor                         # 实时监控模式 (动态刷新)
│   ├── start                       # 启动监控
│   └── status                      # 查看监控状态
├── predict [device_id]             # 查看设备预测
│   ├── --all                       # 所有设备
│   └── --output/-o                 # 输出格式 (json/table)
├── report                          # 生成报告
│   ├── generate                    # 生成HTML报告
│   ├── --device/-d                 # 指定设备
│   ├── --period/-p                 # 时间范围 (24h/7d/30d)
│   └── --output/-o                 # 输出路径
├── devices                         # 设备管理
│   ├── list                        # 列出所有设备
│   ├── add                         # 添加设备
│   ├── remove                      # 移除设备
│   └── detail [id]                 # 查看设备详情
├── alerts                          # 告警管理
│   ├── list                        # 列出告警
│   └── resolve [id]                # 解决告警
├── simulate                        # 启动模拟数据
│   └── --interval                  # 模拟间隔(秒)
├── api                             # 启动API服务 (预留)
│   └── start                       # 启动REST API
│       ├── --port                  # 端口 (默认8765)
│       └── --host                  # 主机 (默认0.0.0.0)
├── config                          # 配置管理
│   ├── show                        # 查看配置
│   └── set <key> <value>           # 设置配置
└── --version                       # 查看版本
```

## 报告输出

HTML报告包含:
1. **概览面板**: 设备总数、在线率、平均健康评分、待处理告警数
2. **设备健康排行榜**: 按健康评分排序的设备列表
3. **风险设备列表**: 高风险/高危设备摘要
4. **AI预测汇总**: 各设备故障风险预测
5. **指标趋势图**: CPU/内存/磁盘/网络 趋势图表
6. **异常检测记录**: 近期AI检测到的异常事件
7. **维护建议**: 基于AI分析生成的维护建议列表

## 实施步骤

### Step 1: 项目骨架
- 创建目录结构和 `__init__.py`
- 创建 `main.py` 入口和Click命令组
- 安装依赖

### Step 2: 数据库和数据层
- 实现 SQLite 数据库管理
- 实现数据模型和仓库层
- 实现数据模拟器

### Step 3: AI引擎
- 实现异常检测模型
- 实现趋势预测模型
- 实现健康评分引擎
- 实现故障风险预测

### Step 4: CLI命令
- 设备管理命令
- 实时监控命令 (Rich动态刷新)
- 预测命令
- 告警管理命令

### Step 5: 报告生成
- 图表生成
- HTML报告模板
- 报告导出

### Step 6: API与集成 (预留)
- Flask REST API
- 真实数据桥接接口
- 认证与配置

## 依赖清单
```
click>=8.0
rich>=13.0
scikit-learn>=1.3
pandas>=2.0
numpy>=1.24
matplotlib>=3.7
plotly>=5.15
flask>=3.0
jinja2>=3.1
```

---

**注**: 系统设计为"开箱演示"模式 —— 内置模拟数据生成器，无需外部数据即可展示完整的AI监控预测能力。同时预留了 `api_bridge.py` 和 REST API 接口，后续可对接 Prometheus、Zabbix、Nagios 等真实监控数据源。

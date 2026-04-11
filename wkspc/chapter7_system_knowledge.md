# 第7章 系统知识库

## 一、系统概况

**系统名称：** 隧道工程综合监测数字孪生系统 V1（城市大型地下基础设施智能暗挖建造云边端一体化平台）

**系统定位：** 面向隧道与市政工程的数字孪生平台，集成多源监测数据（沉降、裂缝、温度、振动、InSAR、盾构机轨迹等），提供数据采集、智能分析和可视化管控。

## 二、技术栈

| 层级 | 技术 |
|------|------|
| 后端 | Flask 3.x, Python, Pandas, NumPy, Scikit-learn, PyTorch |
| 前端 | React 18, TypeScript, Vite 5, Tailwind CSS |
| 数据库 | Supabase (PostgreSQL)，MySQL（原始数据导入） |
| 部署 | Vercel (Serverless Python函数) |
| 移动端 | Capacitor 6 (Android APK) |
| 3D可视化 | Three.js |
| 地图 | Leaflet |
| 图表 | ECharts 5 |

## 三、项目目录结构

```
ygzl_2026_1/
├── api/              # Vercel Serverless入口 (index.py)
├── backend/          # 核心后端逻辑
│   ├── api/          # API服务器入口 (api_server.py)
│   ├── modules/      # 功能模块
│   │   ├── ml_models/    # 26个ML模型文件
│   │   ├── assistant/    # AI智能助手(ReAct Agent)
│   │   ├── data_import/  # 数据导入处理(Excel→MySQL)
│   │   ├── db/repos/     # 数据库抽象层(Supabase+MySQL)
│   │   ├── insar/        # InSAR卫星数据处理
│   │   └── ticket_system/# 工单系统
│   └── requirements.txt
├── frontend/         # React前端
│   ├── src/pages/    # 13个功能页面
│   ├── src/components/
│   └── src/lib/      # API客户端和工具库
├── mobile/           # Android移动端 (Capacitor)
├── scripts/          # 工具脚本
├── supabase/         # SQL迁移脚本(01-07)
├── docs/             # 文档
├── vercel.json       # Vercel部署配置
└── requirements.txt  # Python依赖
```

## 四、ML/AI模型详细清单 (backend/modules/ml_models/)

共26个.py文件，核心模型如下：

### 4.1 Informer时序预测 (informer_predictor.py)
- 算法：ProbSparse Self-Attention Transformer（AAAI 2021）
- 复杂度：O(L log L)，含Self-Attention Distilling和Generative Decoder
- 参数：d_model, n_heads, factor, dropout, enc/dec_layers

### 4.2 PINN物理信息神经网络 (pinn_predictor.py)
- 算法：Physics-Informed Neural Networks
- 物理约束：Terzaghi固结理论 + Mohr-Coulomb准则嵌入损失函数
- 参数：cv（固结系数）, H（土层厚度）

### 4.3 STGCN时空图卷积 (stgcn_predictor.py)
- 算法：Spatio-Temporal Graph Convolutional Networks
- 结构：图卷积（空间）+ 时间卷积（时间）
- 参数：distance_threshold（空间邻接阈值）

### 4.4 异常检测 (anomaly_detector.py)
- 算法：Isolation Forest + LOF双模型
- 特征工程：沉降速率、加速度、7日移动平均/标准差等多维特征
- 参数：method, contamination

### 4.5 Prophet预测 (prophet_predictor.py)
- 算法：趋势/季节性分解，施工事件覆盖
- 参数：changepoint_prior_scale, seasonality_prior_scale

### 4.6 可解释性分析 (explainability.py)
- 算法：SHAP（GradientBoostingRegressor）+ Permutation Importance（兜底）
- 参数：n_repeats

### 4.7 因果推断 (causal_inference.py)
- 算法：双重差分法(DID) + 合成控制法(SCM)

### 4.8 数字孪生仿真器 (digital_twin_simulator.py)
- 算法：Kalman Filter + ODE积分，实时数据同化
- 参数：F（状态转移矩阵）, Q（过程噪声）, R（测量噪声）

## 五、AI智能助手 (backend/modules/assistant/)

- **架构**：ReAct风格Agent循环（agent_loop.py）
- **LLM**：Anthropic Claude API（原始HTTP调用），模型claude-sonnet-4-20250514
- **约束**：最多2次迭代，总超时45秒
- **工具注册**（agent_tools.py）：tool_list_monitoring_points, tool_query_settlement_data, anomalies, events, predictions, papers
- **知识图谱**：NetworkX实现（knowledge_graph_nx.py），另有Supabase版本

## 六、数据采集与导入 (backend/modules/data_import/)

- Excel(.xlsx)导入：pandas读取 → SQLAlchemy写入MySQL
- 目标表：raw_settlement_data, raw_crack_data等
- 支持MDB/ACCDB温度数据导入

## 七、InSAR处理 (backend/modules/insar/)

- Shapefile → GeoJSON转换（service.py）
- 位移时序字段模式：D_YYYYMMDD
- DBSCAN聚类识别风险区域
- 磁盘文件缓存机制

## 八、工单系统 (backend/modules/ticket_system/)

- 状态机：PENDING及其他状态（config.py定义）
- 自动生成ticket_number
- 关联monitoring_point_id和equipment_id
- 邮件通知 + 定时任务

## 九、前端页面清单 (frontend/src/pages/)

| 页面 | 功能 |
|------|------|
| Overview / OverviewV2 | 总览仪表盘 |
| Settlement / SettlementV2 | 沉降监测 |
| Temperature / TemperatureNew | 温度监测 |
| Cracks / CracksNew | 裂缝监测 |
| Vibration / VibrationNew | 振动监测 |
| ShieldTrajectory | 盾构机轨迹 |
| Insar | InSAR卫星监测 |
| ThreeModel | 3D模型可视化 |
| Tickets | 工单管理 |
| AdvancedAnalysis | 高级分析（ML模型调用） |
| Tunnel | 隧道展示 |
| Cover / CoverMapShow | 覆盖/地图展示 |

## 十、数据库迁移 (supabase/sql/)

01_tickets.sql → 07_agent_insights.sql，共7个迁移文件

## 十一、章节对应关系

| 章节 | 系统对应模块 |
|------|-------------|
| 7.1 系统功能与平台架构 | 整体架构、技术栈、Vercel部署、前后端分离、三层架构 |
| 7.2 数据智能采集与融合 | data_import/(Excel/MDB导入)、insar/(卫星数据)、传感器数据处理、MySQL→Supabase数据流 |
| 7.3 智能分析与AI决策 | ml_models/(Informer/PINN/STGCN/异常检测/Prophet/SHAP/因果推断/数字孪生)、assistant/(ReAct Agent+知识图谱) |
| 7.4 集群控制与远程管控 | 移动端Capacitor、工单系统、实时监控页面、盾构轨迹、3D模型 |

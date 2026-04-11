# 第7章 系统知识库（详细版）

## 一、系统概况

**系统名称：** 隧道工程综合监测数字孪生系统 V1（城市大型地下基础设施智能暗挖建造云边端一体化平台）

**系统定位：** 面向隧道与市政工程的数字孪生平台，集成多源监测数据（沉降、裂缝、温度、振动、InSAR、盾构机轨迹等），提供数据采集、智能分析和可视化管控。

**整体架构：** 前后端分离的三层架构（表现层-业务逻辑层-数据层），通过Vercel Serverless部署实现云端一体化。

## 二、技术栈

| 层级 | 技术 | 补充说明 |
|------|------|----------|
| 后端 | Flask 3.x, Python | JSON_AS_ASCII=False, MAX_CONTENT_LENGTH=10MB |
| 前端 | React 18, TypeScript, Vite 5, Tailwind CSS | React Router v6, Zustand状态管理 |
| 数据库 | Supabase (PostgreSQL)，MySQL（原始数据导入） | 工厂模式切换：DB_VENDOR环境变量 |
| 部署 | Vercel (Serverless Python函数) | maxDuration=60s, SPA rewrite |
| 移动端 | Capacitor 6 (Android APK) | VITE_MOBILE环境变量检测 |
| 3D可视化 | Three.js | GLB/GLTF模型，1年缓存 |
| 地图 | Leaflet | KML解析支持 |
| 图表 | ECharts 5 | 赛博朋克主题(cyberpunkTheme) |
| 科学计算 | NumPy 1.23.5, SciPy 1.10.1, Pandas | 数据处理核心 |
| 机器学习 | Scikit-learn, PyTorch 2.2.1, statsmodels | 26个ML模型文件 |
| 知识图谱 | NetworkX, Neo4j(可选) | 内存图+持久化双模式 |

## 三、项目目录结构

```
ygzl_2026_1/
├── api/index.py          # Vercel Serverless入口（12行，路径注入+导入Flask app）
├── backend/
│   ├── modules/
│   │   ├── api/api_server.py  # Flask主服务器（1258行，15个Blueprint）
│   │   ├── ml_models/         # 26个ML模型文件（详见第四节）
│   │   ├── assistant/         # AI智能助手（ReAct Agent循环）
│   │   ├── data_import/       # 数据导入处理(Excel→MySQL)
│   │   ├── db/
│   │   │   ├── vendor.py      # 数据库工厂（get_repo()按DB_VENDOR切换）
│   │   │   └── repos/
│   │   │       ├── supabase_http_repo.py  # Supabase REST客户端（775行）
│   │   │       └── mysql_repo.py          # MySQL客户端（727行）
│   │   ├── insar/             # InSAR卫星数据处理
│   │   └── ticket_system/     # 工单系统
│   └── requirements.txt       # 374个包（Anaconda环境）
├── frontend/
│   ├── src/
│   │   ├── main.tsx           # 路由定义（15个路由，lazyWithRetry懒加载）
│   │   ├── pages/             # 15个功能页面
│   │   ├── components/
│   │   │   ├── layout/        # DashboardGrid, MobileCardSwitcher
│   │   │   ├── shared/        # Nav, PointSelector, ViewModeSwitch
│   │   │   ├── assistant/     # FloatingAssistant（对话+知识图谱+流式）
│   │   │   ├── charts/        # EChartsWrapper + 各监测类型图表
│   │   │   ├── analysis/      # AnomalyCard, CausalAnalysis, PredictionChart
│   │   │   └── trajectory/    # DeviationProfile, RingDetailDrawer
│   │   ├── lib/               # api.ts, mlApi.ts（ML专用客户端）
│   │   ├── utils/apiClient.ts # 基础API工具
│   │   └── stores/agentStore.ts # Zustand状态管理
│   └── package.json
├── mobile/                    # Android移动端 (Capacitor)
├── supabase/sql/              # 7个SQL迁移文件（01-07）
├── vercel.json                # 部署配置（maxDuration=60s）
└── requirements.txt           # 根级Python依赖
```

## 三-B、后端API路由架构

**直接路由（@app.route）：**
- `GET /health` — 健康检查
- `GET /api/points` — 所有监测点
- `GET /api/point/<point_id>` — 单点详情
- `GET /api/summary` — 数据摘要
- `GET /api/trends` — 趋势分析
- `GET /api/prediction/<point_id>` — ML预测
- `GET /api/risk/alerts` — 风险预警
- `POST /api/upload` — 文件上传（10MB限制）
- `GET /temperature/*` — 温度相关5个端点
- `GET /static/glb/<path>` — 3D模型服务（Cache-Control: 1年）

**15个Blueprint模块：**
| Blueprint | URL前缀 | 功能 |
|-----------|---------|------|
| crack_api | /api | 裂缝监测 |
| temperature_api | /api | 温度监测 |
| vibration_bp | /api/vibration | 振动监测 |
| ticket_bp | /api/tickets | 工单管理 |
| user_bp | /api/users | 用户管理(RBAC) |
| analysis_v2_bp | /api/analysis | 分析V2 |
| assistant_bp | /api/assistant | AI助手 |
| insar_bp | /api/insar | InSAR数据 |
| tunnel_bp | /api/tunnel | 隧道管理 |
| advanced_bp | /api/advanced | 高级分析 |
| module_bp | /api/modules | 模块管理 |
| shield_bp | /api/shield | 盾构机(条件加载) |
| ml_api | /api/ml | ML模型(条件加载) |
| agent_bp | /api/agent | Agent(条件加载) |
| temperature_v2_api | /api | 温度V2(条件加载) |

**Vercel部署配置（vercel.json）：**
- 构建：`npm ci --prefix frontend` + `npm run build --prefix frontend`
- 输出：`frontend/dist`
- Serverless函数：`api/index.py`，maxDuration=60s
- 包含文件：`backend/**/*.py, frontend/public/static/data/insar/**`
- URL重写：`/api/:path*` → `/api/index.py`（API），`/(.*)` → `/index.html`（SPA）
- CORS头：`Access-Control-Allow-Origin: *`

## 三-C、数据库工厂模式

```python
# backend/modules/db/vendor.py
def get_repo():
    v = os.environ.get('DB_VENDOR', '').strip().lower()
    if v == 'supabase_http':
        return SupabaseHttpRepo()
    return MySQLRepo()
```

**SupabaseHttpRepo（775行）：** HTTP REST客户端，Bearer Token认证，PostgREST查询语法（eq./ilike.*/gt./lt.），覆盖Settlement/Crack/Temperature/Tickets/Users/Tunnel/TBM等全部领域。

**MySQLRepo（727行）：** mysql-connector-python，pandas DataFrame返回，ON DUPLICATE KEY UPDATE支持，tunnel_ensure_schema()自动建表。

## 四、ML/AI模型完整清单 (backend/modules/ml_models/ — 26个文件)

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

### 4.9 集成学习预测 (ensemble_predictor.py)
- 类名：EnsemblePredictor
- 三种集成方法：Stacking（Ridge/RandomForest元学习器）、加权平均（权重=1/MAE）、投票（简单平均）
- 基模型：ARIMA, Informer, STGCN, PINN
- 参数：method='stacking', meta_learner='ridge', device='cpu'
- 输出：集成预测 + 95%置信区间（基于标准差）

### 4.10 土体力学模型 (soil_mechanics.py)
- 5个经典模型类：
  - MohrCoulombModel：τ = c + σ·tan(φ)，参数cohesion(kPa), friction_angle(度)
  - DruckerPragerModel：三维强度准则
  - TerzaghiConsolidation：一维固结理论，ODE积分
  - BiotConsolidation：三维固结理论
  - DuncanChangModel：非线性弹性本构
- 应用：数字孪生仿真、沉降预测、稳定性分析

### 4.11 空间关联分析 (spatial_correlation.py)
- 类名：SpatialCorrelationAnalyzer
- 算法：欧氏距离邻接矩阵 + Pearson/Spearman相关性
- 参数：distance_threshold=50.0（米）
- 特征：对称归一化邻接矩阵，自环，距离反比权重

### 4.12 ARIMA/SARIMA时序预测 (time_series_predictor.py)
- 类名：TimeSeriesPredictor
- 算法：ARIMA + SARIMA（statsmodels）
- 特征：ADF平稳性检验、自动差分（max_d=2）、自动定阶
- 参数：model_type='arima'

### 4.13 因果推理引擎增强版 (causal_reasoning.py)
- 类名：CausalReasoningEngine
- 5种方法：PC算法(因果发现)、Granger因果检验、DID、SCM、倾向得分匹配(PSM)
- 参数：method='granger', max_lag=5, significance_level=0.05
- 功能：因果发现→因果推断→反事实推理→干预效应估计

### 4.14 模型自动选择器 (model_selector.py)
- 类名：ModelSelector
- 功能：根据数据特征自动选择最优预测模型
- 支持加载预训练参数（trained_models/training_results.json缓存）
- 评估指标：MAE, RMSE

### 4.15 轻量级深度学习替代 (lightweight_deep.py)
- 用途：Vercel Serverless环境（1024MB/60s限制）下的替代方案
- 算法：GradientBoostingRegressor + RandomForestRegressor（sklearn）
- 特征工程：7阶滞后、3/7日滚动均值/标准差、一阶差分、时间索引
- 输出格式：与前端PredictionResult接口对齐

### 4.16 知识图谱构建 (knowledge_graph.py, build_knowledge_graph.py)
- 基于Neo4j的持久化知识图谱
- 节点类型：MonitoringPoint, ConstructionEvent, Anomaly
- 边类型：SPATIAL_NEAR, CORRELATES_WITH, CAUSES, DETECTED_AT

### 4.17 知识图谱问答 (kgqa.py)
- 类名：KGQA
- 5种问题类型：实体查询、关系查询、因果查询、统计查询、路径查询
- 正则模式匹配意图识别 → Cypher查询生成 → 自然语言答案

### 4.18 辅助模块
- **supabase_data.py** — Supabase数据获取层（fetch_point_settlement, fetch_all_settlement, fetch_monitoring_points, find_distant_points）
- **supabase_kg.py** — Supabase版知识图谱存储
- **api.py** — ML模块Flask Blueprint（延迟导入避免冷启动超时，含轻量Prophet替代：ExponentialSmoothing）
- **prepare_data.py** — 数据准备脚本（Supabase导出→预处理→70/15/15划分→CSV/NPY）
- **train_all.py** — 统一训练管理（一键训练Informer/STGCN/PINN + 对比实验 + 评估报告）
- **train_informer.py** — Informer专用训练脚本
- **train_settlement_local.py** — 本地沉降模型训练

## 五、AI智能助手 (backend/modules/assistant/)

### 5.1 Agent循环 (agent_loop.py)
- **架构**：ReAct风格Agent循环（tool_use协议）
- **LLM**：Anthropic Claude API（原始HTTP requests调用）
- **模型**：claude-sonnet-4-20250514（环境变量CLAUDE_MODEL可配置）
- **max_tokens**：4096（环境变量CLAUDE_MAX_TOKENS可配置）
- **约束**：
  - MAX_ITERATIONS = 2（迭代0：选工具→执行；迭代1：读结果→生成答案）
  - AGENT_TIMEOUT = 45秒（Vercel 60s - 15s缓冲）
  - 第一次Claude调用超时10s（仅选工具）
  - 第二次Claude调用超时12s（读结果+写答案）
  - 工具结果截断至2000字符（智能截断：JSON列表保留前5项）
  - 超时后降级为无工具摘要模式

### 5.2 工具注册 (agent_tools.py)
- 6个工具函数，每个直接查询Supabase REST API：
  1. **tool_list_monitoring_points** — 列出所有监测点（limit=500）
  2. **tool_query_settlement_data** — 查询沉降数据（limit=200）
  3. **tool_query_anomalies** — 查询异常记录
  4. **tool_query_events** — 查询施工事件
  5. **tool_query_predictions** — 查询预测结果
  6. **tool_search_papers** — 搜索相关论文
- Supabase认证：Bearer Token（SUPABASE_ANON_KEY），超时8秒

### 5.3 知识图谱 (knowledge_graph_nx.py)
- **实现**：NetworkX DiGraph（有向图），内存构建
- **每次查询重建**：build_fresh_knowledge_graph()，无缓存
- **节点类型**：MonitoringPoint, ConstructionEvent, Anomaly
- **边类型**：SPATIAL_NEAR, CORRELATES_WITH, CAUSES, DETECTED_AT
- **构建参数**：distance_threshold=50, correlation_threshold=0.7
- **数据源**：Supabase（fetch_monitoring_points, fetch_all_settlement）
- **输出**：export_for_visualization()供前端渲染

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

## 九、前端页面与路由 (frontend/src/)

### 9.1 路由表（React Router v6，lazyWithRetry懒加载）

| 路由路径 | 组件 | 功能 |
|----------|------|------|
| / | Navigate→/cover | 根重定向 |
| /cover | Cover.tsx | 项目入口/封面页 |
| /overview | OverviewV2.tsx | 总览仪表盘 |
| /settlement | Settlement.tsx | 沉降监测 |
| /temperature | Temperature.tsx | 温度监测 |
| /cracks | Cracks.tsx | 裂缝监测 |
| /vibration | VibrationV2.tsx | 振动监测(最新版) |
| /vibration-legacy | Vibration.tsx | 振动监测(旧版) |
| /insar | Insar.tsx | InSAR卫星监测 |
| /three | ThreeModel.tsx | 3D模型可视化 |
| /tickets | Tickets.tsx | 工单管理 |
| /tunnel | Tunnel.tsx | 隧道展示 |
| /advanced | AdvancedAnalysis.tsx | 高级分析（ML模型调用） |
| /shield-trajectory | ShieldTrajectory.tsx | 盾构机轨迹 |
| /modules | ModuleAdmin.tsx | 模块管理后台 |

### 9.2 前端架构特征
- **懒加载**：lazyWithRetry包装器，处理chunk加载失败（重部署后自动刷新）
- **移动端检测**：`import.meta.env.VITE_MOBILE === 'true'`条件渲染
- **权限控制**：AuthGuard + ModuleGate（基于功能模块的访问控制）
- **状态管理**：Context API（AuthContext, ModulesContext）+ Zustand（agentStore.ts）
- **API客户端**：api.ts（通用）+ mlApi.ts（ML专用）+ apiClient.ts（基础工具）
- **组件体系**：
  - layout/：DashboardGrid（弹性网格）, MobileCardSwitcher（移动端卡片切换）
  - shared/：Nav, PointSelector, ViewModeSwitch
  - assistant/：FloatingAssistant（浮动AI助手，对话+知识图谱+流式进度）
  - charts/：EChartsWrapper + cracks/temperature/vibration子目录
  - analysis/：AnomalyCard, CausalAnalysis, PredictionChart
  - trajectory/：DeviationProfile, RingDetailDrawer（盾构偏差分析）
- **主题**：Tailwind CSS自定义主题 + cyberpunkTheme.ts（赛博朋克风格图表）
- **地理数据**：insar.ts, kml.ts（KML解析）, mapLayers.ts（地图图层配置）

## 十、数据库Schema (supabase/sql/ — 7个迁移文件)

### 10.1 工单系统 (01_tickets.sql)
- **tickets表**：id(BIGSERIAL), ticket_number(UNIQUE), title, description, ticket_type, sub_type, priority(DEFAULT 'MEDIUM'), status(DEFAULT 'PENDING'), creator_id/name, assignee_id/name, monitoring_point_id, location_info(JSONB), equipment_id, threshold_value, current_value, alert_data(JSONB), due_at, resolved_at, closed_at, attachment_paths(JSONB), metadata(JSONB), is_archived
- **ticket_comments表**：id, ticket_id(FK CASCADE), author_id/name, content, comment_type(DEFAULT 'COMMENT'), attachment_paths(JSONB)
- **ticket_archive表**：归档表，含comments_snapshot(JSONB)
- **视图**：v_tickets_active, v_tickets_due_soon, v_tickets_overdue, v_tickets_to_archive
- **索引**：status, type, priority, creator, assignee, monitoring_point, equipment, created_at(DESC), due_at
- **触发器**：update_tickets_updated_at, update_ticket_comments_updated_at

### 10.2 用户管理 (02_users.sql)
- **system_users表**：user_id(UNIQUE), username, display_name, email, phone, role(DEFAULT 'operator'), permissions(JSONB), is_active, department, team
- **user_notification_settings表**：email_enabled, in_app_enabled, webhook_enabled, email_frequency(DEFAULT 'realtime'), notify_on_ticket_created/assigned/status_change/comment/due_soon/overdue, quiet_hours_start/end, timezone(DEFAULT 'Asia/Shanghai')
- **种子数据**：5个默认用户（admin, system, monitoring_engineer, field_technician, data_analyst）

### 10.3 隧道项目 (03_tunnel.sql)
- **tunnel_projects表**：project_id(UUID), name, description
- **tunnel_alignments表**：alignment_id(UUID), project_id(FK), name, geojson(JSONB), srid(DEFAULT 4326)
- **tunnel_point_mappings表**：mapping_id(UUID), project_id(FK), point_id, alignment_id(FK), chainage_m, offset_m, side, section_name, structure_part, ring_no

### 10.4 TBM遥测 (04_tbm.sql)
- **tbm_telemetry表**：record_id(UUID), project_id(FK), machine_id, ts(时间戳), chainage_m, ring_no, thrust_kN, torque_kNm, face_pressure_kPa, slurry_pressure_kPa, advance_rate_mm_min, cutterhead_rpm, pitch_deg, roll_deg, yaw_deg, grout_volume_L, grout_pressure_kPa, status
- UNIQUE约束：(project_id, machine_id, ts)

### 10.5 高级分析 (05_advanced_analysis.sql)
- **tunnel_profile_config表**：point_id(PK), chainage_m, section_name, x/y/z_coord
- **geological_layers表**：layer_number, layer_name, depth_top/bottom, thickness, unit_weight, cohesion, friction_angle, compression_modulus, poisson_ratio, color
- **settlement_crack_mapping表**：settlement_point, crack_point, distance_m, correlation_strength
- **construction_events表**：event_date, event_type/subtype, title, location_chainage_start/end, affected_points(TEXT[]), intensity, metadata(JSONB)
- **crack_monitoring_data表**：measurement_date, point_id, crack_id, value, daily_change, cumulative_change
- **视图**：v_profile_with_settlement, v_joint_settlement_crack

### 10.6 知识图谱 (06_knowledge_graph.sql)
- **kg_nodes表**：id(TEXT PK), node_type, label, properties(JSONB), document_id(UUID), source(DEFAULT 'auto')
- **kg_edges表**：source_id(FK), target_id(FK), edge_type, properties(JSONB), confidence(FLOAT DEFAULT 1.0)
- **kg_documents表**：title, content, summary, source_type, processed(BOOLEAN), entity_count, relation_count
- **kg_document_entities表**：document_id, entity_id, mention_count, context
- **kg_qa_history表**：question, answer, sources(JSONB), confidence, feedback

### 10.7 Agent洞察 (07_agent_insights.sql)
- **insights表**：insight_type(DEFAULT 'anomaly'), severity(DEFAULT 'info'), point_id, title, body, evidence(JSONB), suggestion, acknowledged, dismissed

## 十一、章节对应关系

| 章节 | 系统对应模块 |
|------|-------------|
| 7.1 系统功能与平台架构 | 整体架构、技术栈、Vercel部署、前后端分离、三层架构 |
| 7.2 数据智能采集与融合 | data_import/(Excel/MDB导入)、insar/(卫星数据)、传感器数据处理、MySQL→Supabase数据流 |
| 7.3 智能分析与AI决策 | ml_models/(Informer/PINN/STGCN/异常检测/Prophet/SHAP/因果推断/数字孪生)、assistant/(ReAct Agent+知识图谱) |
| 7.4 集群控制与远程管控 | 移动端Capacitor、工单系统、实时监控页面、盾构轨迹、3D模型 |

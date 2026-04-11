# 第7章 系统知识库

## 一、系统概况

**系统名称：** 隧道工程综合监测数字孪生系统 V1（城市大型地下基础设施智能暗挖建造云边端一体化平台）

**系统定位：** 面向隧道与市政工程的数字孪生平台，集成多源监测数据（沉降、裂缝、温度、振动、InSAR、盾构机轨迹等），提供数据采集、智能分析和可视化管控。

---

## 二、技术栈

| 层级 | 技术 |
|------|------|
| 后端 | Flask 3.x, Python, Pandas, NumPy, Scikit-learn, PyTorch |
| 前端 | React 18, TypeScript, Vite 5, Tailwind CSS |
| 数据库 | Supabase (PostgreSQL) |
| 部署 | Vercel (Serverless Python函数) |
| 移动端 | Capacitor 6 (Android APK) |
| 3D可视化 | Three.js |
| 地图 | Leaflet |
| 图表 | ECharts 5 |

---

## 三、项目目录结构

```
ygzl_2026_1/
├── api/              # Vercel Serverless入口 (index.py)
├── backend/          # 核心后端逻辑
│   ├── api/          # API服务器入口 (api_server.py)
│   ├── modules/      # 功能模块
│   │   ├── ml_models/    # 20+ 机器学习模型
│   │   ├── assistant/    # AI智能助手
│   │   ├── data_import/  # 数据导入处理
│   │   ├── db/repos/     # 数据库抽象层(Supabase+MySQL)
│   │   ├── insar/        # InSAR卫星数据处理
│   │   └── ticket_system/# 工单系统
│   └── requirements.txt
├── frontend/         # React前端
│   ├── src/pages/    # 13个功能页面
│   ├── src/components/ # 组件(AI助手、工单、可视化)
│   └── src/lib/      # API客户端和工具库
├── mobile/           # Android移动端 (Capacitor)
├── scripts/          # 工具脚本(知识图谱、无人机、隧道处理)
├── supabase/         # SQL迁移脚本
├── docs/             # 文档
├── vercel.json       # Vercel部署配置
└── requirements.txt  # Python依赖
```

---

## 四、系统功能模块（待细化）

### 4.1 数据采集与导入
- Excel沉降数据导入
- MDB/ACCDB温度数据导入
- InSAR卫星数据处理
- （待查：更多数据源和采集细节）

### 4.2 ML/AI模型 (backend/modules/ml_models/)
- 异常检测：Isolation Forest
- 时序预测：ARIMA, Prophet, Informer
- 可解释性：SHAP
- （待查：完整模型列表和具体功能）

### 4.3 AI智能助手 (backend/modules/assistant/)
- Agent架构
- 意图分类
- 知识图谱集成
- （待查：详细实现）

### 4.4 前端页面模块 (frontend/src/pages/)
- 沉降监测、温度监测、裂缝监测
- 3D模型、InSAR
- （待查：完整页面列表和功能）

### 4.5 工单系统 (backend/modules/ticket_system/)
- （待查：工单流程和功能）

### 4.6 移动端
- Capacitor包装React前端为Android APK
- （待查：移动端特有功能）

---

## 五、章节对应关系（初步映射）

| 章节 | 系统对应模块 | 状态 |
|------|-------------|------|
| 7.1 系统功能与平台架构 | 整体架构、技术栈、部署方式、前后端结构 | 待细化 |
| 7.2 数据智能采集与融合 | data_import/, insar/, 传感器数据处理 | 待细化 |
| 7.3 智能分析与AI辅助决策 | ml_models/, assistant/, 知识图谱 | 待细化 |
| 7.4 集群控制与远程管控 | 移动端、工单系统、实时监控、远程控制 | 待细化 |

---

## 六、待进一步勘察的内容

- [ ] backend/modules/ 完整目录结构和每个模块的功能
- [ ] ml_models/ 所有模型文件列表和详细功能
- [ ] frontend/src/pages/ 所有页面列表
- [ ] 数据库表结构 (supabase/ 迁移文件)
- [ ] API路由结构
- [ ] 部署架构细节
- [ ] 移动端具体功能
- [ ] 实时监控/远程管控的实现方式

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

<!-- PLACEHOLDER_SECTION_4 -->

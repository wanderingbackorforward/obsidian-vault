sk-XPVMdZBwGbYNVuJcjY9RjjVY0cPZBXPvTQPc0VwMRjADi0xD

能搞定。**但要用“本地代理”这条路线**。你坚持 Claude Code，就按下面这版走，不再绕。

原因一句话：Claude Code 支持用 `ANTHROPIC_BASE_URL` 指向代理/网关；你的新地址是 OpenAI-compatible `/v1`，所以需要一个代理把 Claude Code 的 Anthropic 请求转成 OpenAI 格式。Claude Code 官方文档确认 `ANTHROPIC_BASE_URL` 就是用来覆盖 API 端点、走代理/网关的；这个代理项目也明确支持把 Anthropic/Claude API 格式转换到 OpenAI-compatible API。([Claude](https://code.claude.com/docs/zh-CN/env-vars "环境变量 - Claude Code Docs"))

---

## 你就照这个做：两个 PowerShell 窗口

### 窗口 1：启动本地代理

先打开一个新的 PowerShell，执行：

```powershell
npm install -g @kiyo-e/claude-code-proxy
```

然后继续在这个窗口执行：

```powershell
$env:CLAUDE_CODE_PROXY_API_KEY = "sk-XPVMdZBwGbYNVuJcjY9RjjVY0cPZBXPvTQPc0VwMRjADi0xD"
$env:ANTHROPIC_PROXY_BASE_URL = "https://myai.3651688.xyz/aikey/v1"

$env:REASONING_MODEL = "glm-5.1"
$env:COMPLETION_MODEL = "glm-5.1"
$env:DEBUG = "true"

claude-code-proxy --port 3000
```

这个窗口**不要关**。它就是转换器。

这个代理的官方 README 里推荐 npm 全局安装，然后用 `claude-code-proxy --port 8080/3000` 启动；它的配置变量就是 `CLAUDE_CODE_PROXY_API_KEY`、`ANTHROPIC_PROXY_BASE_URL`、`REASONING_MODEL`、`COMPLETION_MODEL`。([GitHub](https://github.com/kiyo-e/claude-code-proxy "GitHub - kiyo-e/claude-code-proxy · GitHub"))

---

### 窗口 2：启动 Claude Code

再打开第二个 PowerShell，进入你的项目：

```powershell
cd "D:\mine\myprojects\宁扬项目施组"
```

然后执行：

```powershell
$env:ANTHROPIC_BASE_URL = "http://localhost:3000"

# 给 Claude Code 一个本地占位 key，真正的新 sk-key 已经在代理窗口里配置了
$env:ANTHROPIC_API_KEY = "local-proxy-key"

Remove-Item Env:ANTHROPIC_AUTH_TOKEN -ErrorAction SilentlyContinue

$env:ANTHROPIC_DEFAULT_HAIKU_MODEL = "glm-5.1"
$env:ANTHROPIC_DEFAULT_SONNET_MODEL = "glm-5.1"
$env:ANTHROPIC_DEFAULT_OPUS_MODEL = "glm-5.1"
$env:ANTHROPIC_MODEL = "glm-5.1"

claude --allowedTools "Bash,Read,Edit"
```

代理 README 的 Claude Code 用法就是把 `ANTHROPIC_BASE_URL` 指到本地代理，例如 `http://localhost:3000`，然后正常运行 `claude`。([GitHub](https://github.com/kiyo-e/claude-code-proxy "GitHub - kiyo-e/claude-code-proxy · GitHub"))

---

## 你现在不要再写这个

```powershell
$env:ANTHROPIC_BASE_URL = "https://myai.3651688.xyz/aikey/v1"
```

这句对 Claude Code 不合适。

正确关系是：

```text
Claude Code
  -> http://localhost:3000
  -> https://myai.3651688.xyz/aikey/v1
```

也就是：

```powershell
# Claude Code 只连本地代理
$env:ANTHROPIC_BASE_URL = "http://localhost:3000"

# 新 sk-key 只给代理
$env:CLAUDE_CODE_PROXY_API_KEY = "sk-..."
$env:ANTHROPIC_PROXY_BASE_URL = "https://myai.3651688.xyz/aikey/v1"
```

---

## 如果启动代理时报错

优先检查：

```powershell
node -v
npm -v
claude --version
```

如果 `claude --version` 都跑不起来，那是 Claude Code 本地安装问题；如果 `claude-code-proxy --port 3000` 报错，才是代理安装问题。

你现在目标不是“旧智谱配置怎么改”，而是：

**新 sk 套餐 → 本地 proxy → Claude Code。**  
这条路可以搞定。
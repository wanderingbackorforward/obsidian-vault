# 新 GLM 网关地址
$env:ANTHROPIC_BASE_URL = "https://myai.3651688.xyz/aikey/v1"

# 新 sk- 开头的 key
# 注意：这里填你自己的完整 sk-... 密钥
$env:ANTHROPIC_AUTH_TOKEN = "sk-你的完整密钥"

# 避免旧 API_KEY 或旧配置干扰
Remove-Item Env:ANTHROPIC_API_KEY -ErrorAction SilentlyContinue

# 模型映射
$env:ANTHROPIC_DEFAULT_HAIKU_MODEL = "glm-4.5-air"
$env:ANTHROPIC_DEFAULT_SONNET_MODEL = "glm-5.1"
$env:ANTHROPIC_DEFAULT_OPUS_MODEL = "glm-5.1"

# 推荐额外加一个主模型，避免 Claude Code 没吃到 Sonnet/Opus 映射
$env:ANTHROPIC_MODEL = "glm-5.1"

# 启动 Claude Code
claude --allowedTools "Bash,Read"
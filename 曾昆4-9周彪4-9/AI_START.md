cd "D:\mine\mynotes\obsidian-vault\曾昆4-9周彪4-9\skills"


Stop-Process -Name node -Force -ErrorAction SilentlyContinue
Remove-Item -Path "$HOME\.claude.json" -Force -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force .\.claude -ErrorAction SilentlyContinue
'{"hasCompletedOnboarding": true}' | Out-File -FilePath "$HOME\.claude.json" -Encoding utf8
$env:ANTHROPIC_AUTH_TOKEN="sk-i43P96HyNcFEeHoAq8hh7iWDldwO2ADFij5584Z3xGU980dq"
$env:ANTHROPIC_BASE_URL="https://www.fucheers.top"
$env:CLAUDE_CODE_MODEL="claude-sonnet-4-6"
claude --model claude-sonnet-4-6 --allowedTools "Bash,Read file"


智谱

$env:ANTHROPIC_BASE_URL = "https://open.bigmodel.cn/api/anthropic"

$env:ANTHROPIC_AUTH_TOKEN = "9e5ce137029b42acbf1b063ba2f0ccdf.aFiWykOLs8vwfLUr"

$env:ANTHROPIC_DEFAULT_HAIKU_MODEL = "glm-4.5-air"

$env:ANTHROPIC_DEFAULT_SONNET_MODEL = "glm-5"

$env:ANTHROPIC_DEFAULT_OPUS_MODEL = "glm-5"

Claude --allowedTools "Bash,Read file"


# 1. 彻底清除全局配置文件（删除导致报错的旧模型记忆） Remove-Item -Path "$HOME\.claude.json" -Force -ErrorAction SilentlyContinue # 2. 彻底清除当前项目下的历史对话和局部缓存（注意：这会清空本项目的对话历史） Remove-Item -Recurse -Force .\.claude -ErrorAction SilentlyContinue



minimax：



# 1. 彻底清除残留的错误配置和项目历史缓存
Remove-Item -Path "$HOME\.claude.json" -Force -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force .\.claude -ErrorAction SilentlyContinue

# 2. 注入“已完成引导”状态，绕过官方域名 api.anthropic.com 的强制连通性检查
'{"hasCompletedOnboarding": true}' | Out-File -FilePath "$HOME\.claude.json" -Encoding utf8

# 3. 配置针对 Minimax M2.7 优化的环境变量
# 注意：端点必须使用 /anthropic 后缀，变量名需使用 AUTH_TOKEN
$env:ANTHROPIC_BASE_URL = "https://api.minimaxi.com/anthropic"
$env:ANTHROPIC_AUTH_TOKEN = "sk-cp-SzaxK2wvzlYR0RT5UWjz-YZF2WUKhjqbcGOr_A8X3o9fsMTvR9OAsz9wZUk27tcXC54cemymUpvPAjW9amN3g68WIkVcgwI-yzqBkryI0aSWe5YBwLa3hlg"

# 4. 将 Claude Code 所有的模型档位全部强制重指向 M2.7
$env:CLAUDE_CODE_MODEL = "MiniMax-M2.7"
$env:ANTHROPIC_MODEL = "MiniMax-M2.7"
$env:ANTHROPIC_SMALL_FAST_MODEL = "MiniMax-M2.7"
$env:ANTHROPIC_DEFAULT_SONNET_MODEL = "MiniMax-M2.7"
$env:ANTHROPIC_DEFAULT_OPUS_MODEL = "MiniMax-M2.7"
$env:ANTHROPIC_DEFAULT_HAIKU_MODEL = "MiniMax-M2.7"

# 5. 设置必要性能参数
$env:API_TIMEOUT_MS = "3000000"
$env:CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC = "1"

# 6. 启动 Claude Code
claude --allowedTools "Bash,Read file"














其实还是有问题的 主要是我们确实是研发了一个软件 我担心会彻底转向软件工程产品介绍风格 其实不是不能介绍 但是要把握好度 我们是土木专业的 对于第二个问题 请你要注意 再写一版提示词让它反复发掘模板文档解决这个问题 为此我还来为他提供了另外一个模板 来让这个skill——软件+土木毕业论文.docx


现在我打算是删了技能中的参考文件的docx 你如果要参考docx一律改为md 反正内容是一样的


chapter7_图片清单这个文件没写完 其指的就是4个draft.md文件里面的插入的图片
  因此我们务必要确认对应的figmaAI的提示词应该怎么写
  在此我说明几点：1必须要根据md内容和项目本身（这个就是在根目录有知识文件的）来 2最终看的人是科研隧道工程老教授 中国人
  你符合他们品味 你搞清楚该怎么做了吗 不知道的可以问我 我们先来进行制订计划
切记！！！！！读到的中间内容！一定要先记录！否则一定上下文溢出！！！！切记！你妄图一次记住！做梦！



切记！！！！！读到的中间内容！一定要先记录！否则一定上下文溢出！！！！切记！你妄图一次记住！做梦！


切记！！！！！读到的中间内容！一定要先记录！否则一定上下文溢出！！！！切记！你妄图一次记住！做梦！


切记！！！！！读到的中间内容！一定要先记录！否则一定上下文溢出！！！！切记！你妄图一次记住！做梦！


切记！！！！！读到的中间内容！一定要先记录！否则一定上下文溢出！！！！切记！你妄图一次记住！做梦！










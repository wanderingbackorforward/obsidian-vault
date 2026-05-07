1、在VSC的kilocode或Claude Code等AI编程软件中，配置AI提供商，选择自定义提供商，并按照如下格式填写内容。

2、假如要输入“提供商 ID”和“显示名称”根据你自己喜好来，ID为系统内记录，显示名称是你选择AI时显示的供应商名称。

3、“基础 URL”填写我提供的地址，GLM的 URL格式是： https://myai.3651688.xyz/aikey/v1

4、“API 密钥”填写我提供的key，以 sk- 开头的密钥。

5、填写好后就自动获取到当前可以使用的GLM所有模型，确认选择后，就可以开始使用。

GLM 老套餐无周限量 API key：sk-XPVMdZBwGbYNVuJcjY9RjjVY0cPZBXPvTQPc0VwMRjADi0xD


请你来为我解决：如何能通过这些来改造我的旧的智谱语句
请你来注意
我们千万要记得是在powershell要跑成功：

原先是这样的：
$env:ANTHROPIC_BASE_URL = "https://open.bigmodel.cn/api/anthropic"

$env:ANTHROPIC_AUTH_TOKEN = "9e5ce137029b42acbf1b063ba2f0ccdf.aFiWykOLs8vwfLUr"

$env:ANTHROPIC_DEFAULT_HAIKU_MODEL = "glm-4.5-air"

$env:ANTHROPIC_DEFAULT_SONNET_MODEL = "glm-5.1"

$env:ANTHROPIC_DEFAULT_OPUS_MODEL = "glm-5.1"

Claude --allowedTools "Bash,Read file"



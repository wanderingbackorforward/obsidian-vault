1
感谢 你看看现在我们做的怎么样
明天要进行演示 现在问题是我们得套壳一层gui 
哪怕是不复杂的
现在的情况是不禁老师看不懂 我自己也是
2



---

````text
当前项目已经完成并验证了一个重要更新：

commit 包含：
feat: add stoppage investigation ReAct agent module

新增能力：
- tbm_diag/investigation/ 模块
- investigate 子命令
- 停机案例追查 ReAct Agent
- 支持把碎片化 stoppage_segment 合并为停机 case
- 支持检查停机前后 transition window
- 支持 planned_like / abnormal_like / uncertain / short_operational_pause 分类
- 支持 investigation_report.md / investigation_state.json / case_memory.json 输出
- 已完成一轮系统性验收测试

现在请完成项目文档与开发规范收尾，不要新增功能。

请做以下事情：

一、更新 README.md

请基于当前真实代码状态更新 README.md。

必须补充以下内容：

1. 在“当前支持能力”中加入：
   - investigate：停机案例追查 ReAct Agent
   - 可从单文件或 scan_index.csv 中追查高风险停机案例
   - 能把碎片化停机事件合并成 case
   - 能检查停机前后窗口
   - 能输出 case-level 追查报告

2. 在命令示例中加入：

```bash
python -m tbm_diag.cli investigate --input sample2.xls --output-dir investigation_out
````

以及：

```bash
python -m tbm_diag.cli investigate \
  --scan-index scan_real_out/scan_index.csv \
  --top-n 3 \
  --output-dir investigation_out \
  --max-iterations 30
```

3. 解释 investigate 和 agent 的区别：
    

- agent：  
    OpenAI-compatible tool-using agent，用于单文件工具编排和报告生成。
    
- investigate：  
    ReAct-style investigation agent，用于停机案例追查。它不是固定 inspect→detect→summary 流程，而是根据观察结果决定是否合并停机片段、检查前后窗口、分类停机 case。
    

4. 补充 ReAct Investigation Agent 的工作流：
    

```text
inspect file
→ load event summary
→ 判断是否存在大量停机片段
→ merge stoppage segments into cases
→ inspect transition window
→ classify stoppage cases
→ generate investigation report
```

5. 补充输出文件说明：
    

investigation 输出目录中包含：

- investigation_report.md
    
- investigation_state.json
    
- case_memory.json
    

6. 补充当前限制：
    

- planned_like / abnormal_like 仍是基于数据迹象的初步判断
    
- 没有施工日志时，不能确认计划停机或异常停机
    
- 需要结合现场施工记录、班次记录、检修记录进一步确认
    
- 多文件 investigate 受 max_iterations 限制，top-n 较大时建议调高 --max-iterations
    

7. 更新项目目录结构，加入：
    

```text
tbm_diag/investigation/
  state.py
  tools.py
  planner.py
  controller.py
  memory.py
  context_retriever.py
  report.py
```

8. 文档语气要求：
    

- 简洁务实
    
- 不夸大
    
- 不说“完全自动判断故障”
    
- 强调“疑似”“辅助核查”“需要施工日志确认”
    

二、新增 CLAUDE.md

请在项目根目录新增 CLAUDE.md，作为 Claude Code 后续工作的项目规范。

CLAUDE.md 必须包含以下规则：

1. 每次修改代码后必须测试
    

写清楚：

- 不允许只改代码不跑测试
    
- 至少运行与改动相关的 CLI 验证命令
    
- 如果改动影响核心链路，必须跑回归测试
    

推荐最小回归命令包括：

```bash
python -m tbm_diag.cli inspect --input incoming/anomaly_segment.csv
python -m tbm_diag.cli detect --input incoming/anomaly_segment.csv
python -m tbm_diag.cli scan --input-dir incoming --output-dir scan_test_out --overwrite
python -m tbm_diag.cli investigate --input sample2.xls --output-dir investigation_test_out --max-iterations 12
```

2. 测试成功后必须更新 README
    

写清楚：

- 如果新增 CLI 命令、参数、输出文件、配置项、模块能力，必须同步更新 README.md
    
- README 只能写已经实现并验证的功能
    
- 不允许在 README 里写未来规划当成已实现功能
    

3. 测试成功后必须提交和推送
    

写清楚：

- 测试通过后，必须执行 git status
    
- 确认改动范围合理
    
- git add 相关文件
    
- git commit 写清楚 message
    
- 如果已配置远程仓库，则执行 git push
    
- 如果没有远程仓库或 push 失败，要在输出里明确说明原因
    
- 不允许把 .env、API key、临时输出目录、扫描结果大文件提交进仓库
    

4. 敏感信息规则
    

写清楚：

- 不要把真实 API key 写入代码、README、sample_config、测试脚本或 commit
    
- .env 必须被 .gitignore 忽略
    
- .env.example 只能放占位符
    

5. 不要随意重构主链路
    

写清楚：

- ingestion / cleaning / detector / segmenter / evidence / explainer / state_engine 是稳定主链路
    
- 除非任务明确要求，否则不要大面积重构
    
- 新功能优先通过新增模块或小范围接入实现
    

6. 变更输出规范
    

每次完成任务后，Claude Code 必须输出：

- 改了哪些文件
    
- 跑了哪些测试
    
- 测试结果
    
- 是否更新 README
    
- 是否 commit
    
- 是否 push
    
- 如果没有 push，原因是什么
    

三、更新 .gitignore

请确认以下内容已在 .gitignore 中：

```gitignore
.env
investigation_out/
investigation_test_out/
scan_test_out/
review_test_out/
tmp_drag_runs/
```

如果没有，请补充。

四、提交与推送

完成 README.md、CLAUDE.md、.gitignore 修改后：

1. 运行基础验证：
    

```bash
python -m tbm_diag.cli investigate --help
python -m tbm_diag.cli investigate --input sample2.xls --output-dir investigation_test_out --max-iterations 12
```

2. 若测试通过，执行：
    

```bash
git status
git add README.md CLAUDE.md .gitignore
git commit -m "docs: update README and Claude Code workflow rules for investigation agent"
```

3. 如果远程仓库已配置，执行：
    

```bash
git push
```

4. 如果没有远程仓库或 push 失败，请不要伪造成功，必须明确输出原因。
    

五、输出要求

最后请输出：

- README 更新了哪些部分
    
- CLAUDE.md 包含哪些规则
    
- 跑了哪些测试
    
- 是否 commit 成功
    
- 是否 push 成功
    
- 如果未 push，原因是什么
    

不要新增功能，不要修改核心诊断逻辑。

```

---

这一步非常应该做，因为你现在项目已经复杂了。  
后面如果没有 `CLAUDE.md` 这种规则文件，Claude Code 很容易出现三种问题：

1. 改完不测  
2. 改了功能不更新 README  
3. 生成了东西但忘了 commit / push  

你加上这个文件以后，项目会更像一个真正可维护的工程。
```
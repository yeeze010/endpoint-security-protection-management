# Git 与 GitHub 工程规范

## 1. 分支模型

| 分支 | 用途 | 规则 |
|---|---|---|
| `main` | 稳定验收分支 | 只接受 Release 和 Hotfix 合并 |
| `develop` | 开发集成分支 | 所有功能 PR 合并目标 |
| `feature/<module>` | 功能开发 | 从 `develop` 拉出，PR 回 `develop` |
| `fix/<issue>` | 缺陷修复 | 从 `develop` 拉出 |
| `release/<version>` | 验收发布 | 从 `develop` 拉出，验收后合并 `main` |
| `hotfix/<issue>` | 生产紧急修复 | 从 `main` 拉出，合并回 `main` 和 `develop` |

## 2. Commit Message

使用 Conventional Commits：

| 类型 | 示例 |
|---|---|
| `feat` | `feat: add agent heartbeat api` |
| `fix` | `fix: correct policy conflict validation` |
| `docs` | `docs: update acceptance checklist` |
| `test` | `test: add alert workflow cases` |
| `ci` | `ci: add backend maven workflow` |
| `chore` | `chore: update local run script` |
| `refactor` | `refactor: split risk scoring service` |
| `perf` | `perf: optimize endpoint query` |

## 3. PR 规则

- PR 必须关联 Issue 或任务编号。
- PR 描述必须包含：变更内容、影响范围、测试结果、回滚方式。
- CI 必须通过。
- 至少 1 名 Reviewer 通过。
- 权限、策略、Agent 命令、文件恢复、审计相关 PR 必须由技术负责人 Review。

## 4. CI/CD 检查

| Job | 内容 |
|---|---|
| Backend | Java 21、Maven Test、打包 |
| Frontend | npm install、typecheck、build |
| Deliverables | 检查 docs、diagram、验收文件存在 |
| Security | 依赖扫描、密钥扫描、基础 SAST |

## 5. Release 与 Tag

| Tag | 含义 |
|---|---|
| `v0.1.0` | 工程骨架和文档体系 |
| `v0.3.0` | 终端资产、Agent、权限初版 |
| `v0.5.0` | 策略、补丁、告警主流程联调 |
| `v0.8.0` | 测试演示版 |
| `v1.0.0` | 正式验收版 |

## 6. GitHub Issue 模板建议

### 功能任务

- 背景
- 目标
- 影响模块
- API/页面/数据模型
- 验收标准

### 缺陷

- 现象
- 复现步骤
- 期望结果
- 实际结果
- 日志/截图
- 影响范围

## 7. Review 修改处理

1. 汇总未解决线程。
2. 标记必须修改、建议优化、解释说明。
3. 必须修改项提交修复。
4. 建议优化项进入后续任务或本次处理。
5. 解释说明项在 PR 回复。
6. 全部处理后请求复审。

## 8. 禁止事项

- 不提交 `.env`、密钥、证书、令牌。
- 不在 PR 中粘贴生产凭证。
- 不绕过 CI 合并主干。
- 不删除已发布 Tag；问题版本用后续修复版替代。
- 不在未审批情况下发布生产环境。

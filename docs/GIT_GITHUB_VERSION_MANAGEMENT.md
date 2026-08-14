# Git 与 GitHub 版本管理方案

## 1. 本地 Git 初始化步骤

当前项目必须初始化为 Git 仓库，并建立 `main` 与 `develop` 双主线分支。

```bash
git init
git config user.name "Codex"
git config user.email "codex@example.local"
git branch -M main
git add .
git commit -m "chore: initialize project structure"
git checkout -b develop
```

绑定 GitHub 远程仓库时，将 `<org>` 与 `<repo-name>` 替换为真实组织和仓库名：

```bash
git remote add origin https://github.com/<org>/<repo-name>.git
git push -u origin main
git push -u origin develop
```

## 2. 分支模型

| 分支 | 用途 | 合并目标 | 说明 |
|---|---|---|---|
| `main` | 稳定验收版本 | 无 | 只保留可交付、可回滚、可打 Tag 的版本 |
| `develop` | 开发集成 | `main` 或 `release/*` | 日常功能联调基线 |
| `feature/<module>` | 功能开发 | `develop` | 例如 `feature/endpoint-assets` |
| `fix/<issue>` | 缺陷修复 | `develop` | 例如 `fix/policy-conflict-check` |
| `release/<version>` | 发布验收 | `main` 与 `develop` | 例如 `release/v1.0.0` |
| `hotfix/<issue>` | 生产紧急修复 | `main` 与 `develop` | 修复后必须同步回开发线 |

## 3. Commit Message 规范

统一使用 Conventional Commits，便于生成变更日志、Release 说明和 CI 规则。

| 类型 | 说明 | 示例 |
|---|---|---|
| `feat` | 新功能 | `feat: add endpoint asset module` |
| `fix` | 修复问题 | `fix: resolve alert assignment status error` |
| `docs` | 文档变更 | `docs: update deployment guide` |
| `style` | 代码格式调整 | `style: format policy form component` |
| `refactor` | 重构 | `refactor: split alert service workflow` |
| `test` | 测试相关 | `test: add policy publish integration tests` |
| `chore` | 构建、依赖、脚手架 | `chore: initialize project structure` |
| `ci` | CI/CD 配置 | `ci: add github actions workflow` |
| `perf` | 性能优化 | `perf: optimize endpoint heartbeat query` |
| `revert` | 回滚提交 | `revert: revert policy publish change` |

## 4. Tag 版本规划

| 版本 | 阶段 | 验收含义 |
|---|---|---|
| `v0.1.0` | 项目初始化 | 基础目录、框架、README、Git 规范完成 |
| `v0.3.0` | 核心模块初版 | 登录、权限、资产、Agent 心跳初步完成 |
| `v0.5.0` | 主要功能联调 | 策略、任务、告警、审计主要链路可联调 |
| `v0.8.0` | 测试演示版 | 测试环境可演示，进入缺陷收敛 |
| `v1.0.0` | 正式验收版 | 通过验收测试并形成 Release 归档 |

## 5. Git 与 GitHub 协作流程

1. 从 `develop` 创建功能分支。
2. 在功能分支完成开发。
3. 本地运行 lint、test、build。
4. 使用规范 Commit 提交。
5. 推送到 GitHub。
6. 创建 Pull Request 到 `develop`。
7. GitHub Actions 自动执行检查。
8. Review 通过后合并。
9. 阶段完成后从 `develop` 创建 `release/<version>`。
10. 验收通过后合并到 `main`。
11. 在 `main` 打 Tag。
12. 在 GitHub 创建 Release，并上传验收材料。

## 6. PR 合并策略

- 功能分支合并到 `develop`：使用 Squash Merge，保持主线历史清晰。
- `release/*` 合并到 `main`：使用 Merge Commit，保留发布分支完整上下文。
- `hotfix/*` 合并到 `main`：使用 Merge Commit，并立即反向合并到 `develop`。
- 所有 PR 必须至少 1 人 Review 通过。
- 涉及权限、安全策略、审计、补丁任务的 PR 必须由技术负责人 Review。
- CI 未通过不得合并；如需例外合并，必须在 PR 中说明风险和补救计划。

## 7. 回滚策略

### 普通功能回滚

```bash
git checkout develop
git pull origin develop
git revert <commit-sha>
git push origin develop
```

### 发布版本回滚

```bash
git checkout main
git pull origin main
git checkout -b hotfix/rollback-v1.0.0
git revert <release-merge-commit-sha>
git push -u origin hotfix/rollback-v1.0.0
```

随后创建 PR 到 `main`，Review 与 CI 通过后合并，并同步回 `develop`。

### Tag 回滚说明

已发布 Tag 不建议删除。若 `v1.0.0` 存在问题，应发布 `v1.0.1` 修复版本，并在 GitHub Release 中标注 `v1.0.0` 已废弃或不推荐使用。

## 8. 验收版本封版流程

```bash
git checkout develop
git pull origin develop

git checkout -b release/v1.0.0
git add .
git commit -m "chore: prepare v1.0.0 acceptance release"
git push -u origin release/v1.0.0
```

在 GitHub 创建 `release/v1.0.0 -> main` 的 PR。验收通过后执行：

```bash
git checkout main
git pull origin main
git merge --no-ff release/v1.0.0
git tag -a v1.0.0 -m "v1.0.0 acceptance release"
git push origin main
git push origin v1.0.0
```

GitHub Release 内容应包括：

- 版本号：`v1.0.0`
- 发布日期
- 功能清单
- 修复清单
- 数据库迁移说明
- 部署说明
- 验收报告
- 已知问题与风险接受项

## 9. 功能开发命令模板

```bash
git checkout develop
git pull origin develop

git checkout -b feature/user-auth

git add .
git commit -m "feat: add user authentication module"

git push -u origin feature/user-auth
```

## 10. GitHub Actions 建议

建议为前端、后端和文档交付分别配置检查：

- 前端：install、lint、typecheck、test、build。
- 后端：compile、unit test、integration test、dependency scan。
- 文档：检查关键交付物是否存在，防止验收材料遗漏。

失败处理流程：

1. 使用 GitHub Actions 日志定位失败步骤。
2. 在对应分支修复。
3. 本地复现并验证。
4. 推送后等待 CI 重新运行。
5. CI 全部通过后再进入 Review 或合并。

## 11. PR Review 修改处理

1. 汇总未解决 Review 意见。
2. 区分必须修改、建议优化、解释说明三类。
3. 对必须修改项提交修复 Commit。
4. 对无需改代码的意见，在 PR 中回复原因。
5. Review 线程全部处理后再请求复审。

## 12. 当前项目远程仓库绑定待办

当前本地仓库尚未绑定真实 GitHub 远程地址。确认 GitHub 组织和仓库名后执行：

```bash
git remote add origin https://github.com/<org>/<repo-name>.git
git push -u origin main
git push -u origin develop
```

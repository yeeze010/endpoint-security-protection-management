# 终端安全防护管理平台

本项目用于建设面向企业终端安全运营的防护管理平台，覆盖终端资产台账、Agent 状态采集、安全策略下发、告警处置闭环、漏洞补丁、外设管控、审计日志、报表导出与验收归档。

## 技术栈建议

- 前端：Vue 3 + TypeScript + Vite + Pinia + Vue Router
- 后端：Spring Boot 3 + Java 21
- 数据库：PostgreSQL
- 缓存：Redis
- 文件存储：MinIO
- 部署：Docker + Nginx
- 协作：Git + GitHub + Pull Request + GitHub Actions

## 当前交付物

- `backend/`：Spring Boot 后端接口服务
- `frontend/`：Vue 3 + TypeScript 管理后台
- `infra/`：Docker Compose 与 Nginx 部署配置
- `.github/workflows/ci.yml`：GitHub Actions 检查流程
- `deliverables/终端安全防护管理平台_项目交付方案.docx`
- `deliverables/终端安全防护管理平台_开发排期分工测试用例.xlsx`
- `diagram/endpoint-security-platform/system-architecture.svg`
- `diagram/endpoint-security-platform/business-flow.svg`
- `diagram/endpoint-security-platform/data-flow.svg`
- `docs/GIT_GITHUB_VERSION_MANAGEMENT.md`
- `docs/DEVELOPMENT.md`

## 快速启动

Windows 本地一键启动：

```powershell
.\scripts\start-local.ps1
```

后端：

```bash
cd backend
mvn spring-boot:run
```

前端：

```bash
cd frontend
npm install
npm run dev
```

Docker:

```bash
cd infra
docker compose up -d --build
```

## 分支模型

- `main`：稳定主分支，仅接收验收通过的版本。
- `develop`：开发集成分支，功能分支合并目标。
- `feature/<module>`：功能开发分支。
- `fix/<issue>`：缺陷修复分支。
- `release/<version>`：验收发布分支。
- `hotfix/<issue>`：生产紧急修复分支。

## 提交规范

使用 Conventional Commits：

- `feat:` 新功能
- `fix:` 修复问题
- `docs:` 文档变更
- `style:` 代码格式调整
- `refactor:` 重构
- `test:` 测试相关
- `chore:` 构建、配置、脚手架
- `ci:` CI/CD 配置
- `perf:` 性能优化
- `revert:` 回滚提交

## 版本规划

- `v0.1.0`：项目初始化与基础框架
- `v0.3.0`：核心模块初版
- `v0.5.0`：主要功能联调完成
- `v0.8.0`：测试环境可演示版本
- `v1.0.0`：正式验收版本

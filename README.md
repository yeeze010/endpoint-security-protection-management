# 终端安全防护管理平台

终端安全防护管理平台面向企业安全运营、终端运维和审计治理场景，覆盖终端资产纳管、安全策略下发、告警闭环处置、合规报表和项目验收交付等核心能力。本仓库当前提供 `v0.1.0` 演示版的前后端最小闭环与交付材料。

## 项目结构

| 目录 | 说明 |
| --- | --- |
| `backend/` | Spring Boot 3 后端服务 |
| `frontend/` | Vue 3 + TypeScript 前端控制台 |
| `infra/` | Docker Compose 与 Nginx 配置 |
| `docs/` | 需求、设计、API、测试、部署、验收文档 |
| `diagram/` | 系统架构、业务流和数据流图 |
| `deliverables/` | 交付方案、排期与测试材料 |
| `scripts/` | 本地启动脚本 |

## 当前能力

1. 安全态势总览：资产覆盖、Agent 在线率、告警队列、合规指标。
2. 终端资产中心：终端列表、画像详情、风险评分和设备状态。
3. 策略下发中心：策略新建、审批、灰度发布和回滚状态流转。
4. 告警闭环中心：研判、派单、处置、复核和关闭链路。
5. 合规报表中心：关键指标、部门风险对比与导出提示。
6. 验收中心：测试项、证据材料、整改优先级和交付就绪提示。
7. 审计日志：关键操作留痕与项目验收支持。

## 本地运行

### 根目录命令

```powershell
cmd /c npm run dev
cmd /c npm run build
cmd /c npm run test
cmd /c npm run preview:web
cmd /c npm run start:local
```

根目录脚本会代理到 `frontend/` 和 `backend/`，适合直接做联调、构建和验收。

### 前端单独运行

```powershell
cd frontend
cmd /c npm install
cmd /c npm run dev
cmd /c npm run build
cmd /c npm run preview
```

### 后端单独运行

```powershell
cd backend
mvn spring-boot:run
```

## 访问地址

固定端口定义在项目根目录 `.env.ports`；开发与预览均启用 `strictPort`。

- 前端开发地址：`http://127.0.0.1:5203`
- 前端预览地址：`http://127.0.0.1:6203`
- 后端接口地址：`http://127.0.0.1:8203/api`
- 后端健康检查：`http://127.0.0.1:8203/actuator/health`

## 本轮验收记录

- 已新增根目录 `package.json`，补齐统一开发、构建、测试与本地启动入口。
- 已重做前端控制台壳层与配色，切换为更适合安全运营场景的深色高对比控制台风格。
- 已将移动端导航改为抽屉式入口，避免导航在小屏设备占满首屏。
- 已执行 `cmd /c npm run build` 与 `mvn -f backend/pom.xml test`，结果通过。
- 已使用浏览器检查桌面端与 `390px` 移动端页面，并确认当前控制台无前端错误日志。

## 文档索引

- [需求规格说明](docs/REQUIREMENTS_SPEC.md)
- [系统设计](docs/SYSTEM_DESIGN.md)
- [API 规格说明](docs/API_SPEC.md)
- [测试计划](docs/TEST_PLAN.md)
- [部署指南](docs/DEPLOYMENT_GUIDE.md)
- [验收标准](docs/ACCEPTANCE_CRITERIA.md)

## 后续重点

1. 将演示数据替换为真实后端接口或更完整的 Mock Service。
2. 增补 JWT、RBAC 和数据权限。
3. 补齐自动化测试与端到端验收脚本。
4. 打通报表导出、证据归档和权限验收材料。

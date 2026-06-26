# 计算机终端安全防护管理系统文档索引

本文档集用于指导《计算机终端安全防护管理系统》从功能结构完善、工程开发、测试部署到验收归档的全流程工作。

## 文档结构

| 目录 | 文档 | 用途 |
|---|---|---|
| `docs/requirements/` | `product-requirements.md` | 项目定位、用户角色、功能模块、权限矩阵、业务规则 |
| `docs/architecture/` | `system-architecture.md` | 系统架构、核心流程、数据流、风险评分与 Agent 通信 |
| `docs/design/` | `ui-ux-design.md` | 后台页面清单、交互结构、表单/看板/响应式设计 |
| `docs/api/` | `api-plan.md` | API 接口规划、数据模型、事件与文件接口 |
| `docs/test/` | `test-plan.md` | 测试策略、测试用例分层、质量门禁 |
| `docs/deployment/` | `deployment-plan.md` | Docker/Nginx/PostgreSQL/Redis/MinIO 部署方案 |
| `docs/deployment/` | `git-github-engineering.md` | Git/GitHub 分支、PR、CI、Release 工程规范 |
| `docs/acceptance/` | `acceptance-plan.md` | 验收标准、里程碑、交付物清单 |

## 能力应用说明

- `gstack`：用于工程闭环、测试验证、验收路径和“可运行再交付”的执行口径。
- `frontend-design`：用于确定后台界面的视觉方向、内容纪律和设计系统。
- `ui-ux-pro-max`：用于表单、表格、看板、响应式、可访问性、加载/错误/空态等体验规则。
- `baoyu-diagram`：用于在 `docs/architecture/` 下生成系统架构图、业务流程图、Agent 通信图。
- `documents`：用于按正式项目文档方式组织需求、设计、部署、验收材料。
- `spreadsheets`：用于把里程碑、测试计划、权限矩阵、验收清单设计成可转表格的结构。
- `github`：用于 Git/GitHub 分支、PR、CI、Review、Release、验收归档规范。

## 当前重点细化范围

1. 终端资产台账与 Agent 状态采集。
2. Agent 与管理端通信、心跳、事件上报、策略拉取。
3. 安全策略配置、审批、灰度、下发、回滚。
4. 补丁状态、病毒防护状态、外设管控、软件白名单。
5. 终端风险评分模型与安全合规报表。
6. 告警发现、派单、处置、复核、归档闭环。
7. 文件附件上传、证据留存、隔离文件、报表导出。
8. Git/GitHub 工程协作、测试部署与最终验收。

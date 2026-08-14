# 计算机终端安全防护管理系统部署方案

## 1. 部署目标

支持本地开发、演示环境和后续预生产环境的一致化部署，保证平台具备基本可运行、可验证和可交接能力。

## 2. 目录与组件

| 目录 | 作用 |
|---|---|
| `backend/` | Spring Boot 后端服务 |
| `frontend/` | Vue 管理端 |
| `infra/` | Docker Compose 与 Nginx 配置 |
| `scripts/` | 本地启动脚本 |
| `docs/` | 需求、设计、测试、部署、验收文档 |

## 3. 本地开发部署

### 3.1 前置条件

1. 已安装 JDK 21。
2. 已安装 Node.js 22。
3. PowerShell 可执行项目脚本。

### 3.2 一键启动

```powershell
.\scripts\start-local.ps1
```

脚本将执行：

1. 后端打包。
2. 启动后端并检查 `http://localhost:8203/actuator/health`。
3. 前端构建。
4. 启动前端并验证 `http://localhost:5203/dashboard`。
5. 校验前端代理访问 `/api/endpoints`。

### 3.3 手工启动

后端：

```powershell
cd backend
mvn spring-boot:run
```

前端：

```powershell
cd frontend
npm install
npm run dev
```

## 4. Docker 演示部署

```powershell
cd infra
docker compose up -d --build
```

### 4.1 端口规划

| 组件 | 地址 |
|---|---|
| Nginx 入口 | `http://localhost` |
| Docker 统一入口 | `http://localhost:5203` |
| 后端健康检查 | `http://localhost/actuator/health` |
| PostgreSQL | `localhost:5432` |
| Redis | `localhost:6379` |
| MinIO API | `localhost:9000` |
| MinIO Console | `http://localhost:9001` |

## 5. 环境变量规划

当前演示环境存在默认凭据，生产化前必须替换为外部注入：

| 变量 | 当前状态 | 生产建议 |
|---|---|---|
| `POSTGRES_PASSWORD` | compose 明文 | 由密钥平台注入 |
| `MINIO_ROOT_USER` | compose 明文 | 由密钥平台注入 |
| `MINIO_ROOT_PASSWORD` | compose 明文 | 由密钥平台注入 |
| `SPRING_PROFILES_ACTIVE` | `docker` | 区分 dev/test/prod |

## 6. CI/CD 规划

1. PR 与 `develop`、`main` 推送触发 CI。
2. 后端执行 Maven 测试。
3. 前端执行安装与构建。
4. 交付任务检查核心文档和图示。
5. 下一阶段补齐镜像构建、制品归档、安全扫描和部署预演。

## 7. 回滚方案

1. 演示环境通过切换上一个镜像版本或 Git Tag 回滚。
2. 数据库变更通过新增迁移脚本修复，不直接篡改历史脚本。
3. 前端静态站点保留上一版本构建物，必要时回切 Nginx 发布目录。

## 8. 运维检查清单

1. 后端健康检查返回 `UP`。
2. 前端可访问并代理后端接口。
3. PostgreSQL、Redis、MinIO 容器均为健康状态。
4. 核心日志路径存在且可读。
5. 交付文档已同步到仓库。

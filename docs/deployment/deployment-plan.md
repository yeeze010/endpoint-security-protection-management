# 部署方案

## 1. 部署目标

部署方案服务于开发、测试、演示和验收环境。第一阶段以 Docker Compose 为主，生产可演进到 Kubernetes。所有服务必须具备健康检查、日志、备份、回滚和配置隔离能力。

## 2. 服务清单

| 服务 | 端口 | 说明 |
|---|---:|---|
| `frontend` | 80/5203 | Vue 管理后台 |
| `backend` | 8203 | Spring Boot API |
| `postgres` | 5432 | 业务数据库 |
| `redis` | 6379 | 缓存、限流、任务状态 |
| `minio` | 9000/9001 | 文件对象存储 |
| `nginx` | 80/443 | HTTPS、静态资源、反向代理 |

## 3. 环境划分

| 环境 | 用途 | 数据要求 |
|---|---|---|
| `dev` | 开发联调 | 可使用样例数据 |
| `test` | 测试验证 | 接近真实规模的脱敏数据 |
| `staging` | 验收演示 | 验收基线数据，不随意变更 |
| `prod` | 生产运行 | 严格备份、审计和变更审批 |

## 4. 配置项

| 配置 | 示例 | 说明 |
|---|---|---|
| `SPRING_PROFILES_ACTIVE` | `docker` | 后端环境 |
| `DATABASE_URL` | `jdbc:postgresql://postgres:5432/endpoint_security` | 数据库 |
| `REDIS_HOST` | `redis` | Redis 地址 |
| `MINIO_ENDPOINT` | `http://minio:9000` | MinIO 地址 |
| `JWT_SECRET` | 由密钥管理系统注入 | 不得提交到仓库 |
| `AGENT_TOKEN_SECRET` | 由密钥管理系统注入 | Agent 注册令牌 |

## 5. 发布流程

1. 从 `develop` 创建 `release/<version>`。
2. CI 运行前端构建、后端测试、文档检查。
3. 构建后端镜像与前端镜像。
4. 执行数据库迁移。
5. 部署到 `staging`。
6. 执行冒烟测试与验收测试。
7. 验收通过后合并到 `main` 并打 Tag。
8. 生成 GitHub Release，归档验收材料。

## 6. 回滚方案

| 类型 | 回滚动作 |
|---|---|
| 前端发布失败 | 回退 Nginx 静态资源镜像版本 |
| 后端发布失败 | 回退 Spring Boot 镜像版本 |
| 数据库迁移失败 | 停止发布，执行迁移回滚脚本或恢复备份 |
| 策略误发布 | 策略中心回滚上一稳定版本 |
| Agent 升级失败 | Agent 升级任务停止，回滚上一 Agent 版本 |

## 7. 备份策略

- PostgreSQL：每日全量，每小时 WAL，保留 30 天。
- MinIO：每日增量，保留 90 天；隔离文件按安全策略保留。
- Redis：仅缓存数据，不作为唯一持久化来源。
- 审计日志：长期归档，至少 1 年。

## 8. 监控与日志

| 对象 | 指标 |
|---|---|
| 后端 | QPS、P95、错误率、JVM、线程池 |
| 数据库 | 连接数、慢查询、锁等待、磁盘 |
| Redis | 内存、命中率、连接数、阻塞 |
| MinIO | 容量、对象数、错误率 |
| Agent | 在线率、心跳延迟、上报失败 |

## 9. 本地启动

当前项目已提供：

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\start-local.ps1
```

本地默认：

- 前端：`http://localhost:5203`
- 后端：`http://localhost:8203`
- 健康检查：`http://localhost:8203/actuator/health`

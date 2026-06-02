# 开发运行说明

## 本地开发

### 后端

```bash
cd backend
mvn spring-boot:run
```

后端默认地址：

- API: `http://localhost:8080/api`
- 健康检查: `http://localhost:8080/actuator/health`

### 前端

```bash
cd frontend
npm install
npm run dev
```

前端默认地址：

- `http://localhost:5173`

Vite 已将 `/api` 代理到 `http://localhost:8080`。

## Docker 部署

```bash
cd infra
docker compose up -d --build
```

部署后访问：

- 平台入口：`http://localhost`
- 前端容器直连：`http://localhost:5174`
- 后端健康检查：`http://localhost/actuator/health`
- MinIO 控制台：`http://localhost:9001`

## 当前已实现接口

| 方法 | 路径 | 说明 |
|---|---|---|
| `POST` | `/api/auth/login` | 开发态登录接口 |
| `GET` | `/api/dashboard/overview` | 安全态势总览 |
| `GET` | `/api/endpoints` | 终端资产列表 |
| `GET` | `/api/endpoints/{id}` | 终端详情 |
| `GET` | `/api/policies` | 策略列表 |
| `GET` | `/api/alerts` | 告警列表 |
| `GET` | `/api/audit-logs` | 审计日志列表 |

## 当前已实现页面

| 页面 | 路径 | 说明 |
|---|---|---|
| 安全态势 | `/dashboard` | 指标卡、告警趋势、风险分布 |
| 终端资产 | `/endpoints` | 资产表格、关键字筛选 |
| 策略中心 | `/policies` | 策略卡片列表 |
| 告警处置 | `/alerts` | 告警闭环列表 |
| 审计日志 | `/audit` | 操作审计时间线 |

## 下一阶段开发建议

1. 接入 PostgreSQL、Flyway、JPA/MyBatis Plus，替换当前内存示例数据。
2. 完成真实认证授权：JWT、刷新令牌、RBAC、数据权限。
3. 补齐 Agent 注册、心跳、事件批量上报、策略增量拉取。
4. 建设策略编辑器：目标范围、规则配置、冲突检测、灰度发布、回滚。
5. 建设告警详情和工单状态机：研判、派单、处置、复核、关闭。
6. 增加单元测试、接口测试、前端组件测试和端到端验收测试。

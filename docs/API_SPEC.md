# 终端安全防护管理平台 API 规格说明

## 1. 统一约定

- 基础路径：`/api`
- 返回格式：`ApiResponse<T>`
- 内容类型：`application/json`
- 鉴权方式：当前为演示态，后续采用 `Bearer Token`

## 2. 认证接口

### 2.1 登录

- 方法：`POST`
- 路径：`/api/auth/login`

请求体示例：

```json
{
  "username": "admin",
  "password": "admin123"
}
```

响应体示例：

```json
{
  "success": true,
  "message": "OK",
  "data": {
    "accessToken": "dev-access-token",
    "refreshToken": "dev-refresh-token",
    "username": "admin",
    "roleName": "安全管理员",
    "permissions": ["dashboard", "endpoints", "policies", "alerts", "audit"]
  }
}
```

## 3. 仪表盘接口

### 3.1 查询安全态势总览

- 方法：`GET`
- 路径：`/api/dashboard/overview`

返回字段：

- `metricCards`: 指标卡数组
- `trend`: 趋势点数组
- `riskDistribution`: 风险分布数组

## 4. 终端资产接口

### 4.1 查询终端列表

- 方法：`GET`
- 路径：`/api/endpoints`
- 查询参数：
  - `keyword`：可选，按主机名、IP、部门模糊过滤

### 4.2 查询终端详情

- 方法：`GET`
- 路径：`/api/endpoints/{id}`
- 路径参数：
  - `id`：终端标识

失败响应示例：

```json
{
  "success": false,
  "message": "endpoint not found",
  "data": null
}
```

## 5. 策略接口

### 5.1 查询策略列表

- 方法：`GET`
- 路径：`/api/policies`

返回字段建议包含：

- `id`
- `name`
- `type`
- `version`
- `status`
- `priority`
- `targetScope`
- `updatedAt`

## 6. 告警接口

### 6.1 查询告警列表

- 方法：`GET`
- 路径：`/api/alerts`

返回字段建议包含：

- `id`
- `title`
- `severity`
- `status`
- `endpointName`
- `owner`
- `occurredAt`

## 7. 审计接口

### 7.1 查询审计日志

- 方法：`GET`
- 路径：`/api/audit-logs`

返回字段建议包含：

- `id`
- `operator`
- `action`
- `resourceType`
- `resourceName`
- `createdAt`

## 8. 待补接口规划

| 方法 | 路径 | 说明 |
|---|---|---|
| `POST` | `/api/endpoints/register` | Agent 注册 |
| `POST` | `/api/endpoints/{id}/heartbeat` | Agent 心跳 |
| `POST` | `/api/policies` | 新建策略 |
| `PUT` | `/api/policies/{id}` | 编辑策略 |
| `POST` | `/api/policies/{id}/publish` | 发布策略 |
| `POST` | `/api/alerts/{id}/assign` | 派单或指派 |
| `POST` | `/api/tickets/{id}/close` | 关闭工单 |
| `GET` | `/api/reports/security-overview` | 报表导出 |

## 9. 错误码规划

| 错误码 | 含义 | 处理建议 |
|---|---|---|
| `AUTH_401` | 未认证 | 重新登录 |
| `AUTH_403` | 无权限 | 提示并记录审计 |
| `ENDPOINT_404` | 终端不存在 | 检查终端标识 |
| `POLICY_409` | 策略冲突 | 返回冲突明细 |
| `ALERT_422` | 告警状态非法 | 阻止无效流转 |
| `SYS_500` | 系统异常 | 记录 traceId 并排查 |

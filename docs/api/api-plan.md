# API 与数据模型规划

## 1. API 设计原则

- 统一前缀：`/api`
- 统一响应：`success`、`data`、`message`、`traceId`、`timestamp`
- 统一分页：`page`、`pageSize`、`total`、`items`
- 统一鉴权：`Authorization: Bearer <token>`
- 统一幂等：高频上报和任务执行使用 `Idempotency-Key`
- 统一审计：策略、处置、导出、文件、权限变更必须审计

## 2. 核心数据模型

| 表 | 说明 | 关键字段 |
|---|---|---|
| `users` | 用户 | `id`、`username`、`real_name`、`status`、`org_id` |
| `roles` | 角色 | `id`、`code`、`name`、`status` |
| `permissions` | 权限 | `id`、`code`、`resource`、`action` |
| `organizations` | 组织 | `id`、`parent_id`、`name`、`path` |
| `endpoints` | 终端资产 | `id`、`agent_id`、`hostname`、`ip`、`risk_score`、`online_status` |
| `endpoint_inventory` | 软硬件清单 | `endpoint_id`、`cpu`、`memory`、`disk`、`apps_json` |
| `agents` | Agent | `endpoint_id`、`version`、`heartbeat_at`、`upgrade_status` |
| `agent_heartbeats` | 心跳历史 | `agent_id`、`status_json`、`reported_at` |
| `policies` | 策略 | `name`、`type`、`version`、`status`、`priority` |
| `policy_rules` | 策略规则 | `policy_id`、`rule_key`、`rule_value_json` |
| `policy_targets` | 策略目标 | `policy_id`、`target_type`、`target_id` |
| `policy_dispatches` | 策略下发 | `policy_id`、`endpoint_id`、`status`、`result_json` |
| `patch_statuses` | 补丁状态 | `endpoint_id`、`missing_count`、`critical_missing_count` |
| `antivirus_statuses` | 病毒防护状态 | `endpoint_id`、`engine_status`、`signature_version`、`last_scan_at` |
| `device_control_rules` | 外设规则 | `device_type`、`action`、`policy_id` |
| `device_events` | 外设事件 | `endpoint_id`、`device_type`、`action`、`occurred_at` |
| `software_inventory` | 软件清单 | `endpoint_id`、`name`、`version`、`publisher` |
| `software_whitelist_rules` | 软件白名单 | `name_pattern`、`hash`、`action`、`scope` |
| `risk_scores` | 风险评分 | `endpoint_id`、`score`、`level`、`factor_json` |
| `security_alerts` | 告警 | `endpoint_id`、`severity`、`title`、`status` |
| `incident_tickets` | 工单 | `alert_id`、`assignee_id`、`status`、`closed_at` |
| `file_objects` | 文件附件 | `bucket`、`object_key`、`sha256`、`purpose` |
| `audit_logs` | 审计 | `actor_id`、`action`、`resource_type`、`detail_json` |

## 3. 接口规划

### 3.1 认证与权限

| 方法 | 路径 | 说明 |
|---|---|---|
| `POST` | `/api/auth/login` | 登录 |
| `POST` | `/api/auth/refresh` | 刷新令牌 |
| `POST` | `/api/auth/mfa/verify` | MFA 校验 |
| `GET` | `/api/me` | 当前用户、角色、菜单权限 |
| `GET` | `/api/roles` | 角色列表 |
| `PUT` | `/api/roles/{id}/permissions` | 更新角色权限 |

### 3.2 终端资产与 Agent

| 方法 | 路径 | 说明 |
|---|---|---|
| `GET` | `/api/endpoints` | 终端分页查询 |
| `GET` | `/api/endpoints/{id}` | 终端详情 |
| `GET` | `/api/endpoints/{id}/inventory` | 软硬件清单 |
| `POST` | `/api/agents/register` | Agent 注册 |
| `POST` | `/api/agents/heartbeat` | Agent 心跳 |
| `POST` | `/api/agents/events` | Agent 事件批量上报 |
| `GET` | `/api/agents/{agentId}/policy-sync` | 策略增量拉取 |
| `POST` | `/api/agents/{agentId}/task-results` | 任务执行结果上报 |
| `POST` | `/api/agents/upgrade-tasks` | 创建 Agent 升级任务 |

### 3.3 策略与下发

| 方法 | 路径 | 说明 |
|---|---|---|
| `GET` | `/api/policies` | 策略列表 |
| `POST` | `/api/policies` | 创建策略 |
| `PUT` | `/api/policies/{id}` | 更新策略 |
| `POST` | `/api/policies/{id}/validate` | 冲突检测 |
| `POST` | `/api/policies/{id}/submit` | 提交审批 |
| `POST` | `/api/policies/{id}/approve` | 审批通过 |
| `POST` | `/api/policies/{id}/publish` | 发布策略 |
| `POST` | `/api/policies/{id}/rollback` | 回滚策略 |
| `GET` | `/api/policies/{id}/dispatches` | 下发结果 |

### 3.4 补丁、病毒、外设、白名单

| 方法 | 路径 | 说明 |
|---|---|---|
| `GET` | `/api/patch-statuses` | 补丁状态列表 |
| `POST` | `/api/patch-tasks` | 创建补丁任务 |
| `GET` | `/api/antivirus-statuses` | 病毒防护状态 |
| `POST` | `/api/scan-tasks` | 创建扫描任务 |
| `GET` | `/api/device-control/rules` | 外设规则 |
| `POST` | `/api/device-control/rules` | 新建外设规则 |
| `GET` | `/api/device-control/events` | 外设违规事件 |
| `GET` | `/api/software-whitelist/rules` | 软件白名单规则 |
| `POST` | `/api/software-whitelist/rules` | 新建白名单规则 |

### 3.5 风险、告警、工单

| 方法 | 路径 | 说明 |
|---|---|---|
| `GET` | `/api/risks/endpoints` | 终端风险排行 |
| `GET` | `/api/risks/{endpointId}` | 风险评分明细 |
| `POST` | `/api/risks/recalculate` | 重新计算风险 |
| `GET` | `/api/alerts` | 告警列表 |
| `GET` | `/api/alerts/{id}` | 告警详情 |
| `POST` | `/api/alerts/{id}/assign` | 告警派单 |
| `POST` | `/api/alerts/{id}/actions/isolate-file` | 隔离文件 |
| `POST` | `/api/incidents/{id}/close` | 关闭工单 |

### 3.6 文件、报表、审计

| 方法 | 路径 | 说明 |
|---|---|---|
| `POST` | `/api/files/upload-url` | 获取预签名上传 URL |
| `GET` | `/api/files/{id}/download-url` | 获取下载 URL |
| `POST` | `/api/files/{id}/restore` | 隔离文件恢复申请 |
| `POST` | `/api/reports/export` | 创建报表导出任务 |
| `GET` | `/api/reports/jobs/{id}` | 导出任务状态 |
| `GET` | `/api/audit-logs` | 审计日志查询 |

## 4. Agent 心跳示例

```json
{
  "agentId": "agent-1001",
  "endpointId": "ep-1001",
  "agentVersion": "1.4.2",
  "policyVersion": 12,
  "onlineStatus": "online",
  "antivirus": {
    "engineStatus": "enabled",
    "signatureVersion": "2026.06.04",
    "lastScanAt": "2026-06-04T08:30:00+08:00"
  },
  "patch": {
    "missingCount": 3,
    "criticalMissingCount": 1
  },
  "deviceControl": {
    "lastBlockedAt": "2026-06-04T09:10:00+08:00"
  }
}
```

## 5. 错误码

| 错误码 | 说明 |
|---|---|
| `AUTH_INVALID_TOKEN` | 令牌无效 |
| `PERMISSION_DENIED` | 权限不足 |
| `ENDPOINT_NOT_FOUND` | 终端不存在 |
| `AGENT_NOT_REGISTERED` | Agent 未注册 |
| `POLICY_CONFLICT` | 策略冲突 |
| `TASK_ALREADY_RUNNING` | 任务已在执行 |
| `FILE_TYPE_DENIED` | 文件类型不允许 |
| `ALERT_ALREADY_CLOSED` | 告警已关闭 |

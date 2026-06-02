export interface ApiResponse<T> {
  success: boolean;
  data: T;
  message: string;
  traceId: string;
  timestamp: string;
}

export interface MetricCard {
  label: string;
  value: string;
  helper: string;
  tone: 'normal' | 'warning' | 'danger';
}

export interface DashboardOverview {
  metrics: MetricCard[];
  alertTrend: Array<{ date: string; alerts: number; highRisk: number }>;
  riskDistribution: Array<{ level: string; count: number }>;
}

export interface EndpointAsset {
  id: string;
  hostname: string;
  ip: string;
  os: string;
  department: string;
  owner: string;
  agentVersion: string;
  onlineStatus: string;
  riskLevel: string;
  riskScore: number;
  lastSeenAt: string;
}

export interface Policy {
  id: string;
  name: string;
  type: string;
  status: string;
  targetScope: string;
  priority: number;
  version: string;
}

export interface SecurityAlert {
  id: string;
  endpoint: string;
  title: string;
  severity: string;
  status: string;
  assignee: string;
  lastSeenAt: string;
}

export interface AuditLog {
  id: string;
  actor: string;
  action: string;
  resource: string;
  ip: string;
  createdAt: string;
}

export async function request<T>(path: string): Promise<T> {
  const response = await fetch(path);
  if (!response.ok) {
    throw new Error(`请求失败：${response.status}`);
  }
  const payload = (await response.json()) as ApiResponse<T>;
  if (!payload.success) {
    throw new Error(payload.message);
  }
  return payload.data;
}

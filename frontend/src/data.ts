export type RiskLevel = '低' | '中' | '高' | '严重';
export type OnlineStatus = '在线' | '离线' | '待确认';
export type PolicyStatus = '草稿' | '待审批' | '已批准' | '灰度中' | '已发布' | '已回滚';
export type AlertStatus = '待研判' | '已派单' | '处置中' | '待复核' | '已关闭';
export type MetricStatus = '达标' | '关注' | '未达标';

export interface EndpointAsset {
  id: string;
  hostname: string;
  ip: string;
  department: string;
  owner: string;
  os: string;
  onlineStatus: OnlineStatus;
  agentVersion: string;
  policyVersion: string;
  antivirusStatus: string;
  patchStatus: string;
  deviceControl: string;
  whitelistStatus: string;
  riskLevel: RiskLevel;
  riskScore: number;
  lastSeen: string;
  cpu: string;
  memory: string;
  disk: string;
  openAlerts: number;
  missingPatches: number;
  blockedDevices: number;
  unauthorizedApps: number;
}

export interface SecurityPolicy {
  id: string;
  name: string;
  type: string;
  status: PolicyStatus;
  targetScope: string;
  priority: number;
  version: string;
  owner: string;
  rollout: number;
  lastAction: string;
}

export interface SecurityAlert {
  id: string;
  title: string;
  severity: RiskLevel;
  status: AlertStatus;
  endpointId: string;
  endpoint: string;
  owner: string;
  evidence: string;
  createdAt: string;
  sla: string;
  timeline: string[];
}

export interface ReportMetric {
  label: string;
  value: string;
  target: string;
  status: MetricStatus;
}

export interface AcceptanceItem {
  id: string;
  module: string;
  item: string;
  proof: string;
  done: boolean;
  owner: string;
  dueAt: string;
  nextAction: string;
}

export interface AuditLog {
  time: string;
  actor: string;
  action: string;
  target: string;
  result: string;
}

export interface ReportPackage {
  id: string;
  name: string;
  scope: string;
  status: '待生成' | '生成中' | '可下载';
  owner: string;
  updatedAt: string;
}

export const endpoints: EndpointAsset[] = [
  {
    id: 'ep-1001',
    hostname: 'FIN-PC-023',
    ip: '10.16.4.23',
    department: '财务部',
    owner: '林晨',
    os: 'Windows 11 23H2',
    onlineStatus: '在线',
    agentVersion: '1.4.2',
    policyVersion: 'v12',
    antivirusStatus: '防病毒已开启，病毒库今日完成更新',
    patchStatus: '缺少 2 个重要补丁',
    deviceControl: '移动存储已阻断',
    whitelistStatus: '命中 1 条白名单例外',
    riskLevel: '中',
    riskScore: 58,
    lastSeen: '3 分钟前',
    cpu: 'Intel i5-12400',
    memory: '16 GB',
    disk: '512 GB SSD',
    openAlerts: 1,
    missingPatches: 2,
    blockedDevices: 3,
    unauthorizedApps: 1
  },
  {
    id: 'ep-1002',
    hostname: 'OPS-SRV-007',
    ip: '10.20.8.7',
    department: '运维部',
    owner: '周洋',
    os: 'Ubuntu Server 22.04',
    onlineStatus: '在线',
    agentVersion: '1.4.2',
    policyVersion: 'v12',
    antivirusStatus: 'Linux 防护策略正常',
    patchStatus: '缺少 1 个高危补丁',
    deviceControl: '服务器外设接口禁用',
    whitelistStatus: '软件白名单合规',
    riskLevel: '高',
    riskScore: 76,
    lastSeen: '1 分钟前',
    cpu: 'Xeon Silver',
    memory: '64 GB',
    disk: '2 TB RAID',
    openAlerts: 2,
    missingPatches: 1,
    blockedDevices: 0,
    unauthorizedApps: 0
  },
  {
    id: 'ep-1003',
    hostname: 'HR-PC-118',
    ip: '10.18.9.118',
    department: '人事部',
    owner: '陈宁',
    os: 'Windows 10 22H2',
    onlineStatus: '离线',
    agentVersion: '1.3.8',
    policyVersion: 'v9',
    antivirusStatus: '防护状态待确认',
    patchStatus: '超过 14 天未上报',
    deviceControl: '外设状态未知',
    whitelistStatus: '软件清单未回传',
    riskLevel: '高',
    riskScore: 71,
    lastSeen: '2 小时前',
    cpu: 'Intel i5-9500',
    memory: '8 GB',
    disk: '256 GB SSD',
    openAlerts: 1,
    missingPatches: 7,
    blockedDevices: 0,
    unauthorizedApps: 0
  },
  {
    id: 'ep-1004',
    hostname: 'RND-MAC-031',
    ip: '10.30.6.31',
    department: '研发部',
    owner: '王冉',
    os: 'macOS 14',
    onlineStatus: '在线',
    agentVersion: '1.4.1',
    policyVersion: 'v11',
    antivirusStatus: '行为防护已启用',
    patchStatus: '系统补丁合规',
    deviceControl: '检测到未授权蓝牙设备',
    whitelistStatus: '发现未授权调试工具',
    riskLevel: '严重',
    riskScore: 92,
    lastSeen: '7 分钟前',
    cpu: 'Apple M2',
    memory: '24 GB',
    disk: '1 TB SSD',
    openAlerts: 3,
    missingPatches: 0,
    blockedDevices: 2,
    unauthorizedApps: 2
  },
  {
    id: 'ep-1005',
    hostname: 'SALES-LT-204',
    ip: '10.40.2.204',
    department: '销售部',
    owner: '宋晴',
    os: 'Windows 11 23H2',
    onlineStatus: '待确认',
    agentVersion: '1.4.0',
    policyVersion: 'v10',
    antivirusStatus: '病毒库过期 3 天',
    patchStatus: '等待窗口安装补丁',
    deviceControl: 'USB 设备只读',
    whitelistStatus: '白名单同步延迟',
    riskLevel: '中',
    riskScore: 63,
    lastSeen: '32 分钟前',
    cpu: 'Intel i7-1260P',
    memory: '16 GB',
    disk: '512 GB SSD',
    openAlerts: 1,
    missingPatches: 3,
    blockedDevices: 1,
    unauthorizedApps: 0
  }
];

export const initialPolicies: SecurityPolicy[] = [
  {
    id: 'pol-001',
    name: '默认防病毒防护策略',
    type: '防病毒',
    status: '已发布',
    targetScope: '全公司终端',
    priority: 100,
    version: 'v3',
    owner: '安全管理员',
    rollout: 100,
    lastAction: '2026-06-13 09:10 已发布'
  },
  {
    id: 'pol-002',
    name: '研发外设白名单',
    type: '外设管控',
    status: '待审批',
    targetScope: '研发部',
    priority: 80,
    version: 'v1',
    owner: '王冉',
    rollout: 0,
    lastAction: '2026-06-13 10:32 提交审批'
  },
  {
    id: 'pol-003',
    name: '服务器补丁维护窗口',
    type: '补丁管理',
    status: '草稿',
    targetScope: '服务器分组',
    priority: 70,
    version: 'v2',
    owner: '运维经理',
    rollout: 0,
    lastAction: '2026-06-13 11:05 编辑草稿'
  }
];

export const alerts: SecurityAlert[] = [
  {
    id: 'AL-9001',
    title: '检测到异常外联会话',
    severity: '严重',
    status: '处置中',
    endpointId: 'ep-1004',
    endpoint: 'RND-MAC-031',
    owner: '安全管理员',
    evidence: 'network-session-9001.pcap',
    createdAt: '2026-06-13 09:42',
    sla: '剩余 18 分钟',
    timeline: ['Agent 上报异常外联', '系统聚合同类告警', '已派单给安全管理员', '执行临时网络隔离']
  },
  {
    id: 'AL-9002',
    title: '系统补丁缺失超过 30 天',
    severity: '高',
    status: '已派单',
    endpointId: 'ep-1002',
    endpoint: 'OPS-SRV-007',
    owner: '运维经理',
    evidence: 'patch-scan-9002.json',
    createdAt: '2026-06-13 10:16',
    sla: '剩余 4 小时',
    timeline: ['补丁扫描发现高危缺失', '生成整改工单', '等待运维确认维护窗口']
  },
  {
    id: 'AL-9003',
    title: 'USB 存储设备接入被阻断',
    severity: '中',
    status: '待复核',
    endpointId: 'ep-1001',
    endpoint: 'FIN-PC-023',
    owner: '安全管理员',
    evidence: 'device-control-9003.log',
    createdAt: '2026-06-13 11:20',
    sla: '剩余 1 天',
    timeline: ['Agent 阻断 USB 存储设备', '部门负责人确认非工作设备', '等待安全管理员复核关闭']
  }
];

export const reportMetrics: ReportMetric[] = [
  { label: 'Agent 覆盖率', value: '96.4%', target: '>= 95%', status: '达标' },
  { label: '补丁合规率', value: '87.3%', target: '>= 90%', status: '关注' },
  { label: '防病毒启用率', value: '98.1%', target: '>= 98%', status: '达标' },
  { label: '高危告警闭环率', value: '73.8%', target: '>= 85%', status: '未达标' },
  { label: '外设违规阻断率', value: '100%', target: '= 100%', status: '达标' },
  { label: '软件白名单合规率', value: '91.5%', target: '>= 92%', status: '关注' }
];

export const acceptanceItems: AcceptanceItem[] = [
  {
    id: 'AC-001',
    module: '终端资产',
    item: '终端注册、心跳、在线状态可查看',
    proof: '资产列表与终端详情截图',
    done: true,
    owner: '终端平台组',
    dueAt: '今日 14:00',
    nextAction: '补充离线终端原因说明'
  },
  {
    id: 'AC-002',
    module: 'Agent 通信',
    item: '策略版本、补丁、防病毒、控制状态可上报',
    proof: 'Agent 通信接口记录',
    done: true,
    owner: 'Agent 团队',
    dueAt: '今日 15:00',
    nextAction: '固化异常上报字段'
  },
  {
    id: 'AC-003',
    module: '安全策略',
    item: '策略可创建、审批、灰度、发布、回滚',
    proof: '策略状态流转记录',
    done: false,
    owner: '安全运营',
    dueAt: '今日 16:00',
    nextAction: '补齐审批人和变更窗口信息'
  },
  {
    id: 'AC-004',
    module: '告警闭环',
    item: '告警可派单、处置、复核、关闭',
    proof: '告警时间线与审计日志',
    done: false,
    owner: 'SOC 值班组',
    dueAt: '今日 17:00',
    nextAction: '补齐处置意见和责任人回执'
  },
  {
    id: 'AC-005',
    module: '合规报表',
    item: '生成资产、补丁、防病毒、外设、告警指标报表',
    proof: '报表导出文件',
    done: false,
    owner: '报表运营',
    dueAt: '今日 17:30',
    nextAction: '完成导出任务与归档留痕'
  },
  {
    id: 'AC-006',
    module: '权限审计',
    item: '不同角色菜单与接口权限正确',
    proof: '权限矩阵与测试报告',
    done: false,
    owner: '平台架构组',
    dueAt: '今日 18:00',
    nextAction: '补充审计视角验收说明'
  }
];

export const flowSteps = [
  'Agent 注册终端身份',
  '采集补丁、防病毒、外设、软件状态',
  '风险引擎计算评分',
  '策略中心生成下发任务',
  'Agent 执行策略并回传结果',
  '告警进入派单与处置闭环',
  '报表生成并归档到验收中心'
];

export const auditLogs: AuditLog[] = [
  { time: '09:42', actor: '安全管理员', action: '执行网络隔离', target: 'RND-MAC-031', result: '成功' },
  { time: '10:16', actor: '系统规则', action: '生成补丁整改工单', target: 'OPS-SRV-007', result: '成功' },
  { time: '10:32', actor: '王冉', action: '提交策略审批', target: '研发外设白名单', result: '待审批' },
  { time: '11:20', actor: 'Agent', action: '阻断 USB 存储设备', target: 'FIN-PC-023', result: '已阻断' },
  { time: '11:35', actor: '审计员', action: '导出终端合规周报', target: '2026-W24', result: '已归档' }
];

export const reportPackages: ReportPackage[] = [
  {
    id: 'RP-001',
    name: '终端合规周报',
    scope: '总部与区域办公室',
    status: '可下载',
    owner: '报表运营',
    updatedAt: '2026-06-13 11:35'
  },
  {
    id: 'RP-002',
    name: '高危告警处置报告',
    scope: 'SOC 值班与研发部',
    status: '生成中',
    owner: 'SOC 值班组',
    updatedAt: '2026-06-13 11:48'
  },
  {
    id: 'RP-003',
    name: '外设违规证据包',
    scope: '财务部与审计部',
    status: '待生成',
    owner: '审计员',
    updatedAt: '2026-06-13 11:20'
  }
];

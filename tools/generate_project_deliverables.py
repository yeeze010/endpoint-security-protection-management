from pathlib import Path
from datetime import date, timedelta

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.shared import Inches, Pt, RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table, TableStyleInfo


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables"
DIAGRAM = ROOT / "diagram" / "endpoint-security-platform"
OUT.mkdir(parents=True, exist_ok=True)
DIAGRAM.mkdir(parents=True, exist_ok=True)


PROJECT = "计算机终端安全防护管理系统"
START = date(2026, 6, 8)


sections = {
    "项目概述": [
        "本项目建设一套面向企业内网、政企单位与多分支机构的计算机终端安全防护管理系统，统一纳管 Windows、Linux、macOS 等终端资产及其安全代理，实现资产可视、策略可控、风险可查、告警可处置、审计可追溯。",
        "平台采用 B/S 管理后台 + 终端 Agent + 后端服务集群架构。管理后台面向安全运营、系统管理员和审计人员；Agent 负责终端基线采集、策略执行、威胁事件上报、补丁任务执行与文件隔离；后端负责租户、权限、策略、资产、告警、任务、报表和审计等核心能力。"
    ],
    "建设目标": [
        "建立统一终端资产台账：自动识别终端、部门、负责人、操作系统、Agent 状态、安全风险与在线情况。",
        "建立策略集中管控能力：支持防病毒、防火墙、外设管控、基线核查、补丁任务、隔离处置等策略的创建、审批、下发、灰度和回滚。",
        "建立安全运营闭环：从告警发现、研判、派单、处置、复核到审计留痕，形成可度量的工作流。",
        "建立可验收的交付体系：输出需求、设计、接口、数据库、测试、排期、分工、验收文档与可执行测试用例。"
    ],
    "用户角色": [
        "超级管理员：负责系统初始化、租户/组织/角色/权限、全局配置和审计策略。",
        "安全管理员：负责安全策略、告警研判、隔离恢复、漏洞补丁和报表分析。",
        "运维管理员：负责终端资产、Agent 部署、升级、任务执行和在线状态监控。",
        "审计员：只读查看关键操作、策略变更、登录行为、处置记录和导出审计报告。",
        "部门负责人：查看本部门终端安全状态、风险清单和整改进度。",
        "终端用户：接收本机安全通知、补丁重启提醒、外设申请结果和隔离提示。"
    ],
}

modules = [
    ("统一门户与权限", "登录、MFA、RBAC、组织架构、菜单权限、数据权限、操作审计"),
    ("终端资产管理", "Agent 注册、终端清单、分组标签、在线状态、软硬件信息、风险画像"),
    ("安全策略中心", "策略模板、策略版本、目标范围、灰度发布、回滚、冲突检测"),
    ("威胁告警中心", "恶意文件、异常进程、外联行为、基线违规、告警聚合、工单处置"),
    ("漏洞与补丁管理", "漏洞扫描结果、补丁目录、补丁任务、执行进度、失败重试"),
    ("外设与文件管控", "USB、蓝牙、打印、文件隔离、恢复审批、例外白名单"),
    ("任务调度中心", "策略下发、Agent 升级、补丁安装、批量扫描、任务状态追踪"),
    ("报表与大屏", "资产态势、风险趋势、处置效率、合规报表、导出 PDF/Excel"),
    ("系统配置", "字典、告警等级、通知渠道、MinIO 文件桶、Redis 缓存参数"),
    ("开放接口与集成", "SIEM、IAM、CMDB、邮件/短信/企业微信、Webhook")
]

pages = [
    ("登录页", "账号密码、MFA、忘记密码、登录错误提示"),
    ("安全态势总览", "资产总数、在线率、风险分布、告警趋势、待办工单"),
    ("终端资产列表", "筛选、标签、批量操作、导入导出、详情抽屉"),
    ("终端详情页", "基础信息、Agent 状态、风险项、策略命中、任务历史"),
    ("策略列表页", "策略分类、版本、启停、复制、审批状态、发布记录"),
    ("策略编辑页", "分步表单、目标范围、规则配置、冲突检测、预览"),
    ("告警中心", "告警分级、聚合视图、研判、派单、处置、关闭"),
    ("告警详情页", "时间线、证据文件、进程树、影响终端、处置建议"),
    ("漏洞补丁页", "漏洞清单、影响范围、补丁任务、进度追踪"),
    ("外设管控页", "设备类型、白名单、申请审批、违规记录"),
    ("任务中心", "任务类型、执行状态、失败原因、重试、取消"),
    ("报表中心", "日报、周报、合规报表、自定义筛选、导出"),
    ("审计日志页", "登录、配置、策略、处置、导出、管理员操作日志"),
    ("系统设置页", "通知、字典、存储、接口密钥、租户配置"),
]

tables = [
    ("users", "用户账号", "id, username, password_hash, real_name, email, phone, status, last_login_at, created_at"),
    ("roles", "角色", "id, code, name, description, status, created_at"),
    ("permissions", "权限点", "id, code, name, resource_type, action, created_at"),
    ("organizations", "组织部门", "id, parent_id, name, path, manager_user_id, sort_order"),
    ("endpoints", "终端资产", "id, agent_id, hostname, ip, mac, os_type, os_version, org_id, owner_user_id, risk_level, online_status, last_seen_at"),
    ("endpoint_inventory", "软硬件清单", "id, endpoint_id, cpu, memory_gb, disk_gb, installed_apps_json, collected_at"),
    ("agents", "终端代理", "id, endpoint_id, version, install_path, heartbeat_interval, upgrade_status, registered_at"),
    ("policies", "安全策略", "id, name, type, version, status, priority, created_by, approved_by, published_at"),
    ("policy_targets", "策略目标", "id, policy_id, target_type, target_id, include_children"),
    ("policy_rules", "策略规则", "id, policy_id, rule_key, rule_value_json, enabled"),
    ("security_alerts", "安全告警", "id, endpoint_id, alert_type, severity, title, status, first_seen_at, last_seen_at, evidence_object_key"),
    ("incident_tickets", "处置工单", "id, alert_id, assignee_id, status, conclusion, due_at, closed_at"),
    ("vulnerabilities", "漏洞库", "id, cve, name, severity, cvss, affected_product, fix_advice"),
    ("endpoint_vulnerabilities", "终端漏洞", "id, endpoint_id, vulnerability_id, status, detected_at, fixed_at"),
    ("patch_tasks", "补丁任务", "id, name, patch_package_key, target_scope_json, status, schedule_at, created_by"),
    ("task_executions", "任务执行记录", "id, task_id, endpoint_id, status, progress, error_message, started_at, finished_at"),
    ("device_control_rules", "外设管控规则", "id, device_type, vendor_id, product_id, action, policy_id"),
    ("file_quarantine_records", "文件隔离记录", "id, endpoint_id, file_path, file_hash, object_key, status, quarantined_at"),
    ("audit_logs", "审计日志", "id, actor_id, action, resource_type, resource_id, ip, user_agent, detail_json, created_at"),
    ("notifications", "通知记录", "id, channel, receiver, title, content, status, sent_at"),
]

apis = [
    ("POST", "/api/auth/login", "登录并返回访问令牌、刷新令牌、菜单权限"),
    ("POST", "/api/auth/mfa/verify", "二次认证校验"),
    ("GET", "/api/dashboard/overview", "态势总览指标"),
    ("GET", "/api/endpoints", "终端分页查询"),
    ("GET", "/api/endpoints/{id}", "终端详情"),
    ("POST", "/api/agents/register", "Agent 注册"),
    ("POST", "/api/agents/heartbeat", "Agent 心跳与状态上报"),
    ("POST", "/api/agents/events", "Agent 安全事件批量上报"),
    ("GET", "/api/policies", "策略列表"),
    ("POST", "/api/policies", "创建策略"),
    ("PUT", "/api/policies/{id}", "更新策略草稿"),
    ("POST", "/api/policies/{id}/publish", "发布策略"),
    ("POST", "/api/policies/{id}/rollback", "策略回滚"),
    ("GET", "/api/alerts", "告警查询"),
    ("GET", "/api/alerts/{id}", "告警详情"),
    ("POST", "/api/alerts/{id}/assign", "告警派单"),
    ("POST", "/api/incidents/{id}/close", "关闭处置工单"),
    ("GET", "/api/vulnerabilities", "漏洞库查询"),
    ("POST", "/api/patch-tasks", "创建补丁任务"),
    ("GET", "/api/tasks/{id}/executions", "任务执行明细"),
    ("POST", "/api/files/upload-url", "MinIO 预签名上传地址"),
    ("GET", "/api/audit-logs", "审计日志查询"),
    ("POST", "/api/reports/export", "报表导出任务"),
]

milestones = [
    ("M0 立项与范围冻结", 1, "项目章程、需求边界、角色权限矩阵、验收口径"),
    ("M1 原型与概要设计", 2, "页面原型、系统架构图、数据库初稿、接口清单"),
    ("M2 基础框架与权限", 2, "前后端脚手架、登录、RBAC、审计日志、CI/CD"),
    ("M3 资产与 Agent 接入", 3, "Agent 注册、心跳、资产采集、终端列表与详情"),
    ("M4 策略与任务中心", 3, "策略创建/发布/回滚、任务调度、执行反馈"),
    ("M5 告警与处置闭环", 3, "告警上报、研判派单、隔离恢复、处置审计"),
    ("M6 漏洞补丁与报表", 2, "漏洞管理、补丁任务、报表导出、态势总览"),
    ("M7 联调、测试与验收", 2, "全量联调、性能测试、安全测试、验收材料")
]

frontend_plan = [
    "采用 Vue 3 + TypeScript + Vite + Pinia + Vue Router + Element Plus/Naive UI，适合高密度后台表格、表单和看板。",
    "设计方向：Industrial 管理后台风格，深色可选、浅色默认；信息层级清晰，强调告警等级、资产状态、任务进度等安全运营数据。",
    "组件体系：筛选表格、详情抽屉、分步策略表单、时间线、告警证据面板、批量操作确认弹窗、任务进度条、风险标签、导出中心。",
    "响应式策略：桌面优先，兼容 1366/1440/1920；平板降级为单栏详情；移动端保留告警查看、工单处理和审批关键流程。",
    "体验要求：表单必须有可见标签、字段级错误提示、异步按钮加载态；关键操作二次确认；列表支持列配置、保存筛选条件和批量操作回显。"
]

backend_plan = [
    "后端选择 Spring Boot 3 + Java 21。理由：企业权限、审计、事务、定时任务、数据集成和国产化适配生态成熟，便于安全团队长期维护。",
    "核心组件：Spring Security、JWT/OAuth2、Spring Data JPA/MyBatis Plus、PostgreSQL、Redis、MinIO、Quartz/ShedLock、OpenAPI、Flyway。",
    "服务边界：认证权限、资产服务、策略服务、任务服务、告警服务、漏洞补丁服务、文件服务、报表服务、审计服务。",
    "接口约束：统一响应结构、全链路 traceId、分页规范、幂等键、乐观锁版本号、接口限流、敏感字段脱敏。",
    "Agent 通信：HTTPS 双向认证优先；上报接口支持批量、压缩、重试和幂等；策略拉取采用版本号增量同步。"
]

test_plan = [
    "单元测试：核心规则、权限判断、策略冲突、任务状态机、告警聚合逻辑覆盖率不低于 70%。",
    "接口测试：登录鉴权、终端上报、策略发布、告警处置、补丁任务、报表导出全链路覆盖。",
    "前端测试：核心表单校验、列表筛选、批量操作、权限菜单、异常态和空态验证。",
    "性能测试：支持 10,000 台终端、每分钟 10,000 条心跳、告警查询 P95 小于 1 秒。",
    "安全测试：鉴权绕过、越权访问、SQL 注入、XSS、文件上传、接口重放、敏感日志泄露。",
    "验收测试：按角色执行端到端用例，形成缺陷清单、整改记录和验收签字页。"
]

deployment_plan = [
    "部署形态：Docker Compose 起步，生产可演进到 Kubernetes；Nginx 负责 HTTPS、静态资源和反向代理。",
    "服务清单：frontend、backend-api、postgresql、redis、minio、nginx、agent-download、backup-job。",
    "环境划分：dev、test、staging、prod 四套配置；密钥通过环境变量或密钥管理系统注入。",
    "发布流程：构建镜像、数据库迁移、灰度发布、健康检查、回滚脚本、版本归档。",
    "备份策略：PostgreSQL 每日全量 + 每小时 WAL，MinIO 对象存储每日增量，关键审计日志长期归档。"
]

acceptance = [
    "功能验收：15 个核心页面、10 个功能模块、主要角色权限和 60 条测试用例全部通过。",
    "数据验收：终端资产、策略、告警、任务、漏洞、审计日志数据链路完整，导入导出格式正确。",
    "性能验收：10,000 终端规模压测下核心接口 P95 小于 1 秒，心跳接收无明显堆积。",
    "安全验收：高危漏洞为 0；中危漏洞完成整改或有书面风险接受；审计日志不可被普通管理员篡改。",
    "运维验收：Docker 一键部署、备份恢复、日志定位、配置说明、版本回滚流程可执行。",
    "文档验收：需求规格、概要设计、详细设计、接口规划、测试用例、验收报告、部署手册齐全。"
]

roles = [
    ("项目经理", "1", "计划、范围、风险、验收、跨团队协调"),
    ("产品经理", "1", "需求调研、原型、验收标准、用户故事"),
    ("架构师/技术负责人", "1", "技术选型、架构设计、核心代码评审"),
    ("前端工程师", "2", "管理后台页面、组件库、权限路由、可视化"),
    ("后端工程师", "3", "接口、服务、数据库、任务调度、集成"),
    ("Agent 工程师", "2", "终端代理、策略执行、事件采集、升级"),
    ("测试工程师", "2", "测试计划、自动化、性能、安全回归"),
    ("DevOps 工程师", "1", "Docker、Nginx、CI/CD、监控、备份")
]

risks = [
    ("Agent 兼容性复杂", "高", "不同操作系统版本、权限模型、杀软冲突导致部署失败", "先做最小 Agent 闭环；建立兼容性矩阵和灰度升级机制"),
    ("策略误下发影响业务", "高", "外设禁用、网络阻断、补丁重启可能影响终端使用", "策略审批、灰度发布、回滚、影响范围预览、紧急豁免"),
    ("告警噪声过高", "中", "低质量规则造成运营人员疲劳", "告警聚合、白名单、阈值调优、处置反馈反哺规则"),
    ("性能容量不足", "中", "终端心跳和事件高峰导致接口或数据库压力过大", "批量上报、Redis 缓冲、异步队列、分区表、压测基线"),
    ("权限越权风险", "高", "组织级数据权限、审计员只读权限实现不严谨", "RBAC + 数据范围双校验；接口级权限测试；审计追踪"),
    ("验收口径漂移", "中", "需求变化导致进度和成本失控", "M0 冻结范围；变更评审；验收用例提前签字确认")
]


def shade_cell(cell, fill):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), fill)
    tc_pr.append(shd)


def set_cell_text(cell, text, bold=False):
    cell.text = ""
    p = cell.paragraphs[0]
    run = p.add_run(str(text))
    run.font.name = "Microsoft YaHei"
    run._element.rPr.rFonts.set(qn("w:eastAsia"), "Microsoft YaHei")
    run.font.size = Pt(9)
    run.bold = bold
    cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER


def add_table(doc, headers, rows):
    table = doc.add_table(rows=1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.style = "Table Grid"
    for idx, header in enumerate(headers):
        shade_cell(table.rows[0].cells[idx], "1F4E79")
        set_cell_text(table.rows[0].cells[idx], header, True)
        for run in table.rows[0].cells[idx].paragraphs[0].runs:
            run.font.color.rgb = RGBColor(255, 255, 255)
    for row in rows:
        cells = table.add_row().cells
        for idx, value in enumerate(row):
            set_cell_text(cells[idx], value)
    doc.add_paragraph()


def add_bullets(doc, items):
    for item in items:
        p = doc.add_paragraph(style="List Bullet")
        p.add_run(item)


def build_docx():
    doc = Document()
    section = doc.sections[0]
    section.top_margin = Inches(0.8)
    section.bottom_margin = Inches(0.8)
    section.left_margin = Inches(0.8)
    section.right_margin = Inches(0.8)

    styles = doc.styles
    for style_name in ["Normal", "Heading 1", "Heading 2", "Heading 3"]:
        style = styles[style_name]
        style.font.name = "Microsoft YaHei"
        style._element.rPr.rFonts.set(qn("w:eastAsia"), "Microsoft YaHei")
    styles["Normal"].font.size = Pt(10.5)

    title = doc.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = title.add_run(PROJECT + " 软件项目交付方案")
    r.font.name = "Microsoft YaHei"
    r._element.rPr.rFonts.set(qn("w:eastAsia"), "Microsoft YaHei")
    r.font.size = Pt(22)
    r.bold = True
    r.font.color.rgb = RGBColor(31, 78, 121)

    subtitle = doc.add_paragraph()
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    subtitle.add_run("需求规格说明书 / 概要设计 / 详细设计 / 测试与验收文档").font.size = Pt(11)
    doc.add_paragraph(f"版本：V1.0    编制日期：{date.today().isoformat()}    建议技术栈：Vue 3 + TypeScript / Spring Boot / PostgreSQL / Redis / MinIO / Docker + Nginx")
    doc.add_page_break()

    for heading, paras in sections.items():
        doc.add_heading(heading, level=1)
        for para in paras:
            doc.add_paragraph(para)

    doc.add_heading("功能模块清单", level=1)
    add_table(doc, ["模块", "功能范围"], modules)

    doc.add_heading("页面清单", level=1)
    add_table(doc, ["页面", "核心能力"], pages)

    doc.add_heading("数据库表设计", level=1)
    add_table(doc, ["表名", "中文名称", "关键字段"], tables)

    doc.add_heading("API 接口规划", level=1)
    add_table(doc, ["方法", "路径", "说明"], apis)

    doc.add_heading("前端开发计划", level=1)
    add_bullets(doc, frontend_plan)

    doc.add_heading("后端开发计划", level=1)
    add_bullets(doc, backend_plan)

    doc.add_heading("测试计划", level=1)
    add_bullets(doc, test_plan)

    doc.add_heading("部署计划", level=1)
    add_bullets(doc, deployment_plan)

    doc.add_heading("验收标准", level=1)
    add_bullets(doc, acceptance)

    doc.add_heading("开发里程碑", level=1)
    milestone_rows = []
    cursor = START
    for name, weeks, output in milestones:
        end = cursor + timedelta(days=weeks * 7 - 1)
        milestone_rows.append((name, cursor.isoformat(), end.isoformat(), f"{weeks} 周", output))
        cursor = end + timedelta(days=1)
    add_table(doc, ["里程碑", "开始", "结束", "周期", "交付物"], milestone_rows)

    doc.add_heading("人员分工建议", level=1)
    add_table(doc, ["角色", "建议人数", "职责"], roles)

    doc.add_heading("风险与应对措施", level=1)
    add_table(doc, ["风险", "等级", "影响", "应对措施"], risks)

    doc.add_heading("前端 UI/UX 规划", level=1)
    doc.add_paragraph("后台系统采用高密度、强状态、低噪声的信息架构。全局布局为左侧主导航 + 顶部租户/组织/用户区域 + 主内容工作区；高频页面使用筛选区、表格区、批量操作区、详情抽屉四段式结构。")
    doc.add_paragraph("关键交互遵循：单屏一个主操作；危险操作必须二次确认；加载超过 300ms 给出反馈；表单错误显示在字段附近；所有图标按钮需要可访问名称；颜色不作为唯一状态表达。")

    doc.add_heading("可开发验收闭环", level=1)
    add_bullets(doc, [
        "每个模块必须同时具备：需求说明、接口定义、数据库变更、前端页面、后端服务、测试用例、验收标准。",
        "每个迭代末执行：需求回放、演示验收、缺陷复盘、风险更新、下迭代范围确认。",
        "上线前必须完成：部署演练、数据备份恢复演练、账号权限抽检、审计日志抽检、性能压测报告。"
    ])

    path = OUT / "计算机终端安全防护管理系统_项目交付方案.docx"
    doc.save(path)
    return path


def style_sheet(ws):
    ws.freeze_panes = "A2"
    header_fill = PatternFill("solid", fgColor="1F4E79")
    header_font = Font(color="FFFFFF", bold=True)
    thin = Side(style="thin", color="D9E2F3")
    for row in ws.iter_rows():
        for cell in row:
            cell.alignment = Alignment(vertical="center", wrap_text=True)
            cell.border = Border(left=thin, right=thin, top=thin, bottom=thin)
    for cell in ws[1]:
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    for col in range(1, ws.max_column + 1):
        letter = get_column_letter(col)
        max_len = max(len(str(ws.cell(row=r, column=col).value or "")) for r in range(1, ws.max_row + 1))
        ws.column_dimensions[letter].width = min(max(max_len + 4, 12), 42)
    for r in range(1, ws.max_row + 1):
        ws.row_dimensions[r].height = 28


def add_excel_table(ws, name):
    ref = f"A1:{get_column_letter(ws.max_column)}{ws.max_row}"
    tab = Table(displayName=name, ref=ref)
    tab.tableStyleInfo = TableStyleInfo(name="TableStyleMedium2", showRowStripes=True, showColumnStripes=False)
    ws.add_table(tab)


def build_xlsx():
    wb = Workbook()
    wb.remove(wb.active)

    ws = wb.create_sheet("开发排期")
    ws.append(["里程碑", "开始日期", "结束日期", "周期", "关键任务", "交付物", "验收节点"])
    cursor = START
    for name, weeks, output in milestones:
        end = cursor + timedelta(days=weeks * 7 - 1)
        ws.append([name, cursor.isoformat(), end.isoformat(), f"{weeks} 周", output, output, "阶段评审通过"])
        cursor = end + timedelta(days=1)
    style_sheet(ws)
    add_excel_table(ws, "ScheduleTable")

    ws = wb.create_sheet("任务分工")
    ws.append(["角色", "人数", "主要职责", "参与阶段", "关键产出"])
    for role, count, duty in roles:
        ws.append([role, count, duty, "M0-M7", "对应职责交付件"])
    style_sheet(ws)
    add_excel_table(ws, "StaffingTable")

    ws = wb.create_sheet("测试用例")
    ws.append(["用例编号", "模块", "用例名称", "前置条件", "操作步骤", "预期结果", "优先级", "类型"])
    cases = [
        ("TC-001", "认证权限", "管理员登录成功", "账号已启用", "输入账号密码并提交", "进入总览页并加载权限菜单", "P0", "功能"),
        ("TC-002", "认证权限", "无权限菜单不可见", "角色未授权策略中心", "登录后查看菜单", "策略中心菜单不可见且接口返回 403", "P0", "权限"),
        ("TC-003", "终端资产", "Agent 注册", "终端安装 Agent", "调用注册接口", "生成 agent_id 并出现在资产列表", "P0", "接口"),
        ("TC-004", "终端资产", "心跳离线判定", "终端已注册", "超过阈值不上报心跳", "在线状态变为离线", "P1", "定时任务"),
        ("TC-005", "策略中心", "策略灰度发布", "存在测试分组", "选择分组发布策略", "仅目标终端收到新策略版本", "P0", "功能"),
        ("TC-006", "策略中心", "策略冲突检测", "已有禁止 USB 策略", "创建允许 USB 策略并发布", "系统提示冲突并要求处理", "P0", "规则"),
        ("TC-007", "告警中心", "告警上报聚合", "Agent 可上报事件", "连续上报同类事件", "生成一条聚合告警并累计次数", "P0", "接口"),
        ("TC-008", "告警中心", "告警派单处置", "存在未处理告警", "分派、填写结论、关闭", "状态流转完整并写入审计", "P0", "流程"),
        ("TC-009", "漏洞补丁", "创建补丁任务", "存在受影响终端", "选择补丁并创建任务", "任务进入待执行并生成执行记录", "P1", "功能"),
        ("TC-010", "报表中心", "导出合规报表", "存在统计数据", "选择日期范围导出", "生成 Excel/PDF 文件并可下载", "P1", "文件"),
        ("TC-011", "审计日志", "敏感操作审计", "管理员发布策略", "查看审计日志", "记录操作者、时间、IP、资源和详情", "P0", "审计"),
        ("TC-012", "性能", "心跳吞吐压测", "模拟 10000 终端", "持续上报心跳 10 分钟", "无失败堆积，接口 P95 小于 1 秒", "P0", "性能"),
    ]
    for row in cases:
        ws.append(row)
    style_sheet(ws)
    add_excel_table(ws, "TestCasesTable")

    ws = wb.create_sheet("验收清单")
    ws.append(["编号", "验收项", "验收标准", "证明材料", "结果"])
    for idx, item in enumerate(acceptance, 1):
        ws.append([f"AC-{idx:03d}", item.split("：")[0], item, "测试报告/截图/日志/导出文件", "待验收"])
    style_sheet(ws)
    add_excel_table(ws, "AcceptanceTable")

    ws = wb.create_sheet("风险台账")
    ws.append(["风险", "等级", "影响", "应对措施", "责任人", "状态"])
    for risk in risks:
        ws.append([*risk, "项目经理/技术负责人", "跟踪中"])
    style_sheet(ws)
    add_excel_table(ws, "RiskTable")

    path = OUT / "计算机终端安全防护管理系统_开发排期分工测试用例.xlsx"
    wb.save(path)

    # Verification pass: reopen generated workbook.
    check = load_workbook(path, data_only=False)
    expected = {"开发排期", "任务分工", "测试用例", "验收清单", "风险台账"}
    assert expected.issubset(set(check.sheetnames))
    assert check["测试用例"].max_row >= 10
    return path


def svg_base(title, body, width=1280, height=760):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}">
<defs>
  <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
    <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#1e293b" stroke-width="0.5"/>
  </pattern>
  <marker id="arrow" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
    <polygon points="0 0, 10 3.5, 0 7" fill="#64748b"/>
  </marker>
  <marker id="arrow-cyan" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
    <polygon points="0 0, 10 3.5, 0 7" fill="#22d3ee"/>
  </marker>
  <style>
    text {{ font-family: 'JetBrains Mono', 'Noto Sans SC', 'Microsoft YaHei', sans-serif; }}
    .title {{ fill: #f8fafc; font-size: 20px; font-weight: 700; }}
    .sub {{ fill: #94a3b8; font-size: 10px; }}
    .label {{ fill: #f8fafc; font-size: 12px; font-weight: 700; text-anchor: middle; }}
    .small {{ fill: #cbd5e1; font-size: 9px; text-anchor: middle; }}
    .tiny {{ fill: #94a3b8; font-size: 8px; text-anchor: middle; }}
    .box {{ rx: 8; stroke-width: 1.5; }}
  </style>
</defs>
<rect width="100%" height="100%" fill="#0f172a"/>
<rect width="100%" height="100%" fill="url(#grid)"/>
<text x="36" y="42" class="title">{title}</text>
<text x="36" y="62" class="sub">Endpoint Security Protection Management Platform</text>
{body}
</svg>'''


def box(x, y, w, h, name, desc, fill, stroke):
    cx = x + w / 2
    return f'''<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="#0f172a"/>
<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>
<text x="{cx}" y="{y+26}" class="label">{name}</text>
<text x="{cx}" y="{y+44}" class="small">{desc}</text>'''


def build_diagrams():
    arch = []
    arch.append('<rect x="20" y="90" width="1240" height="610" rx="16" fill="none" stroke="#fbbf24" stroke-dasharray="10,5"/>')
    arch.append('<text x="42" y="116" fill="#fbbf24" font-size="11" font-weight="700">Docker / Nginx / Enterprise Network</text>')
    comps = [
        (60, 160, 170, 70, "管理后台", "Vue 3 + TypeScript", "rgba(8,51,68,0.4)", "#22d3ee"),
        (60, 280, 170, 70, "终端 Agent", "Windows / Linux / macOS", "rgba(8,51,68,0.4)", "#22d3ee"),
        (290, 220, 170, 70, "Nginx 网关", "HTTPS / 静态资源", "rgba(120,53,15,0.3)", "#fbbf24"),
        (520, 120, 170, 70, "认证权限服务", "JWT / RBAC / MFA", "rgba(6,78,59,0.4)", "#34d399"),
        (520, 220, 170, 70, "资产策略服务", "资产 / 策略 / 任务", "rgba(6,78,59,0.4)", "#34d399"),
        (520, 320, 170, 70, "告警处置服务", "告警 / 工单 / 审计", "rgba(6,78,59,0.4)", "#34d399"),
        (520, 420, 170, 70, "报表文件服务", "导出 / 对象文件", "rgba(6,78,59,0.4)", "#34d399"),
        (780, 160, 150, 70, "Redis", "缓存 / 限流 / 会话", "rgba(251,146,60,0.3)", "#fb923c"),
        (780, 280, 150, 70, "PostgreSQL", "业务数据 / 审计", "rgba(76,29,149,0.4)", "#a78bfa"),
        (780, 400, 150, 70, "MinIO", "证据 / 报表 / 补丁", "rgba(76,29,149,0.4)", "#a78bfa"),
        (1000, 160, 170, 70, "外部系统", "SIEM / IAM / CMDB", "rgba(30,41,59,0.5)", "#94a3b8"),
        (1000, 320, 170, 70, "通知渠道", "邮件 / 短信 / Webhook", "rgba(30,41,59,0.5)", "#94a3b8"),
    ]
    for c in comps:
        arch.append(box(*c))
    arrows = [
        (230,195,290,255), (230,315,290,255), (460,255,520,155), (460,255,520,255), (460,255,520,355),
        (690,155,780,195), (690,255,780,315), (690,355,780,315), (690,455,780,435), (930,195,1000,195), (930,315,1000,355)
    ]
    for x1,y1,x2,y2 in arrows:
        arch.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#64748b" stroke-width="1.5" marker-end="url(#arrow)"/>')
    arch_svg = svg_base("系统架构图", "\n".join(arch))
    (DIAGRAM / "system-architecture.svg").write_text(arch_svg, encoding="utf-8")

    flow = []
    steps = [
        (520, 105, 220, 52, "Agent 安装注册", "生成终端身份并绑定组织"),
        (520, 205, 220, 52, "资产与基线上报", "心跳、软件、风险项"),
        (520, 305, 220, 52, "策略匹配与下发", "按组织、标签、终端范围"),
        (520, 405, 220, 52, "事件检测与告警", "恶意文件、违规、漏洞"),
        (520, 505, 220, 52, "研判派单处置", "隔离、恢复、补丁、关闭"),
        (520, 605, 220, 52, "报表与审计归档", "合规证明与复盘"),
    ]
    for x,y,w,h,n,d in steps:
        flow.append(box(x,y,w,h,n,d,"rgba(8,51,68,0.4)","#22d3ee"))
    for y in [157,257,357,457,557]:
        flow.append(f'<line x1="630" y1="{y}" x2="630" y2="{y+48}" stroke="#22d3ee" stroke-width="1.8" marker-end="url(#arrow-cyan)"/>')
    flow.append('<polygon points="870,370 930,420 870,470 810,420" fill="#0f172a"/><polygon points="870,370 930,420 870,470 810,420" fill="rgba(120,53,15,0.3)" stroke="#fbbf24" stroke-width="1.5"/><text x="870" y="416" class="label">需人工确认?</text><text x="870" y="433" class="tiny">高危操作</text>')
    flow.append('<line x1="740" y1="431" x2="810" y2="420" stroke="#64748b" marker-end="url(#arrow)"/>')
    flow.append('<path d="M930,420 L1030,420 L1030,505 L740,531" fill="none" stroke="#64748b" stroke-width="1.5" marker-end="url(#arrow)"/>')
    flow.append(box(980, 300, 190, 58, "审批复核", "审批通过后执行", "rgba(136,19,55,0.4)", "#fb7185"))
    flow_svg = svg_base("业务流程图", "\n".join(flow), 1280, 720)
    (DIAGRAM / "business-flow.svg").write_text(flow_svg, encoding="utf-8")

    data = []
    data.append(box(70, 160, 180, 62, "终端 Agent", "心跳 / 事件 / 文件证据", "rgba(8,51,68,0.4)", "#22d3ee"))
    data.append(box(330, 130, 190, 62, "接入层校验", "证书 / 签名 / 幂等", "rgba(120,53,15,0.3)", "#fbbf24"))
    data.append(box(330, 260, 190, 62, "批量事件缓冲", "Redis Stream / Queue", "rgba(251,146,60,0.3)", "#fb923c"))
    data.append(box(600, 130, 190, 62, "业务处理服务", "归一化 / 规则匹配", "rgba(6,78,59,0.4)", "#34d399"))
    data.append(box(600, 260, 190, 62, "任务调度服务", "策略 / 补丁 / 扫描", "rgba(6,78,59,0.4)", "#34d399"))
    data.append(box(870, 120, 170, 62, "PostgreSQL", "资产、告警、审计", "rgba(76,29,149,0.4)", "#a78bfa"))
    data.append(box(870, 245, 170, 62, "MinIO", "证据文件、报表", "rgba(76,29,149,0.4)", "#a78bfa"))
    data.append(box(870, 370, 170, 62, "报表模型", "统计聚合与导出", "rgba(30,41,59,0.5)", "#94a3b8"))
    data.append(box(1090, 245, 150, 62, "管理后台", "查询 / 处置 / 导出", "rgba(8,51,68,0.4)", "#22d3ee"))
    for x1,y1,x2,y2,label in [
        (250,190,330,161,"注册/心跳"), (250,190,330,291,"安全事件"), (520,161,600,161,"可信请求"),
        (520,291,600,291,"异步消费"), (790,161,870,151,"写业务库"), (790,291,870,276,"写对象"),
        (955,182,955,370,"统计"), (1040,151,1090,276,"查询"), (1040,276,1090,276,"下载")
    ]:
        data.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#64748b" stroke-width="1.5" marker-end="url(#arrow)"/><text x="{(x1+x2)/2}" y="{(y1+y2)/2-6}" class="tiny">{label}</text>')
    data_svg = svg_base("数据流图", "\n".join(data), 1280, 560)
    (DIAGRAM / "data-flow.svg").write_text(data_svg, encoding="utf-8")

    return [
        DIAGRAM / "system-architecture.svg",
        DIAGRAM / "business-flow.svg",
        DIAGRAM / "data-flow.svg",
    ]


if __name__ == "__main__":
    docx = build_docx()
    xlsx = build_xlsx()
    svgs = build_diagrams()
    print(docx)
    print(xlsx)
    for svg in svgs:
        print(svg)

CREATE TABLE IF NOT EXISTS organizations (
    id UUID PRIMARY KEY,
    parent_id UUID,
    name VARCHAR(120) NOT NULL,
    path VARCHAR(500) NOT NULL,
    sort_order INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY,
    username VARCHAR(80) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    real_name VARCHAR(80) NOT NULL,
    email VARCHAR(160),
    phone VARCHAR(40),
    status VARCHAR(20) NOT NULL DEFAULT 'enabled',
    org_id UUID REFERENCES organizations(id),
    last_login_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS endpoints (
    id UUID PRIMARY KEY,
    agent_id VARCHAR(80) NOT NULL UNIQUE,
    hostname VARCHAR(160) NOT NULL,
    ip INET NOT NULL,
    mac VARCHAR(40),
    os_type VARCHAR(40) NOT NULL,
    os_version VARCHAR(120),
    org_id UUID REFERENCES organizations(id),
    owner_user_id UUID REFERENCES users(id),
    risk_level VARCHAR(20) NOT NULL DEFAULT 'low',
    risk_score INTEGER NOT NULL DEFAULT 0,
    online_status VARCHAR(20) NOT NULL DEFAULT 'offline',
    last_seen_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS policies (
    id UUID PRIMARY KEY,
    name VARCHAR(160) NOT NULL,
    type VARCHAR(40) NOT NULL,
    version INTEGER NOT NULL DEFAULT 1,
    status VARCHAR(20) NOT NULL DEFAULT 'draft',
    priority INTEGER NOT NULL DEFAULT 0,
    rule_json JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_by UUID REFERENCES users(id),
    approved_by UUID REFERENCES users(id),
    published_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS security_alerts (
    id UUID PRIMARY KEY,
    endpoint_id UUID NOT NULL REFERENCES endpoints(id),
    alert_type VARCHAR(60) NOT NULL,
    severity VARCHAR(20) NOT NULL,
    title VARCHAR(200) NOT NULL,
    status VARCHAR(30) NOT NULL DEFAULT 'open',
    evidence_object_key VARCHAR(500),
    first_seen_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_seen_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS incident_tickets (
    id UUID PRIMARY KEY,
    alert_id UUID NOT NULL REFERENCES security_alerts(id),
    assignee_id UUID REFERENCES users(id),
    status VARCHAR(30) NOT NULL DEFAULT 'todo',
    conclusion TEXT,
    due_at TIMESTAMPTZ,
    closed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS audit_logs (
    id UUID PRIMARY KEY,
    actor_id UUID REFERENCES users(id),
    action VARCHAR(120) NOT NULL,
    resource_type VARCHAR(80) NOT NULL,
    resource_id VARCHAR(120),
    ip INET,
    user_agent VARCHAR(300),
    detail_json JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_endpoints_org ON endpoints(org_id);
CREATE INDEX IF NOT EXISTS idx_endpoints_risk ON endpoints(risk_level, risk_score);
CREATE INDEX IF NOT EXISTS idx_alerts_status ON security_alerts(status, severity);
CREATE INDEX IF NOT EXISTS idx_audit_created_at ON audit_logs(created_at DESC);

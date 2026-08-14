package com.endpoint.security.auth;

public final class Permissions {
    public static final String DASHBOARD_READ = "dashboard.read";
    public static final String ENDPOINTS_READ = "endpoints.read";
    public static final String ENDPOINTS_REGISTER = "endpoints.register";
    public static final String ENDPOINTS_COMMAND = "endpoints.command";
    public static final String ALERTS_READ = "alerts.read";
    public static final String ALERTS_CONFIRM = "alerts.confirm";
    public static final String ALERTS_ASSIGN = "alerts.assign";
    public static final String RESPONSE_DISPATCH = "response.dispatch";
    public static final String RESPONSE_EXECUTE = "response.execute";
    public static final String RESPONSE_REVIEW = "response.review";
    public static final String POLICIES_READ = "policies.read";
    public static final String POLICIES_WRITE = "policies.write";
    public static final String REPORTS_READ = "reports.read";
    public static final String REPORTS_EXPORT = "reports.export";
    public static final String AUDIT_READ = "audit.read";

    private Permissions() {
    }
}

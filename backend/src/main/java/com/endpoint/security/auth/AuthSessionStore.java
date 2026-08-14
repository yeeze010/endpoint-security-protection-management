package com.endpoint.security.auth;

import org.springframework.stereotype.Component;

import java.time.OffsetDateTime;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;

@Component
public class AuthSessionStore {
    private final List<Account> accounts = List.of(
            account("安全管理员", "secops", "secops123", Set.of(
                    Permissions.DASHBOARD_READ, Permissions.ENDPOINTS_READ, Permissions.ENDPOINTS_REGISTER,
                    Permissions.ENDPOINTS_COMMAND, Permissions.ALERTS_READ, Permissions.ALERTS_CONFIRM,
                    Permissions.ALERTS_ASSIGN, Permissions.RESPONSE_DISPATCH, Permissions.RESPONSE_EXECUTE,
                    Permissions.RESPONSE_REVIEW, Permissions.POLICIES_READ, Permissions.POLICIES_WRITE,
                    Permissions.REPORTS_READ, Permissions.REPORTS_EXPORT, Permissions.AUDIT_READ)),
            account("运维人员", "operator", "operator123", Set.of(
                    Permissions.DASHBOARD_READ, Permissions.ENDPOINTS_READ, Permissions.ENDPOINTS_REGISTER,
                    Permissions.ENDPOINTS_COMMAND, Permissions.ALERTS_READ, Permissions.ALERTS_CONFIRM,
                    Permissions.ALERTS_ASSIGN, Permissions.RESPONSE_EXECUTE, Permissions.POLICIES_READ,
                    Permissions.REPORTS_READ)),
            account("审计员", "auditor", "auditor123", Set.of(
                    Permissions.DASHBOARD_READ, Permissions.ENDPOINTS_READ, Permissions.ALERTS_READ,
                    Permissions.POLICIES_READ, Permissions.RESPONSE_REVIEW, Permissions.REPORTS_READ,
                    Permissions.REPORTS_EXPORT, Permissions.AUDIT_READ)),
            account("普通用户", "user", "user123", Set.of(
                    Permissions.DASHBOARD_READ, Permissions.ENDPOINTS_READ, Permissions.ALERTS_READ,
                    Permissions.POLICIES_READ)),
            account("安全管理员", "admin", "admin123", Set.of(
                    Permissions.DASHBOARD_READ, Permissions.ENDPOINTS_READ, Permissions.ENDPOINTS_REGISTER,
                    Permissions.ENDPOINTS_COMMAND, Permissions.ALERTS_READ, Permissions.ALERTS_CONFIRM,
                    Permissions.ALERTS_ASSIGN, Permissions.RESPONSE_DISPATCH, Permissions.RESPONSE_EXECUTE,
                    Permissions.RESPONSE_REVIEW, Permissions.POLICIES_READ, Permissions.POLICIES_WRITE,
                    Permissions.REPORTS_READ, Permissions.REPORTS_EXPORT, Permissions.AUDIT_READ))
    );
    private final Map<String, AuthenticatedUser> sessions = new ConcurrentHashMap<>();

    public LoginSession login(String role, String username, String password) {
        Account account = accounts.stream()
                .filter(candidate -> candidate.role().equals(role)
                        && candidate.username().equals(username)
                        && candidate.password().equals(password))
                .findFirst()
                .orElse(null);
        if (account == null) {
            return null;
        }

        String accessToken = "dev-access-token-" + UUID.randomUUID();
        String refreshToken = "dev-refresh-token-" + UUID.randomUUID();
        AuthenticatedUser user = new AuthenticatedUser(account.username(), account.role(), account.permissions(), OffsetDateTime.now());
        sessions.put(accessToken, user);
        return new LoginSession(accessToken, refreshToken, user);
    }

    public AuthenticatedUser find(String accessToken) {
        return accessToken == null ? null : sessions.get(accessToken);
    }

    private static Account account(String role, String username, String password, Set<String> permissions) {
        return new Account(role, username, password, permissions);
    }

    private record Account(String role, String username, String password, Set<String> permissions) {
    }

    public record AuthenticatedUser(String username, String role, Set<String> permissions, OffsetDateTime loginAt) {
        public boolean can(String permission) {
            return permissions.contains(permission);
        }

        public List<String> permissionList() {
            return permissions.stream().sorted().toList();
        }
    }

    public record LoginSession(String accessToken, String refreshToken, AuthenticatedUser user) {
    }
}

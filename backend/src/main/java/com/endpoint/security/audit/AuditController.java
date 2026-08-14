package com.endpoint.security.audit;

import com.endpoint.security.api.ApiResponse;
import com.endpoint.security.auth.AuthGuard;
import com.endpoint.security.auth.Permissions;
import jakarta.servlet.http.HttpServletRequest;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/api/audit-logs")
public class AuditController {
    private final AuthGuard authGuard;
    private final AuditLogStore auditLogStore;

    public AuditController(AuthGuard authGuard, AuditLogStore auditLogStore) {
        this.authGuard = authGuard;
        this.auditLogStore = auditLogStore;
    }

    @GetMapping
    public ApiResponse<List<AuditLog>> list(HttpServletRequest request) {
        AuthGuard.Check check = authGuard.require(request.getHeader("Authorization"), Permissions.AUDIT_READ);
        if (!check.allowed()) {
            return ApiResponse.error(check.error());
        }
        return ApiResponse.ok(auditLogStore.list());
    }
}

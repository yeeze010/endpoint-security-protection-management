package com.endpoint.security.audit;

import com.endpoint.security.api.ApiResponse;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.time.OffsetDateTime;
import java.util.List;

@RestController
@RequestMapping("/api/audit-logs")
public class AuditController {
    @GetMapping
    public ApiResponse<List<AuditLog>> list() {
        return ApiResponse.ok(List.of(
                new AuditLog("au-001", "admin", "发布策略", "默认病毒防护策略", "10.1.1.15", OffsetDateTime.now().minusMinutes(18)),
                new AuditLog("au-002", "secops", "关闭告警", "USB 存储设备接入被阻断", "10.1.1.21", OffsetDateTime.now().minusHours(1)),
                new AuditLog("au-003", "ops", "创建补丁任务", "服务器补丁维护窗口", "10.1.1.32", OffsetDateTime.now().minusHours(3))
        ));
    }
}

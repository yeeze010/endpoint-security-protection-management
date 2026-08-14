package com.endpoint.security.audit;

import org.springframework.stereotype.Component;

import java.time.OffsetDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;
import java.util.concurrent.ConcurrentLinkedDeque;

@Component
public class AuditLogStore {
    private final ConcurrentLinkedDeque<AuditLog> logs = new ConcurrentLinkedDeque<>();

    public AuditLogStore() {
        record("系统规则", "初始化演示状态", "终端安全平台", "成功");
    }

    public void record(String actor, String action, String resource, String result) {
        logs.addFirst(new AuditLog(UUID.randomUUID().toString(), actor, action, resource, result, OffsetDateTime.now()));
    }

    public List<AuditLog> list() {
        return new ArrayList<>(logs);
    }
}

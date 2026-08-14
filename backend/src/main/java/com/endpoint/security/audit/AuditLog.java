package com.endpoint.security.audit;

import java.time.OffsetDateTime;

public record AuditLog(
        String id,
        String actor,
        String action,
        String resource,
        String ip,
        OffsetDateTime createdAt
) {
}

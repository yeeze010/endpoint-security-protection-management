package com.endpoint.security.alert;

import java.time.OffsetDateTime;

public record SecurityAlert(
        String id,
        String endpoint,
        String title,
        String severity,
        String status,
        String assignee,
        OffsetDateTime lastSeenAt
) {
}

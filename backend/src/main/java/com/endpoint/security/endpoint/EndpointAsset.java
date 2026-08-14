package com.endpoint.security.endpoint;

import java.time.OffsetDateTime;

public record EndpointAsset(
        String id,
        String hostname,
        String ip,
        String os,
        String department,
        String owner,
        String agentVersion,
        String onlineStatus,
        String riskLevel,
        int riskScore,
        OffsetDateTime lastSeenAt
) {
}

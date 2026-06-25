package com.endpoint.security.response;

import java.util.List;

public record ResponsePlaybook(
        String alertId,
        String endpoint,
        String severity,
        String recommendedPolicy,
        boolean isolationRequired,
        int estimatedMinutes,
        List<ResponseAction> actions
) {
}

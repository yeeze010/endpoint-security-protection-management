package com.endpoint.security.policy;

public record Policy(
        String id,
        String name,
        String type,
        String status,
        String targetScope,
        int priority,
        String version
) {
}

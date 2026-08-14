package com.endpoint.security.response;

public record ResponseAction(
        String id,
        String title,
        String ownerRole,
        String status,
        int orderNo
) {
}

package com.endpoint.security.api;

import java.time.OffsetDateTime;

public record ApiResponse<T>(
        boolean success,
        T data,
        String message,
        String traceId,
        OffsetDateTime timestamp
) {
    public static <T> ApiResponse<T> ok(T data) {
        return new ApiResponse<>(true, data, "ok", TraceIds.current(), OffsetDateTime.now());
    }

    public static <T> ApiResponse<T> error(String message) {
        return new ApiResponse<>(false, null, message, TraceIds.current(), OffsetDateTime.now());
    }
}

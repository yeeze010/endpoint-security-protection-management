package com.endpoint.security.api;

import java.util.UUID;

public final class TraceIds {
    private TraceIds() {
    }

    public static String current() {
        return UUID.randomUUID().toString().substring(0, 12);
    }
}

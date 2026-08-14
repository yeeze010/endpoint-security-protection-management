package com.endpoint.security.auth;

import org.springframework.stereotype.Component;

@Component
public class AuthGuard {
    private final AuthSessionStore sessionStore;

    public AuthGuard(AuthSessionStore sessionStore) {
        this.sessionStore = sessionStore;
    }

    public Check require(String authorization, String permission) {
        AuthSessionStore.AuthenticatedUser user = sessionStore.find(tokenOf(authorization));
        if (user == null) {
            return new Check(null, "AUTH_401: login required");
        }
        if (permission != null && !user.can(permission)) {
            return new Check(null, "AUTH_403: permission denied");
        }
        return new Check(user, null);
    }

    private String tokenOf(String authorization) {
        if (authorization == null || authorization.isBlank()) {
            return null;
        }
        return authorization.startsWith("Bearer ") ? authorization.substring(7) : authorization;
    }

    public record Check(AuthSessionStore.AuthenticatedUser user, String error) {
        public boolean allowed() {
            return user != null;
        }
    }
}

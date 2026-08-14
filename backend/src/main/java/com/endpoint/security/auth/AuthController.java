package com.endpoint.security.auth;

import com.endpoint.security.api.ApiResponse;
import jakarta.validation.Valid;
import jakarta.validation.constraints.NotBlank;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/api/auth")
public class AuthController {
    private final AuthSessionStore sessionStore;

    public AuthController(AuthSessionStore sessionStore) {
        this.sessionStore = sessionStore;
    }

    @PostMapping("/login")
    public ApiResponse<LoginResponse> login(@Valid @RequestBody LoginRequest request) {
        AuthSessionStore.LoginSession session = sessionStore.login(request.role(), request.username(), request.password());
        if (session == null) {
            return ApiResponse.error("role, username or password is invalid");
        }
        AuthSessionStore.AuthenticatedUser user = session.user();
        return ApiResponse.ok(new LoginResponse(
                session.accessToken(), session.refreshToken(), user.username(), user.role(), user.permissionList()));
    }

    public record LoginRequest(@NotBlank String role, @NotBlank String username, @NotBlank String password) {
    }

    public record LoginResponse(
            String accessToken,
            String refreshToken,
            String username,
            String roleName,
            List<String> permissions
    ) {
    }
}

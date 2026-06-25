package com.endpoint.security.auth;

import com.endpoint.security.api.ApiResponse;
import jakarta.validation.Valid;
import jakarta.validation.constraints.NotBlank;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/auth")
public class AuthController {
    private final Map<String, LoginResponse> users = Map.of(
            "admin:admin:admin123", new LoginResponse("dev-access-token-admin", "dev-refresh-token-admin", "admin", "系统管理员", List.of("dashboard", "endpoints", "policies", "alerts", "audit", "response")),
            "security:secops:secops123", new LoginResponse("dev-access-token-secops", "dev-refresh-token-secops", "secops", "安全管理员", List.of("dashboard", "endpoints", "policies", "alerts", "response")),
            "operator:operator:operator123", new LoginResponse("dev-access-token-operator", "dev-refresh-token-operator", "operator", "运维管理员", List.of("dashboard", "endpoints", "alerts")),
            "auditor:auditor:auditor123", new LoginResponse("dev-access-token-auditor", "dev-refresh-token-auditor", "auditor", "只读审计员", List.of("dashboard", "audit"))
    );

    @PostMapping("/login")
    public ApiResponse<LoginResponse> login(@Valid @RequestBody LoginRequest request) {
        LoginResponse response = users.get(request.role() + ":" + request.username() + ":" + request.password());
        if (response == null) {
            return ApiResponse.error("role, username or password is invalid");
        }
        return ApiResponse.ok(response);
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

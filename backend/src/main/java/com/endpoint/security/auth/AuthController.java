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
    @PostMapping("/login")
    public ApiResponse<LoginResponse> login(@Valid @RequestBody LoginRequest request) {
        return ApiResponse.ok(new LoginResponse(
                "dev-access-token",
                "dev-refresh-token",
                request.username(),
                "安全管理员",
                List.of("dashboard", "endpoints", "policies", "alerts", "audit")
        ));
    }

    public record LoginRequest(@NotBlank String username, @NotBlank String password) {
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

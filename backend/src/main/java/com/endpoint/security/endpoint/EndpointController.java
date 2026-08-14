package com.endpoint.security.endpoint;

import com.endpoint.security.api.ApiResponse;
import com.endpoint.security.audit.AuditLogStore;
import com.endpoint.security.auth.AuthGuard;
import com.endpoint.security.auth.Permissions;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.validation.Valid;
import jakarta.validation.constraints.NotBlank;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.time.OffsetDateTime;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicInteger;

@RestController
@RequestMapping("/api/endpoints")
public class EndpointController {
    private final Map<String, EndpointAsset> assets = new ConcurrentHashMap<>();
    private final AtomicInteger nextId = new AtomicInteger(1005);
    private final AuthGuard authGuard;
    private final AuditLogStore auditLogStore;

    public EndpointController(AuthGuard authGuard, AuditLogStore auditLogStore) {
        this.authGuard = authGuard;
        this.auditLogStore = auditLogStore;
        seed();
    }

    @GetMapping
    public ApiResponse<List<EndpointAsset>> list(
            @RequestHeader(value = "Authorization", required = false) String authorization,
            @RequestParam(required = false) String keyword) {
        AuthGuard.Check check = authGuard.require(authorization, Permissions.ENDPOINTS_READ);
        if (!check.allowed()) {
            return ApiResponse.error(check.error());
        }
        String normalized = keyword == null ? "" : keyword.trim().toLowerCase();
        List<EndpointAsset> result = assets.values().stream()
                .filter(asset -> normalized.isBlank()
                        || asset.hostname().toLowerCase().contains(normalized)
                        || asset.ip().contains(normalized)
                        || asset.department().toLowerCase().contains(normalized)
                        || asset.owner().toLowerCase().contains(normalized))
                .sorted(Comparator.comparing(EndpointAsset::id))
                .toList();
        return ApiResponse.ok(result);
    }

    @GetMapping("/{id}")
    public ApiResponse<EndpointAsset> detail(
            @RequestHeader(value = "Authorization", required = false) String authorization,
            @PathVariable String id) {
        AuthGuard.Check check = authGuard.require(authorization, Permissions.ENDPOINTS_READ);
        if (!check.allowed()) {
            return ApiResponse.error(check.error());
        }
        return assets.values().stream()
                .filter(asset -> asset.id().equals(id))
                .findFirst()
                .map(ApiResponse::ok)
                .orElseGet(() -> ApiResponse.error("ENDPOINT_404: endpoint not found"));
    }

    @PostMapping("/register")
    public ApiResponse<EndpointAsset> register(
            @RequestHeader(value = "Authorization", required = false) String authorization,
            @Valid @RequestBody RegisterRequest request) {
        AuthGuard.Check check = authGuard.require(authorization, Permissions.ENDPOINTS_REGISTER);
        if (!check.allowed()) {
            return ApiResponse.error(check.error());
        }
        boolean duplicate = assets.values().stream().anyMatch(asset -> asset.hostname().equalsIgnoreCase(request.hostname()));
        if (duplicate) {
            return ApiResponse.error("ENDPOINT_409: hostname already registered");
        }
        String id = "ep-" + nextId.getAndIncrement();
        EndpointAsset asset = new EndpointAsset(
                id, request.hostname(), request.ip(), request.os(), request.department(), request.owner(),
                request.agentVersion(), "在线", "中", 40, OffsetDateTime.now());
        assets.put(id, asset);
        auditLogStore.record(check.user().username(), "接入终端", asset.hostname(), "成功");
        return ApiResponse.ok(asset);
    }

    @PostMapping("/{id}/heartbeat")
    public ApiResponse<EndpointAsset> heartbeat(
            @RequestHeader(value = "Authorization", required = false) String authorization,
            @PathVariable String id,
            @RequestBody(required = false) HeartbeatRequest request) {
        AuthGuard.Check check = authGuard.require(authorization, Permissions.ENDPOINTS_REGISTER);
        if (!check.allowed()) {
            return ApiResponse.error(check.error());
        }
        EndpointAsset current = assets.get(id);
        if (current == null) {
            return ApiResponse.error("ENDPOINT_404: endpoint not found");
        }
        String status = request != null && !request.onlineStatus().isBlank() ? request.onlineStatus() : "在线";
        EndpointAsset updated = new EndpointAsset(
                current.id(), current.hostname(), current.ip(), current.os(), current.department(), current.owner(),
                current.agentVersion(), status, current.riskLevel(), current.riskScore(), OffsetDateTime.now());
        assets.put(id, updated);
        auditLogStore.record(check.user().username(), "接收终端心跳", updated.hostname(), "成功");
        return ApiResponse.ok(updated);
    }

    @PostMapping("/{id}/commands")
    public ApiResponse<EndpointCommandResult> command(
            @RequestHeader(value = "Authorization", required = false) String authorization,
            @PathVariable String id,
            @Valid @RequestBody CommandRequest request) {
        AuthGuard.Check check = authGuard.require(authorization, Permissions.ENDPOINTS_COMMAND);
        if (!check.allowed()) {
            return ApiResponse.error(check.error());
        }
        EndpointAsset current = assets.get(id);
        if (current == null) {
            return ApiResponse.error("ENDPOINT_404: endpoint not found");
        }
        if (!"在线".equals(current.onlineStatus())) {
            return ApiResponse.error("ENDPOINT_409: endpoint is not online");
        }
        String action = switch (request.command()) {
            case "policy-sync" -> "策略同步";
            case "virus-scan" -> "病毒扫描";
            case "patch-remediation" -> "补丁整改";
            case "device-review" -> "外设复核";
            default -> null;
        };
        if (action == null) {
            return ApiResponse.error("ENDPOINT_422: unsupported command");
        }
        auditLogStore.record(check.user().username(), "下发终端命令", current.hostname() + " / " + action, "已下发");
        return ApiResponse.ok(new EndpointCommandResult(id, action, "已下发", OffsetDateTime.now()));
    }

    private void seed() {
        List<EndpointAsset> initial = List.of(
                new EndpointAsset("ep-1001", "FIN-PC-023", "10.16.4.23", "Windows 11", "财务部", "林晨", "1.4.2", "在线", "中", 62, OffsetDateTime.now().minusMinutes(3)),
                new EndpointAsset("ep-1002", "OPS-SRV-007", "10.20.8.7", "Ubuntu 22.04", "运维部", "周洋", "1.4.2", "在线", "高", 84, OffsetDateTime.now().minusMinutes(1)),
                new EndpointAsset("ep-1003", "HR-PC-118", "10.18.9.118", "Windows 10", "人事部", "陈宁", "1.3.8", "离线", "高", 71, OffsetDateTime.now().minusHours(2)),
                new EndpointAsset("ep-1004", "RND-MAC-031", "10.30.6.31", "macOS 14", "研发部", "王珂", "1.4.1", "在线", "严重", 93, OffsetDateTime.now().minusMinutes(7))
        );
        initial.forEach(asset -> assets.put(asset.id(), asset));
    }

    public record RegisterRequest(
            @NotBlank String hostname,
            @NotBlank String ip,
            @NotBlank String os,
            @NotBlank String department,
            @NotBlank String owner,
            @NotBlank String agentVersion
    ) {
    }

    public record HeartbeatRequest(String onlineStatus) {
    }

    public record CommandRequest(@NotBlank String command) {
    }

    public record EndpointCommandResult(String endpointId, String command, String status, OffsetDateTime acceptedAt) {
    }
}

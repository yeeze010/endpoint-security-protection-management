package com.endpoint.security.policy;

import com.endpoint.security.api.ApiResponse;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/api/policies")
public class PolicyController {
    @GetMapping
    public ApiResponse<List<Policy>> list() {
        return ApiResponse.ok(List.of(
                new Policy("pol-001", "默认病毒防护策略", "防病毒", "已发布", "全公司", 100, "v3"),
                new Policy("pol-002", "研发外设白名单", "外设管控", "审批中", "研发部", 80, "v1"),
                new Policy("pol-003", "服务器补丁维护窗口", "补丁管理", "草稿", "服务器分组", 70, "v2"),
                new Policy("pol-004", "高危终端隔离策略", "隔离处置", "已发布", "高危终端动态组", 120, "v5")
        ));
    }
}

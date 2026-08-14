package com.endpoint.security.response;

import com.endpoint.security.api.ApiResponse;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/response")
public class ResponseController {
    private final Map<String, ResponsePlaybook> playbooks = Map.of(
            "al-9001", new ResponsePlaybook(
                    "al-9001",
                    "RND-MAC-031",
                    "critical",
                    "高危终端隔离策略 v5",
                    true,
                    35,
                    List.of(
                            new ResponseAction("act-001", "隔离终端并保留远程取证通道", "安全管理员", "pending", 1),
                            new ResponseAction("act-002", "采集网络连接、进程、启动项证据", "安全管理员", "pending", 2),
                            new ResponseAction("act-003", "下发外联阻断策略到研发动态组", "安全管理员", "pending", 3),
                            new ResponseAction("act-004", "生成事件复盘和审计记录", "只读审计员", "pending", 4)
                    )
            ),
            "al-9002", new ResponsePlaybook(
                    "al-9002",
                    "OPS-SRV-007",
                    "high",
                    "服务器补丁维护窗口 v2",
                    false,
                    50,
                    List.of(
                            new ResponseAction("act-011", "确认业务低峰维护窗口", "运维管理员", "pending", 1),
                            new ResponseAction("act-012", "创建补丁快照并执行回滚预案检查", "运维管理员", "pending", 2),
                            new ResponseAction("act-013", "推送缺失补丁并验证 Agent 心跳", "运维管理员", "pending", 3)
                    )
            )
    );

    @GetMapping("/playbooks/{alertId}")
    public ApiResponse<ResponsePlaybook> playbook(@PathVariable String alertId) {
        ResponsePlaybook playbook = playbooks.get(alertId);
        if (playbook == null) {
            return ApiResponse.error("response playbook not found");
        }
        return ApiResponse.ok(playbook);
    }
}

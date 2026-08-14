package com.endpoint.security.alert;

import com.endpoint.security.api.ApiResponse;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.time.OffsetDateTime;
import java.util.List;

@RestController
@RequestMapping("/api/alerts")
public class AlertController {
    @GetMapping
    public ApiResponse<List<SecurityAlert>> list() {
        return ApiResponse.ok(List.of(
                new SecurityAlert("al-9001", "RND-MAC-031", "检测到异常外联行为", "严重", "待研判", "安全管理员", OffsetDateTime.now().minusMinutes(8)),
                new SecurityAlert("al-9002", "OPS-SRV-007", "系统补丁缺失超过 30 天", "高", "处理中", "运维管理员", OffsetDateTime.now().minusMinutes(24)),
                new SecurityAlert("al-9003", "FIN-PC-023", "USB 存储设备接入被阻断", "中", "已关闭", "安全管理员", OffsetDateTime.now().minusHours(1)),
                new SecurityAlert("al-9004", "HR-PC-118", "Agent 离线超过阈值", "低", "待处理", "运维管理员", OffsetDateTime.now().minusHours(2))
        ));
    }
}

package com.endpoint.security.dashboard;

import com.endpoint.security.api.ApiResponse;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/api/dashboard")
public class DashboardController {
    @GetMapping("/overview")
    public ApiResponse<DashboardOverview> overview() {
        return ApiResponse.ok(new DashboardOverview(
                List.of(
                        new MetricCard("终端总数", "1286", "+42 本周新增", "normal"),
                        new MetricCard("在线率", "94.8%", "过去 15 分钟", "normal"),
                        new MetricCard("高危告警", "17", "待处置 9 条", "danger"),
                        new MetricCard("补丁合规率", "87.3%", "+3.1% 较上周", "warning")
                ),
                List.of(
                        new TrendPoint("06-01", 45, 12),
                        new TrendPoint("06-02", 63, 17),
                        new TrendPoint("06-03", 38, 9),
                        new TrendPoint("06-04", 52, 11),
                        new TrendPoint("06-05", 71, 19),
                        new TrendPoint("06-06", 49, 13),
                        new TrendPoint("06-07", 34, 8)
                ),
                List.of(
                        new RiskDistribution("低风险", 814),
                        new RiskDistribution("中风险", 326),
                        new RiskDistribution("高风险", 129),
                        new RiskDistribution("严重", 17)
                )
        ));
    }
}

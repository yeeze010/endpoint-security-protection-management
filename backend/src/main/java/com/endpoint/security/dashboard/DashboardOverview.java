package com.endpoint.security.dashboard;

import java.util.List;

public record DashboardOverview(
        List<MetricCard> metrics,
        List<TrendPoint> alertTrend,
        List<RiskDistribution> riskDistribution
) {
}

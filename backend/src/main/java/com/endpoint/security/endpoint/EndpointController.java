package com.endpoint.security.endpoint;

import com.endpoint.security.api.ApiResponse;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.time.OffsetDateTime;
import java.util.List;

@RestController
@RequestMapping("/api/endpoints")
public class EndpointController {
    private final List<EndpointAsset> assets = List.of(
            new EndpointAsset("ep-1001", "FIN-PC-023", "10.16.4.23", "Windows 11", "财务部", "林晨", "1.4.2", "在线", "中", 62, OffsetDateTime.now().minusMinutes(3)),
            new EndpointAsset("ep-1002", "OPS-SRV-007", "10.20.8.7", "Ubuntu 22.04", "运维部", "周洋", "1.4.2", "在线", "高", 84, OffsetDateTime.now().minusMinutes(1)),
            new EndpointAsset("ep-1003", "HR-PC-118", "10.18.9.118", "Windows 10", "人事部", "陈宁", "1.3.8", "离线", "低", 24, OffsetDateTime.now().minusHours(2)),
            new EndpointAsset("ep-1004", "RND-MAC-031", "10.30.6.31", "macOS 14", "研发部", "王珂", "1.4.1", "在线", "严重", 93, OffsetDateTime.now().minusMinutes(7))
    );

    @GetMapping
    public ApiResponse<List<EndpointAsset>> list(@RequestParam(required = false) String keyword) {
        if (keyword == null || keyword.isBlank()) {
            return ApiResponse.ok(assets);
        }
        String lowerKeyword = keyword.toLowerCase();
        return ApiResponse.ok(assets.stream()
                .filter(asset -> asset.hostname().toLowerCase().contains(lowerKeyword)
                        || asset.ip().contains(lowerKeyword)
                        || asset.department().contains(keyword))
                .toList());
    }

    @GetMapping("/{id}")
    public ApiResponse<EndpointAsset> detail(@PathVariable String id) {
        return assets.stream()
                .filter(asset -> asset.id().equals(id))
                .findFirst()
                .map(ApiResponse::ok)
                .orElseGet(() -> ApiResponse.error("endpoint not found"));
    }
}

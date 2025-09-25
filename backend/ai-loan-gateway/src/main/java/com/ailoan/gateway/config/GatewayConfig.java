package com.ailoan.gateway.config;

import org.springframework.cloud.gateway.route.RouteLocator;
import org.springframework.cloud.gateway.route.builder.RouteLocatorBuilder;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/**
 * 网关路由配置
 */
@Configuration
public class GatewayConfig {

    @Bean
    public RouteLocator customRouteLocator(RouteLocatorBuilder builder) {
        return builder.routes()
                // 用户服务路由
                .route("user-service", r -> r.path("/api/users/**")
                        .uri("lb://ai-loan-user-service"))
                
                // 贷款申请服务路由
                .route("loan-service", r -> r.path("/api/loans/**")
                        .uri("lb://ai-loan-loan-service"))
                
                // 风险评估服务路由
                .route("risk-service", r -> r.path("/api/risk/**")
                        .uri("lb://ai-loan-risk-service"))
                
                // 智能匹配服务路由
                .route("matching-service", r -> r.path("/api/matching/**")
                        .uri("lb://ai-loan-matching-service"))
                
                // 管理后台服务路由
                .route("admin-service", r -> r.path("/api/admin/**")
                        .uri("lb://ai-loan-admin-service"))
                
                // AI服务路由
                .route("ai-service", r -> r.path("/api/ai/**")
                        .uri("lb://ai-loan-ai-service"))
                
                .build();
    }
}

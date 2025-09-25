package com.ailoan.gateway;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.netflix.eureka.EnableEurekaClient;

/**
 * AI智能助贷招标平台 - API网关启动类
 */
@SpringBootApplication
@EnableEurekaClient
public class AiLoanGatewayApplication {
    public static void main(String[] args) {
        SpringApplication.run(AiLoanGatewayApplication.class, args);
    }
}

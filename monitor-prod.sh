#!/bin/bash

# AI助贷招标平台 - 生产环境监控脚本
# 作者: AI Loan Platform Team
# 版本: 1.0.0

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查服务状态
check_service_status() {
    local service_name=$1
    local url=$2
    
    if curl -f -s "$url" > /dev/null 2>&1; then
        log_success "$service_name 运行正常"
        return 0
    else
        log_error "$service_name 运行异常"
        return 1
    fi
}

# 检查容器状态
check_container_status() {
    local container_name=$1
    
    if docker ps --format "table {{.Names}}\t{{.Status}}" | grep -q "$container_name.*Up"; then
        log_success "容器 $container_name 运行正常"
        return 0
    else
        log_error "容器 $container_name 运行异常"
        return 1
    fi
}

# 检查资源使用情况
check_resource_usage() {
    log_info "检查资源使用情况..."
    
    echo "=== CPU 使用率 ==="
    docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}"
    
    echo ""
    echo "=== 磁盘使用情况 ==="
    df -h | grep -E "(Filesystem|/dev/)"
    
    echo ""
    echo "=== 内存使用情况 ==="
    free -h
}

# 检查日志错误
check_logs() {
    log_info "检查最近错误日志..."
    
    echo "=== AI服务错误日志 ==="
    docker logs ai-loan-ai-service-prod --tail 20 2>&1 | grep -i error || echo "无错误日志"
    
    echo ""
    echo "=== 网关错误日志 ==="
    docker logs ai-loan-gateway-prod --tail 20 2>&1 | grep -i error || echo "无错误日志"
    
    echo ""
    echo "=== Nginx错误日志 ==="
    docker logs ai-loan-nginx-prod --tail 20 2>&1 | grep -i error || echo "无错误日志"
}

# 检查API响应时间
check_api_performance() {
    log_info "检查API响应时间..."
    
    local apis=(
        "AI服务健康检查:http://localhost:8000/health"
        "网关健康检查:http://localhost:8080/health"
        "前端应用:http://localhost:3000"
        "管理后台:http://localhost:3001"
    )
    
    for api in "${apis[@]}"; do
        IFS=':' read -r name url <<< "$api"
        echo -n "测试 $name... "
        
        start_time=$(date +%s%N)
        if curl -f -s "$url" > /dev/null 2>&1; then
            end_time=$(date +%s%N)
            response_time=$(( (end_time - start_time) / 1000000 ))
            echo "响应时间: ${response_time}ms"
        else
            echo "请求失败"
        fi
    done
}

# 生成监控报告
generate_report() {
    local report_file="monitor-report-$(date +%Y%m%d-%H%M%S).txt"
    
    log_info "生成监控报告: $report_file"
    
    {
        echo "AI助贷招标平台 - 生产环境监控报告"
        echo "生成时间: $(date)"
        echo "=================================="
        echo ""
        
        echo "=== 服务状态 ==="
        docker-compose -f docker-compose.prod.yml ps
        echo ""
        
        echo "=== 资源使用情况 ==="
        docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}"
        echo ""
        
        echo "=== 系统资源 ==="
        echo "CPU使用率:"
        top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1
        echo "内存使用率:"
        free | grep Mem | awk '{printf "%.2f%%\n", $3/$2 * 100.0}'
        echo "磁盘使用率:"
        df -h | grep -E "(Filesystem|/dev/)" | awk '{print $1 " " $5}'
        echo ""
        
        echo "=== 网络连接 ==="
        netstat -tuln | grep -E ":(80|443|3000|3001|8000|8080|3306|6379|27017|9200)"
        echo ""
        
        echo "=== 最近错误日志 ==="
        docker logs ai-loan-ai-service-prod --tail 10 2>&1 | grep -i error || echo "无错误日志"
        
    } > "$report_file"
    
    log_success "监控报告已生成: $report_file"
}

# 主监控函数
main_monitor() {
    log_info "开始生产环境监控..."
    
    echo "=================================="
    echo "AI助贷招标平台 - 生产环境监控"
    echo "时间: $(date)"
    echo "=================================="
    echo ""
    
    # 检查服务状态
    log_info "检查服务状态..."
    check_service_status "AI服务" "http://localhost:8000/health"
    check_service_status "网关服务" "http://localhost:8080/health"
    check_service_status "前端应用" "http://localhost:3000"
    check_service_status "管理后台" "http://localhost:3001"
    echo ""
    
    # 检查容器状态
    log_info "检查容器状态..."
    check_container_status "ai-loan-ai-service-prod"
    check_container_status "ai-loan-gateway-prod"
    check_container_status "ai-loan-web-app-prod"
    check_container_status "ai-loan-admin-app-prod"
    check_container_status "ai-loan-nginx-prod"
    echo ""
    
    # 检查资源使用情况
    check_resource_usage
    echo ""
    
    # 检查API性能
    check_api_performance
    echo ""
    
    # 检查日志错误
    check_logs
    echo ""
    
    # 生成监控报告
    generate_report
}

# 实时监控
real_time_monitor() {
    log_info "开始实时监控 (按 Ctrl+C 退出)..."
    
    while true; do
        clear
        echo "AI助贷招标平台 - 实时监控"
        echo "时间: $(date)"
        echo "=================================="
        
        # 显示容器状态
        echo "=== 容器状态 ==="
        docker-compose -f docker-compose.prod.yml ps
        echo ""
        
        # 显示资源使用情况
        echo "=== 资源使用情况 ==="
        docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}"
        echo ""
        
        # 显示网络连接
        echo "=== 网络连接 ==="
        netstat -tuln | grep -E ":(80|443|3000|3001|8000|8080)" | head -10
        echo ""
        
        echo "按 Ctrl+C 退出监控"
        sleep 5
    done
}

# 主函数
main() {
    case "${1:-monitor}" in
        "monitor")
            main_monitor
            ;;
        "realtime")
            real_time_monitor
            ;;
        "report")
            generate_report
            ;;
        *)
            echo "用法: $0 {monitor|realtime|report}"
            echo "  monitor  - 执行一次监控检查（默认）"
            echo "  realtime - 实时监控"
            echo "  report   - 生成监控报告"
            exit 1
            ;;
    esac
}

# 执行主函数
main "$@"

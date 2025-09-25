#!/bin/bash

# AI助贷招标平台 - 生产环境部署脚本
# 作者: AI Loan Platform Team
# 版本: 1.0.0

set -e

echo "🚀 开始生产环境部署..."

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

# 检查Docker和Docker Compose
check_prerequisites() {
    log_info "检查前置条件..."
    
    if ! command -v docker &> /dev/null; then
        log_error "Docker 未安装，请先安装 Docker"
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        log_error "Docker Compose 未安装，请先安装 Docker Compose"
        exit 1
    fi
    
    log_success "前置条件检查通过"
}

# 创建必要的目录
create_directories() {
    log_info "创建必要的目录..."
    
    mkdir -p data/mysql
    mkdir -p data/redis
    mkdir -p data/mongodb
    mkdir -p data/elasticsearch
    mkdir -p data/ai-models
    mkdir -p data/ai-uploads
    mkdir -p logs/nginx
    mkdir -p logs/applications
    
    log_success "目录创建完成"
}

# 设置环境变量
setup_environment() {
    log_info "设置环境变量..."
    
    if [ ! -f .env.prod ]; then
        log_warning "未找到 .env.prod 文件，使用默认配置"
        cp env.prod.example .env.prod
        log_warning "请编辑 .env.prod 文件以配置生产环境参数"
    fi
    
    log_success "环境变量设置完成"
}

# 构建镜像
build_images() {
    log_info "构建Docker镜像..."
    
    # 构建AI服务
    log_info "构建AI服务镜像..."
    docker-compose -f docker-compose.prod.yml build ai-service
    
    # 构建网关服务
    log_info "构建网关服务镜像..."
    docker-compose -f docker-compose.prod.yml build gateway
    
    # 构建其他服务
    log_info "构建其他服务镜像..."
    docker-compose -f docker-compose.prod.yml build user-service loan-service risk-service matching-service admin-service
    
    # 构建前端应用
    log_info "构建前端应用镜像..."
    docker-compose -f docker-compose.prod.yml build web-app admin-app
    
    log_success "镜像构建完成"
}

# 启动服务
start_services() {
    log_info "启动生产环境服务..."
    
    # 启动数据库服务
    log_info "启动数据库服务..."
    docker-compose -f docker-compose.prod.yml up -d mysql redis mongodb elasticsearch
    
    # 等待数据库启动
    log_info "等待数据库启动..."
    sleep 30
    
    # 启动AI服务
    log_info "启动AI服务..."
    docker-compose -f docker-compose.prod.yml up -d ai-service
    
    # 等待AI服务启动
    log_info "等待AI服务启动..."
    sleep 20
    
    # 启动后端服务
    log_info "启动后端服务..."
    docker-compose -f docker-compose.prod.yml up -d user-service loan-service risk-service matching-service admin-service
    
    # 等待后端服务启动
    log_info "等待后端服务启动..."
    sleep 30
    
    # 启动网关
    log_info "启动网关服务..."
    docker-compose -f docker-compose.prod.yml up -d gateway
    
    # 等待网关启动
    log_info "等待网关启动..."
    sleep 20
    
    # 启动前端应用
    log_info "启动前端应用..."
    docker-compose -f docker-compose.prod.yml up -d web-app admin-app
    
    # 启动Nginx
    log_info "启动Nginx负载均衡器..."
    docker-compose -f docker-compose.prod.yml up -d nginx
    
    log_success "所有服务启动完成"
}

# 健康检查
health_check() {
    log_info "执行健康检查..."
    
    # 检查AI服务
    if curl -f http://localhost:8000/health > /dev/null 2>&1; then
        log_success "AI服务健康检查通过"
    else
        log_error "AI服务健康检查失败"
    fi
    
    # 检查网关
    if curl -f http://localhost:8080/health > /dev/null 2>&1; then
        log_success "网关健康检查通过"
    else
        log_warning "网关健康检查失败，可能正在启动中"
    fi
    
    # 检查前端应用
    if curl -f http://localhost:3000 > /dev/null 2>&1; then
        log_success "前端应用健康检查通过"
    else
        log_warning "前端应用健康检查失败，可能正在启动中"
    fi
    
    # 检查管理后台
    if curl -f http://localhost:3001 > /dev/null 2>&1; then
        log_success "管理后台健康检查通过"
    else
        log_warning "管理后台健康检查失败，可能正在启动中"
    fi
}

# 显示服务状态
show_status() {
    log_info "服务状态:"
    docker-compose -f docker-compose.prod.yml ps
    
    echo ""
    log_info "访问地址:"
    echo "  前端应用: http://localhost:3000"
    echo "  管理后台: http://localhost:3001"
    echo "  API网关: http://localhost:8080"
    echo "  AI服务: http://localhost:8000"
    echo "  Nginx: http://localhost:80"
}

# 清理函数
cleanup() {
    log_info "清理资源..."
    docker-compose -f docker-compose.prod.yml down
    log_success "清理完成"
}

# 主函数
main() {
    case "${1:-deploy}" in
        "deploy")
            check_prerequisites
            create_directories
            setup_environment
            build_images
            start_services
            health_check
            show_status
            ;;
        "start")
            start_services
            health_check
            show_status
            ;;
        "stop")
            cleanup
            ;;
        "restart")
            cleanup
            start_services
            health_check
            show_status
            ;;
        "status")
            show_status
            ;;
        "logs")
            docker-compose -f docker-compose.prod.yml logs -f
            ;;
        *)
            echo "用法: $0 {deploy|start|stop|restart|status|logs}"
            echo "  deploy  - 完整部署（默认）"
            echo "  start   - 启动服务"
            echo "  stop    - 停止服务"
            echo "  restart - 重启服务"
            echo "  status  - 查看状态"
            echo "  logs    - 查看日志"
            exit 1
            ;;
    esac
}

# 执行主函数
main "$@"

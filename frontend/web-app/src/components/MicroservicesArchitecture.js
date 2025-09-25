import React, { useState, useEffect } from 'react';
import { useNotification } from './NotificationSystem';
import './MicroservicesArchitecture.css';

const MicroservicesArchitecture = () => {
  const [services, setServices] = useState([]);
  const [selectedService, setSelectedService] = useState(null);
  const [isDeploying, setIsDeploying] = useState(false);
  const [deploymentLogs, setDeploymentLogs] = useState([]);
  const [serviceMetrics, setServiceMetrics] = useState({});
  const [isScaling, setIsScaling] = useState(false);
  const { showSuccess, showError, showInfo } = useNotification();

  useEffect(() => {
    loadServices();
    loadServiceMetrics();
  }, []);

  const loadServices = async () => {
    try {
      // 模拟微服务数据
      const mockServices = [
        {
          id: 1,
          name: 'user-service',
          displayName: '用户服务',
          version: 'v2.1.0',
          status: 'running',
          replicas: 3,
          desiredReplicas: 3,
          cpu: 45,
          memory: 60,
          uptime: '99.9%',
          lastDeployment: '2025-09-21 14:00:00',
          port: 8080,
          healthCheck: '/health',
          dependencies: ['auth-service', 'notification-service'],
          environment: 'production',
          image: 'ai-loan-platform/user-service:latest',
          resources: {
            cpu: '500m',
            memory: '1Gi',
            storage: '10Gi'
          }
        },
        {
          id: 2,
          name: 'loan-service',
          displayName: '贷款服务',
          version: 'v1.8.2',
          status: 'running',
          replicas: 5,
          desiredReplicas: 5,
          cpu: 75,
          memory: 80,
          uptime: '99.8%',
          lastDeployment: '2025-09-21 13:30:00',
          port: 8081,
          healthCheck: '/health',
          dependencies: ['user-service', 'risk-service', 'payment-service'],
          environment: 'production',
          image: 'ai-loan-platform/loan-service:latest',
          resources: {
            cpu: '1000m',
            memory: '2Gi',
            storage: '20Gi'
          }
        },
        {
          id: 3,
          name: 'risk-service',
          displayName: '风险评估服务',
          version: 'v3.0.1',
          status: 'running',
          replicas: 2,
          desiredReplicas: 2,
          cpu: 85,
          memory: 90,
          uptime: '99.7%',
          lastDeployment: '2025-09-21 12:00:00',
          port: 8082,
          healthCheck: '/health',
          dependencies: ['ai-service', 'data-service'],
          environment: 'production',
          image: 'ai-loan-platform/risk-service:latest',
          resources: {
            cpu: '2000m',
            memory: '4Gi',
            storage: '50Gi'
          }
        },
        {
          id: 4,
          name: 'ai-service',
          displayName: 'AI服务',
          version: 'v4.2.0',
          status: 'running',
          replicas: 1,
          desiredReplicas: 1,
          cpu: 95,
          memory: 95,
          uptime: '99.5%',
          lastDeployment: '2025-09-21 11:00:00',
          port: 8083,
          healthCheck: '/health',
          dependencies: ['data-service'],
          environment: 'production',
          image: 'ai-loan-platform/ai-service:latest',
          resources: {
            cpu: '4000m',
            memory: '8Gi',
            storage: '100Gi'
          }
        },
        {
          id: 5,
          name: 'payment-service',
          displayName: '支付服务',
          version: 'v1.5.3',
          status: 'degraded',
          replicas: 2,
          desiredReplicas: 3,
          cpu: 60,
          memory: 70,
          uptime: '98.5%',
          lastDeployment: '2025-09-21 10:00:00',
          port: 8084,
          healthCheck: '/health',
          dependencies: ['user-service', 'notification-service'],
          environment: 'production',
          image: 'ai-loan-platform/payment-service:latest',
          resources: {
            cpu: '800m',
            memory: '1.5Gi',
            storage: '15Gi'
          }
        },
        {
          id: 6,
          name: 'notification-service',
          displayName: '通知服务',
          version: 'v2.0.0',
          status: 'running',
          replicas: 2,
          desiredReplicas: 2,
          cpu: 30,
          memory: 40,
          uptime: '99.9%',
          lastDeployment: '2025-09-21 09:00:00',
          port: 8085,
          healthCheck: '/health',
          dependencies: [],
          environment: 'production',
          image: 'ai-loan-platform/notification-service:latest',
          resources: {
            cpu: '300m',
            memory: '512Mi',
            storage: '5Gi'
          }
        }
      ];
      setServices(mockServices);
    } catch (error) {
      showError('加载微服务失败');
    }
  };

  const loadServiceMetrics = () => {
    // 模拟服务指标数据
    const mockMetrics = {
      totalServices: 6,
      runningServices: 5,
      degradedServices: 1,
      failedServices: 0,
      totalReplicas: 15,
      avgCpuUsage: 65,
      avgMemoryUsage: 70,
      totalUptime: 99.7
    };
    setServiceMetrics(mockMetrics);
  };

  const handleDeployService = async (service) => {
    setIsDeploying(true);
    setSelectedService(service);
    setDeploymentLogs([]);
    
    showInfo(`正在部署 ${service.displayName}...`);
    
    try {
      // 模拟部署过程
      const deploymentSteps = [
        '正在拉取最新镜像...',
        '正在停止旧实例...',
        '正在启动新实例...',
        '正在执行健康检查...',
        '正在更新负载均衡器...',
        '部署完成！'
      ];
      
      for (let i = 0; i < deploymentSteps.length; i++) {
        await new Promise(resolve => setTimeout(resolve, 1000));
        setDeploymentLogs(prev => [...prev, {
          timestamp: new Date().toLocaleTimeString(),
          message: deploymentSteps[i],
          status: i === deploymentSteps.length - 1 ? 'success' : 'info'
        }]);
      }
      
      // 更新服务状态
      const updatedServices = services.map(s => 
        s.id === service.id 
          ? { ...s, lastDeployment: new Date().toLocaleString(), status: 'running' }
          : s
      );
      setServices(updatedServices);
      
      showSuccess(`${service.displayName} 部署成功`);
    } catch (error) {
      showError(`${service.displayName} 部署失败`);
    } finally {
      setIsDeploying(false);
    }
  };

  const handleScaleService = async (service, replicas) => {
    setIsScaling(true);
    showInfo(`正在调整 ${service.displayName} 副本数量到 ${replicas}...`);
    
    try {
      // 模拟扩缩容过程
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      const updatedServices = services.map(s => 
        s.id === service.id 
          ? { ...s, desiredReplicas: replicas, replicas: replicas }
          : s
      );
      setServices(updatedServices);
      
      showSuccess(`${service.displayName} 扩缩容成功`);
    } catch (error) {
      showError(`${service.displayName} 扩缩容失败`);
    } finally {
      setIsScaling(false);
    }
  };

  const handleRestartService = async (service) => {
    showInfo(`正在重启 ${service.displayName}...`);
    
    try {
      // 模拟重启过程
      await new Promise(resolve => setTimeout(resolve, 3000));
      
      const updatedServices = services.map(s => 
        s.id === service.id 
          ? { ...s, lastDeployment: new Date().toLocaleString() }
          : s
      );
      setServices(updatedServices);
      
      showSuccess(`${service.displayName} 重启成功`);
    } catch (error) {
      showError(`${service.displayName} 重启失败`);
    }
  };

  const handleViewLogs = (service) => {
    setSelectedService(service);
    showInfo(`正在加载 ${service.displayName} 日志...`);
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'running': return '#28a745';
      case 'degraded': return '#ffc107';
      case 'failed': return '#dc3545';
      case 'stopped': return '#6c757d';
      default: return '#6c757d';
    }
  };

  const getStatusText = (status) => {
    switch (status) {
      case 'running': return '运行中';
      case 'degraded': return '降级';
      case 'failed': return '失败';
      case 'stopped': return '已停止';
      default: return '未知';
    }
  };

  const getCpuColor = (cpu) => {
    if (cpu > 80) return '#dc3545';
    if (cpu > 60) return '#ffc107';
    return '#28a745';
  };

  const getMemoryColor = (memory) => {
    if (memory > 80) return '#dc3545';
    if (memory > 60) return '#ffc107';
    return '#28a745';
  };

  return (
    <div className="microservices-architecture">
      <div className="architecture-header">
        <h1>微服务架构管理</h1>
        <p>管理和监控微服务架构，确保系统高可用性和可扩展性</p>
        
        <div className="architecture-stats">
          <div className="stat-card">
            <div className="stat-icon">🔧</div>
            <div className="stat-content">
              <h3>{serviceMetrics.totalServices}</h3>
              <p>总服务数</p>
            </div>
          </div>
          <div className="stat-card">
            <div className="stat-icon">✅</div>
            <div className="stat-content">
              <h3>{serviceMetrics.runningServices}</h3>
              <p>运行中</p>
            </div>
          </div>
          <div className="stat-card">
            <div className="stat-icon">📊</div>
            <div className="stat-content">
              <h3>{serviceMetrics.totalReplicas}</h3>
              <p>总副本数</p>
            </div>
          </div>
          <div className="stat-card">
            <div className="stat-icon">⚡</div>
            <div className="stat-content">
              <h3>{serviceMetrics.avgCpuUsage}%</h3>
              <p>平均CPU使用率</p>
            </div>
          </div>
          <div className="stat-card">
            <div className="stat-icon">💾</div>
            <div className="stat-content">
              <h3>{serviceMetrics.avgMemoryUsage}%</h3>
              <p>平均内存使用率</p>
            </div>
          </div>
          <div className="stat-card">
            <div className="stat-icon">⏱️</div>
            <div className="stat-content">
              <h3>{serviceMetrics.totalUptime}%</h3>
              <p>系统可用性</p>
            </div>
          </div>
        </div>
      </div>

      <div className="architecture-content">
        <div className="services-section">
          <h2>微服务列表</h2>
          
          <div className="services-grid">
            {services.map(service => (
              <div key={service.id} className="service-card">
                <div className="service-header">
                  <div className="service-info">
                    <h3>{service.displayName}</h3>
                    <p className="service-name">{service.name}</p>
                    <span className="service-version">v{service.version}</span>
                    <span 
                      className="status-badge"
                      style={{ color: getStatusColor(service.status) }}
                    >
                      {getStatusText(service.status)}
                    </span>
                  </div>
                  <div className="service-actions">
                    <button 
                      className="action-btn deploy"
                      onClick={() => handleDeployService(service)}
                      disabled={isDeploying}
                    >
                      🚀 部署
                    </button>
                    <button 
                      className="action-btn restart"
                      onClick={() => handleRestartService(service)}
                    >
                      🔄 重启
                    </button>
                    <button 
                      className="action-btn logs"
                      onClick={() => handleViewLogs(service)}
                    >
                      📋 日志
                    </button>
                  </div>
                </div>
                
                <div className="service-content">
                  <div className="service-metrics">
                    <div className="metric">
                      <span className="metric-label">副本数:</span>
                      <span className="metric-value">
                        {service.replicas}/{service.desiredReplicas}
                      </span>
                      <div className="scale-controls">
                        <button 
                          className="scale-btn"
                          onClick={() => handleScaleService(service, Math.max(0, service.desiredReplicas - 1))}
                          disabled={isScaling}
                        >
                          -
                        </button>
                        <button 
                          className="scale-btn"
                          onClick={() => handleScaleService(service, service.desiredReplicas + 1)}
                          disabled={isScaling}
                        >
                          +
                        </button>
                      </div>
                    </div>
                    
                    <div className="metric">
                      <span className="metric-label">CPU使用率:</span>
                      <div className="metric-bar">
                        <div 
                          className="metric-progress"
                          style={{ 
                            width: `${service.cpu}%`,
                            backgroundColor: getCpuColor(service.cpu)
                          }}
                        ></div>
                      </div>
                      <span className="metric-value">{service.cpu}%</span>
                    </div>
                    
                    <div className="metric">
                      <span className="metric-label">内存使用率:</span>
                      <div className="metric-bar">
                        <div 
                          className="metric-progress"
                          style={{ 
                            width: `${service.memory}%`,
                            backgroundColor: getMemoryColor(service.memory)
                          }}
                        ></div>
                      </div>
                      <span className="metric-value">{service.memory}%</span>
                    </div>
                    
                    <div className="metric">
                      <span className="metric-label">可用性:</span>
                      <span className="metric-value">{service.uptime}</span>
                    </div>
                  </div>
                  
                  <div className="service-details">
                    <div className="detail-item">
                      <span className="label">端口:</span>
                      <span className="value">{service.port}</span>
                    </div>
                    <div className="detail-item">
                      <span className="label">环境:</span>
                      <span className="value">{service.environment}</span>
                    </div>
                    <div className="detail-item">
                      <span className="label">镜像:</span>
                      <span className="value">{service.image}</span>
                    </div>
                    <div className="detail-item">
                      <span className="label">最后部署:</span>
                      <span className="value">{service.lastDeployment}</span>
                    </div>
                  </div>
                  
                  {service.dependencies && service.dependencies.length > 0 && (
                    <div className="service-dependencies">
                      <h4>依赖服务:</h4>
                      <div className="dependencies-list">
                        {service.dependencies.map((dep, index) => (
                          <span key={index} className="dependency-tag">
                            {dep}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* 部署日志对话框 */}
      {isDeploying && selectedService && (
        <div className="deployment-modal">
          <div className="modal-content">
            <div className="modal-header">
              <h2>部署 {selectedService.displayName}</h2>
              <button 
                className="close-btn"
                onClick={() => setIsDeploying(false)}
              >
                ✕
              </button>
            </div>
            
            <div className="modal-body">
              <div className="deployment-logs">
                {deploymentLogs.map((log, index) => (
                  <div key={index} className={`log-entry ${log.status}`}>
                    <span className="log-time">{log.timestamp}</span>
                    <span className="log-message">{log.message}</span>
                  </div>
                ))}
                {isDeploying && (
                  <div className="log-entry info">
                    <span className="log-time">{new Date().toLocaleTimeString()}</span>
                    <span className="log-message">部署进行中...</span>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default MicroservicesArchitecture;

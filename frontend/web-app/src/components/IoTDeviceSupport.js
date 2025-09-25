import React, { useState, useEffect } from 'react';
import { useNotification } from './NotificationSystem';
import './IoTDeviceSupport.css';

const IoTDeviceSupport = () => {
  const [devices, setDevices] = useState([]);
  const [deviceTypes, setDeviceTypes] = useState([]);
  const [deviceData, setDeviceData] = useState({});
  const [isConnecting, setIsConnecting] = useState(false);
  const [selectedDevice, setSelectedDevice] = useState(null);
  const [deviceMetrics, setDeviceMetrics] = useState({});
  const { showSuccess, showError, showInfo } = useNotification();

  useEffect(() => {
    loadDevices();
    loadDeviceTypes();
    loadDeviceMetrics();
  }, []);

  const loadDevices = async () => {
    try {
      // 模拟物联网设备数据
      const mockDevices = [
        {
          id: 1,
          name: '智能门锁-001',
          type: 'smart_lock',
          status: 'online',
          location: '办公室大门',
          ipAddress: '192.168.1.101',
          macAddress: '00:11:22:33:44:55',
          firmware: 'v2.1.3',
          batteryLevel: 85,
          signalStrength: -45,
          lastSeen: '2025-09-21 14:30:00',
          capabilities: ['指纹识别', '密码解锁', '远程控制', '访问记录'],
          sensors: [
            { name: '指纹传感器', status: 'active', value: '正常' },
            { name: '温度传感器', status: 'active', value: '23.5°C' },
            { name: '湿度传感器', status: 'active', value: '45%' }
          ],
          alerts: []
        },
        {
          id: 2,
          name: '环境监测器-002',
          type: 'environmental_monitor',
          status: 'online',
          location: '数据中心',
          ipAddress: '192.168.1.102',
          macAddress: '00:11:22:33:44:56',
          firmware: 'v1.8.2',
          batteryLevel: 92,
          signalStrength: -38,
          lastSeen: '2025-09-21 14:29:00',
          capabilities: ['温度监测', '湿度监测', '空气质量', '噪音监测'],
          sensors: [
            { name: '温度传感器', status: 'active', value: '22.1°C' },
            { name: '湿度传感器', status: 'active', value: '52%' },
            { name: 'PM2.5传感器', status: 'active', value: '15 μg/m³' },
            { name: '噪音传感器', status: 'active', value: '45 dB' }
          ],
          alerts: [
            { type: 'warning', message: '温度异常', timestamp: '2025-09-21 14:25:00' }
          ]
        },
        {
          id: 3,
          name: '安全摄像头-003',
          type: 'security_camera',
          status: 'online',
          location: '入口大厅',
          ipAddress: '192.168.1.103',
          macAddress: '00:11:22:33:44:57',
          firmware: 'v3.0.1',
          batteryLevel: 100,
          signalStrength: -42,
          lastSeen: '2025-09-21 14:30:00',
          capabilities: ['视频录制', '人脸识别', '运动检测', '夜视功能'],
          sensors: [
            { name: '摄像头', status: 'active', value: '1080p@30fps' },
            { name: '红外传感器', status: 'active', value: '夜视模式' },
            { name: '麦克风', status: 'active', value: '音频录制' }
          ],
          alerts: []
        },
        {
          id: 4,
          name: '智能照明-004',
          type: 'smart_lighting',
          status: 'offline',
          location: '会议室A',
          ipAddress: '192.168.1.104',
          macAddress: '00:11:22:33:44:58',
          firmware: 'v1.5.0',
          batteryLevel: 0,
          signalStrength: 0,
          lastSeen: '2025-09-21 13:45:00',
          capabilities: ['亮度调节', '颜色调节', '定时控制', '场景模式'],
          sensors: [
            { name: '光敏传感器', status: 'inactive', value: '无数据' },
            { name: '运动传感器', status: 'inactive', value: '无数据' }
          ],
          alerts: [
            { type: 'error', message: '设备离线', timestamp: '2025-09-21 13:45:00' }
          ]
        },
        {
          id: 5,
          name: '温控器-005',
          type: 'thermostat',
          status: 'online',
          location: '服务器机房',
          ipAddress: '192.168.1.105',
          macAddress: '00:11:22:33:44:59',
          firmware: 'v2.3.1',
          batteryLevel: 78,
          signalStrength: -55,
          lastSeen: '2025-09-21 14:28:00',
          capabilities: ['温度控制', '湿度控制', '定时调节', '远程监控'],
          sensors: [
            { name: '温度传感器', status: 'active', value: '18.5°C' },
            { name: '湿度传感器', status: 'active', value: '35%' },
            { name: '压力传感器', status: 'active', value: '1013 hPa' }
          ],
          alerts: []
        }
      ];
      setDevices(mockDevices);
    } catch (error) {
      showError('加载设备列表失败');
    }
  };

  const loadDeviceTypes = () => {
    // 模拟设备类型数据
    const mockTypes = [
      { id: 1, name: '智能门锁', type: 'smart_lock', icon: '🔐', count: 1 },
      { id: 2, name: '环境监测器', type: 'environmental_monitor', icon: '🌡️', count: 1 },
      { id: 3, name: '安全摄像头', type: 'security_camera', icon: '📹', count: 1 },
      { id: 4, name: '智能照明', type: 'smart_lighting', icon: '💡', count: 1 },
      { id: 5, name: '温控器', type: 'thermostat', icon: '🌡️', count: 1 }
    ];
    setDeviceTypes(mockTypes);
  };

  const loadDeviceMetrics = () => {
    // 模拟设备指标数据
    const mockMetrics = {
      totalDevices: 5,
      onlineDevices: 4,
      offlineDevices: 1,
      avgBatteryLevel: 79,
      avgSignalStrength: -44,
      totalAlerts: 2,
      dataTransmission: '2.5 MB/s',
      networkLatency: '12ms'
    };
    setDeviceMetrics(mockMetrics);
  };

  const handleConnectDevice = async (device) => {
    setIsConnecting(true);
    showInfo(`正在连接设备 ${device.name}...`);
    
    try {
      // 模拟设备连接
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      const updatedDevices = devices.map(d => 
        d.id === device.id 
          ? { ...d, status: 'online', lastSeen: new Date().toLocaleString() }
          : d
      );
      setDevices(updatedDevices);
      
      showSuccess(`设备 ${device.name} 连接成功`);
    } catch (error) {
      showError(`设备 ${device.name} 连接失败`);
    } finally {
      setIsConnecting(false);
    }
  };

  const handleDisconnectDevice = async (device) => {
    showInfo(`正在断开设备 ${device.name}...`);
    
    try {
      // 模拟设备断开
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      const updatedDevices = devices.map(d => 
        d.id === device.id 
          ? { ...d, status: 'offline' }
          : d
      );
      setDevices(updatedDevices);
      
      showSuccess(`设备 ${device.name} 已断开`);
    } catch (error) {
      showError(`设备 ${device.name} 断开失败`);
    }
  };

  const handleUpdateFirmware = async (device) => {
    showInfo(`正在更新设备 ${device.name} 固件...`);
    
    try {
      // 模拟固件更新
      await new Promise(resolve => setTimeout(resolve, 5000));
      
      const updatedDevices = devices.map(d => 
        d.id === device.id 
          ? { ...d, firmware: 'v' + (Math.random() * 2 + 1).toFixed(1) + '.0' }
          : d
      );
      setDevices(updatedDevices);
      
      showSuccess(`设备 ${device.name} 固件更新成功`);
    } catch (error) {
      showError(`设备 ${device.name} 固件更新失败`);
    }
  };

  const handleViewDeviceData = (device) => {
    setSelectedDevice(device);
    setDeviceData(device);
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'online': return '#28a745';
      case 'offline': return '#dc3545';
      case 'maintenance': return '#ffc107';
      default: return '#6c757d';
    }
  };

  const getStatusText = (status) => {
    switch (status) {
      case 'online': return '在线';
      case 'offline': return '离线';
      case 'maintenance': return '维护中';
      default: return '未知';
    }
  };

  const getAlertTypeColor = (type) => {
    switch (type) {
      case 'error': return '#dc3545';
      case 'warning': return '#ffc107';
      case 'info': return '#17a2b8';
      default: return '#6c757d';
    }
  };

  const getSignalStrengthText = (strength) => {
    if (strength === 0) return '无信号';
    if (strength > -30) return '优秀';
    if (strength > -50) return '良好';
    if (strength > -70) return '一般';
    return '较差';
  };

  const getBatteryLevelColor = (level) => {
    if (level > 80) return '#28a745';
    if (level > 50) return '#ffc107';
    if (level > 20) return '#fd7e14';
    return '#dc3545';
  };

  return (
    <div className="iot-device-support">
      <div className="iot-header">
        <h1>物联网设备支持</h1>
        <p>管理和监控物联网设备，实现智能化运维</p>
        
        <div className="iot-stats">
          <div className="stat-card">
            <div className="stat-icon">📱</div>
            <div className="stat-content">
              <h3>{deviceMetrics.totalDevices}</h3>
              <p>总设备数</p>
            </div>
          </div>
          <div className="stat-card">
            <div className="stat-icon">✅</div>
            <div className="stat-content">
              <h3>{deviceMetrics.onlineDevices}</h3>
              <p>在线设备</p>
            </div>
          </div>
          <div className="stat-card">
            <div className="stat-icon">🔋</div>
            <div className="stat-content">
              <h3>{deviceMetrics.avgBatteryLevel}%</h3>
              <p>平均电量</p>
            </div>
          </div>
          <div className="stat-card">
            <div className="stat-icon">📶</div>
            <div className="stat-content">
              <h3>{deviceMetrics.avgSignalStrength} dBm</h3>
              <p>平均信号强度</p>
            </div>
          </div>
          <div className="stat-card">
            <div className="stat-icon">⚠️</div>
            <div className="stat-content">
              <h3>{deviceMetrics.totalAlerts}</h3>
              <p>活跃告警</p>
            </div>
          </div>
          <div className="stat-card">
            <div className="stat-icon">📊</div>
            <div className="stat-content">
              <h3>{deviceMetrics.dataTransmission}</h3>
              <p>数据传输速率</p>
            </div>
          </div>
        </div>
      </div>

      <div className="iot-content">
        <div className="devices-section">
          <h2>设备列表</h2>
          
          <div className="device-filters">
            <select>
              <option value="all">全部设备</option>
              <option value="online">在线设备</option>
              <option value="offline">离线设备</option>
            </select>
            <select>
              <option value="all">全部类型</option>
              {deviceTypes.map(type => (
                <option key={type.id} value={type.type}>{type.name}</option>
              ))}
            </select>
            <input type="text" placeholder="搜索设备..." />
          </div>

          <div className="devices-grid">
            {devices.map(device => (
              <div key={device.id} className="device-card">
                <div className="device-header">
                  <div className="device-info">
                    <h3>{device.name}</h3>
                    <p className="device-location">{device.location}</p>
                    <span 
                      className="status-badge"
                      style={{ color: getStatusColor(device.status) }}
                    >
                      {getStatusText(device.status)}
                    </span>
                  </div>
                  <div className="device-actions">
                    <button 
                      className="action-btn connect"
                      onClick={() => handleConnectDevice(device)}
                      disabled={isConnecting || device.status === 'online'}
                    >
                      {device.status === 'online' ? '已连接' : '连接'}
                    </button>
                    <button 
                      className="action-btn disconnect"
                      onClick={() => handleDisconnectDevice(device)}
                      disabled={device.status === 'offline'}
                    >
                      断开
                    </button>
                    <button 
                      className="action-btn update"
                      onClick={() => handleUpdateFirmware(device)}
                    >
                      更新固件
                    </button>
                    <button 
                      className="action-btn view"
                      onClick={() => handleViewDeviceData(device)}
                    >
                      查看数据
                    </button>
                  </div>
                </div>
                
                <div className="device-content">
                  <div className="device-details">
                    <div className="detail-item">
                      <span className="label">IP地址:</span>
                      <span className="value">{device.ipAddress}</span>
                    </div>
                    <div className="detail-item">
                      <span className="label">MAC地址:</span>
                      <span className="value">{device.macAddress}</span>
                    </div>
                    <div className="detail-item">
                      <span className="label">固件版本:</span>
                      <span className="value">{device.firmware}</span>
                    </div>
                    <div className="detail-item">
                      <span className="label">最后在线:</span>
                      <span className="value">{device.lastSeen}</span>
                    </div>
                  </div>
                  
                  <div className="device-metrics">
                    <div className="metric">
                      <span className="metric-label">电量:</span>
                      <div className="metric-bar">
                        <div 
                          className="metric-progress"
                          style={{ 
                            width: `${device.batteryLevel}%`,
                            backgroundColor: getBatteryLevelColor(device.batteryLevel)
                          }}
                        ></div>
                      </div>
                      <span className="metric-value">{device.batteryLevel}%</span>
                    </div>
                    
                    <div className="metric">
                      <span className="metric-label">信号强度:</span>
                      <div className="metric-bar">
                        <div 
                          className="metric-progress"
                          style={{ 
                            width: `${Math.abs(device.signalStrength) / 100 * 100}%`,
                            backgroundColor: device.signalStrength > -50 ? '#28a745' : '#ffc107'
                          }}
                        ></div>
                      </div>
                      <span className="metric-value">
                        {device.signalStrength} dBm ({getSignalStrengthText(device.signalStrength)})
                      </span>
                    </div>
                  </div>
                  
                  <div className="device-sensors">
                    <h4>传感器状态:</h4>
                    <div className="sensors-list">
                      {device.sensors.map((sensor, index) => (
                        <div key={index} className="sensor-item">
                          <span className="sensor-name">{sensor.name}</span>
                          <span className={`sensor-status ${sensor.status}`}>
                            {sensor.status === 'active' ? '正常' : '异常'}
                          </span>
                          <span className="sensor-value">{sensor.value}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                  
                  {device.alerts && device.alerts.length > 0 && (
                    <div className="device-alerts">
                      <h4>告警信息:</h4>
                      <div className="alerts-list">
                        {device.alerts.map((alert, index) => (
                          <div key={index} className={`alert-item ${alert.type}`}>
                            <span className="alert-icon">
                              {alert.type === 'error' ? '❌' : 
                               alert.type === 'warning' ? '⚠️' : 'ℹ️'}
                            </span>
                            <span className="alert-message">{alert.message}</span>
                            <span className="alert-time">{alert.timestamp}</span>
                          </div>
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

      {/* 设备数据查看器 */}
      {selectedDevice && (
        <div className="device-data-modal">
          <div className="modal-content">
            <div className="modal-header">
              <h2>{selectedDevice.name} - 实时数据</h2>
              <button 
                className="close-btn"
                onClick={() => setSelectedDevice(null)}
              >
                ✕
              </button>
            </div>
            
            <div className="modal-body">
              <div className="device-data-grid">
                <div className="data-section">
                  <h3>设备信息</h3>
                  <div className="data-list">
                    <div className="data-item">
                      <span className="label">设备类型:</span>
                      <span className="value">{selectedDevice.type}</span>
                    </div>
                    <div className="data-item">
                      <span className="label">位置:</span>
                      <span className="value">{selectedDevice.location}</span>
                    </div>
                    <div className="data-item">
                      <span className="label">固件版本:</span>
                      <span className="value">{selectedDevice.firmware}</span>
                    </div>
                  </div>
                </div>
                
                <div className="data-section">
                  <h3>传感器数据</h3>
                  <div className="sensors-grid">
                    {selectedDevice.sensors.map((sensor, index) => (
                      <div key={index} className="sensor-card">
                        <h4>{sensor.name}</h4>
                        <div className="sensor-value-large">{sensor.value}</div>
                        <div className={`sensor-status ${sensor.status}`}>
                          {sensor.status === 'active' ? '正常' : '异常'}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
                
                <div className="data-section">
                  <h3>设备能力</h3>
                  <div className="capabilities-list">
                    {selectedDevice.capabilities.map((capability, index) => (
                      <span key={index} className="capability-tag">
                        {capability}
                      </span>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default IoTDeviceSupport;

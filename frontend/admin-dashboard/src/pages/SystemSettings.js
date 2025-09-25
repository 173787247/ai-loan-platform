import React, { useState } from 'react';
import './SystemSettings.css';

function SystemSettings() {
  const [settings, setSettings] = useState({
    system: {
      platformName: 'AI助贷招标平台',
      version: '1.1.0',
      maintenanceMode: false,
      debugMode: false,
      logLevel: 'info'
    },
    ai: {
      modelVersion: 'v2.7.0',
      riskThreshold: 70,
      autoApproval: false,
      gpuEnabled: true,
      maxConcurrentRequests: 100
    },
    security: {
      sessionTimeout: 30,
      maxLoginAttempts: 5,
      passwordMinLength: 8,
      twoFactorAuth: false,
      ipWhitelist: []
    },
    notification: {
      emailEnabled: true,
      smsEnabled: false,
      webhookEnabled: true,
      alertThreshold: 80
    }
  });

  const [activeTab, setActiveTab] = useState('system');

  const handleSettingChange = (category, key, value) => {
    setSettings(prev => ({
      ...prev,
      [category]: {
        ...prev[category],
        [key]: value
      }
    }));
  };

  const handleSave = () => {
    // 模拟保存设置
    console.log('保存设置:', settings);
    alert('设置已保存！');
  };

  const handleReset = () => {
    if (window.confirm('确定要重置所有设置为默认值吗？')) {
      // 重置为默认值
      alert('设置已重置！');
    }
  };

  const tabs = [
    { id: 'system', label: '系统设置', icon: '⚙️' },
    { id: 'ai', label: 'AI配置', icon: '🤖' },
    { id: 'security', label: '安全设置', icon: '🔒' },
    { id: 'notification', label: '通知设置', icon: '📧' }
  ];

  return (
    <div className="system-settings">
      <div className="page-header">
        <h1>系统设置</h1>
        <p>配置系统参数和功能选项</p>
      </div>

      <div className="settings-container">
        {/* 设置标签页 */}
        <div className="settings-tabs">
          {tabs.map(tab => (
            <button
              key={tab.id}
              className={`tab-button ${activeTab === tab.id ? 'active' : ''}`}
              onClick={() => setActiveTab(tab.id)}
            >
              <span className="tab-icon">{tab.icon}</span>
              <span className="tab-label">{tab.label}</span>
            </button>
          ))}
        </div>

        {/* 设置内容 */}
        <div className="settings-content">
          {activeTab === 'system' && (
            <div className="settings-section">
              <h2>系统配置</h2>
              <div className="settings-grid">
                <div className="setting-item">
                  <label>平台名称</label>
                  <input
                    type="text"
                    value={settings.system.platformName}
                    onChange={(e) => handleSettingChange('system', 'platformName', e.target.value)}
                  />
                </div>

                <div className="setting-item">
                  <label>系统版本</label>
                  <input
                    type="text"
                    value={settings.system.version}
                    disabled
                  />
                </div>

                <div className="setting-item">
                  <label>维护模式</label>
                  <label className="switch">
                    <input
                      type="checkbox"
                      checked={settings.system.maintenanceMode}
                      onChange={(e) => handleSettingChange('system', 'maintenanceMode', e.target.checked)}
                    />
                    <span className="slider"></span>
                  </label>
                </div>

                <div className="setting-item">
                  <label>调试模式</label>
                  <label className="switch">
                    <input
                      type="checkbox"
                      checked={settings.system.debugMode}
                      onChange={(e) => handleSettingChange('system', 'debugMode', e.target.checked)}
                    />
                    <span className="slider"></span>
                  </label>
                </div>

                <div className="setting-item">
                  <label>日志级别</label>
                  <select
                    value={settings.system.logLevel}
                    onChange={(e) => handleSettingChange('system', 'logLevel', e.target.value)}
                  >
                    <option value="debug">Debug</option>
                    <option value="info">Info</option>
                    <option value="warn">Warning</option>
                    <option value="error">Error</option>
                  </select>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'ai' && (
            <div className="settings-section">
              <h2>AI配置</h2>
              <div className="settings-grid">
                <div className="setting-item">
                  <label>模型版本</label>
                  <input
                    type="text"
                    value={settings.ai.modelVersion}
                    disabled
                  />
                </div>

                <div className="setting-item">
                  <label>风险阈值</label>
                  <input
                    type="number"
                    min="0"
                    max="100"
                    value={settings.ai.riskThreshold}
                    onChange={(e) => handleSettingChange('ai', 'riskThreshold', parseInt(e.target.value))}
                  />
                  <span className="setting-hint">超过此分数将被标记为高风险</span>
                </div>

                <div className="setting-item">
                  <label>自动审批</label>
                  <label className="switch">
                    <input
                      type="checkbox"
                      checked={settings.ai.autoApproval}
                      onChange={(e) => handleSettingChange('ai', 'autoApproval', e.target.checked)}
                    />
                    <span className="slider"></span>
                  </label>
                </div>

                <div className="setting-item">
                  <label>GPU加速</label>
                  <label className="switch">
                    <input
                      type="checkbox"
                      checked={settings.ai.gpuEnabled}
                      onChange={(e) => handleSettingChange('ai', 'gpuEnabled', e.target.checked)}
                    />
                    <span className="slider"></span>
                  </label>
                </div>

                <div className="setting-item">
                  <label>最大并发请求</label>
                  <input
                    type="number"
                    min="1"
                    max="1000"
                    value={settings.ai.maxConcurrentRequests}
                    onChange={(e) => handleSettingChange('ai', 'maxConcurrentRequests', parseInt(e.target.value))}
                  />
                </div>
              </div>
            </div>
          )}

          {activeTab === 'security' && (
            <div className="settings-section">
              <h2>安全设置</h2>
              <div className="settings-grid">
                <div className="setting-item">
                  <label>会话超时时间（分钟）</label>
                  <input
                    type="number"
                    min="5"
                    max="480"
                    value={settings.security.sessionTimeout}
                    onChange={(e) => handleSettingChange('security', 'sessionTimeout', parseInt(e.target.value))}
                  />
                </div>

                <div className="setting-item">
                  <label>最大登录尝试次数</label>
                  <input
                    type="number"
                    min="3"
                    max="10"
                    value={settings.security.maxLoginAttempts}
                    onChange={(e) => handleSettingChange('security', 'maxLoginAttempts', parseInt(e.target.value))}
                  />
                </div>

                <div className="setting-item">
                  <label>密码最小长度</label>
                  <input
                    type="number"
                    min="6"
                    max="20"
                    value={settings.security.passwordMinLength}
                    onChange={(e) => handleSettingChange('security', 'passwordMinLength', parseInt(e.target.value))}
                  />
                </div>

                <div className="setting-item">
                  <label>双因素认证</label>
                  <label className="switch">
                    <input
                      type="checkbox"
                      checked={settings.security.twoFactorAuth}
                      onChange={(e) => handleSettingChange('security', 'twoFactorAuth', e.target.checked)}
                    />
                    <span className="slider"></span>
                  </label>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'notification' && (
            <div className="settings-section">
              <h2>通知设置</h2>
              <div className="settings-grid">
                <div className="setting-item">
                  <label>邮件通知</label>
                  <label className="switch">
                    <input
                      type="checkbox"
                      checked={settings.notification.emailEnabled}
                      onChange={(e) => handleSettingChange('notification', 'emailEnabled', e.target.checked)}
                    />
                    <span className="slider"></span>
                  </label>
                </div>

                <div className="setting-item">
                  <label>短信通知</label>
                  <label className="switch">
                    <input
                      type="checkbox"
                      checked={settings.notification.smsEnabled}
                      onChange={(e) => handleSettingChange('notification', 'smsEnabled', e.target.checked)}
                    />
                    <span className="slider"></span>
                  </label>
                </div>

                <div className="setting-item">
                  <label>Webhook通知</label>
                  <label className="switch">
                    <input
                      type="checkbox"
                      checked={settings.notification.webhookEnabled}
                      onChange={(e) => handleSettingChange('notification', 'webhookEnabled', e.target.checked)}
                    />
                    <span className="slider"></span>
                  </label>
                </div>

                <div className="setting-item">
                  <label>警报阈值</label>
                  <input
                    type="number"
                    min="0"
                    max="100"
                    value={settings.notification.alertThreshold}
                    onChange={(e) => handleSettingChange('notification', 'alertThreshold', parseInt(e.target.value))}
                  />
                  <span className="setting-hint">超过此分数将发送警报</span>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* 操作按钮 */}
      <div className="settings-actions">
        <button className="btn btn-primary" onClick={handleSave}>
          保存设置
        </button>
        <button className="btn btn-warning" onClick={handleReset}>
          重置为默认
        </button>
      </div>
    </div>
  );
}

export default SystemSettings;

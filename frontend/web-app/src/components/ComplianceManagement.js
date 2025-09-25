import React, { useState, useEffect } from 'react';
import { useNotification } from './NotificationSystem';
import './ComplianceManagement.css';

const ComplianceManagement = () => {
  const [complianceData, setComplianceData] = useState({});
  const [complianceRules, setComplianceRules] = useState([]);
  const [complianceReports, setComplianceReports] = useState([]);
  const [complianceAlerts, setComplianceAlerts] = useState([]);
  const [isGeneratingReport, setIsGeneratingReport] = useState(false);
  const { showSuccess, showError, showInfo } = useNotification();

  useEffect(() => {
    loadComplianceData();
    loadComplianceRules();
    loadComplianceReports();
    loadComplianceAlerts();
  }, []);

  const loadComplianceData = async () => {
    try {
      // 模拟合规数据
      const mockData = {
        overallCompliance: 92.5,
        complianceTrend: 'improving',
        totalRules: 45,
        activeRules: 42,
        violatedRules: 3,
        complianceScore: 92.5,
        lastAudit: '2025-09-20 14:30:00',
        nextAudit: '2025-10-20 14:30:00',
        complianceAreas: [
          { area: '反洗钱', score: 95, status: 'compliant', violations: 0 },
          { area: '数据保护', score: 90, status: 'compliant', violations: 1 },
          { area: '客户身份识别', score: 88, status: 'warning', violations: 2 },
          { area: '风险披露', score: 96, status: 'compliant', violations: 0 },
          { area: '利率合规', score: 94, status: 'compliant', violations: 0 },
          { area: '信息披露', score: 89, status: 'warning', violations: 1 }
        ],
        monthlyCompliance: Array.from({ length: 12 }, (_, i) => ({
          month: `2025-${String(i + 1).padStart(2, '0')}`,
          score: Math.floor(Math.random() * 10) + 85,
          violations: Math.floor(Math.random() * 5),
          audits: Math.floor(Math.random() * 3) + 1
        }))
      };
      setComplianceData(mockData);
    } catch (error) {
      showError('加载合规数据失败');
    }
  };

  const loadComplianceRules = async () => {
    try {
      // 模拟合规规则数据
      const mockRules = [
        {
          id: 1,
          name: '反洗钱规则',
          category: '反洗钱',
          description: '客户身份识别和可疑交易报告规则',
          status: 'active',
          priority: 'high',
          requirements: [
            '客户身份验证',
            '可疑交易监控',
            '大额交易报告',
            '客户尽职调查'
          ],
          lastUpdated: '2025-09-20 10:00:00',
          complianceRate: 95.2,
          violations: 0
        },
        {
          id: 2,
          name: '数据保护规则',
          category: '数据保护',
          description: '个人信息保护和数据安全规则',
          status: 'active',
          priority: 'high',
          requirements: [
            '数据加密存储',
            '访问权限控制',
            '数据备份',
            '隐私政策更新'
          ],
          lastUpdated: '2025-09-19 15:30:00',
          complianceRate: 90.0,
          violations: 1
        },
        {
          id: 3,
          name: '客户身份识别规则',
          category: '客户身份识别',
          description: 'KYC和客户身份验证规则',
          status: 'active',
          priority: 'high',
          requirements: [
            '身份证明文件验证',
            '地址证明验证',
            '收入证明验证',
            '信用记录核查'
          ],
          lastUpdated: '2025-09-18 09:15:00',
          complianceRate: 88.5,
          violations: 2
        },
        {
          id: 4,
          name: '风险披露规则',
          category: '风险披露',
          description: '贷款风险披露和客户告知规则',
          status: 'active',
          priority: 'medium',
          requirements: [
            '风险提示书',
            '利率说明',
            '费用明细',
            '还款计划说明'
          ],
          lastUpdated: '2025-09-17 14:20:00',
          complianceRate: 96.0,
          violations: 0
        },
        {
          id: 5,
          name: '利率合规规则',
          category: '利率合规',
          description: '贷款利率和费用合规规则',
          status: 'active',
          priority: 'high',
          requirements: [
            '利率上限控制',
            '费用透明化',
            '提前还款政策',
            '逾期费用标准'
          ],
          lastUpdated: '2025-09-16 11:45:00',
          complianceRate: 94.0,
          violations: 0
        },
        {
          id: 6,
          name: '信息披露规则',
          category: '信息披露',
          description: '产品信息和服务条款披露规则',
          status: 'active',
          priority: 'medium',
          requirements: [
            '产品说明书',
            '服务协议',
            '收费标准',
            '联系方式'
          ],
          lastUpdated: '2025-09-15 16:30:00',
          complianceRate: 89.0,
          violations: 1
        }
      ];
      setComplianceRules(mockRules);
    } catch (error) {
      showError('加载合规规则失败');
    }
  };

  const loadComplianceReports = async () => {
    try {
      // 模拟合规报告数据
      const mockReports = [
        {
          id: 1,
          name: '月度合规报告',
          type: 'monthly',
          period: '2025-09',
          status: 'completed',
          generatedAt: '2025-09-21 10:00:00',
          complianceScore: 92.5,
          violations: 3,
          recommendations: 5,
          fileSize: '2.3MB',
          downloadUrl: '/reports/compliance-2025-09.pdf'
        },
        {
          id: 2,
          name: '季度合规报告',
          type: 'quarterly',
          period: '2025-Q3',
          status: 'completed',
          generatedAt: '2025-09-20 15:30:00',
          complianceScore: 91.8,
          violations: 8,
          recommendations: 12,
          fileSize: '5.7MB',
          downloadUrl: '/reports/compliance-2025-Q3.pdf'
        },
        {
          id: 3,
          name: '年度合规报告',
          type: 'annual',
          period: '2025',
          status: 'in_progress',
          generatedAt: null,
          complianceScore: 0,
          violations: 0,
          recommendations: 0,
          fileSize: '0MB',
          downloadUrl: null
        },
        {
          id: 4,
          name: '专项合规报告',
          type: 'special',
          period: '反洗钱专项',
          status: 'completed',
          generatedAt: '2025-09-19 14:20:00',
          complianceScore: 95.0,
          violations: 0,
          recommendations: 2,
          fileSize: '1.8MB',
          downloadUrl: '/reports/aml-special-2025-09.pdf'
        }
      ];
      setComplianceReports(mockReports);
    } catch (error) {
      showError('加载合规报告失败');
    }
  };

  const loadComplianceAlerts = async () => {
    try {
      // 模拟合规告警数据
      const mockAlerts = [
        {
          id: 1,
          type: 'violation',
          title: '数据保护违规',
          description: '发现1个数据保护规则违规事件',
          severity: 'high',
          timestamp: '2025-09-21 14:30:00',
          status: 'active',
          affectedArea: '数据保护',
          ruleId: 2
        },
        {
          id: 2,
          type: 'deadline',
          title: '合规报告截止提醒',
          description: '月度合规报告将于3天后截止',
          severity: 'medium',
          timestamp: '2025-09-21 13:45:00',
          status: 'active',
          affectedArea: '报告管理',
          ruleId: null
        },
        {
          id: 3,
          type: 'audit',
          title: '合规审计提醒',
          description: '下月将进行年度合规审计',
          severity: 'medium',
          timestamp: '2025-09-21 12:00:00',
          status: 'active',
          affectedArea: '审计管理',
          ruleId: null
        },
        {
          id: 4,
          type: 'update',
          title: '合规规则更新',
          description: '反洗钱规则已更新，请及时学习',
          severity: 'low',
          timestamp: '2025-09-21 11:15:00',
          status: 'resolved',
          affectedArea: '反洗钱',
          ruleId: 1
        }
      ];
      setComplianceAlerts(mockAlerts);
    } catch (error) {
      showError('加载合规告警失败');
    }
  };

  const handleGenerateReport = async (reportType) => {
    setIsGeneratingReport(true);
    showInfo('正在生成合规报告...');
    
    try {
      // 模拟报告生成
      await new Promise(resolve => setTimeout(resolve, 3000));
      
      // 添加新报告
      const newReport = {
        id: Date.now(),
        name: `${reportType}合规报告`,
        type: reportType,
        period: new Date().toISOString().slice(0, 7),
        status: 'completed',
        generatedAt: new Date().toLocaleString(),
        complianceScore: Math.floor(Math.random() * 10) + 85,
        violations: Math.floor(Math.random() * 5),
        recommendations: Math.floor(Math.random() * 8) + 3,
        fileSize: `${(Math.random() * 5 + 1).toFixed(1)}MB`,
        downloadUrl: `/reports/compliance-${Date.now()}.pdf`
      };
      
      setComplianceReports(prev => [newReport, ...prev]);
      showSuccess('合规报告生成成功');
    } catch (error) {
      showError('合规报告生成失败');
    } finally {
      setIsGeneratingReport(false);
    }
  };

  const handleUpdateRule = async (ruleId, updates) => {
    showInfo('正在更新合规规则...');
    
    try {
      // 模拟规则更新
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      const updatedRules = complianceRules.map(rule => 
        rule.id === ruleId 
          ? { ...rule, ...updates, lastUpdated: new Date().toLocaleString() }
          : rule
      );
      setComplianceRules(updatedRules);
      
      showSuccess('合规规则更新成功');
    } catch (error) {
      showError('合规规则更新失败');
    }
  };

  const handleResolveAlert = async (alertId) => {
    showInfo('正在处理合规告警...');
    
    try {
      // 模拟告警处理
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      const updatedAlerts = complianceAlerts.map(alert => 
        alert.id === alertId 
          ? { ...alert, status: 'resolved' }
          : alert
      );
      setComplianceAlerts(updatedAlerts);
      
      showSuccess('合规告警已处理');
    } catch (error) {
      showError('合规告警处理失败');
    }
  };

  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'high': return '#dc3545';
      case 'medium': return '#ffc107';
      case 'low': return '#17a2b8';
      default: return '#6c757d';
    }
  };

  const getSeverityText = (severity) => {
    switch (severity) {
      case 'high': return '高';
      case 'medium': return '中';
      case 'low': return '低';
      default: return '未知';
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'active': return '#28a745';
      case 'inactive': return '#6c757d';
      case 'completed': return '#17a2b8';
      case 'in_progress': return '#ffc107';
      case 'resolved': return '#28a745';
      default: return '#6c757d';
    }
  };

  const getStatusText = (status) => {
    switch (status) {
      case 'active': return '活跃';
      case 'inactive': return '停用';
      case 'completed': return '已完成';
      case 'in_progress': return '进行中';
      case 'resolved': return '已解决';
      default: return '未知';
    }
  };

  const getComplianceStatus = (score) => {
    if (score >= 95) return { status: 'compliant', color: '#28a745', text: '合规' };
    if (score >= 85) return { status: 'warning', color: '#ffc107', text: '警告' };
    return { status: 'violation', color: '#dc3545', text: '违规' };
  };

  return (
    <div className="compliance-management">
      <div className="compliance-header">
        <h1>合规管理</h1>
        <p>确保平台运营符合监管要求，维护合规标准</p>
        
        <div className="compliance-stats">
          <div className="stat-card">
            <div className="stat-icon">📊</div>
            <div className="stat-content">
              <h3>{complianceData.overallCompliance}%</h3>
              <p>整体合规率</p>
            </div>
          </div>
          <div className="stat-card">
            <div className="stat-icon">📋</div>
            <div className="stat-content">
              <h3>{complianceData.totalRules}</h3>
              <p>合规规则总数</p>
            </div>
          </div>
          <div className="stat-card">
            <div className="stat-icon">✅</div>
            <div className="stat-content">
              <h3>{complianceData.activeRules}</h3>
              <p>活跃规则</p>
            </div>
          </div>
          <div className="stat-card">
            <div className="stat-icon">⚠️</div>
            <div className="stat-content">
              <h3>{complianceData.violatedRules}</h3>
              <p>违规规则</p>
            </div>
          </div>
          <div className="stat-card">
            <div className="stat-icon">📈</div>
            <div className="stat-content">
              <h3>{complianceData.complianceTrend}</h3>
              <p>合规趋势</p>
            </div>
          </div>
          <div className="stat-card">
            <div className="stat-icon">🔍</div>
            <div className="stat-content">
              <h3>{complianceData.nextAudit?.split(' ')[0]}</h3>
              <p>下次审计</p>
            </div>
          </div>
        </div>
      </div>

      <div className="compliance-content">
        <div className="content-grid">
          {/* 合规概览 */}
          <div className="compliance-overview-section">
            <h2>合规概览</h2>
            <div className="overview-cards">
              <div className="overview-card">
                <h3>合规领域</h3>
                <div className="compliance-areas">
                  {complianceData.complianceAreas?.map((area, index) => {
                    const complianceStatus = getComplianceStatus(area.score);
                    return (
                      <div key={index} className="area-item">
                        <div className="area-header">
                          <span className="area-name">{area.area}</span>
                          <span className="area-score">{area.score}%</span>
                        </div>
                        <div className="area-progress">
                          <div className="progress-bar">
                            <div 
                              className="progress-fill"
                              style={{ 
                                width: `${area.score}%`,
                                backgroundColor: complianceStatus.color
                              }}
                            ></div>
                          </div>
                          <div className="area-status">
                            <span className={`status ${complianceStatus.status}`}>
                              {complianceStatus.text}
                            </span>
                            <span className="violations">
                              违规: {area.violations}
                            </span>
                          </div>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            </div>
          </div>

          {/* 合规规则 */}
          <div className="compliance-rules-section">
            <h2>合规规则</h2>
            <div className="rules-list">
              {complianceRules.map(rule => (
                <div key={rule.id} className="rule-card">
                  <div className="rule-header">
                    <div className="rule-info">
                      <h3>{rule.name}</h3>
                      <p>{rule.description}</p>
                      <div className="rule-meta">
                        <span className="category">{rule.category}</span>
                        <span className={`priority ${rule.priority}`}>
                          优先级: {rule.priority}
                        </span>
                        <span className={`status ${rule.status}`}>
                          {getStatusText(rule.status)}
                        </span>
                        <span className="compliance-rate">
                          合规率: {rule.complianceRate}%
                        </span>
                        <span className="violations">
                          违规: {rule.violations}
                        </span>
                      </div>
                    </div>
                    <div className="rule-actions">
                      <button 
                        className="action-btn edit"
                        onClick={() => handleUpdateRule(rule.id, {})}
                      >
                        编辑
                      </button>
                      <button 
                        className="action-btn toggle"
                        onClick={() => handleUpdateRule(rule.id, { 
                          status: rule.status === 'active' ? 'inactive' : 'active' 
                        })}
                      >
                        {rule.status === 'active' ? '停用' : '启用'}
                      </button>
                    </div>
                  </div>
                  
                  <div className="rule-requirements">
                    <h4>合规要求:</h4>
                    <div className="requirements-list">
                      {rule.requirements.map((requirement, index) => (
                        <div key={index} className="requirement-item">
                          <span className="requirement-text">{requirement}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* 合规报告 */}
          <div className="compliance-reports-section">
            <h2>合规报告</h2>
            <div className="reports-list">
              {complianceReports.map(report => (
                <div key={report.id} className="report-card">
                  <div className="report-header">
                    <div className="report-info">
                      <h3>{report.name}</h3>
                      <p>期间: {report.period}</p>
                      <div className="report-meta">
                        <span className={`status ${report.status}`}>
                          {getStatusText(report.status)}
                        </span>
                        <span className="compliance-score">
                          合规分数: {report.complianceScore}%
                        </span>
                        <span className="violations">
                          违规: {report.violations}
                        </span>
                        <span className="recommendations">
                          建议: {report.recommendations}
                        </span>
                        <span className="file-size">
                          文件大小: {report.fileSize}
                        </span>
                      </div>
                    </div>
                    <div className="report-actions">
                      {report.status === 'completed' && (
                        <button className="action-btn download">
                          下载
                        </button>
                      )}
                      {report.status === 'in_progress' && (
                        <button 
                          className="action-btn generate"
                          onClick={() => handleGenerateReport(report.type)}
                          disabled={isGeneratingReport}
                        >
                          {isGeneratingReport ? '生成中...' : '生成报告'}
                        </button>
                      )}
                      <button className="action-btn view">查看</button>
                    </div>
                  </div>
                  
                  {report.generatedAt && (
                    <div className="report-time">
                      生成时间: {report.generatedAt}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>

          {/* 合规告警 */}
          <div className="compliance-alerts-section">
            <h2>合规告警</h2>
            <div className="alerts-list">
              {complianceAlerts.map(alert => (
                <div key={alert.id} className={`alert-card ${alert.severity}`}>
                  <div className="alert-header">
                    <div className="alert-info">
                      <h3>{alert.title}</h3>
                      <p>{alert.description}</p>
                      <div className="alert-meta">
                        <span className={`severity ${alert.severity}`}>
                          严重程度: {getSeverityText(alert.severity)}
                        </span>
                        <span className={`status ${alert.status}`}>
                          {getStatusText(alert.status)}
                        </span>
                        <span className="affected-area">
                          影响领域: {alert.affectedArea}
                        </span>
                      </div>
                    </div>
                    <div className="alert-actions">
                      {alert.status === 'active' && (
                        <button 
                          className="action-btn resolve"
                          onClick={() => handleResolveAlert(alert.id)}
                        >
                          解决
                        </button>
                      )}
                      <button className="action-btn investigate">调查</button>
                    </div>
                  </div>
                  <div className="alert-time">
                    {alert.timestamp}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
        
        <div className="compliance-actions">
          <button 
            className="action-btn generate"
            onClick={() => handleGenerateReport('月度')}
            disabled={isGeneratingReport}
          >
            {isGeneratingReport ? '生成中...' : '📊 生成合规报告'}
          </button>
          <button className="action-btn audit">🔍 启动合规审计</button>
          <button className="action-btn export">📤 导出合规数据</button>
        </div>
      </div>
    </div>
  );
};

export default ComplianceManagement;

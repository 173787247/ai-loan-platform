import React, { useState, useEffect } from 'react';
import { useNotification } from './NotificationSystem';
import Charts from './Charts';
import './AdvancedReporting.css';

const AdvancedReporting = () => {
  const [reports, setReports] = useState([]);
  const [selectedReport, setSelectedReport] = useState(null);
  const [isGenerating, setIsGenerating] = useState(false);
  const [reportData, setReportData] = useState({});
  const [filters, setFilters] = useState({
    dateRange: '30days',
    reportType: 'all',
    status: 'all',
    userType: 'all'
  });
  const [scheduledReports, setScheduledReports] = useState([]);
  const [isCreating, setIsCreating] = useState(false);
  const { showSuccess, showError, showInfo } = useNotification();

  useEffect(() => {
    loadReports();
    loadScheduledReports();
  }, []);

  const loadReports = async () => {
    try {
      // 模拟报表数据
      const mockReports = [
        {
          id: 1,
          name: '贷款业务月报',
          type: 'monthly',
          status: 'completed',
          createdAt: '2025-09-21 10:00:00',
          generatedAt: '2025-09-21 10:05:00',
          fileSize: '2.5MB',
          format: 'PDF',
          data: {
            totalLoans: 1250,
            totalAmount: 125000000,
            successRate: 85.2,
            avgProcessingTime: 2.3,
            riskDistribution: [
              { level: '低风险', count: 450, percentage: 36 },
              { level: '中风险', count: 600, percentage: 48 },
              { level: '高风险', count: 200, percentage: 16 }
            ],
            monthlyTrend: Array.from({ length: 12 }, (_, i) => ({
              month: `2025-${String(i + 1).padStart(2, '0')}`,
              loans: Math.floor(Math.random() * 200) + 100,
              amount: Math.floor(Math.random() * 20000000) + 10000000
            }))
          }
        },
        {
          id: 2,
          name: '风险评估报告',
          type: 'risk_analysis',
          status: 'completed',
          createdAt: '2025-09-21 09:30:00',
          generatedAt: '2025-09-21 09:35:00',
          fileSize: '1.8MB',
          format: 'Excel',
          data: {
            totalAssessments: 2500,
            avgRiskScore: 65.5,
            highRiskCount: 180,
            riskFactors: [
              { factor: '信用历史', weight: 0.3, score: 70 },
              { factor: '收入稳定性', weight: 0.25, score: 65 },
              { factor: '负债比例', weight: 0.2, score: 60 },
              { factor: '行业风险', weight: 0.15, score: 75 },
              { factor: '担保情况', weight: 0.1, score: 80 }
            ]
          }
        },
        {
          id: 3,
          name: '用户行为分析',
          type: 'user_behavior',
          status: 'generating',
          createdAt: '2025-09-21 11:00:00',
          generatedAt: null,
          fileSize: null,
          format: 'PDF',
          data: null
        },
        {
          id: 4,
          name: '系统性能报告',
          type: 'performance',
          status: 'completed',
          createdAt: '2025-09-20 23:00:00',
          generatedAt: '2025-09-20 23:05:00',
          fileSize: '3.2MB',
          format: 'PDF',
          data: {
            avgResponseTime: 850,
            uptime: 99.8,
            errorRate: 0.2,
            peakConcurrency: 1500,
            systemLoad: [
              { time: '00:00', cpu: 45, memory: 60, disk: 30 },
              { time: '06:00', cpu: 55, memory: 65, disk: 32 },
              { time: '12:00', cpu: 75, memory: 70, disk: 35 },
              { time: '18:00', cpu: 80, memory: 75, disk: 38 }
            ]
          }
        },
        {
          id: 5,
          name: '财务审计报告',
          type: 'financial_audit',
          status: 'completed',
          createdAt: '2025-09-19 14:00:00',
          generatedAt: '2025-09-19 14:10:00',
          fileSize: '5.1MB',
          format: 'PDF',
          data: {
            totalRevenue: 2500000,
            totalCosts: 1800000,
            netProfit: 700000,
            profitMargin: 28,
            revenueBreakdown: [
              { source: '利息收入', amount: 2000000, percentage: 80 },
              { source: '服务费', amount: 300000, percentage: 12 },
              { source: '其他收入', amount: 200000, percentage: 8 }
            ]
          }
        }
      ];
      setReports(mockReports);
    } catch (error) {
      showError('加载报表失败');
    }
  };

  const loadScheduledReports = () => {
    // 模拟定时报表数据
    const mockScheduled = [
      {
        id: 1,
        name: '每日业务概览',
        frequency: 'daily',
        time: '09:00',
        recipients: ['admin@company.com', 'manager@company.com'],
        status: 'active',
        lastRun: '2025-09-21 09:00:00',
        nextRun: '2025-09-22 09:00:00'
      },
      {
        id: 2,
        name: '周度风险报告',
        frequency: 'weekly',
        time: '18:00',
        day: 'friday',
        recipients: ['risk@company.com'],
        status: 'active',
        lastRun: '2025-09-19 18:00:00',
        nextRun: '2025-09-26 18:00:00'
      },
      {
        id: 3,
        name: '月度财务报告',
        frequency: 'monthly',
        time: '10:00',
        day: 1,
        recipients: ['finance@company.com', 'ceo@company.com'],
        status: 'active',
        lastRun: '2025-09-01 10:00:00',
        nextRun: '2025-10-01 10:00:00'
      }
    ];
    setScheduledReports(mockScheduled);
  };

  const handleGenerateReport = async (reportType) => {
    setIsGenerating(true);
    showInfo('正在生成报表...');
    
    try {
      // 模拟报表生成
      await new Promise(resolve => setTimeout(resolve, 3000));
      
      const newReport = {
        id: Date.now(),
        name: getReportName(reportType),
        type: reportType,
        status: 'completed',
        createdAt: new Date().toLocaleString(),
        generatedAt: new Date().toLocaleString(),
        fileSize: `${(Math.random() * 5 + 1).toFixed(1)}MB`,
        format: 'PDF',
        data: generateReportData(reportType)
      };
      
      setReports(prev => [newReport, ...prev]);
      showSuccess('报表生成成功');
    } catch (error) {
      showError('报表生成失败');
    } finally {
      setIsGenerating(false);
    }
  };

  const getReportName = (type) => {
    const names = {
      monthly: '贷款业务月报',
      risk_analysis: '风险评估报告',
      user_behavior: '用户行为分析',
      performance: '系统性能报告',
      financial_audit: '财务审计报告',
      custom: '自定义报表'
    };
    return names[type] || '未知报表';
  };

  const generateReportData = (type) => {
    // 根据报表类型生成模拟数据
    const baseData = {
      totalLoans: Math.floor(Math.random() * 2000) + 1000,
      totalAmount: Math.floor(Math.random() * 200000000) + 50000000,
      successRate: Math.random() * 20 + 80,
      avgProcessingTime: Math.random() * 3 + 1
    };
    
    return { ...baseData, type };
  };

  const handleViewReport = (report) => {
    setSelectedReport(report);
    setReportData(report.data);
  };

  const handleDownloadReport = (report) => {
    showInfo('正在下载报表...');
    // 模拟下载
    setTimeout(() => {
      showSuccess('报表下载完成');
    }, 1000);
  };

  const handleScheduleReport = () => {
    setIsCreating(true);
  };

  const handleCreateScheduledReport = (scheduleData) => {
    const newSchedule = {
      id: Date.now(),
      ...scheduleData,
      status: 'active',
      lastRun: null,
      nextRun: calculateNextRun(scheduleData)
    };
    
    setScheduledReports(prev => [...prev, newSchedule]);
    showSuccess('定时报表创建成功');
    setIsCreating(false);
  };

  const calculateNextRun = (scheduleData) => {
    const now = new Date();
    const nextRun = new Date(now);
    
    if (scheduleData.frequency === 'daily') {
      nextRun.setDate(now.getDate() + 1);
    } else if (scheduleData.frequency === 'weekly') {
      const daysUntilNext = (7 - now.getDay() + scheduleData.day) % 7;
      nextRun.setDate(now.getDate() + daysUntilNext);
    } else if (scheduleData.frequency === 'monthly') {
      nextRun.setMonth(now.getMonth() + 1);
    }
    
    return nextRun.toLocaleString();
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'completed': return '#28a745';
      case 'generating': return '#ffc107';
      case 'failed': return '#dc3545';
      case 'pending': return '#6c757d';
      default: return '#6c757d';
    }
  };

  const getStatusText = (status) => {
    switch (status) {
      case 'completed': return '已完成';
      case 'generating': return '生成中';
      case 'failed': return '失败';
      case 'pending': return '等待中';
      default: return '未知';
    }
  };

  const getFormatIcon = (format) => {
    switch (format) {
      case 'PDF': return '📄';
      case 'Excel': return '📊';
      case 'Word': return '📝';
      case 'CSV': return '📋';
      default: return '📄';
    }
  };

  return (
    <div className="advanced-reporting">
      <div className="reporting-header">
        <h1>高级报表系统</h1>
        <p>生成、管理和分发各类业务报表，提供数据洞察和决策支持</p>
        
        <div className="reporting-actions">
          <button 
            className="action-btn generate"
            onClick={() => handleGenerateReport('monthly')}
            disabled={isGenerating}
          >
            <span className="btn-icon">📊</span>
            {isGenerating ? '生成中...' : '生成月报'}
          </button>
          <button 
            className="action-btn generate"
            onClick={() => handleGenerateReport('risk_analysis')}
            disabled={isGenerating}
          >
            <span className="btn-icon">🛡️</span>
            风险评估
          </button>
          <button 
            className="action-btn generate"
            onClick={() => handleGenerateReport('performance')}
            disabled={isGenerating}
          >
            <span className="btn-icon">⚡</span>
            性能报告
          </button>
          <button 
            className="action-btn schedule"
            onClick={handleScheduleReport}
          >
            <span className="btn-icon">⏰</span>
            定时报表
          </button>
        </div>
      </div>

      <div className="reporting-content">
        <div className="reports-section">
          <h2>报表列表</h2>
          
          <div className="filters">
            <select 
              value={filters.dateRange}
              onChange={(e) => setFilters({...filters, dateRange: e.target.value})}
            >
              <option value="7days">近7天</option>
              <option value="30days">近30天</option>
              <option value="90days">近90天</option>
              <option value="all">全部</option>
            </select>
            
            <select 
              value={filters.reportType}
              onChange={(e) => setFilters({...filters, reportType: e.target.value})}
            >
              <option value="all">全部类型</option>
              <option value="monthly">月报</option>
              <option value="risk_analysis">风险评估</option>
              <option value="user_behavior">用户行为</option>
              <option value="performance">性能报告</option>
              <option value="financial_audit">财务审计</option>
            </select>
            
            <select 
              value={filters.status}
              onChange={(e) => setFilters({...filters, status: e.target.value})}
            >
              <option value="all">全部状态</option>
              <option value="completed">已完成</option>
              <option value="generating">生成中</option>
              <option value="failed">失败</option>
            </select>
          </div>

          <div className="reports-grid">
            {reports.map(report => (
              <div key={report.id} className="report-card">
                <div className="card-header">
                  <div className="report-info">
                    <h3>{report.name}</h3>
                    <p className="report-type">{report.type}</p>
                    <span 
                      className="status-badge"
                      style={{ color: getStatusColor(report.status) }}
                    >
                      {getStatusText(report.status)}
                    </span>
                  </div>
                  <div className="report-format">
                    <span className="format-icon">
                      {getFormatIcon(report.format)}
                    </span>
                    <span className="format-text">{report.format}</span>
                  </div>
                </div>
                
                <div className="card-content">
                  <div className="report-details">
                    <div className="detail-item">
                      <span className="label">创建时间:</span>
                      <span className="value">{report.createdAt}</span>
                    </div>
                    {report.generatedAt && (
                      <div className="detail-item">
                        <span className="label">生成时间:</span>
                        <span className="value">{report.generatedAt}</span>
                      </div>
                    )}
                    {report.fileSize && (
                      <div className="detail-item">
                        <span className="label">文件大小:</span>
                        <span className="value">{report.fileSize}</span>
                      </div>
                    )}
                  </div>
                  
                  {report.data && (
                    <div className="report-preview">
                      <h4>数据预览:</h4>
                      <div className="preview-stats">
                        {report.data.totalLoans && (
                          <div className="stat">
                            <span className="stat-label">总贷款数:</span>
                            <span className="stat-value">{report.data.totalLoans.toLocaleString()}</span>
                          </div>
                        )}
                        {report.data.totalAmount && (
                          <div className="stat">
                            <span className="stat-label">总金额:</span>
                            <span className="stat-value">¥{(report.data.totalAmount / 10000).toFixed(0)}万</span>
                          </div>
                        )}
                        {report.data.successRate && (
                          <div className="stat">
                            <span className="stat-label">成功率:</span>
                            <span className="stat-value">{report.data.successRate}%</span>
                          </div>
                        )}
                      </div>
                    </div>
                  )}
                </div>
                
                <div className="card-actions">
                  <button 
                    className="action-btn view"
                    onClick={() => handleViewReport(report)}
                  >
                    👁️ 查看
                  </button>
                  <button 
                    className="action-btn download"
                    onClick={() => handleDownloadReport(report)}
                    disabled={report.status !== 'completed'}
                  >
                    📥 下载
                  </button>
                  <button className="action-btn share">
                    🔗 分享
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="scheduled-section">
          <h2>定时报表</h2>
          <div className="scheduled-grid">
            {scheduledReports.map(schedule => (
              <div key={schedule.id} className="schedule-card">
                <div className="schedule-header">
                  <h3>{schedule.name}</h3>
                  <span className={`schedule-status ${schedule.status}`}>
                    {schedule.status === 'active' ? '运行中' : '已停用'}
                  </span>
                </div>
                
                <div className="schedule-content">
                  <div className="schedule-details">
                    <div className="detail">
                      <span className="label">频率:</span>
                      <span className="value">
                        {schedule.frequency === 'daily' ? '每日' :
                         schedule.frequency === 'weekly' ? '每周' :
                         schedule.frequency === 'monthly' ? '每月' : '未知'}
                      </span>
                    </div>
                    <div className="detail">
                      <span className="label">时间:</span>
                      <span className="value">{schedule.time}</span>
                    </div>
                    <div className="detail">
                      <span className="label">收件人:</span>
                      <span className="value">{schedule.recipients.length}人</span>
                    </div>
                    <div className="detail">
                      <span className="label">下次运行:</span>
                      <span className="value">{schedule.nextRun}</span>
                    </div>
                  </div>
                </div>
                
                <div className="schedule-actions">
                  <button className="action-btn edit">编辑</button>
                  <button className="action-btn toggle">
                    {schedule.status === 'active' ? '停用' : '启用'}
                  </button>
                  <button className="action-btn delete">删除</button>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* 报表查看器 */}
      {selectedReport && (
        <div className="report-viewer">
          <div className="viewer-header">
            <h2>{selectedReport.name}</h2>
            <button 
              className="close-btn"
              onClick={() => setSelectedReport(null)}
            >
              ✕
            </button>
          </div>
          
          <div className="viewer-content">
            {selectedReport.data && (
              <div className="report-data">
                <Charts.ReportVisualization data={selectedReport.data} />
              </div>
            )}
          </div>
        </div>
      )}

      {/* 创建定时报表对话框 */}
      {isCreating && (
        <div className="schedule-modal">
          <div className="modal-content">
            <div className="modal-header">
              <h2>创建定时报表</h2>
              <button 
                className="close-btn"
                onClick={() => setIsCreating(false)}
              >
                ✕
              </button>
            </div>
            
            <div className="modal-body">
              <div className="form-group">
                <label>报表名称</label>
                <input type="text" placeholder="输入报表名称" />
              </div>
              
              <div className="form-group">
                <label>报表类型</label>
                <select>
                  <option value="monthly">月报</option>
                  <option value="risk_analysis">风险评估</option>
                  <option value="performance">性能报告</option>
                  <option value="financial_audit">财务审计</option>
                </select>
              </div>
              
              <div className="form-row">
                <div className="form-group">
                  <label>频率</label>
                  <select>
                    <option value="daily">每日</option>
                    <option value="weekly">每周</option>
                    <option value="monthly">每月</option>
                  </select>
                </div>
                
                <div className="form-group">
                  <label>时间</label>
                  <input type="time" />
                </div>
              </div>
              
              <div className="form-group">
                <label>收件人邮箱</label>
                <textarea 
                  placeholder="输入邮箱地址，多个邮箱用逗号分隔"
                  rows="3"
                ></textarea>
              </div>
            </div>
            
            <div className="modal-footer">
              <button 
                className="btn-cancel"
                onClick={() => setIsCreating(false)}
              >
                取消
              </button>
              <button 
                className="btn-save"
                onClick={() => handleCreateScheduledReport({})}
              >
                创建
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default AdvancedReporting;

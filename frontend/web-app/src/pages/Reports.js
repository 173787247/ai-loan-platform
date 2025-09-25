import React, { useState, useEffect } from 'react';
import './Reports.css';

const Reports = () => {
  const [reports, setReports] = useState([]);
  const [templates, setTemplates] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [isGenerating, setIsGenerating] = useState(false);

  useEffect(() => {
    // 模拟报表数据
    const mockReports = [
      {
        id: 1,
        name: '月度贷款申请报告',
        category: 'loan',
        type: 'monthly',
        status: 'completed',
        createdDate: '2025-09-24',
        size: '2.3 MB',
        format: 'PDF',
        description: '包含本月所有贷款申请的详细分析'
      },
      {
        id: 2,
        name: '风险评估汇总报告',
        category: 'risk',
        type: 'weekly',
        status: 'completed',
        createdDate: '2025-09-23',
        size: '1.8 MB',
        format: 'Excel',
        description: '本周风险评估结果汇总'
      },
      {
        id: 3,
        name: '用户增长分析报告',
        category: 'user',
        type: 'quarterly',
        status: 'generating',
        createdDate: '2025-09-24',
        size: '-',
        format: 'PDF',
        description: '第三季度用户增长趋势分析'
      },
      {
        id: 4,
        name: '系统性能监控报告',
        category: 'system',
        type: 'daily',
        status: 'completed',
        createdDate: '2025-09-24',
        size: '856 KB',
        format: 'CSV',
        description: '系统运行状态和性能指标'
      },
      {
        id: 5,
        name: '合规性审计报告',
        category: 'compliance',
        type: 'monthly',
        status: 'pending',
        createdDate: '2025-09-24',
        size: '-',
        format: 'PDF',
        description: '月度合规性检查和审计结果'
      }
    ];

    const mockTemplates = [
      {
        id: 1,
        name: '标准贷款报告模板',
        category: 'loan',
        description: '包含贷款申请、审批、放款等全流程数据',
        fields: ['申请数量', '批准率', '平均金额', '处理时间'],
        isDefault: true
      },
      {
        id: 2,
        name: '风险评估模板',
        category: 'risk',
        description: '风险评分、分布分析、趋势预测',
        fields: ['风险等级', '评分分布', '趋势分析', '预警指标'],
        isDefault: false
      },
      {
        id: 3,
        name: '用户分析模板',
        category: 'user',
        description: '用户增长、活跃度、行为分析',
        fields: ['新增用户', '活跃用户', '留存率', '行为数据'],
        isDefault: false
      },
      {
        id: 4,
        name: '系统监控模板',
        category: 'system',
        description: '系统性能、错误日志、资源使用',
        fields: ['响应时间', '错误率', 'CPU使用率', '内存使用率'],
        isDefault: false
      }
    ];

    setReports(mockReports);
    setTemplates(mockTemplates);
  }, []);

  const getStatusIcon = (status) => {
    switch (status) {
      case 'completed': return '✅';
      case 'generating': return '⏳';
      case 'pending': return '⏸️';
      case 'failed': return '❌';
      default: return '📄';
    }
  };

  const getStatusClass = (status) => {
    switch (status) {
      case 'completed': return 'status-completed';
      case 'generating': return 'status-generating';
      case 'pending': return 'status-pending';
      case 'failed': return 'status-failed';
      default: return 'status-default';
    }
  };

  const getCategoryName = (category) => {
    const categories = {
      'loan': '贷款报告',
      'risk': '风险评估',
      'user': '用户分析',
      'system': '系统监控',
      'compliance': '合规审计',
      'all': '全部'
    };
    return categories[category] || category;
  };

  const filteredReports = reports.filter(report => 
    selectedCategory === 'all' || report.category === selectedCategory
  );

  const generateReport = (templateId) => {
    setIsGenerating(true);
    // 模拟报表生成
    setTimeout(() => {
      const newReport = {
        id: Date.now(),
        name: `新生成的报表_${new Date().toLocaleDateString()}`,
        category: templates.find(t => t.id === templateId)?.category || 'system',
        type: 'custom',
        status: 'generating',
        createdDate: new Date().toISOString().split('T')[0],
        size: '-',
        format: 'PDF',
        description: '正在生成中...'
      };
      setReports(prev => [newReport, ...prev]);
      setIsGenerating(false);
    }, 2000);
  };

  const downloadReport = (reportId) => {
    // 模拟下载
    alert(`开始下载报表 ${reportId}`);
  };

  const deleteReport = (reportId) => {
    setReports(prev => prev.filter(report => report.id !== reportId));
  };

  return (
    <div className="reports-container">
      <div className="reports-header">
        <h1>📋 报表中心</h1>
        <p>生成、管理和下载各类业务报表</p>
      </div>

      <div className="reports-controls">
        <div className="category-filter">
          <label>报表分类：</label>
          <select 
            value={selectedCategory} 
            onChange={(e) => setSelectedCategory(e.target.value)}
            className="category-selector"
          >
            <option value="all">全部报表</option>
            <option value="loan">贷款报告</option>
            <option value="risk">风险评估</option>
            <option value="user">用户分析</option>
            <option value="system">系统监控</option>
            <option value="compliance">合规审计</option>
          </select>
        </div>
        <button 
          className="generate-btn"
          onClick={() => generateReport(1)}
          disabled={isGenerating}
        >
          {isGenerating ? '生成中...' : '📊 生成新报表'}
        </button>
      </div>

      <div className="reports-content">
        <div className="reports-section">
          <h2>📄 现有报表</h2>
          <div className="reports-list">
            {filteredReports.length === 0 ? (
              <div className="no-reports">
                <p>暂无报表</p>
              </div>
            ) : (
              filteredReports.map(report => (
                <div key={report.id} className="report-item">
                  <div className="report-icon">
                    {getStatusIcon(report.status)}
                  </div>
                  <div className="report-content">
                    <div className="report-header">
                      <h3>{report.name}</h3>
                      <span className={`report-status ${getStatusClass(report.status)}`}>
                        {getStatusIcon(report.status)} {report.status}
                      </span>
                    </div>
                    <p className="report-description">{report.description}</p>
                    <div className="report-meta">
                      <span className="report-category">{getCategoryName(report.category)}</span>
                      <span className="report-type">{report.type}</span>
                      <span className="report-format">{report.format}</span>
                      <span className="report-size">{report.size}</span>
                      <span className="report-date">{report.createdDate}</span>
                    </div>
                  </div>
                  <div className="report-actions">
                    {report.status === 'completed' && (
                      <button 
                        className="action-btn download-btn"
                        onClick={() => downloadReport(report.id)}
                      >
                        📥 下载
                      </button>
                    )}
                    <button 
                      className="action-btn delete-btn"
                      onClick={() => deleteReport(report.id)}
                    >
                      🗑️ 删除
                    </button>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>

        <div className="templates-section">
          <h2>📝 报表模板</h2>
          <div className="templates-grid">
            {templates.map(template => (
              <div key={template.id} className="template-card">
                <div className="template-header">
                  <h3>{template.name}</h3>
                  {template.isDefault && <span className="default-badge">默认</span>}
                </div>
                <p className="template-description">{template.description}</p>
                <div className="template-fields">
                  <h4>包含字段：</h4>
                  <ul>
                    {template.fields.map((field, index) => (
                      <li key={index}>{field}</li>
                    ))}
                  </ul>
                </div>
                <button 
                  className="template-btn"
                  onClick={() => generateReport(template.id)}
                  disabled={isGenerating}
                >
                  {isGenerating ? '生成中...' : '使用此模板'}
                </button>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Reports;

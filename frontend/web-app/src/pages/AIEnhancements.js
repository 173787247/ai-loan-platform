import React, { useState, useEffect } from 'react';
import './AIEnhancements.css';

const AIEnhancements = () => {
  const [aiFeatures, setAiFeatures] = useState([]);
  const [selectedFeature, setSelectedFeature] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);

  useEffect(() => {
    const mockFeatures = [
      {
        id: 1,
        name: '智能风险评估',
        description: '基于机器学习的风险评估模型，自动分析用户信用状况',
        icon: '🛡️',
        status: 'active',
        accuracy: 95.2,
        usage: 1250,
        category: 'risk'
      },
      {
        id: 2,
        name: '智能匹配算法',
        description: 'AI驱动的借贷双方智能匹配，提高匹配成功率',
        icon: '🎯',
        status: 'active',
        accuracy: 88.7,
        usage: 890,
        category: 'matching'
      },
      {
        id: 3,
        name: '自然语言处理',
        description: '智能客服和文档理解，提升用户体验',
        icon: '💬',
        status: 'active',
        accuracy: 92.1,
        usage: 2100,
        category: 'nlp'
      },
      {
        id: 4,
        name: '预测分析',
        description: '基于历史数据的趋势预测和风险预警',
        icon: '📈',
        status: 'active',
        accuracy: 87.3,
        usage: 650,
        category: 'prediction'
      },
      {
        id: 5,
        name: '文档智能处理',
        description: 'OCR识别和文档内容提取，自动化文档处理',
        icon: '📄',
        status: 'active',
        accuracy: 94.8,
        usage: 1800,
        category: 'document'
      },
      {
        id: 6,
        name: '欺诈检测',
        description: '实时欺诈检测和异常行为识别',
        icon: '🔍',
        status: 'active',
        accuracy: 96.5,
        usage: 3200,
        category: 'fraud'
      }
    ];
    setAiFeatures(mockFeatures);
  }, []);

  const getCategoryName = (category) => {
    const categories = {
      'risk': '风险评估',
      'matching': '智能匹配',
      'nlp': '自然语言处理',
      'prediction': '预测分析',
      'document': '文档处理',
      'fraud': '欺诈检测'
    };
    return categories[category] || category;
  };

  const getStatusClass = (status) => {
    return status === 'active' ? 'status-active' : 'status-inactive';
  };

  const runAIAnalysis = (featureId) => {
    setIsProcessing(true);
    setSelectedFeature(featureId);
    
    // 模拟AI分析过程
    setTimeout(() => {
      setIsProcessing(false);
      setSelectedFeature(null);
      alert(`AI分析完成！功能ID: ${featureId}`);
    }, 3000);
  };

  const FeatureCard = ({ feature }) => (
    <div className={`feature-card ${getStatusClass(feature.status)}`}>
      <div className="feature-header">
        <div className="feature-icon">{feature.icon}</div>
        <div className="feature-info">
          <h3>{feature.name}</h3>
          <span className="feature-category">{getCategoryName(feature.category)}</span>
        </div>
        <div className="feature-status">
          <span className={`status-indicator ${getStatusClass(feature.status)}`}>
            {feature.status === 'active' ? '✅' : '⏸️'}
          </span>
        </div>
      </div>
      
      <p className="feature-description">{feature.description}</p>
      
      <div className="feature-metrics">
        <div className="metric">
          <span className="metric-label">准确率</span>
          <span className="metric-value">{feature.accuracy}%</span>
        </div>
        <div className="metric">
          <span className="metric-label">使用次数</span>
          <span className="metric-value">{feature.usage.toLocaleString()}</span>
        </div>
      </div>
      
      <div className="feature-actions">
        <button 
          className="action-btn primary"
          onClick={() => runAIAnalysis(feature.id)}
          disabled={isProcessing && selectedFeature === feature.id}
        >
          {isProcessing && selectedFeature === feature.id ? '分析中...' : '🚀 运行分析'}
        </button>
        <button className="action-btn secondary">
          ⚙️ 配置
        </button>
      </div>
    </div>
  );

  return (
    <div className="ai-enhancements-container">
      <div className="ai-enhancements-header">
        <h1>🤖 AI增强功能</h1>
        <p>基于人工智能的智能分析和自动化工具</p>
        {isProcessing && (
          <div className="processing-indicator">
            <div className="spinner"></div>
            <span>AI正在处理中，请稍候...</span>
          </div>
        )}
      </div>

      <div className="ai-stats">
        <div className="stat-card">
          <div className="stat-icon">🧠</div>
          <div className="stat-content">
            <h3>AI模型数量</h3>
            <p className="stat-value">{aiFeatures.length}</p>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon">⚡</div>
          <div className="stat-content">
            <h3>总使用次数</h3>
            <p className="stat-value">{aiFeatures.reduce((sum, f) => sum + f.usage, 0).toLocaleString()}</p>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon">🎯</div>
          <div className="stat-content">
            <h3>平均准确率</h3>
            <p className="stat-value">{(aiFeatures.reduce((sum, f) => sum + f.accuracy, 0) / aiFeatures.length).toFixed(1)}%</p>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon">🔄</div>
          <div className="stat-content">
            <h3>活跃功能</h3>
            <p className="stat-value">{aiFeatures.filter(f => f.status === 'active').length}</p>
          </div>
        </div>
      </div>

      <div className="features-grid">
        {aiFeatures.map(feature => (
          <FeatureCard key={feature.id} feature={feature} />
        ))}
      </div>

      <div className="ai-tools">
        <h2>🛠️ AI工具集</h2>
        <div className="tools-grid">
          <div className="tool-card">
            <h3>📊 数据可视化</h3>
            <p>智能生成图表和报告</p>
            <button className="tool-btn">使用工具</button>
          </div>
          <div className="tool-card">
            <h3>🔍 智能搜索</h3>
            <p>语义搜索和智能推荐</p>
            <button className="tool-btn">使用工具</button>
          </div>
          <div className="tool-card">
            <h3>📝 自动报告</h3>
            <p>AI生成业务报告</p>
            <button className="tool-btn">使用工具</button>
          </div>
          <div className="tool-card">
            <h3>🎨 智能设计</h3>
            <p>自动生成界面和布局</p>
            <button className="tool-btn">使用工具</button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AIEnhancements;

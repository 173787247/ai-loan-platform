import React, { useState, useEffect } from 'react';
import { useNotification } from './NotificationSystem';
import './WorkflowAutomation.css';

const WorkflowAutomation = () => {
  const [workflows, setWorkflows] = useState([]);
  const [selectedWorkflow, setSelectedWorkflow] = useState(null);
  const [isCreating, setIsCreating] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const [workflowData, setWorkflowData] = useState({
    name: '',
    description: '',
    triggers: [],
    actions: [],
    conditions: [],
    status: 'draft'
  });
  const { showSuccess, showError, showInfo } = useNotification();

  useEffect(() => {
    loadWorkflows();
  }, []);

  const loadWorkflows = async () => {
    try {
      // 模拟工作流数据
      const mockWorkflows = [
        {
          id: 1,
          name: '贷款申请自动审批',
          description: '自动处理低风险贷款申请',
          status: 'active',
          triggers: ['loan_application_submitted'],
          actions: ['risk_assessment', 'auto_approval'],
          conditions: ['risk_score < 30', 'amount < 1000000'],
          lastRun: '2025-09-21 14:30:00',
          nextRun: '2025-09-21 15:00:00',
          successRate: 95.2,
          totalRuns: 1250
        },
        {
          id: 2,
          name: '高风险贷款人工审核',
          description: '高风险贷款自动转人工审核',
          status: 'active',
          triggers: ['risk_assessment_completed'],
          actions: ['assign_to_human', 'send_notification'],
          conditions: ['risk_score > 70'],
          lastRun: '2025-09-21 14:25:00',
          nextRun: '2025-09-21 15:00:00',
          successRate: 100.0,
          totalRuns: 89
        },
        {
          id: 3,
          name: '逾期贷款提醒',
          description: '自动发送逾期提醒通知',
          status: 'active',
          triggers: ['payment_due_date_reached'],
          actions: ['send_reminder', 'update_status'],
          conditions: ['payment_status = overdue'],
          lastRun: '2025-09-21 09:00:00',
          nextRun: '2025-09-22 09:00:00',
          successRate: 98.7,
          totalRuns: 456
        },
        {
          id: 4,
          name: '新用户欢迎流程',
          description: '新用户注册后的欢迎流程',
          status: 'draft',
          triggers: ['user_registered'],
          actions: ['send_welcome_email', 'create_profile'],
          conditions: ['user_type = borrower'],
          lastRun: null,
          nextRun: null,
          successRate: 0,
          totalRuns: 0
        }
      ];
      setWorkflows(mockWorkflows);
    } catch (error) {
      showError('加载工作流失败');
    }
  };

  const handleCreateWorkflow = () => {
    setIsCreating(true);
    setWorkflowData({
      name: '',
      description: '',
      triggers: [],
      actions: [],
      conditions: [],
      status: 'draft'
    });
  };

  const handleEditWorkflow = (workflow) => {
    setSelectedWorkflow(workflow);
    setWorkflowData(workflow);
    setIsEditing(true);
  };

  const handleSaveWorkflow = () => {
    if (!workflowData.name || !workflowData.description) {
      showError('请填写工作流名称和描述');
      return;
    }

    if (isCreating) {
      const newWorkflow = {
        ...workflowData,
        id: Date.now(),
        lastRun: null,
        nextRun: null,
        successRate: 0,
        totalRuns: 0
      };
      setWorkflows([...workflows, newWorkflow]);
      showSuccess('工作流创建成功');
    } else {
      const updatedWorkflows = workflows.map(w => 
        w.id === selectedWorkflow.id ? { ...workflowData, id: selectedWorkflow.id } : w
      );
      setWorkflows(updatedWorkflows);
      showSuccess('工作流更新成功');
    }

    setIsCreating(false);
    setIsEditing(false);
    setSelectedWorkflow(null);
  };

  const handleDeleteWorkflow = (workflowId) => {
    setWorkflows(workflows.filter(w => w.id !== workflowId));
    showSuccess('工作流删除成功');
  };

  const handleToggleWorkflow = (workflowId) => {
    const updatedWorkflows = workflows.map(w => 
      w.id === workflowId 
        ? { ...w, status: w.status === 'active' ? 'inactive' : 'active' }
        : w
    );
    setWorkflows(updatedWorkflows);
    showInfo(`工作流已${workflows.find(w => w.id === workflowId)?.status === 'active' ? '停用' : '启用'}`);
  };

  const handleRunWorkflow = (workflowId) => {
    showInfo('工作流执行中...');
    // 模拟工作流执行
    setTimeout(() => {
      showSuccess('工作流执行完成');
    }, 2000);
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'active': return '#28a745';
      case 'inactive': return '#6c757d';
      case 'draft': return '#ffc107';
      case 'error': return '#dc3545';
      default: return '#6c757d';
    }
  };

  const getStatusText = (status) => {
    switch (status) {
      case 'active': return '运行中';
      case 'inactive': return '已停用';
      case 'draft': return '草稿';
      case 'error': return '错误';
      default: return '未知';
    }
  };

  return (
    <div className="workflow-automation">
      <div className="workflow-header">
        <h1>工作流自动化</h1>
        <p>创建和管理自动化工作流，提升业务效率</p>
        
        <div className="workflow-actions">
          <button className="create-btn" onClick={handleCreateWorkflow}>
            <span className="btn-icon">➕</span>
            创建工作流
          </button>
          <button className="import-btn">
            <span className="btn-icon">📥</span>
            导入工作流
          </button>
          <button className="export-btn">
            <span className="btn-icon">📤</span>
            导出工作流
          </button>
        </div>
      </div>

      <div className="workflow-content">
        {/* 工作流列表 */}
        <div className="workflows-section">
          <h2>工作流列表</h2>
          <div className="workflows-grid">
            {workflows.map(workflow => (
              <div key={workflow.id} className="workflow-card">
                <div className="workflow-header">
                  <div className="workflow-title">
                    <h3>{workflow.name}</h3>
                    <span 
                      className="status-badge"
                      style={{ color: getStatusColor(workflow.status) }}
                    >
                      {getStatusText(workflow.status)}
                    </span>
                  </div>
                  <div className="workflow-actions">
                    <button 
                      className="action-btn run"
                      onClick={() => handleRunWorkflow(workflow.id)}
                    >
                      运行
                    </button>
                    <button 
                      className="action-btn edit"
                      onClick={() => handleEditWorkflow(workflow)}
                    >
                      编辑
                    </button>
                    <button 
                      className="action-btn toggle"
                      onClick={() => handleToggleWorkflow(workflow.id)}
                    >
                      {workflow.status === 'active' ? '停用' : '启用'}
                    </button>
                    <button 
                      className="action-btn delete"
                      onClick={() => handleDeleteWorkflow(workflow.id)}
                    >
                      删除
                    </button>
                  </div>
                </div>
                
                <div className="workflow-description">
                  <p>{workflow.description}</p>
                </div>
                
                <div className="workflow-details">
                  <div className="detail-item">
                    <span className="detail-label">触发器:</span>
                    <span className="detail-value">{workflow.triggers.join(', ')}</span>
                  </div>
                  <div className="detail-item">
                    <span className="detail-label">动作:</span>
                    <span className="detail-value">{workflow.actions.join(', ')}</span>
                  </div>
                  <div className="detail-item">
                    <span className="detail-label">条件:</span>
                    <span className="detail-value">{workflow.conditions.join(', ')}</span>
                  </div>
                </div>
                
                <div className="workflow-stats">
                  <div className="stat-item">
                    <span className="stat-label">成功率</span>
                    <span className="stat-value">{workflow.successRate}%</span>
                  </div>
                  <div className="stat-item">
                    <span className="stat-label">总运行次数</span>
                    <span className="stat-value">{workflow.totalRuns}</span>
                  </div>
                  <div className="stat-item">
                    <span className="stat-label">最后运行</span>
                    <span className="stat-value">
                      {workflow.lastRun || '未运行'}
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* 工作流编辑器 */}
        {(isCreating || isEditing) && (
          <div className="workflow-editor">
            <div className="editor-header">
              <h2>{isCreating ? '创建工作流' : '编辑工作流'}</h2>
              <div className="editor-actions">
                <button className="save-btn" onClick={handleSaveWorkflow}>
                  保存
                </button>
                <button 
                  className="cancel-btn"
                  onClick={() => {
                    setIsCreating(false);
                    setIsEditing(false);
                    setSelectedWorkflow(null);
                  }}
                >
                  取消
                </button>
              </div>
            </div>
            
            <div className="editor-content">
              <div className="form-group">
                <label>工作流名称</label>
                <input
                  type="text"
                  value={workflowData.name}
                  onChange={(e) => setWorkflowData({...workflowData, name: e.target.value})}
                  placeholder="输入工作流名称"
                />
              </div>
              
              <div className="form-group">
                <label>描述</label>
                <textarea
                  value={workflowData.description}
                  onChange={(e) => setWorkflowData({...workflowData, description: e.target.value})}
                  placeholder="输入工作流描述"
                  rows="3"
                />
              </div>
              
              <div className="form-group">
                <label>触发器</label>
                <div className="trigger-list">
                  {workflowData.triggers.map((trigger, index) => (
                    <div key={index} className="trigger-item">
                      <select
                        value={trigger}
                        onChange={(e) => {
                          const newTriggers = [...workflowData.triggers];
                          newTriggers[index] = e.target.value;
                          setWorkflowData({...workflowData, triggers: newTriggers});
                        }}
                      >
                        <option value="loan_application_submitted">贷款申请提交</option>
                        <option value="risk_assessment_completed">风险评估完成</option>
                        <option value="payment_due_date_reached">还款到期</option>
                        <option value="user_registered">用户注册</option>
                        <option value="document_uploaded">文档上传</option>
                      </select>
                      <button 
                        className="remove-btn"
                        onClick={() => {
                          const newTriggers = workflowData.triggers.filter((_, i) => i !== index);
                          setWorkflowData({...workflowData, triggers: newTriggers});
                        }}
                      >
                        ×
                      </button>
                    </div>
                  ))}
                  <button 
                    className="add-btn"
                    onClick={() => {
                      setWorkflowData({
                        ...workflowData, 
                        triggers: [...workflowData.triggers, 'loan_application_submitted']
                      });
                    }}
                  >
                    + 添加触发器
                  </button>
                </div>
              </div>
              
              <div className="form-group">
                <label>动作</label>
                <div className="action-list">
                  {workflowData.actions.map((action, index) => (
                    <div key={index} className="action-item">
                      <select
                        value={action}
                        onChange={(e) => {
                          const newActions = [...workflowData.actions];
                          newActions[index] = e.target.value;
                          setWorkflowData({...workflowData, actions: newActions});
                        }}
                      >
                        <option value="risk_assessment">风险评估</option>
                        <option value="auto_approval">自动审批</option>
                        <option value="assign_to_human">转人工审核</option>
                        <option value="send_notification">发送通知</option>
                        <option value="send_reminder">发送提醒</option>
                        <option value="update_status">更新状态</option>
                        <option value="send_welcome_email">发送欢迎邮件</option>
                        <option value="create_profile">创建档案</option>
                      </select>
                      <button 
                        className="remove-btn"
                        onClick={() => {
                          const newActions = workflowData.actions.filter((_, i) => i !== index);
                          setWorkflowData({...workflowData, actions: newActions});
                        }}
                      >
                        ×
                      </button>
                    </div>
                  ))}
                  <button 
                    className="add-btn"
                    onClick={() => {
                      setWorkflowData({
                        ...workflowData, 
                        actions: [...workflowData.actions, 'risk_assessment']
                      });
                    }}
                  >
                    + 添加动作
                  </button>
                </div>
              </div>
              
              <div className="form-group">
                <label>条件</label>
                <div className="condition-list">
                  {workflowData.conditions.map((condition, index) => (
                    <div key={index} className="condition-item">
                      <input
                        type="text"
                        value={condition}
                        onChange={(e) => {
                          const newConditions = [...workflowData.conditions];
                          newConditions[index] = e.target.value;
                          setWorkflowData({...workflowData, conditions: newConditions});
                        }}
                        placeholder="例如: risk_score < 30"
                      />
                      <button 
                        className="remove-btn"
                        onClick={() => {
                          const newConditions = workflowData.conditions.filter((_, i) => i !== index);
                          setWorkflowData({...workflowData, conditions: newConditions});
                        }}
                      >
                        ×
                      </button>
                    </div>
                  ))}
                  <button 
                    className="add-btn"
                    onClick={() => {
                      setWorkflowData({
                        ...workflowData, 
                        conditions: [...workflowData.conditions, '']
                      });
                    }}
                  >
                    + 添加条件
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default WorkflowAutomation;

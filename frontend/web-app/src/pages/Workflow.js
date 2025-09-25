import React, { useState } from 'react';
import './Workflow.css';

const Workflow = () => {
  const [workflows] = useState([
    { id: 1, name: '贷款申请流程', status: 'active', steps: 5, completed: 3 },
    { id: 2, name: '风险评估流程', status: 'active', steps: 4, completed: 2 },
    { id: 3, name: '审批流程', status: 'pending', steps: 3, completed: 0 },
    { id: 4, name: '放款流程', status: 'active', steps: 6, completed: 4 }
  ]);

  return (
    <div className="workflow-container">
      <div className="workflow-header">
        <h1>🔄 工作流管理</h1>
        <p>业务流程自动化和管理</p>
      </div>
      
      <div className="workflow-grid">
        {workflows.map(workflow => (
          <div key={workflow.id} className="workflow-card">
            <h3>{workflow.name}</h3>
            <div className="workflow-progress">
              <div className="progress-bar">
                <div 
                  className="progress-fill" 
                  style={{ width: `${(workflow.completed / workflow.steps) * 100}%` }}
                ></div>
              </div>
              <span>{workflow.completed}/{workflow.steps} 步骤</span>
            </div>
            <div className="workflow-status">
              状态: <span className={`status ${workflow.status}`}>{workflow.status}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Workflow;

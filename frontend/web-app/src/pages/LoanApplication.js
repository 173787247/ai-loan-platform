import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import './LoanApplication.css';

const LoanApplication = () => {
  const location = useLocation();
  const navigate = useNavigate();
  
  // 从URL参数获取用户档案ID
  const profileId = new URLSearchParams(location.search).get('profile_id') || 'default';
  
  // 表单状态
  const [formData, setFormData] = useState({
    // 基本信息
    name: '',
    phone: '',
    idCard: '',
    email: '',
    
    // 贷款需求
    purpose: '',
    amount: '',
    term: '',
    region: '',
    
    // 收入信息
    monthlyIncome: '',
    incomeSource: '',
    workYears: '',
    companyName: '',
    position: '',
    
    // 负债信息
    monthlyDebtPayment: '',
    existingLoans: [],
    
    // 信用信息
    creditScore: '',
    creditHistory: '',
    
    // 担保信息
    hasCollateral: false,
    hasGuarantor: false,
    collateralType: '',
    guarantorInfo: '',
    
    // 材料上传
    documents: []
  });
  
  // 表单验证状态
  const [errors, setErrors] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  
  // 从后端获取用户档案
  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const response = await fetch(`http://localhost:8000/api/v1/loan-agent/profile/${profileId}`);
        if (response.ok) {
          const result = await response.json();
          if (result.success && result.data.profile) {
            const profile = result.data.profile;
            setFormData(prev => ({
              ...prev,
              name: profile.name || '',
              phone: profile.phone || '',
              purpose: profile.purpose || '',
              amount: profile.amount || '',
              term: profile.term || '',
              region: profile.region || '',
              monthlyIncome: profile.monthly_income || '',
              incomeSource: profile.income_source || '',
              workYears: profile.work_years || '',
              monthlyDebtPayment: profile.monthly_debt_payment || '',
              creditScore: profile.credit_score || '',
              creditHistory: profile.credit_history || '',
              hasCollateral: profile.has_collateral || false,
              hasGuarantor: profile.has_guarantor || false
            }));
          }
        }
      } catch (error) {
        console.error('获取用户档案失败:', error);
      }
    };
    
    if (profileId !== 'default') {
      fetchProfile();
    }
  }, [profileId]);
  
  // 表单验证
  const validateForm = () => {
    const newErrors = {};
    
    // 基本信息验证
    if (!formData.name.trim()) newErrors.name = '请输入姓名';
    if (!formData.phone.trim()) newErrors.phone = '请输入电话号码';
    if (!formData.idCard.trim()) newErrors.idCard = '请输入身份证号';
    
    // 贷款需求验证
    if (!formData.purpose) newErrors.purpose = '请选择贷款用途';
    if (!formData.amount || formData.amount <= 0) newErrors.amount = '请输入有效的申请金额';
    if (!formData.term || formData.term <= 0) newErrors.term = '请输入有效的贷款期限';
    if (!formData.region.trim()) newErrors.region = '请输入申请地区';
    
    // 收入信息验证
    if (!formData.monthlyIncome || formData.monthlyIncome <= 0) newErrors.monthlyIncome = '请输入有效的月收入';
    if (!formData.incomeSource) newErrors.incomeSource = '请选择收入来源';
    if (!formData.workYears || formData.workYears <= 0) newErrors.workYears = '请输入有效的工作年限';
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };
  
  // 处理输入变化
  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
    
    // 清除对应字段的错误
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }));
    }
  };
  
  // 处理文件上传
  const handleFileUpload = (e) => {
    const files = Array.from(e.target.files);
    setFormData(prev => ({
      ...prev,
      documents: [...prev.documents, ...files]
    }));
  };
  
  // 移除文件
  const removeFile = (index) => {
    setFormData(prev => ({
      ...prev,
      documents: prev.documents.filter((_, i) => i !== index)
    }));
  };
  
  // 添加现有贷款
  const addExistingLoan = () => {
    setFormData(prev => ({
      ...prev,
      existingLoans: [...prev.existingLoans, { type: '', amount: '', bank: '' }]
    }));
  };
  
  // 移除现有贷款
  const removeExistingLoan = (index) => {
    setFormData(prev => ({
      ...prev,
      existingLoans: prev.existingLoans.filter((_, i) => i !== index)
    }));
  };
  
  // 更新现有贷款
  const updateExistingLoan = (index, field, value) => {
    setFormData(prev => ({
      ...prev,
      existingLoans: prev.existingLoans.map((loan, i) => 
        i === index ? { ...loan, [field]: value } : loan
      )
    }));
  };
  
  // 提交表单
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }
    
    setIsSubmitting(true);
    
    try {
      // 准备提交数据
      const submitData = {
        ...formData,
        profileId: profileId,
        submittedAt: new Date().toISOString()
      };
      
      // 这里应该调用后端API提交申请
      console.log('提交申请数据:', submitData);
      
      // 模拟提交成功
      setTimeout(() => {
        alert('申请提交成功！我们将在1-3个工作日内联系您。');
        navigate('/ai-chatbot-demo');
      }, 2000);
      
    } catch (error) {
      console.error('提交申请失败:', error);
      alert('提交失败，请稍后重试。');
    } finally {
      setIsSubmitting(false);
    }
  };
  
  return (
    <div className="loan-application">
      <div className="container">
        <h1>贷款申请表</h1>
        <p className="subtitle">请填写以下信息，我们将为您匹配合适的贷款产品</p>
        
        <form onSubmit={handleSubmit} className="application-form">
          {/* 基本信息 */}
          <section className="form-section">
            <h2>基本信息</h2>
            <div className="form-grid">
              <div className="form-group">
                <label>姓名 *</label>
                <input
                  type="text"
                  name="name"
                  value={formData.name}
                  onChange={handleInputChange}
                  className={errors.name ? 'error' : ''}
                  placeholder="请输入您的姓名"
                />
                {errors.name && <span className="error-message">{errors.name}</span>}
              </div>
              
              <div className="form-group">
                <label>联系电话 *</label>
                <input
                  type="tel"
                  name="phone"
                  value={formData.phone}
                  onChange={handleInputChange}
                  className={errors.phone ? 'error' : ''}
                  placeholder="请输入手机号码"
                />
                {errors.phone && <span className="error-message">{errors.phone}</span>}
              </div>
              
              <div className="form-group">
                <label>身份证号 *</label>
                <input
                  type="text"
                  name="idCard"
                  value={formData.idCard}
                  onChange={handleInputChange}
                  className={errors.idCard ? 'error' : ''}
                  placeholder="请输入身份证号码"
                />
                {errors.idCard && <span className="error-message">{errors.idCard}</span>}
              </div>
              
              <div className="form-group">
                <label>邮箱</label>
                <input
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={handleInputChange}
                  placeholder="请输入邮箱地址"
                />
              </div>
            </div>
          </section>
          
          {/* 贷款需求 */}
          <section className="form-section">
            <h2>贷款需求</h2>
            <div className="form-grid">
              <div className="form-group">
                <label>贷款用途 *</label>
                <select
                  name="purpose"
                  value={formData.purpose}
                  onChange={handleInputChange}
                  className={errors.purpose ? 'error' : ''}
                >
                  <option value="">请选择贷款用途</option>
                  <option value="消费">个人消费</option>
                  <option value="经营">企业经营</option>
                  <option value="教育">教育培训</option>
                  <option value="医疗">医疗费用</option>
                  <option value="旅游">旅游出行</option>
                  <option value="装修">房屋装修</option>
                  <option value="其他">其他用途</option>
                </select>
                {errors.purpose && <span className="error-message">{errors.purpose}</span>}
              </div>
              
              <div className="form-group">
                <label>申请金额 *</label>
                <div className="input-group">
                  <input
                    type="number"
                    name="amount"
                    value={formData.amount}
                    onChange={handleInputChange}
                    className={errors.amount ? 'error' : ''}
                    placeholder="请输入申请金额"
                    min="1"
                    step="0.1"
                  />
                  <span className="input-suffix">万元</span>
                </div>
                {errors.amount && <span className="error-message">{errors.amount}</span>}
              </div>
              
              <div className="form-group">
                <label>贷款期限 *</label>
                <div className="input-group">
                  <input
                    type="number"
                    name="term"
                    value={formData.term}
                    onChange={handleInputChange}
                    className={errors.term ? 'error' : ''}
                    placeholder="请输入贷款期限"
                    min="1"
                  />
                  <span className="input-suffix">个月</span>
                </div>
                {errors.term && <span className="error-message">{errors.term}</span>}
              </div>
              
              <div className="form-group">
                <label>申请地区 *</label>
                <input
                  type="text"
                  name="region"
                  value={formData.region}
                  onChange={handleInputChange}
                  className={errors.region ? 'error' : ''}
                  placeholder="请输入申请地区"
                />
                {errors.region && <span className="error-message">{errors.region}</span>}
              </div>
            </div>
          </section>
          
          {/* 收入信息 */}
          <section className="form-section">
            <h2>收入信息</h2>
            <div className="form-grid">
              <div className="form-group">
                <label>月收入 *</label>
                <div className="input-group">
                  <input
                    type="number"
                    name="monthlyIncome"
                    value={formData.monthlyIncome}
                    onChange={handleInputChange}
                    className={errors.monthlyIncome ? 'error' : ''}
                    placeholder="请输入月收入"
                    min="0"
                    step="100"
                  />
                  <span className="input-suffix">元</span>
                </div>
                {errors.monthlyIncome && <span className="error-message">{errors.monthlyIncome}</span>}
              </div>
              
              <div className="form-group">
                <label>收入来源 *</label>
                <select
                  name="incomeSource"
                  value={formData.incomeSource}
                  onChange={handleInputChange}
                  className={errors.incomeSource ? 'error' : ''}
                >
                  <option value="">请选择收入来源</option>
                  <option value="工资">工资收入</option>
                  <option value="经营">经营收入</option>
                  <option value="其他">其他收入</option>
                </select>
                {errors.incomeSource && <span className="error-message">{errors.incomeSource}</span>}
              </div>
              
              <div className="form-group">
                <label>工作年限 *</label>
                <div className="input-group">
                  <input
                    type="number"
                    name="workYears"
                    value={formData.workYears}
                    onChange={handleInputChange}
                    className={errors.workYears ? 'error' : ''}
                    placeholder="请输入工作年限"
                    min="0"
                    step="0.5"
                  />
                  <span className="input-suffix">年</span>
                </div>
                {errors.workYears && <span className="error-message">{errors.workYears}</span>}
              </div>
              
              <div className="form-group">
                <label>公司名称</label>
                <input
                  type="text"
                  name="companyName"
                  value={formData.companyName}
                  onChange={handleInputChange}
                  placeholder="请输入公司名称"
                />
              </div>
              
              <div className="form-group">
                <label>职位</label>
                <input
                  type="text"
                  name="position"
                  value={formData.position}
                  onChange={handleInputChange}
                  placeholder="请输入职位"
                />
              </div>
            </div>
          </section>
          
          {/* 负债信息 */}
          <section className="form-section">
            <h2>负债信息</h2>
            <div className="form-group">
              <label>月还款总额</label>
              <div className="input-group">
                <input
                  type="number"
                  name="monthlyDebtPayment"
                  value={formData.monthlyDebtPayment}
                  onChange={handleInputChange}
                  placeholder="请输入月还款总额"
                  min="0"
                  step="100"
                />
                <span className="input-suffix">元</span>
              </div>
            </div>
            
            <div className="existing-loans">
              <label>现有贷款</label>
              {formData.existingLoans.map((loan, index) => (
                <div key={index} className="loan-item">
                  <select
                    value={loan.type}
                    onChange={(e) => updateExistingLoan(index, 'type', e.target.value)}
                    placeholder="贷款类型"
                  >
                    <option value="">选择贷款类型</option>
                    <option value="房贷">房贷</option>
                    <option value="车贷">车贷</option>
                    <option value="信用卡">信用卡</option>
                    <option value="其他">其他</option>
                  </select>
                  <input
                    type="number"
                    value={loan.amount}
                    onChange={(e) => updateExistingLoan(index, 'amount', e.target.value)}
                    placeholder="月还款额"
                    min="0"
                    step="100"
                  />
                  <input
                    type="text"
                    value={loan.bank}
                    onChange={(e) => updateExistingLoan(index, 'bank', e.target.value)}
                    placeholder="银行名称"
                  />
                  <button
                    type="button"
                    onClick={() => removeExistingLoan(index)}
                    className="remove-btn"
                  >
                    删除
                  </button>
                </div>
              ))}
              <button
                type="button"
                onClick={addExistingLoan}
                className="add-btn"
              >
                + 添加现有贷款
              </button>
            </div>
          </section>
          
          {/* 信用信息 */}
          <section className="form-section">
            <h2>信用信息</h2>
            <div className="form-grid">
              <div className="form-group">
                <label>信用评分</label>
                <input
                  type="number"
                  name="creditScore"
                  value={formData.creditScore}
                  onChange={handleInputChange}
                  placeholder="请输入信用评分"
                  min="300"
                  max="850"
                />
              </div>
              
              <div className="form-group">
                <label>信用历史</label>
                <textarea
                  name="creditHistory"
                  value={formData.creditHistory}
                  onChange={handleInputChange}
                  placeholder="请描述您的信用历史（如：无逾期记录、有轻微逾期等）"
                  rows="3"
                />
              </div>
            </div>
          </section>
          
          {/* 担保信息 */}
          <section className="form-section">
            <h2>担保信息</h2>
            <div className="form-group">
              <label className="checkbox-label">
                <input
                  type="checkbox"
                  name="hasCollateral"
                  checked={formData.hasCollateral}
                  onChange={handleInputChange}
                />
                是否有抵押物
              </label>
            </div>
            
            {formData.hasCollateral && (
              <div className="form-group">
                <label>抵押物类型</label>
                <select
                  name="collateralType"
                  value={formData.collateralType}
                  onChange={handleInputChange}
                >
                  <option value="">请选择抵押物类型</option>
                  <option value="房产">房产</option>
                  <option value="车辆">车辆</option>
                  <option value="其他">其他</option>
                </select>
              </div>
            )}
            
            <div className="form-group">
              <label className="checkbox-label">
                <input
                  type="checkbox"
                  name="hasGuarantor"
                  checked={formData.hasGuarantor}
                  onChange={handleInputChange}
                />
                是否有担保人
              </label>
            </div>
            
            {formData.hasGuarantor && (
              <div className="form-group">
                <label>担保人信息</label>
                <textarea
                  name="guarantorInfo"
                  value={formData.guarantorInfo}
                  onChange={handleInputChange}
                  placeholder="请填写担保人基本信息"
                  rows="3"
                />
              </div>
            )}
          </section>
          
          {/* 材料上传 */}
          <section className="form-section">
            <h2>材料上传</h2>
            <div className="file-upload">
              <input
                type="file"
                id="documents"
                multiple
                accept=".pdf,.jpg,.jpeg,.png,.doc,.docx"
                onChange={handleFileUpload}
                style={{ display: 'none' }}
              />
              <label htmlFor="documents" className="file-upload-btn">
                选择文件
              </label>
              <p className="file-upload-hint">支持PDF、图片、Word文档，单个文件不超过10MB</p>
            </div>
            
            {formData.documents.length > 0 && (
              <div className="file-list">
                {formData.documents.map((file, index) => (
                  <div key={index} className="file-item">
                    <span className="file-name">{file.name}</span>
                    <span className="file-size">({(file.size / 1024 / 1024).toFixed(2)} MB)</span>
                    <button
                      type="button"
                      onClick={() => removeFile(index)}
                      className="remove-file-btn"
                    >
                      删除
                    </button>
                  </div>
                ))}
              </div>
            )}
          </section>
          
          {/* 提交按钮 */}
          <div className="form-actions">
            <button
              type="button"
              onClick={() => navigate('/ai-chatbot-demo')}
              className="btn btn-secondary"
            >
              返回聊天
            </button>
            <button
              type="submit"
              disabled={isSubmitting}
              className="btn btn-primary"
            >
              {isSubmitting ? '提交中...' : '提交申请'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default LoanApplication;

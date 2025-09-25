-- AI智能贷款平台增强数据库设计
-- 基于金融行业最佳实践和监管要求

-- 创建数据库
CREATE DATABASE IF NOT EXISTS ai_loan_platform CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE ai_loan_platform;

-- 用户表（增强版）
CREATE TABLE IF NOT EXISTS users (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL COMMENT '用户名',
    email VARCHAR(100) UNIQUE NOT NULL COMMENT '邮箱',
    phone VARCHAR(20) UNIQUE NOT NULL COMMENT '手机号',
    password_hash VARCHAR(255) NOT NULL COMMENT '密码哈希',
    
    -- 个人/企业信息
    user_type ENUM('INDIVIDUAL', 'ENTERPRISE') NOT NULL DEFAULT 'INDIVIDUAL' COMMENT '用户类型',
    company_name VARCHAR(200) COMMENT '公司名称',
    company_type VARCHAR(50) COMMENT '公司类型',
    company_address TEXT COMMENT '公司地址',
    business_license VARCHAR(100) COMMENT '营业执照号',
    tax_id VARCHAR(50) COMMENT '税号',
    
    -- 信用信息
    credit_score INT DEFAULT 0 COMMENT '信用评分',
    credit_rating VARCHAR(10) DEFAULT 'C' COMMENT '信用等级',
    risk_level ENUM('LOW', 'MEDIUM', 'HIGH', 'CRITICAL') DEFAULT 'LOW' COMMENT '风险等级',
    risk_score DECIMAL(5,2) DEFAULT 0.00 COMMENT '风险评分',
    
    -- 财务信息
    annual_revenue DECIMAL(15,2) DEFAULT 0.00 COMMENT '年收入',
    monthly_income DECIMAL(12,2) DEFAULT 0.00 COMMENT '月收入',
    total_assets DECIMAL(15,2) DEFAULT 0.00 COMMENT '总资产',
    total_liabilities DECIMAL(15,2) DEFAULT 0.00 COMMENT '总负债',
    net_worth DECIMAL(15,2) DEFAULT 0.00 COMMENT '净资产',
    
    -- 状态信息
    status ENUM('ACTIVE', 'INACTIVE', 'SUSPENDED', 'DELETED', 'PENDING_VERIFICATION') DEFAULT 'PENDING_VERIFICATION' COMMENT '用户状态',
    verification_status ENUM('UNVERIFIED', 'PENDING', 'VERIFIED', 'REJECTED') DEFAULT 'UNVERIFIED' COMMENT '认证状态',
    kyc_status ENUM('NOT_STARTED', 'IN_PROGRESS', 'COMPLETED', 'FAILED') DEFAULT 'NOT_STARTED' COMMENT 'KYC状态',
    
    -- 时间戳
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    last_login_at TIMESTAMP NULL COMMENT '最后登录时间',
    
    -- 索引
    INDEX idx_email (email),
    INDEX idx_phone (phone),
    INDEX idx_company (company_name),
    INDEX idx_risk_level (risk_level),
    INDEX idx_status (status),
    INDEX idx_credit_score (credit_score),
    INDEX idx_user_type (user_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户表';

-- 贷款申请表（增强版）
CREATE TABLE IF NOT EXISTS loan_applications (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL COMMENT '用户ID',
    application_number VARCHAR(50) UNIQUE NOT NULL COMMENT '申请编号',
    
    -- 贷款基本信息
    loan_amount DECIMAL(15,2) NOT NULL COMMENT '申请金额',
    loan_purpose VARCHAR(200) NOT NULL COMMENT '贷款用途',
    loan_term_months INT NOT NULL COMMENT '贷款期限（月）',
    repayment_type ENUM('MONTHLY', 'QUARTERLY', 'SEMI_ANNUAL', 'ANNUAL', 'BULLET') DEFAULT 'MONTHLY' COMMENT '还款方式',
    
    -- 利率信息
    requested_rate DECIMAL(5,4) COMMENT '申请利率',
    approved_rate DECIMAL(5,4) COMMENT '批准利率',
    base_rate DECIMAL(5,4) COMMENT '基准利率',
    spread DECIMAL(5,4) COMMENT '利差',
    
    -- 风险评估
    risk_score DECIMAL(5,2) DEFAULT 0.00 COMMENT '风险评分',
    risk_level ENUM('LOW', 'MEDIUM', 'HIGH', 'CRITICAL') DEFAULT 'LOW' COMMENT '风险等级',
    credit_rating VARCHAR(10) COMMENT '信用等级',
    
    -- 审批信息
    status ENUM('DRAFT', 'SUBMITTED', 'UNDER_REVIEW', 'APPROVED', 'REJECTED', 'CANCELLED', 'DISBURSED', 'COMPLETED') DEFAULT 'DRAFT' COMMENT '申请状态',
    approval_amount DECIMAL(15,2) COMMENT '批准金额',
    approval_term_months INT COMMENT '批准期限',
    approval_date TIMESTAMP NULL COMMENT '批准日期',
    rejection_reason TEXT COMMENT '拒绝原因',
    
    -- 担保信息
    has_guarantor BOOLEAN DEFAULT FALSE COMMENT '是否有担保人',
    guarantor_name VARCHAR(100) COMMENT '担保人姓名',
    guarantor_phone VARCHAR(20) COMMENT '担保人电话',
    collateral_type VARCHAR(50) COMMENT '抵押物类型',
    collateral_value DECIMAL(15,2) COMMENT '抵押物价值',
    
    -- 时间戳
    submitted_at TIMESTAMP NULL COMMENT '提交时间',
    reviewed_at TIMESTAMP NULL COMMENT '审核时间',
    disbursed_at TIMESTAMP NULL COMMENT '放款时间',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    
    -- 外键约束
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    
    -- 索引
    INDEX idx_user (user_id),
    INDEX idx_status (status),
    INDEX idx_amount (loan_amount),
    INDEX idx_submitted_at (submitted_at),
    INDEX idx_risk_level (risk_level)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='贷款申请表';

-- 风险评估表（增强版）
CREATE TABLE IF NOT EXISTS risk_assessments (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    application_id BIGINT NOT NULL COMMENT '申请ID',
    user_id BIGINT NOT NULL COMMENT '用户ID',
    
    -- 风险评分
    credit_risk_score DECIMAL(5,2) DEFAULT 0.00 COMMENT '信用风险评分',
    market_risk_score DECIMAL(5,2) DEFAULT 0.00 COMMENT '市场风险评分',
    operational_risk_score DECIMAL(5,2) DEFAULT 0.00 COMMENT '操作风险评分',
    liquidity_risk_score DECIMAL(5,2) DEFAULT 0.00 COMMENT '流动性风险评分',
    total_risk_score DECIMAL(5,2) DEFAULT 0.00 COMMENT '综合风险评分',
    
    -- 风险等级
    risk_level ENUM('LOW', 'MEDIUM', 'HIGH', 'CRITICAL') DEFAULT 'LOW' COMMENT '风险等级',
    risk_description TEXT COMMENT '风险描述',
    
    -- 模型信息
    model_version VARCHAR(20) DEFAULT '1.0.0' COMMENT '模型版本',
    model_confidence DECIMAL(3,2) DEFAULT 0.00 COMMENT '模型置信度',
    feature_importance JSON COMMENT '特征重要性',
    
    -- 建议信息
    recommended_rate DECIMAL(5,4) COMMENT '推荐利率',
    max_loan_amount DECIMAL(15,2) COMMENT '最大贷款金额',
    recommended_term_months INT COMMENT '推荐期限',
    
    -- 风险因素
    risk_factors JSON COMMENT '风险因素',
    mitigation_strategies JSON COMMENT '缓解策略',
    recommendations JSON COMMENT '建议',
    
    -- 审批决策
    approved BOOLEAN DEFAULT FALSE COMMENT '是否批准',
    approval_reason TEXT COMMENT '审批原因',
    conditions TEXT COMMENT '放款条件',
    
    -- 时间戳
    assessed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '评估时间',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    
    -- 外键约束
    FOREIGN KEY (application_id) REFERENCES loan_applications(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    
    -- 索引
    INDEX idx_application (application_id),
    INDEX idx_user (user_id),
    INDEX idx_risk_level (risk_level),
    INDEX idx_total_score (total_risk_score)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='风险评估表';

-- 智能匹配表
CREATE TABLE IF NOT EXISTS smart_matches (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    application_id BIGINT NOT NULL COMMENT '申请ID',
    user_id BIGINT NOT NULL COMMENT '用户ID',
    
    -- 匹配信息
    match_score DECIMAL(5,2) DEFAULT 0.00 COMMENT '匹配分数',
    match_rank INT DEFAULT 0 COMMENT '匹配排名',
    match_reason TEXT COMMENT '匹配原因',
    
    -- 产品信息
    product_id VARCHAR(50) COMMENT '产品ID',
    product_name VARCHAR(200) COMMENT '产品名称',
    product_type VARCHAR(50) COMMENT '产品类型',
    institution_name VARCHAR(200) COMMENT '机构名称',
    
    -- 产品详情
    interest_rate DECIMAL(5,4) COMMENT '利率',
    term_months INT COMMENT '期限',
    amount DECIMAL(15,2) COMMENT '金额',
    features JSON COMMENT '产品特性',
    requirements JSON COMMENT '申请条件',
    
    -- 匹配算法信息
    algorithm_version VARCHAR(20) DEFAULT '1.0.0' COMMENT '算法版本',
    matching_criteria JSON COMMENT '匹配标准',
    feature_weights JSON COMMENT '特征权重',
    
    -- 状态信息
    status ENUM('PENDING', 'ACCEPTED', 'REJECTED', 'EXPIRED') DEFAULT 'PENDING' COMMENT '匹配状态',
    user_feedback ENUM('LIKE', 'DISLIKE', 'NEUTRAL') COMMENT '用户反馈',
    
    -- 时间戳
    matched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '匹配时间',
    expires_at TIMESTAMP NULL COMMENT '过期时间',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    
    -- 外键约束
    FOREIGN KEY (application_id) REFERENCES loan_applications(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    
    -- 索引
    INDEX idx_application (application_id),
    INDEX idx_user (user_id),
    INDEX idx_match_score (match_score),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='智能匹配表';

-- 文档表（增强版）
CREATE TABLE IF NOT EXISTS documents (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL COMMENT '用户ID',
    application_id BIGINT COMMENT '申请ID',
    
    -- 文件信息
    file_name VARCHAR(255) NOT NULL COMMENT '文件名',
    file_path VARCHAR(500) NOT NULL COMMENT '文件路径',
    file_type VARCHAR(50) NOT NULL COMMENT '文件类型',
    file_size BIGINT NOT NULL COMMENT '文件大小',
    file_hash VARCHAR(64) NOT NULL COMMENT '文件哈希',
    
    -- 文档分类
    document_type ENUM('IDENTITY', 'INCOME', 'ASSET', 'LIABILITY', 'BUSINESS', 'OTHER') NOT NULL COMMENT '文档类型',
    document_category VARCHAR(50) COMMENT '文档分类',
    
    -- OCR和AI处理
    ocr_text TEXT COMMENT 'OCR识别文本',
    extracted_data JSON COMMENT '提取的结构化数据',
    ai_analysis JSON COMMENT 'AI分析结果',
    confidence_score DECIMAL(3,2) DEFAULT 0.00 COMMENT '置信度评分',
    
    -- 验证信息
    verification_status ENUM('PENDING', 'VERIFIED', 'REJECTED', 'MANUAL_REVIEW') DEFAULT 'PENDING' COMMENT '验证状态',
    verification_notes TEXT COMMENT '验证备注',
    verified_by VARCHAR(50) COMMENT '验证人',
    verified_at TIMESTAMP NULL COMMENT '验证时间',
    
    -- 状态信息
    status ENUM('UPLOADED', 'PROCESSING', 'COMPLETED', 'FAILED', 'EXPIRED') DEFAULT 'UPLOADED' COMMENT '处理状态',
    error_message TEXT COMMENT '错误信息',
    
    -- 时间戳
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    
    -- 外键约束
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (application_id) REFERENCES loan_applications(id) ON DELETE CASCADE,
    
    -- 索引
    INDEX idx_user (user_id),
    INDEX idx_application (application_id),
    INDEX idx_type (document_type),
    INDEX idx_status (status),
    INDEX idx_verification (verification_status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='文档表';

-- 还款计划表
CREATE TABLE IF NOT EXISTS repayment_schedules (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    application_id BIGINT NOT NULL COMMENT '申请ID',
    user_id BIGINT NOT NULL COMMENT '用户ID',
    
    -- 还款信息
    installment_number INT NOT NULL COMMENT '期数',
    due_date DATE NOT NULL COMMENT '到期日期',
    principal_amount DECIMAL(12,2) NOT NULL COMMENT '本金金额',
    interest_amount DECIMAL(12,2) NOT NULL COMMENT '利息金额',
    total_amount DECIMAL(12,2) NOT NULL COMMENT '总金额',
    remaining_principal DECIMAL(15,2) NOT NULL COMMENT '剩余本金',
    
    -- 还款状态
    status ENUM('PENDING', 'PAID', 'OVERDUE', 'CANCELLED') DEFAULT 'PENDING' COMMENT '还款状态',
    paid_amount DECIMAL(12,2) DEFAULT 0.00 COMMENT '已还金额',
    paid_date TIMESTAMP NULL COMMENT '还款日期',
    late_fee DECIMAL(12,2) DEFAULT 0.00 COMMENT '滞纳金',
    
    -- 时间戳
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    
    -- 外键约束
    FOREIGN KEY (application_id) REFERENCES loan_applications(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    
    -- 索引
    INDEX idx_application (application_id),
    INDEX idx_user (user_id),
    INDEX idx_due_date (due_date),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='还款计划表';

-- 系统配置表（增强版）
CREATE TABLE IF NOT EXISTS system_configs (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    config_key VARCHAR(100) UNIQUE NOT NULL COMMENT '配置键',
    config_value TEXT COMMENT '配置值',
    config_type ENUM('STRING', 'NUMBER', 'BOOLEAN', 'JSON') DEFAULT 'STRING' COMMENT '配置类型',
    category VARCHAR(50) DEFAULT 'GENERAL' COMMENT '配置分类',
    description VARCHAR(500) COMMENT '配置描述',
    is_encrypted BOOLEAN DEFAULT FALSE COMMENT '是否加密',
    is_editable BOOLEAN DEFAULT TRUE COMMENT '是否可编辑',
    
    -- 时间戳
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    
    -- 索引
    INDEX idx_key (config_key),
    INDEX idx_category (category)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='系统配置表';

-- 审计日志表
CREATE TABLE IF NOT EXISTS audit_logs (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT COMMENT '用户ID',
    action VARCHAR(100) NOT NULL COMMENT '操作',
    resource_type VARCHAR(50) NOT NULL COMMENT '资源类型',
    resource_id VARCHAR(50) COMMENT '资源ID',
    old_values JSON COMMENT '旧值',
    new_values JSON COMMENT '新值',
    ip_address VARCHAR(45) COMMENT 'IP地址',
    user_agent TEXT COMMENT '用户代理',
    
    -- 时间戳
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    
    -- 外键约束
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    
    -- 索引
    INDEX idx_user (user_id),
    INDEX idx_action (action),
    INDEX idx_resource (resource_type, resource_id),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='审计日志表';

-- 插入初始配置数据
INSERT INTO system_configs (config_key, config_value, config_type, category, description) VALUES
('platform_name', 'AI智能贷款平台', 'STRING', 'GENERAL', '平台名称'),
('platform_version', '1.1.0', 'STRING', 'GENERAL', '平台版本'),
('max_file_size', '10485760', 'NUMBER', 'UPLOAD', '最大文件大小（字节）'),
('allowed_file_types', 'pdf,doc,docx,jpg,jpeg,png', 'STRING', 'UPLOAD', '允许的文件类型'),
('max_loan_amount', '10000000', 'NUMBER', 'LOAN', '最大贷款金额'),
('min_loan_amount', '10000', 'NUMBER', 'LOAN', '最小贷款金额'),
('max_loan_term', '120', 'NUMBER', 'LOAN', '最大贷款期限（月）'),
('min_loan_term', '1', 'NUMBER', 'LOAN', '最小贷款期限（月）'),
('base_interest_rate', '0.045', 'NUMBER', 'RATE', '基准利率'),
('risk_tolerance_threshold', '0.75', 'NUMBER', 'RISK', '风险容忍度阈值'),
('ai_model_version', '1.1.0', 'STRING', 'AI', 'AI模型版本'),
('enable_ai_risk_assessment', 'true', 'BOOLEAN', 'AI', '启用AI风险评估'),
('enable_smart_matching', 'true', 'BOOLEAN', 'AI', '启用智能匹配'),
('session_timeout', '3600', 'NUMBER', 'SECURITY', '会话超时时间（秒）'),
('max_login_attempts', '5', 'NUMBER', 'SECURITY', '最大登录尝试次数'),
('password_min_length', '8', 'NUMBER', 'SECURITY', '密码最小长度'),
('require_2fa', 'false', 'BOOLEAN', 'SECURITY', '是否要求双因子认证');

-- 创建视图：用户贷款统计
CREATE VIEW user_loan_stats AS
SELECT 
    u.id as user_id,
    u.username,
    u.company_name,
    COUNT(la.id) as total_applications,
    COUNT(CASE WHEN la.status = 'APPROVED' THEN 1 END) as approved_applications,
    COUNT(CASE WHEN la.status = 'REJECTED' THEN 1 END) as rejected_applications,
    COALESCE(SUM(la.loan_amount), 0) as total_requested_amount,
    COALESCE(SUM(la.approval_amount), 0) as total_approved_amount,
    AVG(la.risk_score) as avg_risk_score,
    MAX(la.created_at) as last_application_date
FROM users u
LEFT JOIN loan_applications la ON u.id = la.user_id
GROUP BY u.id, u.username, u.company_name;

-- 创建视图：风险统计
CREATE VIEW risk_statistics AS
SELECT 
    risk_level,
    COUNT(*) as count,
    AVG(total_risk_score) as avg_risk_score,
    AVG(credit_risk_score) as avg_credit_risk,
    AVG(market_risk_score) as avg_market_risk,
    AVG(operational_risk_score) as avg_operational_risk,
    AVG(liquidity_risk_score) as avg_liquidity_risk,
    COUNT(CASE WHEN approved = TRUE THEN 1 END) as approved_count,
    COUNT(CASE WHEN approved = FALSE THEN 1 END) as rejected_count
FROM risk_assessments
GROUP BY risk_level;

-- 创建存储过程：计算用户信用评分
DELIMITER //
CREATE PROCEDURE CalculateUserCreditScore(IN user_id BIGINT)
BEGIN
    DECLARE credit_score INT DEFAULT 0;
    DECLARE risk_score DECIMAL(5,2) DEFAULT 0.00;
    DECLARE risk_level VARCHAR(20) DEFAULT 'LOW';
    
    -- 基于历史数据计算信用评分
    SELECT 
        COALESCE(AVG(ra.total_risk_score), 0.00),
        COALESCE(AVG(ra.credit_risk_score), 0.00)
    INTO risk_score, credit_score
    FROM risk_assessments ra
    WHERE ra.user_id = user_id;
    
    -- 转换为信用评分（0-850）
    SET credit_score = GREATEST(300, LEAST(850, 850 - (credit_score * 5)));
    
    -- 确定风险等级
    IF credit_score >= 750 THEN
        SET risk_level = 'LOW';
    ELSEIF credit_score >= 700 THEN
        SET risk_level = 'MEDIUM';
    ELSEIF credit_score >= 650 THEN
        SET risk_level = 'HIGH';
    ELSE
        SET risk_level = 'CRITICAL';
    END IF;
    
    -- 更新用户表
    UPDATE users 
    SET 
        credit_score = credit_score,
        risk_level = risk_level,
        risk_score = risk_score,
        updated_at = CURRENT_TIMESTAMP
    WHERE id = user_id;
    
END //
DELIMITER ;

-- 创建触发器：自动更新用户风险等级
DELIMITER //
CREATE TRIGGER update_user_risk_after_assessment
AFTER INSERT ON risk_assessments
FOR EACH ROW
BEGIN
    CALL CalculateUserCreditScore(NEW.user_id);
END //
DELIMITER ;

-- 创建索引优化
CREATE INDEX idx_loan_applications_composite ON loan_applications(user_id, status, created_at);
CREATE INDEX idx_risk_assessments_composite ON risk_assessments(application_id, risk_level, total_risk_score);
CREATE INDEX idx_documents_composite ON documents(user_id, document_type, status);
CREATE INDEX idx_repayment_schedules_composite ON repayment_schedules(application_id, status, due_date);

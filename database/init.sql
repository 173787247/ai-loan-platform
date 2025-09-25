-- AI智能助贷招标平台数据库初始化脚本

-- 创建数据库
CREATE DATABASE IF NOT EXISTS ai_loan_platform CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE ai_loan_platform;

-- 用户表
CREATE TABLE IF NOT EXISTS users (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL COMMENT '用户名',
    email VARCHAR(100) UNIQUE NOT NULL COMMENT '邮箱',
    phone VARCHAR(20) UNIQUE NOT NULL COMMENT '手机号',
    password_hash VARCHAR(255) NOT NULL COMMENT '密码哈希',
    company_name VARCHAR(200) COMMENT '公司名称',
    company_type VARCHAR(50) COMMENT '公司类型',
    company_address TEXT COMMENT '公司地址',
    business_license VARCHAR(100) COMMENT '营业执照号',
    credit_score INT DEFAULT 0 COMMENT '信用评分',
    risk_level ENUM('LOW', 'MEDIUM', 'HIGH', 'VERY_HIGH') DEFAULT 'LOW' COMMENT '风险等级',
    status ENUM('ACTIVE', 'INACTIVE', 'SUSPENDED', 'DELETED') DEFAULT 'ACTIVE' COMMENT '用户状态',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_email (email),
    INDEX idx_phone (phone),
    INDEX idx_company (company_name),
    INDEX idx_risk_level (risk_level),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户表';

-- 招标表
CREATE TABLE IF NOT EXISTS tenders (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL COMMENT '用户ID',
    title VARCHAR(200) NOT NULL COMMENT '招标标题',
    description TEXT COMMENT '招标描述',
    amount DECIMAL(15,2) NOT NULL COMMENT '需求金额',
    term_months INT NOT NULL COMMENT '期限（月）',
    purpose VARCHAR(200) COMMENT '资金用途',
    repayment_type VARCHAR(50) COMMENT '还款方式',
    interest_rate_min DECIMAL(5,2) COMMENT '最低利率',
    interest_rate_max DECIMAL(5,2) COMMENT '最高利率',
    status ENUM('DRAFT', 'PUBLISHED', 'CLOSED', 'CANCELLED') DEFAULT 'DRAFT' COMMENT '招标状态',
    publish_time TIMESTAMP NULL COMMENT '发布时间',
    deadline TIMESTAMP NULL COMMENT '截止时间',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user (user_id),
    INDEX idx_status (status),
    INDEX idx_amount (amount),
    INDEX idx_publish_time (publish_time)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='招标表';

-- 方案表
CREATE TABLE IF NOT EXISTS proposals (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    tender_id BIGINT NOT NULL COMMENT '招标ID',
    institution_id BIGINT NOT NULL COMMENT '机构ID',
    institution_name VARCHAR(200) NOT NULL COMMENT '机构名称',
    interest_rate DECIMAL(5,2) NOT NULL COMMENT '利率',
    term_months INT NOT NULL COMMENT '期限（月）',
    amount DECIMAL(15,2) NOT NULL COMMENT '金额',
    repayment_type VARCHAR(50) COMMENT '还款方式',
    conditions TEXT COMMENT '申请条件',
    advantages TEXT COMMENT '产品优势',
    requirements TEXT COMMENT '所需材料',
    processing_time VARCHAR(100) COMMENT '办理时间',
    status ENUM('PENDING', 'ACCEPTED', 'REJECTED', 'CANCELLED') DEFAULT 'PENDING' COMMENT '方案状态',
    score DECIMAL(3,1) DEFAULT 0 COMMENT '评分',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (tender_id) REFERENCES tenders(id) ON DELETE CASCADE,
    INDEX idx_tender (tender_id),
    INDEX idx_institution (institution_id),
    INDEX idx_score (score),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='方案表';

-- 文档表
CREATE TABLE IF NOT EXISTS documents (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL COMMENT '用户ID',
    tender_id BIGINT COMMENT '招标ID',
    file_name VARCHAR(255) NOT NULL COMMENT '文件名',
    file_path VARCHAR(500) NOT NULL COMMENT '文件路径',
    file_type VARCHAR(50) NOT NULL COMMENT '文件类型',
    file_size BIGINT NOT NULL COMMENT '文件大小',
    file_hash VARCHAR(64) NOT NULL COMMENT '文件哈希',
    ocr_text TEXT COMMENT 'OCR识别文本',
    extracted_data JSON COMMENT '提取的数据',
    status ENUM('UPLOADED', 'PROCESSING', 'COMPLETED', 'FAILED') DEFAULT 'UPLOADED' COMMENT '处理状态',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (tender_id) REFERENCES tenders(id) ON DELETE CASCADE,
    INDEX idx_user (user_id),
    INDEX idx_tender (tender_id),
    INDEX idx_type (file_type),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='文档表';

-- 风险评估表
CREATE TABLE IF NOT EXISTS risk_assessments (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL COMMENT '用户ID',
    tender_id BIGINT COMMENT '招标ID',
    credit_score INT NOT NULL COMMENT '信用评分',
    business_risk_score INT NOT NULL COMMENT '经营风险评分',
    market_risk_score INT NOT NULL COMMENT '市场风险评分',
    total_risk_score INT NOT NULL COMMENT '总风险评分',
    risk_level ENUM('LOW', 'MEDIUM', 'HIGH', 'VERY_HIGH') NOT NULL COMMENT '风险等级',
    assessment_data JSON COMMENT '评估数据',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (tender_id) REFERENCES tenders(id) ON DELETE CASCADE,
    INDEX idx_user (user_id),
    INDEX idx_tender (tender_id),
    INDEX idx_risk_level (risk_level)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='风险评估表';

-- 办理记录表
CREATE TABLE IF NOT EXISTS process_records (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    tender_id BIGINT NOT NULL COMMENT '招标ID',
    proposal_id BIGINT NOT NULL COMMENT '方案ID',
    user_id BIGINT NOT NULL COMMENT '用户ID',
    status ENUM('PENDING', 'IN_PROGRESS', 'COMPLETED', 'FAILED') DEFAULT 'PENDING' COMMENT '办理状态',
    current_step VARCHAR(100) COMMENT '当前步骤',
    progress_percentage INT DEFAULT 0 COMMENT '进度百分比',
    notes TEXT COMMENT '备注',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (tender_id) REFERENCES tenders(id) ON DELETE CASCADE,
    FOREIGN KEY (proposal_id) REFERENCES proposals(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_tender (tender_id),
    INDEX idx_proposal (proposal_id),
    INDEX idx_user (user_id),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='办理记录表';

-- 系统配置表
CREATE TABLE IF NOT EXISTS system_configs (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    config_key VARCHAR(100) UNIQUE NOT NULL COMMENT '配置键',
    config_value TEXT COMMENT '配置值',
    description VARCHAR(500) COMMENT '配置描述',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_key (config_key)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='系统配置表';

-- 插入初始配置数据
INSERT INTO system_configs (config_key, config_value, description) VALUES
('platform_name', 'AI智能助贷招标平台', '平台名称'),
('platform_version', '1.0.0', '平台版本'),
('max_file_size', '10485760', '最大文件大小（字节）'),
('allowed_file_types', 'pdf,doc,docx,jpg,jpeg,png', '允许的文件类型'),
('default_credit_score', '600', '默认信用评分'),
('risk_threshold_low', '800', '低风险阈值'),
('risk_threshold_medium', '600', '中风险阈值'),
('risk_threshold_high', '400', '高风险阈值');

-- 创建视图：用户招标统计
CREATE VIEW user_tender_stats AS
SELECT 
    u.id as user_id,
    u.username,
    u.company_name,
    COUNT(t.id) as total_tenders,
    COUNT(CASE WHEN t.status = 'PUBLISHED' THEN 1 END) as published_tenders,
    COUNT(CASE WHEN t.status = 'CLOSED' THEN 1 END) as closed_tenders,
    COALESCE(SUM(t.amount), 0) as total_amount
FROM users u
LEFT JOIN tenders t ON u.id = t.user_id
GROUP BY u.id, u.username, u.company_name;

-- 创建视图：方案统计
CREATE VIEW proposal_stats AS
SELECT 
    p.id as proposal_id,
    p.tender_id,
    p.institution_name,
    p.interest_rate,
    p.amount,
    p.score,
    p.status,
    t.title as tender_title,
    t.amount as tender_amount
FROM proposals p
JOIN tenders t ON p.tender_id = t.id;

-- 创建存储过程：更新用户信用评分
DELIMITER //
CREATE PROCEDURE UpdateUserCreditScore(
    IN p_user_id BIGINT,
    IN p_credit_score INT
)
BEGIN
    DECLARE p_risk_level VARCHAR(20);
    
    -- 根据信用评分确定风险等级
    IF p_credit_score >= 800 THEN
        SET p_risk_level = 'LOW';
    ELSEIF p_credit_score >= 600 THEN
        SET p_risk_level = 'MEDIUM';
    ELSEIF p_credit_score >= 400 THEN
        SET p_risk_level = 'HIGH';
    ELSE
        SET p_risk_level = 'VERY_HIGH';
    END IF;
    
    -- 更新用户信用评分和风险等级
    UPDATE users 
    SET credit_score = p_credit_score, 
        risk_level = p_risk_level,
        updated_at = CURRENT_TIMESTAMP
    WHERE id = p_user_id;
    
    -- 记录风险评估
    INSERT INTO risk_assessments (user_id, credit_score, business_risk_score, market_risk_score, total_risk_score, risk_level)
    VALUES (p_user_id, p_credit_score, p_credit_score, p_credit_score, p_credit_score, p_risk_level);
END //
DELIMITER ;

-- 创建触发器：更新招标状态
DELIMITER //
CREATE TRIGGER update_tender_status
AFTER UPDATE ON tenders
FOR EACH ROW
BEGIN
    IF NEW.status = 'PUBLISHED' AND OLD.status != 'PUBLISHED' THEN
        UPDATE tenders 
        SET publish_time = CURRENT_TIMESTAMP 
        WHERE id = NEW.id;
    END IF;
END //
DELIMITER ;

-- 创建索引优化查询性能
CREATE INDEX idx_tenders_user_status ON tenders(user_id, status);
CREATE INDEX idx_proposals_tender_status ON proposals(tender_id, status);
CREATE INDEX idx_documents_user_tender ON documents(user_id, tender_id);
CREATE INDEX idx_risk_assessments_user_tender ON risk_assessments(user_id, tender_id);
CREATE INDEX idx_process_records_tender_proposal ON process_records(tender_id, proposal_id);

-- 插入测试数据
INSERT INTO users (username, email, phone, password_hash, company_name, company_type, credit_score, risk_level) VALUES
('testuser1', 'test1@example.com', '13800138001', '$2a$10$N.zmdr9k7uOCQb376NoUnuTJ8iKyVhQyF0J0QpQpQpQpQpQpQpQpQ', '测试科技有限公司', '科技', 750, 'LOW'),
('testuser2', 'test2@example.com', '13800138002', '$2a$10$N.zmdr9k7uOCQb376NoUnuTJ8iKyVhQyF0J0QpQpQpQpQpQpQpQpQ', '测试贸易有限公司', '贸易', 650, 'MEDIUM');

COMMIT;

-- RAG向量数据库初始化脚本
-- 启用pgvector扩展
CREATE EXTENSION IF NOT EXISTS vector;

-- 启用中文全文搜索支持
CREATE TEXT SEARCH CONFIGURATION chinese (COPY = simple);

-- 创建知识库表
CREATE TABLE IF NOT EXISTS knowledge_base (
    id SERIAL PRIMARY KEY,
    category VARCHAR(50) NOT NULL,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    embedding VECTOR(384), -- sentence-transformers all-MiniLM-L6-v2维度
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建向量索引
CREATE INDEX IF NOT EXISTS knowledge_base_embedding_idx 
ON knowledge_base USING ivfflat (embedding vector_cosine_ops) 
WITH (lists = 100);

-- 创建分类索引
CREATE INDEX IF NOT EXISTS knowledge_base_category_idx 
ON knowledge_base (category);

-- 创建全文搜索索引
CREATE INDEX IF NOT EXISTS knowledge_base_content_fts_idx 
ON knowledge_base USING gin (to_tsvector('chinese', content));

-- 插入初始知识库数据
INSERT INTO knowledge_base (category, title, content, metadata) VALUES
-- 贷款产品知识
('loan_products', '个人信用贷款', '基于个人信用评分的无抵押贷款产品，额度1-50万，期限1-5年，年利率5.5%-15%', '{"requirements": ["身份证", "收入证明", "银行流水", "征信报告"], "interest_rate": "年利率5.5%-15%", "amount_range": "1-50万", "term_range": "1-5年"}'),
('loan_products', '企业经营贷款', '面向企业法人的经营性贷款，额度10-500万，期限1-3年，年利率4.5%-12%', '{"requirements": ["营业执照", "财务报表", "经营场所证明", "担保材料"], "interest_rate": "年利率4.5%-12%", "amount_range": "10-500万", "term_range": "1-3年"}'),
('loan_products', '房屋抵押贷款', '以房产作为抵押物的贷款，额度为房产评估价的70%，年利率3.5%-8%', '{"requirements": ["房产证", "评估报告", "收入证明", "征信报告"], "interest_rate": "年利率3.5%-8%", "amount_range": "房产评估价70%", "term_range": "1-20年"}'),
('loan_products', '车辆抵押贷款', '以车辆作为抵押物的贷款，额度为车辆评估价的80%，年利率6%-12%', '{"requirements": ["行驶证", "车辆登记证", "保险单", "收入证明"], "interest_rate": "年利率6%-12%", "amount_range": "车辆评估价80%", "term_range": "1-3年"}'),
('loan_products', '消费贷款', '用于个人消费的贷款产品，额度5-30万，期限6-60个月，年利率5.5%-15%', '{"requirements": ["身份证", "收入证明", "消费用途证明"], "interest_rate": "年利率5.5%-15%", "amount_range": "5-30万", "term_range": "6-60个月"}'),

-- 申请条件知识
('requirements', '个人贷款条件', '年满18周岁，有稳定收入，信用记录良好，月收入不低于3000元，征信评分600分以上', '{"age_min": 18, "income_min": 3000, "credit_score_min": 600, "stable_income": true}'),
('requirements', '企业贷款条件', '企业成立满1年，有正常经营，财务状况良好，年营业额不低于100万，有固定经营场所', '{"company_age_min": 1, "revenue_min": 1000000, "profit_required": true, "business_place": true}'),
('requirements', '抵押贷款条件', '抵押物产权清晰，价值充足，无法律纠纷，符合银行要求，抵押物评估价值充足', '{"collateral_clear": true, "value_sufficient": true, "no_disputes": true, "bank_approved": true}'),
('requirements', '担保人条件', '担保人需有稳定收入，信用记录良好，年龄在18-65岁之间，有担保能力', '{"age_range": "18-65", "stable_income": true, "good_credit": true, "guarantee_capacity": true}'),

-- 利率政策知识
('interest_rates', '个人信用贷款利率', '年利率5.5%-15%，根据信用评分和收入水平确定，信用越好利率越低', '{"min_rate": 5.5, "max_rate": 15, "factors": ["credit_score", "income_level"], "credit_impact": true}'),
('interest_rates', '企业贷款利率', '年利率4.5%-12%，根据企业规模和经营状况确定，规模越大利率越低', '{"min_rate": 4.5, "max_rate": 12, "factors": ["company_size", "business_condition"], "size_impact": true}'),
('interest_rates', '抵押贷款利率', '年利率3.5%-8%，根据抵押物类型和价值确定，抵押物价值越高利率越低', '{"min_rate": 3.5, "max_rate": 8, "factors": ["collateral_type", "collateral_value"], "value_impact": true}'),
('interest_rates', '浮动利率', '部分产品采用浮动利率，随市场利率变化调整，有上限保护', '{"type": "floating", "market_linked": true, "cap_protection": true}'),

-- 还款方式知识
('repayment', '等额本息', '每月还款金额相同，前期利息多本金少，后期本金多利息少，适合收入稳定的借款人', '{"monthly_payment": "fixed", "early_interest": "high", "late_principal": "high", "suitable_for": "stable_income"}'),
('repayment', '等额本金', '每月还款本金相同，利息逐月递减，总利息较少，适合收入递增的借款人', '{"monthly_principal": "fixed", "interest_decreasing": true, "total_interest": "lower", "suitable_for": "increasing_income"}'),
('repayment', '先息后本', '前期只还利息，到期一次性还本金，适合短期资金周转，总利息较高', '{"early_interest_only": true, "principal_at_end": true, "suitable_for": "short_term", "total_interest": "higher"}'),
('repayment', '随借随还', '按日计息，随借随还，适合资金需求不固定的借款人', '{"daily_interest": true, "flexible_repayment": true, "suitable_for": "flexible_needs"}'),

-- 申请流程知识
('process', '在线申请流程', '1.注册账号 2.填写基本信息 3.选择贷款产品 4.上传申请材料 5.等待审核结果', '{"steps": 5, "online": true, "timeframe": "即时"}'),
('process', '材料审核流程', '1.系统预审 2.人工审核 3.征信查询 4.风险评估 5.审批决定', '{"steps": 5, "automated": true, "manual": true, "timeframe": "1-3天"}'),
('process', '放款流程', '1.签署合同 2.办理抵押登记 3.放款到账 4.开始还款', '{"steps": 4, "contract": true, "collateral_registration": true, "timeframe": "1-2天"}'),
('process', '贷后管理', '1.还款提醒 2.账户管理 3.额度调整 4.提前还款', '{"steps": 4, "reminder": true, "account_management": true, "adjustment": true}'),

-- 常见问题知识
('faq', '申请流程', '1.在线申请 2.提交材料 3.审核评估 4.放款到账，一般3-7个工作日完成', '{"steps": 4, "timeframe": "3-7天", "online_application": true}'),
('faq', '提前还款', '支持提前还款，无违约金，可节省利息支出，需提前申请', '{"allowed": true, "penalty": false, "interest_saving": true, "advance_notice": true}'),
('faq', '逾期处理', '逾期将产生罚息，影响征信记录，建议按时还款，可申请展期', '{"penalty_interest": true, "credit_impact": true, "recommendation": "on_time", "extension": true}'),
('faq', '额度调整', '根据还款记录和信用状况，可申请提高贷款额度，需重新审核', '{"adjustable": true, "factors": ["repayment_record", "credit_status"], "re_audit": true}'),
('faq', '利率调整', '固定利率不变，浮动利率随市场调整，有上限保护', '{"fixed_rate": "unchanged", "floating_rate": "market_adjusted", "cap_protection": true}'),
('faq', '担保要求', '根据贷款金额和风险等级，可能需要提供担保人或担保物', '{"guarantor_required": "conditional", "collateral_required": "conditional", "amount_dependent": true}'),

-- 政策法规知识
('policies', '贷款利率上限', '年利率不超过24%，超过部分不受法律保护，实际利率根据风险评估确定', '{"max_rate": 24, "legal_protection": false, "risk_based": true}'),
('policies', '征信查询', '申请贷款会查询个人征信，查询记录会保留2年，影响后续贷款申请', '{"credit_inquiry": true, "retention_period": "2年", "future_impact": true}'),
('policies', '担保要求', '根据贷款金额和风险等级，可能需要提供担保人或担保物，降低银行风险', '{"guarantor_required": "conditional", "collateral_required": "conditional", "risk_reduction": true}'),
('policies', '合同条款', '贷款合同受法律保护，双方应严格履行合同义务，违约将承担法律责任', '{"legal_protection": true, "contract_binding": true, "legal_consequences": true}'),
('policies', '隐私保护', '严格保护客户隐私信息，不得泄露给第三方，符合数据保护法规', '{"privacy_protection": true, "no_disclosure": true, "data_protection": true}'),

-- 风险控制知识
('risk_control', '信用风险评估', '通过征信报告、收入证明、银行流水等评估借款人信用风险', '{"factors": ["credit_report", "income_proof", "bank_statement"], "assessment": "comprehensive"}'),
('risk_control', '还款能力评估', '根据收入水平、负债情况、家庭状况等评估还款能力', '{"factors": ["income_level", "debt_ratio", "family_situation"], "assessment": "repayment_capacity"}'),
('risk_control', '抵押物评估', '专业机构评估抵押物价值，确保抵押物价值充足', '{"professional_appraisal": true, "value_verification": true, "sufficient_value": true}'),
('risk_control', '反欺诈检测', '通过大数据分析、人脸识别等技术防范欺诈行为', '{"big_data_analysis": true, "face_recognition": true, "fraud_prevention": true}'),

-- 银行信息知识
('bank_info', '招商银行简介', '招商银行成立于1987年，是中国内地规模第六大的银行，也是中国内地首家完全由企业法人持股的股份制商业银行。总行设在深圳，是中国内地市值第五大的银行。', '{"founded": "1987", "headquarters": "深圳", "type": "股份制商业银行", "rank": "第六大银行"}'),
('bank_info', '招商银行贷款产品', '招商银行提供个人贷款、企业贷款、住房贷款、汽车贷款等多种产品。个人信用贷款额度1-50万，年利率4.5%-12%；企业贷款额度10-500万，年利率3.8%-8.5%。', '{"personal_loan": "1-50万", "enterprise_loan": "10-500万", "personal_rate": "4.5%-12%", "enterprise_rate": "3.8%-8.5%"}'),
('bank_info', '招商银行特色服务', '招商银行以零售银行业务见长，提供专业的财富管理、私人银行、信用卡等金融服务。拥有完善的线上银行系统和移动银行APP。', '{"strength": "零售银行", "services": ["财富管理", "私人银行", "信用卡"], "digital": "线上银行"}'),
('bank_info', '招商银行网点分布', '招商银行在全国主要城市设有分支机构，网点覆盖一二线城市，同时提供7×24小时网上银行和手机银行服务。', '{"coverage": "一二线城市", "online": "7×24小时", "channels": ["网点", "网银", "手机银行"]}'),
('bank_info', '招商银行申请条件', '个人贷款需年满18周岁，有稳定收入，信用记录良好；企业贷款需成立满1年，有正常经营，财务状况良好。', '{"personal_age": "18周岁", "personal_income": "稳定收入", "enterprise_age": "1年", "enterprise_condition": "正常经营"}'),
('bank_info', '招商银行联系方式', '招商银行客服热线：95555，官方网站：www.cmbchina.com，可在线申请贷款和查询产品信息。', '{"hotline": "95555", "website": "www.cmbchina.com", "online_application": true}');

-- 创建函数：计算文本相似度
CREATE OR REPLACE FUNCTION calculate_text_similarity(query_text TEXT, content_text TEXT)
RETURNS FLOAT AS $$
BEGIN
    -- 简单的文本相似度计算（可以后续替换为更复杂的算法）
    RETURN similarity(query_text, content_text);
END;
$$ LANGUAGE plpgsql;

-- 创建函数：向量相似度搜索
CREATE OR REPLACE FUNCTION search_knowledge_by_vector(
    query_embedding VECTOR(1536),
    similarity_threshold FLOAT DEFAULT 0.7,
    max_results INTEGER DEFAULT 5
)
RETURNS TABLE (
    id INTEGER,
    category VARCHAR(50),
    title VARCHAR(200),
    content TEXT,
    similarity_score FLOAT,
    metadata JSONB
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        kb.id,
        kb.category,
        kb.title,
        kb.content,
        1 - (kb.embedding <=> query_embedding) AS similarity_score,
        kb.metadata
    FROM knowledge_base kb
    WHERE kb.embedding IS NOT NULL
    AND 1 - (kb.embedding <=> query_embedding) > similarity_threshold
    ORDER BY kb.embedding <=> query_embedding
    LIMIT max_results;
END;
$$ LANGUAGE plpgsql;

-- 创建函数：混合搜索（向量+全文）
CREATE OR REPLACE FUNCTION search_knowledge_hybrid(
    query_text TEXT,
    query_embedding VECTOR(1536),
    category_filter VARCHAR(50) DEFAULT NULL,
    max_results INTEGER DEFAULT 5
)
RETURNS TABLE (
    id INTEGER,
    category VARCHAR(50),
    title VARCHAR(200),
    content TEXT,
    relevance_score FLOAT,
    metadata JSONB
) AS $$
BEGIN
    RETURN QUERY
    WITH vector_search AS (
        SELECT 
            kb.id,
            kb.category,
            kb.title,
            kb.content,
            1 - (kb.embedding <=> query_embedding) AS vector_score,
            kb.metadata
        FROM knowledge_base kb
        WHERE kb.embedding IS NOT NULL
        AND (category_filter IS NULL OR kb.category = category_filter)
    ),
    text_search AS (
        SELECT 
            kb.id,
            kb.category,
            kb.title,
            kb.content,
            ts_rank(to_tsvector('chinese', kb.content), plainto_tsquery('chinese', query_text)) AS text_score,
            kb.metadata
        FROM knowledge_base kb
        WHERE to_tsvector('chinese', kb.content) @@ plainto_tsquery('chinese', query_text)
        AND (category_filter IS NULL OR kb.category = category_filter)
    ),
    combined_results AS (
        SELECT 
            COALESCE(vs.id, ts.id) AS id,
            COALESCE(vs.category, ts.category) AS category,
            COALESCE(vs.title, ts.title) AS title,
            COALESCE(vs.content, ts.content) AS content,
            COALESCE(vs.vector_score, 0) * 0.7 + COALESCE(ts.text_score, 0) * 0.3 AS relevance_score,
            COALESCE(vs.metadata, ts.metadata) AS metadata
        FROM vector_search vs
        FULL OUTER JOIN text_search ts ON vs.id = ts.id
    )
    SELECT 
        cr.id,
        cr.category,
        cr.title,
        cr.content,
        cr.relevance_score,
        cr.metadata
    FROM combined_results cr
    ORDER BY cr.relevance_score DESC
    LIMIT max_results;
END;
$$ LANGUAGE plpgsql;

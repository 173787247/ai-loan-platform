-- 重新创建RAG搜索函数，修复类型不匹配问题

-- 创建混合搜索函数
CREATE OR REPLACE FUNCTION search_knowledge_hybrid(
    query_text text,
    query_embedding vector(384),
    max_results integer,
    category_filter text DEFAULT ''
)
RETURNS TABLE(
    id integer,
    title text,
    content text,
    category text,
    similarity_score float,
    text_score float,
    combined_score float
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        kb.id,
        kb.title::text,
        kb.content::text,
        kb.category::text,
        (1 - (kb.embedding <=> query_embedding))::float as similarity_score,
        ts_rank(to_tsvector('chinese', kb.content), plainto_tsquery('chinese', query_text))::float as text_score,
        (0.7 * (1 - (kb.embedding <=> query_embedding)) + 0.3 * ts_rank(to_tsvector('chinese', kb.content), plainto_tsquery('chinese', query_text)))::float as combined_score
    FROM knowledge_base kb
    WHERE 
        (category_filter = '' OR kb.category ILIKE '%' || category_filter || '%')
        AND kb.embedding IS NOT NULL
    ORDER BY combined_score DESC
    LIMIT max_results;
END;
$$ LANGUAGE plpgsql;

-- 创建全文搜索函数
CREATE OR REPLACE FUNCTION search_knowledge_text(
    query_text text,
    max_results integer,
    category_filter text DEFAULT ''
)
RETURNS TABLE(
    id integer,
    title text,
    content text,
    category text,
    text_score float
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        kb.id,
        kb.title::text,
        kb.content::text,
        kb.category::text,
        CASE 
            WHEN kb.content ILIKE '%' || query_text || '%' THEN 1.0
            ELSE 0.5
        END::float as text_score
    FROM knowledge_base kb
    WHERE 
        (category_filter = '' OR kb.category ILIKE '%' || category_filter || '%')
        AND kb.content ILIKE '%' || query_text || '%'
    ORDER BY text_score DESC
    LIMIT max_results;
END;
$$ LANGUAGE plpgsql;

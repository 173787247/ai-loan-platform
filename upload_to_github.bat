@echo off
echo ========================================
echo AI智能贷款平台 - GitHub上传脚本
echo ========================================
echo.

echo 正在检查Git状态...
git status

echo.
echo 正在添加所有文件到暂存区...
git add .

echo.
echo 正在提交更改...
git commit -m "Update: AI智能贷款平台 v1.1.0

- 更新项目统计信息 (49个Java文件 + 15个前端文件 + 19个Python文件)
- 完善金融合规文档和AI技术文档
- 增强风险评估算法和智能匹配算法
- 优化数据库设计和安全机制
- 添加GitHub上传指南和环境变量配置
- 完善项目文档和部署配置

项目规模:
- 后端代码: ~25,000行
- 前端代码: ~12,000行  
- AI服务代码: ~8,000行
- 配置文件: ~3,000行
- 文档: ~15,000字

服务架构:
- 8个微服务
- 4个数据库
- 6个监控服务
- 20+个容器"

echo.
echo 正在推送到GitHub...
git push origin main

echo.
echo ========================================
echo 上传完成！
echo ========================================
echo.
echo 请访问以下链接查看项目：
echo https://github.com/173787247/ai-loan-platform
echo.
echo 如果遇到问题，请检查：
echo 1. 网络连接是否正常
echo 2. GitHub认证是否配置正确
echo 3. 是否有未提交的更改
echo.
pause

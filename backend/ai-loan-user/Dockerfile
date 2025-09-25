# AI助贷招标平台 - 用户服务Dockerfile (多阶段构建)

# 构建阶段
FROM maven:3.8.6-openjdk-11-slim AS builder

WORKDIR /app

# 配置Maven使用阿里云镜像
RUN mkdir -p /root/.m2
COPY <<EOF /root/.m2/settings.xml
<?xml version="1.0" encoding="UTF-8"?>
<settings xmlns="http://maven.apache.org/SETTINGS/1.0.0"
          xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xsi:schemaLocation="http://maven.apache.org/SETTINGS/1.0.0
          http://maven.apache.org/xsd/settings-1.0.0.xsd">
  <mirrors>
    <mirror>
      <id>aliyun</id>
      <mirrorOf>*</mirrorOf>
      <name>Aliyun Maven Mirror</name>
      <url>https://maven.aliyun.com/repository/public</url>
    </mirror>
  </mirrors>
</settings>
EOF

# 复制pom.xml
COPY pom.xml .

# 复制源代码
COPY src ./src

# 构建应用
RUN mvn clean package -DskipTests

# 运行阶段
FROM openjdk:11-jre-slim

WORKDIR /app

# 从构建阶段复制jar文件
COPY --from=builder /app/target/ai-loan-user-1.1.0.jar app.jar

EXPOSE 8080
ENV JAVA_OPTS="-Xms512m -Xmx1024m -Dspring.profiles.active=docker"
ENTRYPOINT ["sh", "-c", "java $JAVA_OPTS -jar app.jar"]

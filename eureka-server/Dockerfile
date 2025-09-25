# 构建阶段
FROM maven:3.8.6-openjdk-11-slim AS build

# 设置工作目录
WORKDIR /app

# 复制pom.xml
COPY pom.xml .

# 下载依赖
RUN mvn dependency:go-offline -B

# 复制源代码
COPY src ./src

# 构建应用
RUN mvn clean package -DskipTests

# 运行阶段
FROM openjdk:11-jre-slim

# 设置工作目录
WORKDIR /app

# 复制构建的jar文件
COPY --from=build /app/target/eureka-server-1.0.0.jar app.jar

# 暴露端口
EXPOSE 8761

# 启动Eureka服务器
CMD ["java", "-jar", "app.jar"]

FROM openjdk:11-jre-slim
WORKDIR /app
COPY target/ai-loan-notification-1.0.0.jar app.jar
EXPOSE 8086
ENV JAVA_OPTS="-Xms512m -Xmx1024m -Dspring.profiles.active=docker"
ENTRYPOINT ["sh", "-c", "java $JAVA_OPTS -jar app.jar"]

FROM openjdk:11-jre-slim
WORKDIR /app
COPY target/ai-loan-ai-1.0.0.jar app.jar
EXPOSE 8087
ENV JAVA_OPTS="-Xms512m -Xmx1024m -Dspring.profiles.active=docker"
ENTRYPOINT ["sh", "-c", "java $JAVA_OPTS -jar app.jar"]

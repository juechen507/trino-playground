FROM flink:2.0.0-scala_2.12-java21

ENV FLINK_HOME=/opt/flink

ENV FLINK_VERSION_SHORT=2.0
ENV FLINK_VERSION=2.0.0
RUN mv ${FLINK_HOME}/opt/flink-s3-fs-hadoop-${FLINK_VERSION}.jar ${FLINK_HOME}/lib/

ARG AWS_SDK_VERSION=1.12.797
ARG HADOOP_AWS_VERSION=3.5.0

# Configure Haddoop (flink need use hadoop relevant jar to access S3)
WORKDIR /opt
RUN curl -L http://archive.apache.org/dist/hadoop/common/hadoop-${HADOOP_AWS_VERSION}/hadoop-${HADOOP_AWS_VERSION}.tar.gz  \
    -o /opt/hadoop-${HADOOP_AWS_VERSION}.tar.gz
RUN tar xzvf hadoop-${HADOOP_AWS_VERSION}.tar.gz && rm hadoop-${HADOOP_AWS_VERSION}.tar.gz

RUN ln -s /opt/hadoop-${HADOOP_AWS_VERSION} /opt/hadoop
ENV HADOOP_HOME="/opt/hadoop"

# Configure HMS
ARG HIVE_VERSION=3.1.3
RUN curl -L https://repo1.maven.org/maven2/org/apache/hive/hive-metastore/${HIVE_VERSION}/hive-metastore-${HIVE_VERSION}.jar  \
    -o /opt/flink/lib/hive-metastore-${HIVE_VERSION}.jar
RUN curl -L https://repo1.maven.org/maven2/org/apache/hive/hive-exec/${HIVE_VERSION}/hive-exec-${HIVE_VERSION}.jar  \
    -o /opt/flink/lib/hive-exec-${HIVE_VERSION}.jar
RUN curl -L https://repo1.maven.org/maven2/org/apache/thrift/libthrift/0.13.0/libthrift-0.13.0.jar \
    -o /opt/flink/lib/libthrift-0.13.0.jar
RUN curl -L https://repo1.maven.org/maven2/org/apache/thrift/libfb303/0.9.3/libfb303-0.9.3.jar \
    -o /opt/flink/lib/libfb303-0.9.3.jar

# Configure ICEBERG
ENV ICEBERG_VERSION=1.10.0
RUN curl -L https://repo1.maven.org/maven2/org/apache/iceberg/iceberg-flink-runtime-${FLINK_VERSION_SHORT}/${ICEBERG_VERSION}/iceberg-flink-runtime-${FLINK_VERSION_SHORT}-${ICEBERG_VERSION}.jar \
    -o ${FLINK_HOME}/lib/iceberg-flink-runtime-${FLINK_VERSION_SHORT}-${ICEBERG_VERSION}.jar

# Configure Kafka
ENV KAFKA_VERSION=4.0.0
RUN curl -L https://repo1.maven.org/maven2/org/apache/flink/flink-sql-connector-kafka/${KAFKA_VERSION}-${FLINK_VERSION_SHORT}/flink-sql-connector-kafka-${KAFKA_VERSION}-${FLINK_VERSION_SHORT}.jar \
    -o ${FLINK_HOME}/lib/flink-sql-connector-kafka-${KAFKA_VERSION}-${FLINK_VERSION_SHORT}.jar

# Configure FLINK CLI
ENV SQL_CLIENT_HOME /opt/flink-client
ENV PATH="/opt/flink-client:${PATH}"
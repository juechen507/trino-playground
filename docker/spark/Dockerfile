FROM apache/spark:4.0.2-java21

WORKDIR /opt/spark/jars
# iceberg
RUN wget https://search.maven.org/remotecontent?filepath=org/apache/iceberg/iceberg-spark-runtime-4.0_2.13/1.10.1/iceberg-spark-runtime-4.0_2.13-1.10.1.jar

# iceberg-s3
RUN wget https://repo1.maven.org/maven2/org/apache/iceberg/iceberg-aws/1.10.1/iceberg-aws-1.10.1.jar
RUN wget https://repo1.maven.org/maven2/org/apache/iceberg/iceberg-aws-bundle/1.10.1/iceberg-aws-bundle-1.10.1.jar

# kafka connector
RUN wget https://repo1.maven.org/maven2/org/apache/spark/spark-sql-kafka-0-10_2.13/4.0.2/spark-sql-kafka-0-10_2.13-4.0.2.jar

WORKDIR /opt/spark
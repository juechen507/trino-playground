# Flink (消费 Kafka 数据写入 Iceberg) 搭建指南

## 搭建Flink

### 下载项目，使用特定分支
```shell
git clone https://github.com/apache/flink.git
cd flink
git checkout -b origin/release-2.0
```

### 编译项目
```shell
./mvnw clean package -DskipTests -Djdk21 -Pjava21-target
```
### 部署
```shell
# 省略
# 直接使用apache/flink 镜像，具体细节见 ./docker/flink/Dockerfile
# 如果开发的话，将flink编译后的build-target映射到容器内
```

### 启动 Flink SQL CLI
```shell
export HADOOP_CLASSPATH=`$HADOOP_HOME/bin/hadoop classpath`
/opt/flink/bin/sql-client.sh
```

### 创建实时任务（Flink）
```sql(flink)
-- 创建 catalog
CREATE CATALOG iceberg WITH (
    'type'='iceberg',
    'metastore' = 'hive',
    'uri'='thrift://hive-metastore:9083',
    'clients'='5',
    'property-version'='1',
    'warehouse'='s3a://datalake/iceberg'
);

-- 查看已经存在的database
SHOW DATABASES FROM iceberg;

CREATE DATABASE IF NOT EXISTS iceberg.demo;

-- 表不存在则创建
CREATE TABLE IF NOT EXISTS iceberg.demo.event_iceberg (
     t TIMESTAMP,
     id BIGINT,
     name VARCHAR(50)
)

-- 必须在default_catalog下才能创建 kafka table
USE CATALOG default_catalog;
CREATE TABLE event_kafka (id int, name String) WITH (
   'connector' = 'kafka',
   'topic' = 'events',
   'properties.bootstrap.servers' = 'kafka:9092',
   'properties.group.id' = 'flink',
   'scan.startup.mode' = 'earliest-offset',
   'format' = 'csv',
   'csv.ignore-parse-errors' = 'true'
   );

-- 必须开启！！！ 每 30 秒做一次 checkpoint，触发 Iceberg 提交
SET execution.checkpointing.interval = 30s;
-- 精确一次语义
SET execution.checkpointing.mode = EXACTLY_ONCE;
-- 取消任务时保留 checkpoint，保证续跑
SET execution.checkpointing.externalized-checkpoint-retention = RETAIN_ON_CANCELLATION;

-- 创建实时任务
INSERT INTO iceberg.demo.event_iceberg 
  SELECT current_timestamp,id,name FROM default_catalog.default_database.event_kafka;

--停止任务
stop job 'xxxxx';
```

### 查看iceberg的文件地址（Trino）
```sql(trino)
SELECT * FROM iceberg.demo."event_iceberg.$files";
```

### 使用kafka客户端生产消息
```shell
sh /opt/kafka/bin/kafka-console-producer.sh \
  --bootstrap-server kafka:9092 \
  --topic events
```
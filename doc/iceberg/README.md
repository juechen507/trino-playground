# 在本项目中使用 Trino 查询 Apache Iceberg（MinIO + Hive Metastore）

本项目已集成 Trino、MinIO、Hive Metastore 等服务。本文档在原有 Iceberg 指南基础上，结合本仓库配置（docker-compose 与 Trino catalog），说明如何快速在本 playground 中使用 Iceberg。

重要文件参考：
- docker-compose.yaml（项目根）
- ./conf/trino/catalog/iceberg_1.properties
- ./conf/trino/catalog/iceberg_2.properties

---

## 先决条件
- Docker 与 docker-compose
- 在仓库根目录使用 playground 启动：

```bash
./playground.sh start
```

Trino Web UI: http://localhost:28080
MinIO 控制台: http://localhost:9000

---

## 1. 本项目中的服务与凭证（重要）
- MinIO
  - 服务名/容器名: minio
  - UI: http://localhost:9000
  - Access key: minio
  - Secret key: minio123
- Hive Metastore
  - 容器名: hive-metastore
  - Thrift URI: thrift://hive-metastore:9083
  - 使用内置 Postgres（容器: postgres）作为 metastore DB
- Trino
  - 容器名: trino
  - 配置目录挂载: ./conf/trino -> /etc/trino
  - 已在 ./conf/trino/catalog 下包含 iceberg_1.properties 与 iceberg_2.properties

说明：上述凭证来自 docker-compose.yaml 的 environment 配置，文中示例均基于这些值。

---

## 2. 已存在的 Trino Iceberg catalog（本项目）
项目提供两份 catalog：

- iceberg_1（./conf/trino/catalog/iceberg_1.properties）
  - connector.name=lakehouse（lakehouse 接入）

- iceberg_2（./conf/trino/catalog/iceberg_2.properties）
  - connector.name=iceberg（官方 Iceberg connector）

选择建议：
- 想把 Iceberg 元数据保存在 Hive Metastore（与 Hive 兼容）且使用 Trino 的 iceberg connector：使用 iceberg_2。
- 想以 lakehouse 风格（lakehouse connector）管理 Iceberg 表：使用 iceberg_1。

在 SQL 中使用的 catalog 名称即对应文件名（去掉 .properties）：iceberg_1、iceberg_2。

---

## 3. 在 MinIO 上创建 bucket（本项目默认 warehouse）

本项目的 Hive Metastore 配置中，默认 warehouse 指向 s3://datalake/（见 docker-compose 环境变量 HIVE_METASTORE_WAREHOUSE_DIR）。请确保在 MinIO 内创建名为 datalake 的 bucket：

可在 minio UI 上创建

注意：Iceberg 表的实际数据目录会位于 s3://datalake/... 或者 Trino catalog 中指定的 iceberg.warehouse 路径下。

---

## 4. 在 Trino 中操作 Iceberg（示例 SQL）

登录 Trino 容器并打开 trino CLI：

```bash
docker exec -it trino trino
```

以下示例展示在 iceberg_2（官方 connector）和 iceberg_1（lakehouse）上的常见操作。

示例 A — 使用 iceberg_2（hive-metastore 风格）

```sql
-- 创建 schema（可选择指定 location）
CREATE SCHEMA iceberg_2.demo WITH (location = 's3a://datalake/warehouse/demo');

-- 创建表
CREATE TABLE iceberg_2.demo.users (
  id BIGINT,
  name VARCHAR,
  email VARCHAR
)
WITH (format = 'PARQUET');

-- 插入与查询
INSERT INTO iceberg_2.demo.users (id, name, email) 
  VALUES (1, 'Alice', 'alice@example.com');
SELECT * FROM iceberg_2.demo.users;
```

示例 B — 使用 iceberg_1（lakehouse）

```sql
CREATE SCHEMA iceberg_1.demo;
CREATE TABLE iceberg_1.demo.events (
  ts TIMESTAMP,
  user_id BIGINT,
  action VARCHAR
)
WITH (format='PARQUET');

INSERT INTO iceberg_1.demo.events VALUES (current_timestamp, 1, 'click');
SELECT * FROM iceberg_1.demo.events;
```

说明：在本环境 Trino 与 MinIO 通过 s3a/native-s3 配置互通，SQL 中使用的 s3 协议通常为 s3a:// 或 catalog 所期望的 URI。

---

## 5. 常见排错要点（结合本仓库）
- 确认 playground 已启动：./playground.sh status
- MinIO 控制台（http://localhost:9000）能登录（minio / minio123），并能看到 datalake bucket。
- Hive Metastore 可访问（thrift://hive-metastore:9083）。
- Trino catalog 文件位于 ./conf/trino/catalog，重启 Trino 后会加载这些 catalog（playground.sh start 会将配置挂载进容器）。
- 若 S3 写入失败，检查 catalog 文件中的 s3.endpoint 与 access key/secret 是否与 docker-compose 中的 MinIO 值一致。
- 若表无数据，查看 MinIO 对应路径（./data/minio）是否有写入文件。

---

## 6. 扩展建议
- 若需要把示例 catalog 的配置调整为真实生产环境（比如使用 AWS S3 / Glue / IAM），优先在 ./conf/trino/catalog 中修改对应文件并重启 Trino。
- 需要我把 datalake bucket 的初始化命令加入 docker-compose 启动脚本或提供一个初始化脚本吗？回复“是”即可，我会帮你把脚本添加到 init/ 并更新 README。

---

更新自本仓库配置：docker-compose.yaml、./conf/trino/catalog/iceberg_1.properties、iceberg_2.properties。

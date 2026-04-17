## Playground introduction

The playground is a Trino Docker runtime environment.

Depending on your network and computer, startup time may take some seconds. Once the playground environment has started, you can open [http://localhost:28080](http://localhost:8090) in a browser to access the Trino Web UI.

## Prerequisites

Install Git (optional), Docker, Docker Compose.

## System Resource Requirements

2 CPU cores, 2 GB RAM, 25 GB disk storage, MacOS or Linux OS (Verified Ubuntu22.04 Ubuntu24.04 AmazonLinux).

## TCP ports used

The playground runs several services. The TCP ports used may clash with existing services you run, such as MySQL or Postgres.

| Docker container      | Ports used  |
| --------------------- |-------------|
| playground-trino      | 28080,29043 |

## Playground usage

### Start
```shell
./playground.sh start
```

### Check status
```shell
./playground.sh status
```

### Stop
```shell
./playground.sh stop
```

## Containner

### Using Trino CLI in Docker Container

1. Login to the Trino Docker container using the following command:
```shell
docker exec -it trino bash
```

2. Open the Trino CLI in the container.
```shell
trino
```

3. Replay tpch/tpcds queries
```shell
trino --catalog tpch --schema tiny -f /tmp/sql/tpch/q01.sql
```
or
```shell
trino --catalog tpcds --schema tiny -f /tmp/sql/tpcds/q01.sql
```

### kafka
1. Login to the Kafka Docker container using the following command:
```shell
docker exec -it kafka bash
```

2. Show topics
```shell
sh /opt/kafka/bin/kafka-topics.sh \
  --bootstrap-server localhost:9092 \
  --list
```

3. Produce message
```shell
sh /opt/kafka/bin/kafka-console-producer.sh \
  --bootstrap-server kafka:9092 \
  --topic trino_query_complete
```

4. Consume message
```shell
sh /opt/kafka/bin/kafka-console-consumer.sh \
  --bootstrap-server kafka:9092 \
  --topic trino_query_complete
```

### postgres

1. Open PostgreSQL CLI in Docker container
```shell
psql -U postgres
```

2. List databases
```sql
\l
```

3. Use database
```sql
\c metastore
```

4. List tables
```sql
\dt
```

5. Query
```sql
select * from ${table_name};
```

6. Exit
```sql
\q
```

## Browse Web UI
- Trino Web UI: [http://localhost:28080](http://localhost:28080)
- Jaeger UI (Trace): [http://localhost:16686/](http://localhost:16686)
- Prometheus UI: [http://localhost:29090](http://localhost:29090)
- Grafana UI: [http://localhost:23000](http://localhost:23000)
- Minio UI: [http://localhost:9000](http://localhost:9000)
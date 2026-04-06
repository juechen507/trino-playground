## Playground introduction

The playground is a Trino Docker runtime environment.

Depending on your network and computer, startup time may take some seconds. Once the playground environment has started, you can open [http://localhost:28080](http://localhost:8090) in a browser to access the Trino Web UI.

## Prerequisites

Install Git (optional), Docker, Docker Compose.

## System Resource Requirements

2 CPU cores, 2 GB RAM, 25 GB disk storage, MacOS or Linux OS (Verified Ubuntu22.04 Ubuntu24.04 AmazonLinux).

## TCP ports used

The playground runs several services. The TCP ports used may clash with existing services you run, such as MySQL or Postgres.

| Docker container      | Ports used             |
| --------------------- |------------------------|
| playground-trino      | 28080                  |

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

### Using Trino CLI in Docker Container

1. Login to the Trino Docker container using the following command:

```shell
docker exec -it trino bash
```

2. Open the Trino CLI in the container.

```shell
trino
```
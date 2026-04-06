#!/bin/bash

# install toolst
apt update && apt install -y less vim net-tools telnet curl

# install Trino server and CLI
if [[ ! -d /usr/lib/trino-server ]] ; then
  mkdir -p /usr/lib/trino-server
fi
tar -zxvf /usr/lib/trino-server.tar.gz -C /usr/lib/trino-server --strip-components=1

cp /tmp/trino/trino-cli-*.jar /usr/lib/trino-cli-executable.jar

cat > /usr/bin/trino << 'EOF'
#!/bin/bash
java -jar /usr/lib/trino-cli-executable.jar "$@"
EOF

chmod +x /usr/bin/trino

# star Trino server
exec /bin/bash /tmp/trino/start.sh

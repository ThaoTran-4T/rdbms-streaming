curl  -X POST \
  'http://localhost:8080/api/connector/1/postgres' \
  --header 'Accept: */*' \
  --header 'User-Agent: Thunder Client (https://www.thunderclient.com)' \
  --header 'Content-Type: application/json' \
  --data-raw '{
    "name": "test",
    "config": {
        "topic.prefix": "inventory",
        "database.hostname": "postgres",
        "database.port":"5432",
        "database.user": "thaotran",
        "database.password": "thaotran123",
        "database.dbname": "debezium-test",
        "schema.include.list": "public",
        "table.include.list": "public.products,public.inventory" ,
        "heartbeat.interval.ms": 30000,
        "heartbeat.action.query": "select * from public.inventory where product_id = 8",
        "query.fetch.size": 500,
        "topic.creation.groups": "debezium-etl",
        "topic.creation.debezium-etl.include": "",
        "topic.creation.debezium-etl.exclude": "",
        "topic.creation.default.partitions": -1,
        "topic.creation.default.replication.factor": -1,
        "plugin.name": "pgoutput",
        "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
        "tasks.max": "1",
        "skipped.operations": "r",
        "snapshot.mode": "never",
        "slot.name": "debezium_order",
        "publication.autocreate.mode": "filtered",
        "publication.name": "dbz_order_publication"
    }
}
'
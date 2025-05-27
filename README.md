# rdbms-streaming
## Architecture
![Untitled Diagram-Page-1 drawio (1)](https://github.com/user-attachments/assets/8603f4ff-dcfd-4727-9469-b66e7bfc0a2d)

## How to run
**Step 1: Start all docker services**
```bash
docker compose up
```

**Step 2: Create 2 buckets on Minio UI** (http://localhost:9001/)
- inventorylogs
- inventorylog.checkpoint

_Alternative_: we can use aws command line instead

**Step 3: Create Debezium Connector**
``` 
script/create-debezium-connector.sh
```

**Step 4: Insert Data to Postgres**
```
script/insert-data-postgres.sh
```

**Step 5: Create venv and start Spark Job**
```
python script/ingest.py
```
View data on Minio UI

## UI
- Minio: http://localhost:9001/
- Kafka UI: http://localhost:8081/
- Debezium UI: http://localhost:8080/
  
## To-do list
- Handle update and delete event
- .....

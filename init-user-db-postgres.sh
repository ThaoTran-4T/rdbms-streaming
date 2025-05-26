#!/usr/bin/env bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE "debezium-test";
EOSQL

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "debezium-test" <<-EOSQL
    -- Create the products table
    CREATE TABLE IF NOT EXISTS products (
        product_id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        description TEXT,
        category VARCHAR(50),
        price NUMERIC(10, 2) CHECK (price >= 0),
        stock_quantity INT CHECK (stock_quantity >= 0),
        is_active BOOLEAN DEFAULT TRUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    -- Create inventory table
    CREATE TABLE IF NOT EXISTS inventory (
        inventory_id SERIAL PRIMARY KEY,
        product_id INT NOT NULL REFERENCES products(product_id) ON DELETE CASCADE,
        warehouse_location VARCHAR(100),
        quantity_available INT CHECK (quantity_available >= 0),
        restock_date DATE
    );

	CREATE USER hive WITH PASSWORD 'hive';
	CREATE DATABASE metastore_db;
    ALTER DATABASE metastore_db OWNER TO hive;
    ALTER USER hive SET search_path = public;
	
EOSQL

-- Database: e_commerce
-- DROP DATABASE IF EXISTS e_commerce;

-- Note: 'IF NOT EXISTS' is not supported for CREATE DATABASE in standard PostgreSQL.
-- If the database already exists, this command will fail. You can ignore that error.
CREATE DATABASE e_commerce
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'English_Rwanda.1252'
    LC_CTYPE = 'English_Rwanda.1252'
    LOCALE_PROVIDER = 'libc'
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;

COMMENT ON DATABASE "e-commerce"
    IS 'Database for learning data streaming using Spark during Apprenticeship at AmaliTech 2025/2026 Data Engineering KWISANGA Ernest';
/*
- Switch to the new database (if running in psql, use \c e_commerce)
- If running in a tool like pgAdmin, allow the subsequent queries to 
run in the current connection, 
- but you must manually ensure you are connected to 'e_commerce' 
if you want tables created there.
*/
-- Creating table to store e-commerce events
CREATE TABLE IF NOT EXISTS e_commerce_events (
    event_id VARCHAR(50) PRIMARY KEY,
    event_type VARCHAR(20),
    product_id VARCHAR(20),
    user_id VARCHAR(20),
    event_timestamp TIMESTAMP,
    quantity INTEGER,
    price DECIMAL(10, 2)
);
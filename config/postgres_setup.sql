-- Real-Time E-Commerce Streaming Pipeline
-- PostgreSQL Database Setup Script
-- 
-- This script creates the database and events table for the streaming pipeline.
-- Run as superuser (postgres)

-- Create database (if not exists)
CREATE DATABASE IF NOT EXISTS ecommerce_streaming;

-- Connect to the database
\c ecommerce_streaming;

-- Create events table
-- This table stores all ingested e-commerce events
CREATE TABLE IF NOT EXISTS events (
    event_id UUID PRIMARY KEY,
    event_type VARCHAR(50) NOT NULL,
    product_id VARCHAR(100) NOT NULL,
    user_id VARCHAR(100) NOT NULL,
    event_timestamp TIMESTAMP NOT NULL,
    quantity INTEGER,
    price NUMERIC(10, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_events_event_type ON events(event_type);
CREATE INDEX IF NOT EXISTS idx_events_user_id ON events(user_id);
CREATE INDEX IF NOT EXISTS idx_events_product_id ON events(product_id);
CREATE INDEX IF NOT EXISTS idx_events_timestamp ON events(event_timestamp);

-- Grant permissions to postgres user
GRANT ALL PRIVILEGES ON DATABASE ecommerce_streaming TO postgres;
GRANT ALL PRIVILEGES ON TABLE events TO postgres;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO postgres;

-- Verify table creation
SELECT tablename FROM pg_tables WHERE tablename = 'events';

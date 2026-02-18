-- Initialize URL Shortener Database

-- Create urls table
CREATE TABLE IF NOT EXISTS urls (
    id SERIAL PRIMARY KEY,
    short_code VARCHAR(8) UNIQUE NOT NULL,
    original_url TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index on short_code for faster lookups
CREATE INDEX IF NOT EXISTS idx_short_code ON urls(short_code);

-- Create index on created_at for analytics
CREATE INDEX IF NOT EXISTS idx_created_at ON urls(created_at);


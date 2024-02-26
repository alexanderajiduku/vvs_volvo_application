-- db.sql

-- Create the "users" table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR,
    last_name VARCHAR,
    department VARCHAR,
    username VARCHAR UNIQUE,
    email VARCHAR UNIQUE,
    hashed_password VARCHAR,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Drop the "users" table if it exists
DROP TABLE IF EXISTS users;

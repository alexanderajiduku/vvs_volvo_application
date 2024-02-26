-- User Table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR NOT NULL,
    last_name VARCHAR NOT NULL,
    username VARCHAR UNIQUE NOT NULL,
    email VARCHAR UNIQUE NOT NULL,
    hashed_password TEXT NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT current_timestamp
);

-- Camera Table
CREATE TABLE camera (
    id SERIAL PRIMARY KEY,
    camera_name VARCHAR NOT NULL,
    camera_model VARCHAR,
    checkerboard_width INTEGER,
    checkerboard_height INTEGER,
    description TEXT
);

-- CalibrationData Table
CREATE TABLE calibrationdata (
    id SERIAL PRIMARY KEY,
    camera_id INTEGER NOT NULL,
    calibration_file_path VARCHAR NOT NULL,
    FOREIGN KEY (camera_id) REFERENCES camera(id)
);

-- UploadedFile Table
CREATE TABLE images (
    id SERIAL PRIMARY KEY,
    filename VARCHAR NOT NULL,
    content_type VARCHAR,
    upload_timestamp TIMESTAMP WITHOUT TIME ZONE DEFAULT current_timestamp,
    file_path VARCHAR,
    camera_id INTEGER,
    FOREIGN KEY (camera_id) REFERENCES camera(id)
);

-- AnnotatedFile Table
CREATE TABLE annotated_files (
    id SERIAL PRIMARY KEY,
    original_filename VARCHAR,
    annotated_filename VARCHAR,
    annotated_filepath VARCHAR,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT current_timestamp
);

-- Model Table
CREATE TABLE models (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    description TEXT,
    filename VARCHAR,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT current_timestamp
);

-- UploadedImages Table
CREATE TABLE ultralyticsuploads (
    id SERIAL PRIMARY KEY,
    filename VARCHAR NOT NULL,
    content_type VARCHAR,
    file_path VARCHAR,
    upload_timestamp TIMESTAMP WITHOUT TIME ZONE DEFAULT current_timestamp
);

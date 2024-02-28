



![VVS_Database_Schema](project_images/DB_Schema.png)


# Database Summary and Relationships

## Tables

### User Table

Columns:
- id: Serial primary key.
- first_name: VARCHAR, not null.
- last_name: VARCHAR, not null.
- username: VARCHAR, unique, not null.
- email: VARCHAR, unique, not null.
- hashed_password: TEXT, not null.
- is_active: BOOLEAN, not null, default true.
- created_at: TIMESTAMP without time zone, default current timestamp.

### Camera Table

Columns:
- id: Serial primary key.
- camera_name: VARCHAR, not null.
- camera_model: VARCHAR.
- checkerboard_width: INTEGER.
- checkerboard_height: INTEGER.
- description: TEXT.

### CalibrationData Table

Columns:
- id: Serial primary key.
- camera_id: INTEGER, not null, foreign key referencing camera(id).
- calibration_file_path: VARCHAR, not null.

### UploadedFile Table

Columns:
- id: Serial primary key.
- filename: VARCHAR, not null.
- content_type: VARCHAR.
- upload_timestamp: TIMESTAMP without time zone, default current timestamp.
- file_path: VARCHAR.
- camera_id: INTEGER, foreign key referencing camera(id).

### AnnotatedFile Table

Columns:
- id: Serial primary key.
- original_filename: VARCHAR.
- annotated_filename: VARCHAR.
- annotated_filepath: VARCHAR.
- created_at: TIMESTAMP without time zone, default current timestamp.

### Model Table

Columns:
- id: Serial primary key.
- name: VARCHAR, not null.
- description: TEXT.
- filename: VARCHAR.
- created_at: TIMESTAMP without time zone, default current timestamp.

### UploadedImages Table

Columns:
- id: Serial primary key.
- filename: VARCHAR, not null.
- content_type: VARCHAR.
- file_path: VARCHAR.
- upload_timestamp: TIMESTAMP without time zone, default current timestamp.

## Relationships

- calibrationdata.camera_id references camera.id.
- images.camera_id references camera.id.

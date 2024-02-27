-- Seed Users
INSERT INTO users (first_name, last_name, username, email, hashed_password, is_active, created_at) VALUES
('Alex', 'Ajiduku', 'aajiduku', 'jalexajiduku@gmail.com', '123456789', TRUE, CURRENT_TIMESTAMP),
('Jane', 'Doe', 'janedoe', 'janedoe@example.com', 'hashed_janedoe_password', TRUE, CURRENT_TIMESTAMP);
-- Add more user records as needed

-- Seed Cameras
INSERT INTO camera (camera_name, camera_model, checkerboard_width, checkerboard_height, description) VALUES
('Camera A', 'Model A', 9, 6, 'Camera A Description'),
('Camera B', 'Model B', 8, 5, 'Camera B Description');
-- Add more camera records as needed

-- Seed CalibrationData, UploadedFile, AnnotatedFile, Model, and UploadedImages
-- Follow the same pattern as above for other tables, constructing INSERT statements for each table.

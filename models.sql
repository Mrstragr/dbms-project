-- SAU Equipment & Lab Resource Management System Database Schema
-- Designed by: Ansh (DB Designer)
-- Database: MySQL

-- Create database
CREATE DATABASE IF NOT EXISTS sau_lab_mgmt;
USE sau_lab_mgmt;

-- Users table
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role ENUM('student', 'lab_assistant', 'faculty', 'admin') NOT NULL DEFAULT 'student',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Equipment table
CREATE TABLE equipment (
    equipment_id INT AUTO_INCREMENT PRIMARY KEY,
    equipment_name VARCHAR(100) NOT NULL,
    equipment_type ENUM('laptop', 'projector', 'oscilloscope', 'multimeter', 'power_supply', 'microscope', 'other') NOT NULL,
    description TEXT,
    location VARCHAR(100) NOT NULL,
    status ENUM('available', 'booked', 'maintenance', 'retired') NOT NULL DEFAULT 'available',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Bookings table
CREATE TABLE bookings (
    booking_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    equipment_id INT NOT NULL,
    issued_by INT NULL,  -- Lab assistant or faculty who issued the equipment
    booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    return_date TIMESTAMP NOT NULL,
    actual_return_date TIMESTAMP NULL,
    status ENUM('active', 'returned', 'cancelled') NOT NULL DEFAULT 'active',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (equipment_id) REFERENCES equipment(equipment_id) ON DELETE CASCADE,
    FOREIGN KEY (issued_by) REFERENCES users(user_id) ON DELETE SET NULL
);

-- Maintenance table
CREATE TABLE maintenance (
    maintenance_id INT AUTO_INCREMENT PRIMARY KEY,
    equipment_id INT NOT NULL,
    maintenance_type ENUM('routine', 'repair', 'upgrade', 'calibration', 'cleaning', 'other') NOT NULL,
    description TEXT NOT NULL,
    cost DECIMAL(10,2) DEFAULT 0.00,
    maintenance_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    next_maintenance_date TIMESTAMP NULL,
    status ENUM('pending', 'in_progress', 'completed') NOT NULL DEFAULT 'pending',
    technician VARCHAR(100),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (equipment_id) REFERENCES equipment(equipment_id) ON DELETE CASCADE
);

-- Notifications table
CREATE TABLE notifications (
    notification_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NULL,
    title VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    type ENUM('booking', 'return', 'maintenance', 'overdue', 'system') NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Feedback table
CREATE TABLE feedback (
    feedback_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    booking_id INT NULL,
    equipment_id INT NULL,
    rating INT CHECK (rating >= 1 AND rating <= 5),
    comments TEXT,
    feedback_type ENUM('equipment', 'service', 'lab_assistant', 'faculty') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (booking_id) REFERENCES bookings(booking_id) ON DELETE CASCADE,
    FOREIGN KEY (equipment_id) REFERENCES equipment(equipment_id) ON DELETE CASCADE
);

-- User limitations table
CREATE TABLE user_limitations (
    limitation_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    limitation_type ENUM('booking_limit', 'overdue_penalty', 'blacklist') NOT NULL,
    description TEXT,
    active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Create indexes for better performance
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_equipment_status ON equipment(status);
CREATE INDEX idx_equipment_type ON equipment(equipment_type);
CREATE INDEX idx_bookings_user_id ON bookings(user_id);
CREATE INDEX idx_bookings_equipment_id ON bookings(equipment_id);
CREATE INDEX idx_bookings_status ON bookings(status);
CREATE INDEX idx_bookings_return_date ON bookings(return_date);
CREATE INDEX idx_maintenance_equipment_id ON maintenance(equipment_id);
CREATE INDEX idx_maintenance_status ON maintenance(status);
CREATE INDEX idx_notifications_user_id ON notifications(user_id);
CREATE INDEX idx_notifications_is_read ON notifications(is_read);

-- Insert sample data
INSERT INTO users (username, email, password, role) VALUES
('admin', 'messi@sau.edu', '$2b$12$ILX0/uf7A/nDlwNvmbemD.QarMrlDi3JNYJS7re11C8j2Win6XKZe', 'admin'),
('nikhil', 'nikhil@sau.edu', '$2b$12$ILX0/uf7A/nDlwNvmbemD.QarMrlDi3JNYJS7re11C8j2Win6XKZe', 'student'),
('jane_smith', 'jane.smith@sau.edu', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/8Qz8K2O', 'lab_assistant'),
('prof_sau', 'heee@sau.edu', '$2b$12$ILX0/uf7A/nDlwNvmbemD.QarMrlDi3JNYJS7re11C8j2Win6XKZe', 'faculty');

INSERT INTO equipment (equipment_name, equipment_type, description, location, status) VALUES
('Dell Laptop 001', 'laptop', 'Dell Inspiron 15 3000 Series, Intel i5, 8GB RAM', 'Lab A-101', 'available'),
('HP Laptop 002', 'laptop', 'HP Pavilion 15, Intel i7, 16GB RAM', 'Lab A-101', 'available'),
('Epson Projector 001', 'projector', 'Epson PowerLite 1781W, 3000 lumens', 'Lab B-201', 'available'),
('Tektronix Oscilloscope 001', 'oscilloscope', 'Tektronix TBS1000 Series, 100MHz', 'Lab C-301', 'available'),
('Fluke Multimeter 001', 'multimeter', 'Fluke 87V Digital Multimeter', 'Lab C-301', 'available'),
('Keysight Power Supply 001', 'power_supply', 'Keysight E3631A Triple Output Power Supply', 'Lab C-301', 'available'),
('Olympus Microscope 001', 'microscope', 'Olympus BX51 Research Microscope', 'Lab D-401', 'available'),
('Dell Laptop 003', 'laptop', 'Dell Latitude 5520, Intel i5, 8GB RAM', 'Lab A-102', 'booked'),
('BenQ Projector 002', 'projector', 'BenQ MW632ST, 3200 lumens', 'Lab B-202', 'maintenance');

INSERT INTO bookings (user_id, equipment_id, return_date, status) VALUES
(2, 8, DATE_ADD(NOW(), INTERVAL 7 DAY), 'active'),
(3, 1, DATE_ADD(NOW(), INTERVAL 3 DAY), 'returned');

INSERT INTO maintenance (equipment_id, maintenance_type, description, cost, status) VALUES
(9, 'repair', 'Bulb replacement and lens cleaning', 150.00, 'pending'),
(1, 'routine', 'Monthly cleaning and software update', 25.00, 'completed'),
(3, 'calibration', 'Annual calibration check', 200.00, 'pending');

-- Create views for common queries
CREATE VIEW equipment_availability AS
SELECT 
    e.equipment_id,
    e.equipment_name,
    e.equipment_type,
    e.location,
    e.status,
    CASE 
        WHEN e.status = 'available' THEN 'Yes'
        WHEN e.status = 'booked' THEN 'No'
        WHEN e.status = 'maintenance' THEN 'Under Maintenance'
        ELSE 'Retired'
    END as availability_status
FROM equipment e;

CREATE VIEW active_bookings AS
SELECT 
    b.booking_id,
    u.username,
    e.equipment_name,
    e.equipment_type,
    b.booking_date,
    b.return_date,
    DATEDIFF(b.return_date, NOW()) as days_remaining
FROM bookings b
JOIN users u ON b.user_id = u.user_id
JOIN equipment e ON b.equipment_id = e.equipment_id
WHERE b.status = 'active';

CREATE VIEW overdue_bookings AS
SELECT 
    b.booking_id,
    u.username,
    u.email,
    e.equipment_name,
    b.return_date,
    DATEDIFF(NOW(), b.return_date) as days_overdue
FROM bookings b
JOIN users u ON b.user_id = u.user_id
JOIN equipment e ON b.equipment_id = e.equipment_id
WHERE b.status = 'active' AND b.return_date < NOW();

-- Create stored procedures for common operations
DELIMITER //

CREATE PROCEDURE GetEquipmentByType(IN equipment_type_param VARCHAR(50))
BEGIN
    SELECT * FROM equipment 
    WHERE equipment_type = equipment_type_param 
    ORDER BY equipment_name;
END //

CREATE PROCEDURE GetUserBookings(IN user_id_param INT)
BEGIN
    SELECT 
        b.*,
        e.equipment_name,
        e.equipment_type
    FROM bookings b
    JOIN equipment e ON b.equipment_id = e.equipment_id
    WHERE b.user_id = user_id_param
    ORDER BY b.booking_date DESC;
END //

CREATE PROCEDURE GetMaintenanceSchedule()
BEGIN
    SELECT 
        m.*,
        e.equipment_name,
        e.equipment_type
    FROM maintenance m
    JOIN equipment e ON m.equipment_id = e.equipment_id
    WHERE m.status IN ('pending', 'in_progress')
    ORDER BY m.maintenance_date ASC;
END //

DELIMITER ;

-- Grant permissions (to be configured by Amar - DB Administrator)
-- GRANT SELECT, INSERT, UPDATE, DELETE ON sau_lab_mgmt.* TO 'app_user'@'localhost' IDENTIFIED BY 'secure_password';
-- GRANT SELECT ON sau_lab_mgmt.* TO 'readonly_user'@'localhost' IDENTIFIED BY 'readonly_password';

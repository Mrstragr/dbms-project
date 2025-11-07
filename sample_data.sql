-- Sample Data Insertion Script for SAU Lab Management System
-- This script adds additional sample data for testing purposes

USE sau_lab_mgmt;

-- Insert more users
INSERT INTO users (username, email, password, role) VALUES
('alice_johnson', 'alice.johnson@sau.edu', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/8Qz8K2O', 'student'),
('bob_wilson', 'bob.wilson@sau.edu', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/8Qz8K2O', 'student'),
('sarah_davis', 'sarah.davis@sau.edu', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/8Qz8K2O', 'lab_assistant'),
('mike_brown', 'messi@sau.edu', '$2b$12$ILX0/uf7A/nDlwNvmbemD.QarMrlDi3JNYJS7re11C8j2Win6XKZe', 'faculty'),
('dr_smith', 'messi@sau.edu', '$2b$12$ILX0/uf7A/nDlwNvmbemD.QarMrlDi3JNYJS7re11C8j2Win6XKZe', 'admin');

-- Insert more equipment
INSERT INTO equipment (equipment_name, equipment_type, description, location, status) VALUES
('MacBook Pro 001', 'laptop', 'Apple MacBook Pro 13-inch, M1 Chip, 8GB RAM', 'Lab A-103', 'available'),
('Lenovo ThinkPad 001', 'laptop', 'Lenovo ThinkPad E15, Intel i7, 16GB RAM', 'Lab A-103', 'available'),
('Sony Projector 003', 'projector', 'Sony VPL-FHZ75, 7000 lumens, 4K', 'Lab B-203', 'available'),
('Rigol Oscilloscope 002', 'oscilloscope', 'Rigol DS1054Z, 50MHz, 4 channels', 'Lab C-302', 'available'),
('Agilent Multimeter 002', 'multimeter', 'Agilent 34401A Digital Multimeter', 'Lab C-302', 'available'),
('Keithley Power Supply 002', 'power_supply', 'Keithley 2230G-30-1 Triple Channel Power Supply', 'Lab C-302', 'available'),
('Leica Microscope 002', 'microscope', 'Leica DM2500 LED Research Microscope', 'Lab D-402', 'available'),
('Canon Projector 004', 'projector', 'Canon LV-WX320, 3200 lumens', 'Lab B-204', 'booked'),
('Dell Laptop 004', 'laptop', 'Dell Precision 5550, Intel i7, 32GB RAM', 'Lab A-104', 'maintenance'),
('HP Laptop 005', 'laptop', 'HP EliteBook 850 G8, Intel i5, 16GB RAM', 'Lab A-104', 'available');

-- Insert more bookings
INSERT INTO bookings (user_id, equipment_id, return_date, status) VALUES
(5, 8, DATE_ADD(NOW(), INTERVAL 5 DAY), 'active'),
(6, 1, DATE_ADD(NOW(), INTERVAL 2 DAY), 'active'),
(7, 3, DATE_ADD(NOW(), INTERVAL 10 DAY), 'active'),
(2, 4, DATE_SUB(NOW(), INTERVAL 2 DAY), 'returned'),
(3, 5, DATE_SUB(NOW(), INTERVAL 1 DAY), 'returned'),
(4, 6, DATE_SUB(NOW(), INTERVAL 3 DAY), 'returned');

-- Insert more maintenance records
INSERT INTO maintenance (equipment_id, maintenance_type, description, cost, status, technician) VALUES
(9, 'repair', 'Screen replacement and keyboard cleaning', 300.00, 'in_progress', 'Tech Support Team'),
(2, 'routine', 'Monthly cleaning and antivirus update', 30.00, 'completed', 'Lab Assistant'),
(4, 'calibration', 'Annual calibration and accuracy check', 250.00, 'pending', 'Calibration Specialist'),
(7, 'upgrade', 'RAM upgrade from 8GB to 16GB', 150.00, 'completed', 'Hardware Team'),
(10, 'cleaning', 'Deep cleaning and dust removal', 20.00, 'pending', 'Maintenance Staff');

-- Insert notifications
INSERT INTO notifications (user_id, title, message, type) VALUES
(5, 'Equipment Booking Confirmation', 'You have successfully booked Canon Projector 004. Return date: ' || DATE_ADD(NOW(), INTERVAL 5 DAY), 'booking'),
(6, 'Equipment Booking Confirmation', 'You have successfully booked Dell Laptop 001. Return date: ' || DATE_ADD(NOW(), INTERVAL 2 DAY), 'booking'),
(7, 'Equipment Booking Confirmation', 'You have successfully booked Sony Projector 003. Return date: ' || DATE_ADD(NOW(), INTERVAL 10 DAY), 'booking'),
(NULL, 'System Maintenance', 'Scheduled maintenance will be performed on Lab C-302 equipment this weekend.', 'system'),
(NULL, 'New Equipment Added', 'New MacBook Pro and Lenovo ThinkPad have been added to Lab A-103.', 'system');

-- Update some equipment statuses based on bookings
UPDATE equipment SET status = 'booked' WHERE equipment_id IN (8, 1, 3);
UPDATE equipment SET status = 'maintenance' WHERE equipment_id = 9;

-- Create some overdue bookings for testing notifications
INSERT INTO bookings (user_id, equipment_id, booking_date, return_date, status) VALUES
(2, 2, DATE_SUB(NOW(), INTERVAL 10 DAY), DATE_SUB(NOW(), INTERVAL 3 DAY), 'active'),
(3, 5, DATE_SUB(NOW(), INTERVAL 8 DAY), DATE_SUB(NOW(), INTERVAL 1 DAY), 'active');

-- Insert corresponding overdue notifications
INSERT INTO notifications (user_id, title, message, type) VALUES
(2, 'Overdue Equipment Return', 'HP Laptop 002 is overdue for return. Please return immediately.', 'overdue'),
(3, 'Overdue Equipment Return', 'Agilent Multimeter 002 is overdue for return. Please return immediately.', 'overdue');

-- Verify data insertion
SELECT 'Users' as Table_Name, COUNT(*) as Count FROM users
UNION ALL
SELECT 'Equipment', COUNT(*) FROM equipment
UNION ALL
SELECT 'Bookings', COUNT(*) FROM bookings
UNION ALL
SELECT 'Maintenance', COUNT(*) FROM maintenance
UNION ALL
SELECT 'Notifications', COUNT(*) FROM notifications;

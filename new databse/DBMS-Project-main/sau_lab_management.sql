CREATE DATABASE IF NOT EXISTS sau_lab_management CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci;
USE sau_lab_management;

-- Faculty Table
CREATE TABLE IF NOT EXISTS Faculty (
    Faculty_ID INT PRIMARY KEY AUTO_INCREMENT,
    First_Name VARCHAR(50) NOT NULL,
    Last_Name VARCHAR(50),
    Dept VARCHAR(50),
    Email VARCHAR(100) UNIQUE,
    Role VARCHAR(50)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- Faculty_Contact Table
CREATE TABLE IF NOT EXISTS Faculty_Contact (
    Contact_Number VARCHAR(15) PRIMARY KEY,
    Faculty_ID INT,
    FOREIGN KEY (Faculty_ID) REFERENCES Faculty(Faculty_ID)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- Lab Table
CREATE TABLE IF NOT EXISTS Lab (
    Lab_ID INT PRIMARY KEY AUTO_INCREMENT,
    Lab_Name VARCHAR(100),
    Location VARCHAR(100),
    Incharge_ID INT NULL,
    FOREIGN KEY (Incharge_ID) REFERENCES Faculty(Faculty_ID)
        ON DELETE SET NULL
        ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- Lab_Assistant Table
CREATE TABLE IF NOT EXISTS Lab_Assistant (
    Assistant_ID INT PRIMARY KEY AUTO_INCREMENT,
    First_Name VARCHAR(50) NOT NULL,
    Last_Name VARCHAR(50),
    Email VARCHAR(100) UNIQUE,
    Lab_ID INT NULL,
    FOREIGN KEY (Lab_ID) REFERENCES Lab(Lab_ID)
        ON DELETE SET NULL
        ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- Student Table
CREATE TABLE IF NOT EXISTS Student (
    Student_ID INT PRIMARY KEY AUTO_INCREMENT,
    First_Name VARCHAR(50) NOT NULL,
    Last_Name VARCHAR(50),
    Dept VARCHAR(50),
    Email VARCHAR(100) UNIQUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- Student_Contact Table
CREATE TABLE IF NOT EXISTS Student_Contact (
    Contact_Number VARCHAR(15) PRIMARY KEY,
    Student_ID INT,
    FOREIGN KEY (Student_ID) REFERENCES Student(Student_ID)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- Equipment Table
CREATE TABLE IF NOT EXISTS Equipment (
    Equipment_ID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(100),
    Category VARCHAR(100),
    Equipment_Condition VARCHAR(50),
    Purchase_Date DATE,
    Status VARCHAR(50),
    Lab_ID INT NULL,
    FOREIGN KEY (Lab_ID) REFERENCES Lab(Lab_ID)
        ON DELETE SET NULL
        ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- Booking Table
CREATE TABLE IF NOT EXISTS Booking (
    Booking_ID INT PRIMARY KEY AUTO_INCREMENT,
    Equipment_ID INT,
    Student_ID INT,
    Faculty_ID INT NULL,
    Booking_Date DATE NOT NULL,
    Issue_Date DATE NOT NULL,
    Return_Date DATE,
    Status VARCHAR(50),
    FOREIGN KEY (Equipment_ID) REFERENCES Equipment(Equipment_ID)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (Student_ID) REFERENCES Student(Student_ID)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (Faculty_ID) REFERENCES Faculty(Faculty_ID)
        ON DELETE SET NULL
        ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- Maintenance Table
CREATE TABLE IF NOT EXISTS Maintenance (
    Maintenance_ID INT PRIMARY KEY AUTO_INCREMENT,
    Equipment_ID INT,
    Issue_Reported_Date DATE NOT NULL,
    Fix_Date DATE,
    Issue_Description  TEXT,
    Status VARCHAR(50),
    FOREIGN KEY (Equipment_ID) REFERENCES Equipment(Equipment_ID)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

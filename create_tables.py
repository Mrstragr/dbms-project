import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

# Database configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'sau_lab_mgmt'),
    'port': int(os.getenv('DB_PORT', '3306'))
}

def create_tables():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    # Create feedback table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
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
        )
    """)

    # Create user_limitations table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_limitations (
            limitation_id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            limitation_type ENUM('booking_limit', 'overdue_penalty', 'blacklist') NOT NULL,
            description TEXT,
            active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
        )
    """)

    # Add issued_by column to bookings table if it doesn't exist
    try:
        cursor.execute("ALTER TABLE bookings ADD COLUMN issued_by INT NULL")
        cursor.execute("ALTER TABLE bookings ADD FOREIGN KEY (issued_by) REFERENCES users(user_id) ON DELETE SET NULL")
    except mysql.connector.Error as e:
        if "Duplicate column name" not in str(e):
            print(f"Error adding issued_by column: {e}")

    conn.commit()
    cursor.close()
    conn.close()
    print("Tables created successfully!")

if __name__ == "__main__":
    create_tables()

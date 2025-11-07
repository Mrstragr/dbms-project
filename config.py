# SAU Lab Management System Configuration
# Update these values according to your MySQL setup

# Database Configuration
DB_HOST = localhost
DB_USER = root
DB_PASSWORD = 
DB_NAME = sau_lab_mgmt

# Application Configuration
SECRET_KEY = your-secret-key-change-this-in-production
DEBUG = True
HOST = 0.0.0.0
PORT = 5000

# Email Configuration (for future notifications)
MAIL_SERVER = smtp.gmail.com
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = your-email@gmail.com
MAIL_PASSWORD = your-app-password

# File Upload Configuration
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
UPLOAD_FOLDER = static/uploads

# Pagination
ITEMS_PER_PAGE = 10

# Notification Settings
NOTIFICATION_RETENTION_DAYS = 30
OVERDUE_REMINDER_DAYS = 1
MAINTENANCE_REMINDER_DAYS = 7

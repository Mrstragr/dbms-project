# SAU Equipment & Lab Resource Management System

A comprehensive Flask-based web application for managing laboratory equipment, bookings, returns, and maintenance tracking.

## 🚀 Project Overview

This system efficiently manages laboratory equipment (laptops, projectors, oscilloscopes, etc.) by tracking bookings, returns, and maintenance, ensuring real-time availability with automated notifications for overdue returns and maintenance reminders.

## 👥 Team Structure

- **Ansh** - DB Designer (ER Diagram, Schema Design, Normalization)
- **Amar** - DB Administrator (Database Setup, Security, Backup)
- **Nikhil** - Application Developer (Flask App, Frontend Integration)
- **Prakash** - Query & Optimization Specialist (SQL Queries, Performance)
- **Krish** - Tester & Documentation Lead (Testing, Documentation)

## 🛠️ Technology Stack

- **Backend**: Python Flask
- **Database**: MySQL
- **Frontend**: HTML, CSS, Bootstrap 5
- **Authentication**: Flask-Login
- **Icons**: Font Awesome
- **Development**: XAMPP/MySQL Workbench

## 📋 Features

### Core Functionality
- ✅ User Authentication & Role Management
- ✅ Equipment CRUD Operations
- ✅ Equipment Booking & Return System
- ✅ Maintenance Tracking & Scheduling
- ✅ Real-time Notifications
- ✅ Overdue Return Alerts
- ✅ Maintenance Reminders
- ✅ Responsive Web Interface

### User Roles
- **Students**: Book and return equipment, view availability
- **Lab Assistants**: Manage equipment, track maintenance
- **Faculty**: Full system access, approve requests
- **Admin**: Complete system administration

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- MySQL Server
- XAMPP (recommended for local development)

### Installation

1. **Clone/Download the project**
   ```bash
   cd /Users/nikhilanand/Desktop/dbms
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Database Setup** (Amar's responsibility)
   - Start MySQL server (via XAMPP)
   - Run the database schema:
   ```sql
   mysql -u root -p < models.sql
   ```
   - Insert sample data:
   ```sql
   mysql -u root -p < sample_data.sql
   ```

4. **Configure Environment (.env)**
   - Create a `.env` file at the project root using `env.example`:
   ```bash
   cp env.example .env
   ```
   - Update values in `.env` with your MySQL credentials and secret key.

5. **Run the Application**
   ```bash
   python app.py
   ```

6. **Access the Application**
   - Open browser and go to: `http://localhost:5000`

## 🔐 Default Login Credentials

| Role | Username | Email | Password |
|------|----------|-------|----------|
| Admin | admin | admin@sau.edu | password123 |
| Student | john_doe | john.doe@sau.edu | password123 |
| Lab Assistant | jane_smith | jane.smith@sau.edu | password123 |
| Faculty | prof_wilson | prof.wilson@sau.edu | password123 |

## 📁 Project Structure

```
dbms/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── models.sql            # Database schema (Ansh)
├── sample_data.sql       # Sample data for testing
├── README.md             # This file
├── templates/            # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── signup.html
│   ├── dashboard.html
│   ├── equipment.html
│   ├── admin_equipment.html
│   ├── add_equipment.html
│   ├── edit_equipment.html
│   ├── maintenance.html
│   ├── add_maintenance.html
│   └── notifications.html
└── static/               # Static files
    ├── css/
    │   └── style.css
    └── js/
        └── main.js
```

## 🔧 Configuration

### Configuration
- The app reads settings from environment variables via `.env` (see `env.example`).
- Do not use `config.py`; it is deprecated.

### Security Settings
For production deployment:
- Set a strong `SECRET_KEY` in `.env`
- Use environment variables for sensitive data
- Implement proper user authentication
- Enable HTTPS

## 📊 Database Schema

### Main Tables
- **users**: User accounts and roles
- **equipment**: Equipment inventory
- **bookings**: Equipment booking records
- **maintenance**: Maintenance tracking
- **notifications**: System notifications

### Key Relationships
- Users can have multiple bookings (1:many)
- Equipment can have multiple bookings (1:many)
- Equipment can have multiple maintenance records (1:many)

## 🧪 Testing

### Manual Testing Checklist
- [ ] User registration and login
- [ ] Equipment booking and return
- [ ] Admin equipment management
- [ ] Maintenance record creation
- [ ] Notification system
- [ ] Role-based access control

### Test Data
The `sample_data.sql` file includes:
- Multiple user accounts with different roles
- Various equipment types
- Sample bookings and maintenance records
- Test notifications

## 🚀 Deployment

### Production Considerations
1. **Database Security**
   - Create dedicated database users
   - Implement proper access controls
   - Regular backups

2. **Application Security**
   - Use environment variables
   - Enable HTTPS
   - Implement rate limiting

3. **Performance**
   - Database indexing (already implemented)
   - Query optimization
   - Caching strategies

## 🔄 Team Workflow

1. **Ansh**: Provides ER diagram and SQL schema
2. **Amar**: Sets up database and executes schema
3. **Nikhil**: Develops Flask application
4. **Prakash**: Optimizes queries and performance
5. **Krish**: Tests all features and prepares documentation

## 📈 Future Enhancements

- [ ] Email notifications
- [ ] Mobile app integration
- [ ] Advanced reporting dashboard
- [ ] QR code equipment tracking
- [ ] Automated maintenance scheduling
- [ ] Equipment usage analytics

## 🐛 Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Check MySQL server is running
   - Verify database credentials
   - Ensure database exists

2. **Import Errors**
   - Install all requirements: `pip install -r requirements.txt`
   - Check Python version compatibility

3. **Permission Errors**
   - Ensure proper file permissions
   - Check database user privileges

## 📞 Support

For technical support or questions:
- **Database Issues**: Contact Amar (DB Administrator)
- **Application Issues**: Contact Nikhil (Application Developer)
- **Performance Issues**: Contact Prakash (Query Specialist)
- **Testing Issues**: Contact Krish (Tester)

## 📄 License

This project is developed for educational purposes as part of the SAU DBMS course.

---

**Developed with ❤️ by Team: Ansh, Amar, Nikhil, Prakash, Krish**

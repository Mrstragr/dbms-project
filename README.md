# SAU Equipment & Lab Resource Management System

A comprehensive Flask-based web application for managing laboratory equipment, bookings, returns, and maintenance tracking.

## 🚀 Project Overview

This system efficiently manages laboratory equipment (laptops, projectors, oscilloscopes, etc.) by tracking bookings, returns, and maintenance, ensuring real-time availability with automated notifications for overdue returns and maintenance reminders.

## ✨ Recent Updates (UI Polish)

### Summary
Every page now shares a consistent look and feel:
- **Design tokens**: CSS variables for the primary color, radius, shadows and spacing, plus base typography (`static/css/style.css`)
- **Navigation**: Sidebar branded "SAU Lab Resource Management" with icons, active-link highlighting and a collapsible mobile menu
- **Layout**: Consistent page container spacing and footer
- **Login / Sign Up**: Centered cards with an icon and a clean form (login uses Student / Faculty / Admin tabs)
- **Dashboards**: Stat cards with icons on the student, faculty and admin dashboards and on admin analytics
- **Status badges**: Available = green, Booked = yellow, Maintenance = red, Overdue = dark red
- **Tables & forms**: Striped/hover admin tables with aligned action buttons; consistent add/edit form layout
- **Empty states**: Friendly messages such as "No bookings yet" instead of blank tables
- **Mobile**: Responsive layouts across pages; duplicated inline styles moved into `style.css`

### Bug Fixes
- **dashboard.html**: Closed the unclosed `content` block so all templates compile
- **Flash messages**: Correct colors per category (error, success, warning, info) instead of everything non-error showing green
- **Notifications**: "Mark Read" / "Mark All Read" now send the CSRF token, so the requests are no longer rejected
- **Alerts**: Auto-hide (after 4 seconds) now applies only to flash messages; in-page notices such as account limitations stay visible
- **`showAlert()`**: Inserts alerts into the existing page container (it previously looked for a `.container` element that does not exist)
- **Templates**: `datetime` is exposed to Jinja templates, so the dashboards, admin bookings and notifications pages render when there are active or overdue bookings

### How to Update
```bash
git pull origin main
python app.py
```
No new packages and no database changes are needed.

## 🤝 Recent Contributions (14 November 2026)

The following UI, usability, and bug-fix improvements were contributed by **Amarkumar30**. These changes are included in the `main` branch.

### UI and User Experience
- Introduced shared CSS design tokens for primary colours, typography, spacing, border radii, and shadows.
- Refined the application navigation with updated branding, icons, active-link states, and a collapsible mobile sidebar.
- Standardised page spacing and the footer across the application.
- Redesigned the login and signup forms for a consistent authentication experience.
- Improved student, faculty, and admin dashboard statistic cards and analytics presentation.
- Added clearer equipment-status badges for available, booked, maintenance, and overdue states.
- Refined admin tables, maintenance pages, add/edit forms, profile and notification screens.
- Added friendly empty states and improved responsive layouts for smaller screens.
- Consolidated repeated inline styling into the shared stylesheet.

### Functional Fixes and Maintenance
- Corrected the missing Jinja template block closure in `templates/dashboard.html`.
- Exposed Python's `datetime` object to Jinja templates so date-dependent dashboard and notification views can render.
- Corrected flash-message category styling and limited the four-second auto-hide behaviour to flash alerts.
- Corrected alert insertion in the existing page layout.
- Added CSRF token handling to notification actions such as **Mark Read** and **Mark All Read**.
- Removed tracked Python `__pycache__` files from version control.

### Database and Dependency Impact
These updates are application/UI and maintenance changes. According to the update notes, they require no new Python packages and no database schema changes.

### Contributor
- **GitHub:** [Amarkumar30](https://github.com/Amarkumar30)
- **Contribution period:** 14 November 2026
- **Commit history:** [View the contributor's commits](https://github.com/Mrstragr/dbms-project/commits/main)

## 👥 Team Structure

- **Ansh** - DB Designer (ER Diagram, Schema Design, Normalization) and Backend Design
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
   cd dbms-project
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

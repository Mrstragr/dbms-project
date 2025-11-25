import os
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import CSRFProtect
from flask_wtf.csrf import CSRFError
import bcrypt
import mysql.connector
from datetime import datetime, timedelta
import json
import logging
from functools import wraps

from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-change-me')
csrf = CSRFProtect(app)

# Database configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'sau_lab_mgmt'),
    'port': int(os.getenv('DB_PORT', '3306'))
}

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, user_id, username, email, role):
        self.id = user_id
        self.username = username
        self.email = email
        self.role = role

@login_manager.user_loader
def load_user(user_id):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        user_data = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if user_data:
            return User(user_data['user_id'], user_data['username'], 
                       user_data['email'], user_data['role'])
        return None
    except Exception as e:
        print(f"Error loading user: {e}")
        return None

@app.route('/health/db')
def health_db():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchone()
        cursor.close()
        conn.close()
        return jsonify(status='ok'), 200
    except Exception as e:
        return jsonify(status='error', message=str(e)), 500

def get_db_connection():
    """Get database connection"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as e:
        print(f"Database connection error: {e}")
        return None

def admin_required(f):
    """Decorator to require admin role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('Admin access required!', 'error')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

def create_notification(user_id, title, message, notification_type, conn=None):
    """Helper function to create a notification"""
    should_close = False
    if conn is None:
        conn = get_db_connection()
        should_close = True
    
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO notifications (user_id, title, message, type, created_at)
                VALUES (%s, %s, %s, %s, %s)
            """, (user_id, title, message, notification_type, datetime.now()))
            conn.commit()
        except Exception as e:
            print(f"Error creating notification: {e}")
        finally:
            cursor.close()
            if should_close:
                conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        logger.info(f"Login attempt for email: {email}, method: {request.method}, path: {request.path}")

        conn = get_db_connection()
        if conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user_data = cursor.fetchone()
            cursor.close()
            conn.close()

            password_hash = user_data['password'] if user_data else None

            is_valid = False
            if password_hash:
                # Support bcrypt ($2b$...) hashes from seed data
                if password_hash.startswith('$2'):
                    try:
                        is_valid = bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
                    except Exception:
                        is_valid = False
                else:
                    is_valid = check_password_hash(password_hash, password)

            if user_data and is_valid:
                user = User(user_data['user_id'], user_data['username'],
                           user_data['email'], user_data['role'])
                login_user(user)
                logger.info(f"Login successful for user: {user.username} (ID: {user.id}), role: {user.role}")
                flash('Login successful!', 'success')

                # Redirect based on role
                if user.role == 'admin':
                    return redirect(url_for('admin_dashboard'))
                elif user.role == 'faculty':
                    return redirect(url_for('faculty_dashboard'))
                else:  # student and any other role
                    return redirect(url_for('student_dashboard'))
            else:
                logger.warning(f"Failed login attempt for email: {email}")
                flash('Invalid email or password!', 'error')

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            try:
                # Check if email already exists
                cursor.execute("SELECT email FROM users WHERE email = %s", (email,))
                if cursor.fetchone():
                    flash('Email already exists!', 'error')
                    return render_template('signup.html')
                
                # Insert new user
                hashed_password = generate_password_hash(password)
                cursor.execute("""
                    INSERT INTO users (username, email, password, role, created_at) 
                    VALUES (%s, %s, %s, %s, %s)
                """, (username, email, hashed_password, role, datetime.now()))
                conn.commit()
                flash('Registration successful! Please login.', 'success')
                return redirect(url_for('login'))
            except Exception as e:
                flash(f'Registration failed: {str(e)}', 'error')
            finally:
                cursor.close()
                conn.close()
    
    return render_template('signup.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    conn = get_db_connection()
    if not conn:
        flash('Database connection failed!', 'error')
        return redirect(url_for('dashboard'))
    
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        
        try:
            # Check if email is already taken by another user
            cursor.execute("SELECT user_id FROM users WHERE email = %s AND user_id != %s", 
                          (email, current_user.id))
            if cursor.fetchone():
                flash('Email already exists!', 'error')
                return redirect(url_for('profile'))
            
            # Update user profile
            cursor.execute("""
                UPDATE users 
                SET username = %s, email = %s, updated_at = %s 
                WHERE user_id = %s
            """, (username, email, datetime.now(), current_user.id))
            conn.commit()
            flash('Profile updated successfully!', 'success')
            
            # Update current_user object
            current_user.username = username
            current_user.email = email
        except Exception as e:
            flash(f'Failed to update profile: {str(e)}', 'error')
        finally:
            cursor.close()
            conn.close()
        return redirect(url_for('profile'))
    
    # GET request - show profile
    try:
        cursor.execute("SELECT * FROM users WHERE user_id = %s", (current_user.id,))
        user_data = cursor.fetchone()
        
        # Get user statistics
        cursor.execute("""
            SELECT 
                COUNT(*) as total_bookings,
                SUM(CASE WHEN status = 'active' THEN 1 ELSE 0 END) as active_bookings,
                SUM(CASE WHEN status = 'returned' THEN 1 ELSE 0 END) as returned_bookings
            FROM bookings 
            WHERE user_id = %s
        """, (current_user.id,))
        stats = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        return render_template('profile.html', user=user_data, stats=stats)
    except Exception as e:
        flash(f'Error loading profile: {str(e)}', 'error')
        cursor.close()
        conn.close()
        return redirect(url_for('dashboard'))

@app.route('/change-password', methods=['POST'])
@login_required
def change_password():
    old_password = request.form.get('old_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')
    
    if not old_password or not new_password or not confirm_password:
        flash('All password fields are required!', 'error')
        return redirect(url_for('profile'))
    
    if new_password != confirm_password:
        flash('New passwords do not match!', 'error')
        return redirect(url_for('profile'))
    
    if len(new_password) < 6:
        flash('Password must be at least 6 characters long!', 'error')
        return redirect(url_for('profile'))
    
    conn = get_db_connection()
    if not conn:
        flash('Database connection failed!', 'error')
        return redirect(url_for('profile'))
    
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT password FROM users WHERE user_id = %s", (current_user.id,))
        user_data = cursor.fetchone()
        
        if not user_data:
            flash('User not found!', 'error')
            return redirect(url_for('profile'))
        
        password_hash = user_data['password']
        
        # Check old password
        is_valid = False
        if password_hash.startswith('$2'):
            try:
                import bcrypt
                is_valid = bcrypt.checkpw(old_password.encode('utf-8'), password_hash.encode('utf-8'))
            except Exception:
                is_valid = False
        else:
            is_valid = check_password_hash(password_hash, old_password)
        
        if not is_valid:
            flash('Current password is incorrect!', 'error')
            return redirect(url_for('profile'))
        
        # Update password
        new_password_hash = generate_password_hash(new_password)
        cursor.execute("""
            UPDATE users 
            SET password = %s, updated_at = %s 
            WHERE user_id = %s
        """, (new_password_hash, datetime.now(), current_user.id))
        conn.commit()
        flash('Password changed successfully!', 'success')
    except Exception as e:
        flash(f'Failed to change password: {str(e)}', 'error')
    finally:
        cursor.close()
        conn.close()
    
    return redirect(url_for('profile'))

@app.route('/dashboard')
@login_required
def dashboard():
    # Legacy route - redirect to role-specific dashboard
    if current_user.role == 'admin':
        return redirect(url_for('admin_dashboard'))
    elif current_user.role == 'faculty':
        return redirect(url_for('faculty_dashboard'))
    else:  # student and any other role
        return redirect(url_for('student_dashboard'))

@app.route('/student/dashboard')
@login_required
def student_dashboard():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)

        # Get user's bookings with issuer details
        cursor.execute("""
            SELECT b.*, e.equipment_name, e.equipment_type, e.location,
                   u.username as issued_by_name, u.role as issued_by_role
            FROM bookings b
            JOIN equipment e ON b.equipment_id = e.equipment_id
            LEFT JOIN users u ON b.issued_by = u.user_id
            WHERE b.user_id = %s
            ORDER BY b.booking_date DESC
        """, (current_user.id,))
        user_bookings = cursor.fetchall()

        # Get available equipment
        cursor.execute("""
            SELECT * FROM equipment
            WHERE status = 'available'
            ORDER BY equipment_name
        """, ())
        available_equipment = cursor.fetchall()

        # Get user's feedback history
        cursor.execute("""
            SELECT f.*, e.equipment_name, b.booking_date
            FROM feedback f
            LEFT JOIN equipment e ON f.equipment_id = e.equipment_id
            LEFT JOIN bookings b ON f.booking_id = b.booking_id
            WHERE f.user_id = %s
            ORDER BY f.created_at DESC
        """, (current_user.id,))
        user_feedback = cursor.fetchall()

        # Get user limitations
        cursor.execute("""
            SELECT * FROM user_limitations
            WHERE user_id = %s AND active = TRUE
            ORDER BY created_at DESC
        """, (current_user.id,))
        user_limitations = cursor.fetchall()

        # Get booking statistics
        cursor.execute("""
            SELECT
                COUNT(*) as total_bookings,
                SUM(CASE WHEN status = 'active' THEN 1 ELSE 0 END) as active_bookings,
                SUM(CASE WHEN status = 'returned' THEN 1 ELSE 0 END) as returned_bookings,
                SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END) as cancelled_bookings,
                SUM(CASE WHEN status = 'active' AND return_date < NOW() THEN 1 ELSE 0 END) as overdue_bookings
            FROM bookings
            WHERE user_id = %s
        """, (current_user.id,))
        booking_stats = cursor.fetchone()

        cursor.close()
        conn.close()

        return render_template('student_dashboard.html',
                             user_bookings=user_bookings,
                             available_equipment=available_equipment,
                             user_feedback=user_feedback,
                             user_limitations=user_limitations,
                             booking_stats=booking_stats)

    return render_template('student_dashboard.html',
                         user_bookings=[],
                         available_equipment=[],
                         user_feedback=[],
                         user_limitations=[],
                         booking_stats={'total_bookings': 0, 'active_bookings': 0, 'returned_bookings': 0, 'cancelled_bookings': 0, 'overdue_bookings': 0})

@app.route('/faculty/dashboard')
@login_required
def faculty_dashboard():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)

        # Get user's bookings
        cursor.execute("""
            SELECT b.*, e.equipment_name, e.equipment_type
            FROM bookings b
            JOIN equipment e ON b.equipment_id = e.equipment_id
            WHERE b.user_id = %s
            ORDER BY b.booking_date DESC
        """, (current_user.id,))
        user_bookings = cursor.fetchall()

        # Get available equipment
        cursor.execute("""
            SELECT * FROM equipment
            WHERE status = 'available'
            ORDER BY equipment_name
        """, ())
        available_equipment = cursor.fetchall()

        # Faculty-specific stats
        cursor.execute("""
            SELECT
                COUNT(*) as total_bookings,
                SUM(CASE WHEN status = 'active' THEN 1 ELSE 0 END) as active_bookings,
                SUM(CASE WHEN status = 'returned' THEN 1 ELSE 0 END) as returned_bookings
            FROM bookings
            WHERE user_id = %s
        """, (current_user.id,))
        faculty_stats = cursor.fetchone()

        # Get maintenance records for faculty oversight
        cursor.execute("""
            SELECT m.*, e.equipment_name
            FROM maintenance m
            JOIN equipment e ON m.equipment_id = e.equipment_id
            ORDER BY m.maintenance_date DESC
            LIMIT 5
        """)
        recent_maintenance = cursor.fetchall()

        cursor.close()
        conn.close()

        return render_template('faculty_dashboard.html',
                             user_bookings=user_bookings,
                             available_equipment=available_equipment,
                             faculty_stats=faculty_stats,
                             recent_maintenance=recent_maintenance)

    return render_template('faculty_dashboard.html', user_bookings=[], available_equipment=[], faculty_stats=None, recent_maintenance=[])

@app.route('/admin/dashboard')
@login_required
@admin_required
def admin_dashboard():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)

        # Get user's bookings (admin can also book equipment)
        cursor.execute("""
            SELECT b.*, e.equipment_name, e.equipment_type
            FROM bookings b
            JOIN equipment e ON b.equipment_id = e.equipment_id
            WHERE b.user_id = %s
            ORDER BY b.booking_date DESC
        """, (current_user.id,))
        user_bookings = cursor.fetchall()

        # Get available equipment
        cursor.execute("""
            SELECT * FROM equipment
            WHERE status = 'available'
            ORDER BY equipment_name
        """, ())
        available_equipment = cursor.fetchall()

        # Admin statistics
        # Total equipment
        cursor.execute("SELECT COUNT(*) as total FROM equipment")
        total_equipment = cursor.fetchone()['total']

        # Equipment by status
        cursor.execute("""
            SELECT status, COUNT(*) as count
            FROM equipment
            GROUP BY status
        """)
        equipment_by_status = cursor.fetchall()

        # Total bookings
        cursor.execute("SELECT COUNT(*) as total FROM bookings")
        total_bookings = cursor.fetchone()['total']

        # Active bookings
        cursor.execute("SELECT COUNT(*) as active FROM bookings WHERE status = 'active'")
        active_bookings = cursor.fetchone()['active']

        # Total users
        cursor.execute("SELECT COUNT(*) as total FROM users")
        total_users = cursor.fetchone()['total']

        # Users by role
        cursor.execute("""
            SELECT role, COUNT(*) as count
            FROM users
            GROUP BY role
        """)
        users_by_role = cursor.fetchall()

        # Overdue bookings
        cursor.execute("""
            SELECT COUNT(*) as overdue
            FROM bookings
            WHERE status = 'active' AND return_date < %s
        """, (datetime.now(),))
        overdue_count = cursor.fetchone()['overdue']

        # Pending maintenance
        cursor.execute("SELECT COUNT(*) as pending FROM maintenance WHERE status = 'pending'")
        pending_maintenance = cursor.fetchone()['pending']

        # Recent activities
        cursor.execute("""
            SELECT 'booking' as type, b.booking_date as date, u.username, e.equipment_name as item
            FROM bookings b
            JOIN users u ON b.user_id = u.user_id
            JOIN equipment e ON b.equipment_id = e.equipment_id
            UNION ALL
            SELECT 'maintenance' as type, m.maintenance_date as date, 'System' as username, e.equipment_name as item
            FROM maintenance m
            JOIN equipment e ON m.equipment_id = e.equipment_id
            ORDER BY date DESC
            LIMIT 10
        """)
        recent_activities = cursor.fetchall()

        admin_stats = {
            'total_equipment': total_equipment,
            'equipment_by_status': equipment_by_status,
            'total_bookings': total_bookings,
            'active_bookings': active_bookings,
            'total_users': total_users,
            'users_by_role': users_by_role,
            'overdue_count': overdue_count,
            'pending_maintenance': pending_maintenance
        }

        cursor.close()
        conn.close()

        return render_template('admin_dashboard.html',
                             user_bookings=user_bookings,
                             available_equipment=available_equipment,
                             admin_stats=admin_stats,
                             recent_activities=recent_activities)

    return render_template('admin_dashboard.html', user_bookings=[], available_equipment=[], admin_stats=None, recent_activities=[])

@app.route('/equipment')
@login_required
def equipment_list():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM equipment ORDER BY equipment_name")
        equipment = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('equipment.html', equipment=equipment)
    
    return render_template('equipment.html', equipment=[])

@app.route('/book_equipment/<int:equipment_id>')
@login_required
def book_equipment(equipment_id):
    logger.info(f"Booking attempt for equipment ID: {equipment_id}, user: {current_user.username} (ID: {current_user.id}), method: {request.method}, path: {request.path}")

    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            # Check if equipment is available
            cursor.execute("SELECT status FROM equipment WHERE equipment_id = %s", (equipment_id,))
            result = cursor.fetchone()

            if not result or result[0] != 'available':
                logger.warning(f"Booking failed: Equipment ID {equipment_id} not available for user {current_user.username}")
                flash('Equipment not available for booking!', 'error')
                return redirect(url_for('equipment_list'))

            # Create booking
            cursor.execute("""
                INSERT INTO bookings (user_id, equipment_id, booking_date, return_date, status)
                VALUES (%s, %s, %s, %s, %s)
            """, (current_user.id, equipment_id, datetime.now(),
                  datetime.now() + timedelta(days=7), 'active'))

            # Update equipment status
            cursor.execute("UPDATE equipment SET status = 'booked' WHERE equipment_id = %s", (equipment_id,))

            # Get equipment name for notification
            cursor.execute("SELECT equipment_name FROM equipment WHERE equipment_id = %s", (equipment_id,))
            equipment = cursor.fetchone()
            equipment_name = equipment[0] if equipment else 'Equipment'

            conn.commit()

            logger.info(f"Equipment booked successfully: {equipment_name} (ID: {equipment_id}) by user {current_user.username} (ID: {current_user.id})")

            # Create notification
            create_notification(
                current_user.id,
                'Equipment Booked Successfully',
                f'You have successfully booked {equipment_name}. Return date: {(datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")}',
                'booking',
                conn
            )

            flash('Equipment booked successfully!', 'success')
        except Exception as e:
            logger.error(f"Booking failed for equipment ID {equipment_id} by user {current_user.username}: {str(e)}")
            flash(f'Booking failed: {str(e)}', 'error')
        finally:
            cursor.close()
            conn.close()

    return redirect(url_for('dashboard'))

@app.route('/return_equipment/<int:booking_id>')
@login_required
def return_equipment(booking_id):
    logger.info(f"Return attempt for booking ID: {booking_id}, user: {current_user.username} (ID: {current_user.id}), method: {request.method}, path: {request.path}")

    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            # Get booking details
            cursor.execute("SELECT equipment_id FROM bookings WHERE booking_id = %s AND user_id = %s",
                          (booking_id, current_user.id))
            result = cursor.fetchone()

            if not result:
                logger.warning(f"Return failed: Booking ID {booking_id} not found for user {current_user.username}")
                flash('Booking not found!', 'error')
                return redirect(url_for('dashboard'))

            equipment_id = result[0]

            # Update booking status
            cursor.execute("""
                UPDATE bookings
                SET status = 'returned', actual_return_date = %s
                WHERE booking_id = %s
            """, (datetime.now(), booking_id))

            # Update equipment status
            cursor.execute("UPDATE equipment SET status = 'available' WHERE equipment_id = %s", (equipment_id,))

            # Get equipment name for notification
            cursor.execute("SELECT equipment_name FROM equipment WHERE equipment_id = %s", (equipment_id,))
            equipment = cursor.fetchone()
            equipment_name = equipment[0] if equipment else 'Equipment'

            conn.commit()

            logger.info(f"Equipment returned successfully: {equipment_name} (ID: {equipment_id}) by user {current_user.username} (ID: {current_user.id})")

            # Create notification
            create_notification(
                current_user.id,
                'Equipment Returned',
                f'You have successfully returned {equipment_name}.',
                'return',
                conn
            )

            flash('Equipment returned successfully!', 'success')
        except Exception as e:
            logger.error(f"Return failed for booking ID {booking_id} by user {current_user.username}: {str(e)}")
            flash(f'Return failed: {str(e)}', 'error')
        finally:
            cursor.close()
            conn.close()

    return redirect(url_for('dashboard'))

@app.route('/cancel_booking/<int:booking_id>')
@login_required
def cancel_booking(booking_id):
    logger.info(f"Cancellation attempt for booking ID: {booking_id}, user: {current_user.username} (ID: {current_user.id}), method: {request.method}, path: {request.path}")

    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            # Get booking details
            cursor.execute("SELECT equipment_id FROM bookings WHERE booking_id = %s AND user_id = %s AND status = 'active'",
                          (booking_id, current_user.id))
            result = cursor.fetchone()

            if not result:
                logger.warning(f"Cancellation failed: Booking ID {booking_id} not found or not active for user {current_user.username}")
                flash('Booking not found or cannot be cancelled!', 'error')
                return redirect(url_for('dashboard'))

            equipment_id = result[0]

            # Update booking status
            cursor.execute("""
                UPDATE bookings
                SET status = 'cancelled', updated_at = %s
                WHERE booking_id = %s
            """, (datetime.now(), booking_id))

            # Update equipment status back to available
            cursor.execute("UPDATE equipment SET status = 'available' WHERE equipment_id = %s", (equipment_id,))

            # Get equipment name for notification
            cursor.execute("SELECT equipment_name FROM equipment WHERE equipment_id = %s", (equipment_id,))
            equipment = cursor.fetchone()
            equipment_name = equipment[0] if equipment else 'Equipment'

            conn.commit()

            logger.info(f"Booking cancelled successfully: {equipment_name} (ID: {equipment_id}) by user {current_user.username} (ID: {current_user.id})")

            # Create notification
            create_notification(
                current_user.id,
                'Booking Cancelled',
                f'Your booking for {equipment_name} has been cancelled.',
                'booking',
                conn
            )

            flash('Booking cancelled successfully!', 'success')
        except Exception as e:
            logger.error(f"Cancellation failed for booking ID {booking_id} by user {current_user.username}: {str(e)}")
            flash(f'Cancellation failed: {str(e)}', 'error')
        finally:
            cursor.close()
            conn.close()

    return redirect(url_for('dashboard'))

@app.route('/admin/bookings')
@login_required
@admin_required
def admin_bookings():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        
        # Get all bookings with user and equipment info
        cursor.execute("""
            SELECT b.*, u.username, u.email, u.role, 
                   e.equipment_name, e.equipment_type, e.location
            FROM bookings b
            JOIN users u ON b.user_id = u.user_id
            JOIN equipment e ON b.equipment_id = e.equipment_id
            ORDER BY b.booking_date DESC
        """)
        all_bookings = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return render_template('admin_bookings.html', bookings=all_bookings)
    
    return render_template('admin_bookings.html', bookings=[])

@app.route('/admin/equipment')
@login_required
@admin_required
def admin_equipment():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM equipment ORDER BY equipment_name")
        equipment = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('admin_equipment.html', equipment=equipment)
    
    return render_template('admin_equipment.html', equipment=[])

@app.route('/admin/add_equipment', methods=['GET', 'POST'])
@login_required
@admin_required
def add_equipment():
    if request.method == 'POST':
        equipment_name = request.form['equipment_name']
        equipment_type = request.form['equipment_type']
        description = request.form['description']
        location = request.form['location']
        
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    INSERT INTO equipment (equipment_name, equipment_type, description, location, status) 
                    VALUES (%s, %s, %s, %s, %s)
                """, (equipment_name, equipment_type, description, location, 'available'))
                conn.commit()
                flash('Equipment added successfully!', 'success')
                return redirect(url_for('admin_equipment'))
            except Exception as e:
                flash(f'Failed to add equipment: {str(e)}', 'error')
            finally:
                cursor.close()
                conn.close()
    
    return render_template('add_equipment.html')

@app.route('/admin/edit_equipment/<int:equipment_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_equipment(equipment_id):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        
        if request.method == 'POST':
            equipment_name = request.form['equipment_name']
            equipment_type = request.form['equipment_type']
            description = request.form['description']
            location = request.form['location']
            status = request.form['status']
            
            try:
                cursor.execute("""
                    UPDATE equipment 
                    SET equipment_name = %s, equipment_type = %s, description = %s, 
                        location = %s, status = %s 
                    WHERE equipment_id = %s
                """, (equipment_name, equipment_type, description, location, status, equipment_id))
                conn.commit()
                flash('Equipment updated successfully!', 'success')
                return redirect(url_for('admin_equipment'))
            except Exception as e:
                flash(f'Failed to update equipment: {str(e)}', 'error')
        
        # Get equipment details for editing
        cursor.execute("SELECT * FROM equipment WHERE equipment_id = %s", (equipment_id,))
        equipment = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if equipment:
            return render_template('edit_equipment.html', equipment=equipment)
    
    flash('Equipment not found!', 'error')
    return redirect(url_for('admin_equipment'))

@app.route('/admin/delete_equipment/<int:equipment_id>', methods=['POST'])
@login_required
@admin_required
def delete_equipment(equipment_id):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        try:
            # Check if equipment has active bookings
            cursor.execute("""
                SELECT COUNT(*) as count FROM bookings 
                WHERE equipment_id = %s AND status = 'active'
            """, (equipment_id,))
            result = cursor.fetchone()
            
            if result['count'] > 0:
                flash('Cannot delete equipment with active bookings!', 'error')
                return redirect(url_for('admin_equipment'))
            
            # Get equipment name for flash message
            cursor.execute("SELECT equipment_name FROM equipment WHERE equipment_id = %s", (equipment_id,))
            equipment = cursor.fetchone()
            
            # Delete equipment
            cursor.execute("DELETE FROM equipment WHERE equipment_id = %s", (equipment_id,))
            conn.commit()
            
            if equipment:
                flash(f"Equipment '{equipment['equipment_name']}' deleted successfully!", 'success')
            else:
                flash('Equipment deleted successfully!', 'success')
        except Exception as e:
            flash(f'Failed to delete equipment: {str(e)}', 'error')
        finally:
            cursor.close()
            conn.close()
    
    return redirect(url_for('admin_equipment'))

@app.route('/equipment/<int:equipment_id>')
@login_required
def equipment_details(equipment_id):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        
        # Get equipment details
        cursor.execute("SELECT * FROM equipment WHERE equipment_id = %s", (equipment_id,))
        equipment = cursor.fetchone()
        
        if not equipment:
            flash('Equipment not found!', 'error')
            return redirect(url_for('equipment_list'))
        
        # Get booking history for this equipment
        cursor.execute("""
            SELECT b.*, u.username, u.email 
            FROM bookings b 
            JOIN users u ON b.user_id = u.user_id 
            WHERE b.equipment_id = %s 
            ORDER BY b.booking_date DESC 
            LIMIT 10
        """, (equipment_id,))
        booking_history = cursor.fetchall()
        
        # Get maintenance history
        cursor.execute("""
            SELECT * FROM maintenance 
            WHERE equipment_id = %s 
            ORDER BY maintenance_date DESC 
            LIMIT 10
        """, (equipment_id,))
        maintenance_history = cursor.fetchall()
        
        # Get statistics
        cursor.execute("""
            SELECT 
                COUNT(*) as total_bookings,
                SUM(CASE WHEN status = 'active' THEN 1 ELSE 0 END) as active_bookings,
                SUM(CASE WHEN status = 'returned' THEN 1 ELSE 0 END) as returned_bookings
            FROM bookings 
            WHERE equipment_id = %s
        """, (equipment_id,))
        stats = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        return render_template('equipment_details.html', 
                             equipment=equipment, 
                             booking_history=booking_history,
                             maintenance_history=maintenance_history,
                             stats=stats)
    
    return redirect(url_for('equipment_list'))

@app.route('/maintenance')
@login_required
def maintenance():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT m.*, e.equipment_name 
            FROM maintenance m 
            JOIN equipment e ON m.equipment_id = e.equipment_id 
            ORDER BY m.maintenance_date DESC
        """)
        maintenance_records = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('maintenance.html', maintenance_records=maintenance_records)
    
    return render_template('maintenance.html', maintenance_records=[])

@app.route('/add_maintenance', methods=['GET', 'POST'])
@login_required
def add_maintenance():
    if request.method == 'POST':
        equipment_id = request.form['equipment_id']
        maintenance_type = request.form['maintenance_type']
        description = request.form['description']
        cost = request.form['cost']
        
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    INSERT INTO maintenance (equipment_id, maintenance_type, description, cost, maintenance_date) 
                    VALUES (%s, %s, %s, %s, %s)
                """, (equipment_id, maintenance_type, description, cost, datetime.now()))
                conn.commit()
                flash('Maintenance record added successfully!', 'success')
                return redirect(url_for('maintenance'))
            except Exception as e:
                flash(f'Failed to add maintenance record: {str(e)}', 'error')
            finally:
                cursor.close()
                conn.close()
    
    # Get equipment list for dropdown
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT equipment_id, equipment_name FROM equipment ORDER BY equipment_name")
        equipment = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('add_maintenance.html', equipment=equipment)
    
    return render_template('add_maintenance.html', equipment=[])

@app.route('/edit_maintenance/<int:maintenance_id>', methods=['GET', 'POST'])
@login_required
def edit_maintenance(maintenance_id):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        
        if request.method == 'POST':
            maintenance_type = request.form['maintenance_type']
            description = request.form['description']
            cost = request.form['cost']
            status = request.form['status']
            
            try:
                cursor.execute("""
                    UPDATE maintenance 
                    SET maintenance_type = %s, description = %s, cost = %s, status = %s, updated_at = %s 
                    WHERE maintenance_id = %s
                """, (maintenance_type, description, cost, status, datetime.now(), maintenance_id))
                conn.commit()
                flash('Maintenance record updated successfully!', 'success')
                return redirect(url_for('maintenance'))
            except Exception as e:
                flash(f'Failed to update maintenance record: {str(e)}', 'error')
        
        # GET request - show edit form
        cursor.execute("SELECT * FROM maintenance WHERE maintenance_id = %s", (maintenance_id,))
        maintenance = cursor.fetchone()
        
        if not maintenance:
            flash('Maintenance record not found!', 'error')
            return redirect(url_for('maintenance'))
        
        # Get equipment list
        cursor.execute("SELECT equipment_id, equipment_name FROM equipment ORDER BY equipment_name")
        equipment = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return render_template('edit_maintenance.html', maintenance=maintenance, equipment=equipment)
    
    return redirect(url_for('maintenance'))

@app.route('/delete_maintenance/<int:maintenance_id>', methods=['POST'])
@login_required
def delete_maintenance(maintenance_id):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM maintenance WHERE maintenance_id = %s", (maintenance_id,))
            conn.commit()
            flash('Maintenance record deleted successfully!', 'success')
        except Exception as e:
            flash(f'Failed to delete maintenance record: {str(e)}', 'error')
        finally:
            cursor.close()
            conn.close()
    
    return redirect(url_for('maintenance'))

@app.route('/admin/users')
@login_required
@admin_required
def admin_users():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT u.*, 
                   COUNT(b.booking_id) as total_bookings,
                   SUM(CASE WHEN b.status = 'active' THEN 1 ELSE 0 END) as active_bookings
            FROM users u
            LEFT JOIN bookings b ON u.user_id = b.user_id
            GROUP BY u.user_id
            ORDER BY u.created_at DESC
        """)
        users = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('admin_users.html', users=users)
    
    return render_template('admin_users.html', users=[])

@app.route('/admin/edit_user/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def edit_user(user_id):
    if user_id == current_user.id:
        flash('You cannot edit your own account from here!', 'error')
        return redirect(url_for('admin_users'))
    
    username = request.form.get('username')
    email = request.form.get('email')
    role = request.form.get('role')
    
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        try:
            # Check if email is taken by another user
            cursor.execute("SELECT user_id FROM users WHERE email = %s AND user_id != %s", (email, user_id))
            if cursor.fetchone():
                flash('Email already exists!', 'error')
                return redirect(url_for('admin_users'))
            
            cursor.execute("""
                UPDATE users 
                SET username = %s, email = %s, role = %s, updated_at = %s 
                WHERE user_id = %s
            """, (username, email, role, datetime.now(), user_id))
            conn.commit()
            flash('User updated successfully!', 'success')
        except Exception as e:
            flash(f'Failed to update user: {str(e)}', 'error')
        finally:
            cursor.close()
            conn.close()
    
    return redirect(url_for('admin_users'))

@app.route('/admin/delete_user/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    if user_id == current_user.id:
        flash('You cannot delete your own account!', 'error')
        return redirect(url_for('admin_users'))
    
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        try:
            # Check for active bookings
            cursor.execute("""
                SELECT COUNT(*) as count FROM bookings 
                WHERE user_id = %s AND status = 'active'
            """, (user_id,))
            result = cursor.fetchone()
            
            if result['count'] > 0:
                flash('Cannot delete user with active bookings!', 'error')
                return redirect(url_for('admin_users'))
            
            cursor.execute("SELECT username FROM users WHERE user_id = %s", (user_id,))
            user = cursor.fetchone()
            
            cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
            conn.commit()
            
            if user:
                flash(f"User '{user['username']}' deleted successfully!", 'success')
        except Exception as e:
            flash(f'Failed to delete user: {str(e)}', 'error')
        finally:
            cursor.close()
            conn.close()
    
    return redirect(url_for('admin_users'))

@app.route('/notifications')
@login_required
def notifications():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        
        # Get user notifications from notifications table
        cursor.execute("""
            SELECT * FROM notifications 
            WHERE user_id = %s OR user_id IS NULL
            ORDER BY created_at DESC
            LIMIT 50
        """, (current_user.id,))
        notifications_list = cursor.fetchall()
        
        # Get overdue bookings (for admin/system notifications)
        cursor.execute("""
            SELECT b.*, e.equipment_name, u.username 
            FROM bookings b 
            JOIN equipment e ON b.equipment_id = e.equipment_id 
            JOIN users u ON b.user_id = u.user_id 
            WHERE b.status = 'active' AND b.return_date < %s
        """, (datetime.now(),))
        overdue_bookings = cursor.fetchall()
        
        # Get maintenance reminders
        cursor.execute("""
            SELECT e.equipment_name, m.maintenance_date, m.description 
            FROM maintenance m 
            JOIN equipment e ON m.equipment_id = e.equipment_id 
            WHERE m.maintenance_date <= %s AND m.status = 'pending'
        """, (datetime.now() + timedelta(days=7),))
        maintenance_reminders = cursor.fetchall()
        
        # Get unread count
        cursor.execute("""
            SELECT COUNT(*) as unread_count FROM notifications 
            WHERE (user_id = %s OR user_id IS NULL) AND is_read = FALSE
        """, (current_user.id,))
        unread_count = cursor.fetchone()['unread_count']
        
        cursor.close()
        conn.close()
        
        return render_template('notifications.html', 
                             notifications=notifications_list,
                             overdue_bookings=overdue_bookings,
                             maintenance_reminders=maintenance_reminders,
                             unread_count=unread_count)
    
    return render_template('notifications.html', notifications=[], overdue_bookings=[], maintenance_reminders=[], unread_count=0)

@app.route('/notifications/mark_read/<int:notification_id>', methods=['POST'])
@login_required
def mark_notification_read(notification_id):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE notifications 
                SET is_read = TRUE 
                WHERE notification_id = %s AND (user_id = %s OR user_id IS NULL)
            """, (notification_id, current_user.id))
            conn.commit()
            return jsonify(success=True)
        except Exception as e:
            return jsonify(success=False, error=str(e)), 500
        finally:
            cursor.close()
            conn.close()
    return jsonify(success=False, error='Database connection failed'), 500

@app.route('/notifications/mark_all_read', methods=['POST'])
@login_required
def mark_all_notifications_read():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE notifications 
                SET is_read = TRUE 
                WHERE (user_id = %s OR user_id IS NULL) AND is_read = FALSE
            """, (current_user.id,))
            conn.commit()
            return jsonify(success=True)
        except Exception as e:
            return jsonify(success=False, error=str(e)), 500
        finally:
            cursor.close()
            conn.close()
    return jsonify(success=False, error='Database connection failed'), 500

@app.route('/api/notifications/unread_count')
@login_required
def unread_notifications_count():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT COUNT(*) as count FROM notifications
                WHERE (user_id = %s OR user_id IS NULL) AND is_read = FALSE
            """, (current_user.id,))
            result = cursor.fetchone()
            return jsonify(count=result['count'])
        except Exception as e:
            return jsonify(count=0, error=str(e)), 500
        finally:
            cursor.close()
            conn.close()
    return jsonify(count=0)

@app.route('/submit_feedback', methods=['POST'])
@login_required
def submit_feedback():
    booking_id = request.form.get('booking_id')
    equipment_id = request.form.get('equipment_id')
    rating = request.form.get('rating')
    feedback_type = request.form.get('feedback_type')
    comments = request.form.get('comments')

    if not rating or not feedback_type:
        flash('Rating and feedback type are required!', 'error')
        return redirect(url_for('student_dashboard'))

    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO feedback (user_id, booking_id, equipment_id, rating, comments, feedback_type)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (current_user.id, booking_id or None, equipment_id or None, rating, comments, feedback_type))
            conn.commit()
            flash('Feedback submitted successfully!', 'success')
        except Exception as e:
            flash(f'Failed to submit feedback: {str(e)}', 'error')
        finally:
            cursor.close()
            conn.close()

    return redirect(url_for('student_dashboard'))

@app.route('/admin/manage_limitations/<int:user_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def manage_limitations(user_id):
    conn = get_db_connection()
    if not conn:
        flash('Database connection failed!', 'error')
        return redirect(url_for('admin_users'))

    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        limitation_type = request.form.get('limitation_type')
        description = request.form.get('description')
        active = request.form.get('active') == 'on'

        try:
            cursor.execute("""
                INSERT INTO user_limitations (user_id, limitation_type, description, active)
                VALUES (%s, %s, %s, %s)
            """, (user_id, limitation_type, description, active))
            conn.commit()
            flash('Limitation added successfully!', 'success')
        except Exception as e:
            flash(f'Failed to add limitation: {str(e)}', 'error')

    # Get user info
    cursor.execute("SELECT username FROM users WHERE user_id = %s", (user_id,))
    user = cursor.fetchone()

    # Get existing limitations
    cursor.execute("""
        SELECT * FROM user_limitations
        WHERE user_id = %s
        ORDER BY created_at DESC
    """, (user_id,))
    limitations = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('manage_limitations.html', user=user, limitations=limitations)

@app.route('/admin/remove_limitation/<int:limitation_id>', methods=['POST'])
@login_required
@admin_required
def remove_limitation(limitation_id):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM user_limitations WHERE limitation_id = %s", (limitation_id,))
            conn.commit()
            flash('Limitation removed successfully!', 'success')
        except Exception as e:
            flash(f'Failed to remove limitation: {str(e)}', 'error')
        finally:
            cursor.close()
            conn.close()

    return redirect(request.referrer or url_for('admin_users'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)

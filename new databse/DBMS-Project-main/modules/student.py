from mysql.connector import Error

# ============================
#  ADD STUDENT (supports multiple contacts)
# ============================
def add_student(con):
    if con is None:
        print("❌ Connection not established!")
        return
    try:
        cursor = con.cursor()

        print("\n=== Add New Student ===")
        first_name = input("First Name: ").strip()
        last_name = input("Last Name (optional): ").strip() or None
        dept = input("Department: ").strip()
        email = input("Email: ").strip()

        # Insert into Student table
        cursor.execute("""
            INSERT INTO Student (First_Name, Last_Name, Dept, Email)
            VALUES (%s, %s, %s, %s)
        """, (first_name, last_name, dept, email))
        student_id = cursor.lastrowid

        # Handle multiple contacts (comma-separated)
        print("\nEnter contact numbers (comma-separated if multiple):")
        contacts_input = input("Contacts: ").strip()
        if contacts_input:
            contacts = [c.strip() for c in contacts_input.split(",") if c.strip()]
            for contact in contacts:
                cursor.execute("""
                    INSERT INTO Student_Contact (Contact_Number, Student_ID)
                    VALUES (%s, %s)
                """, (contact, student_id))

        con.commit()
        print("✅ Student added successfully with contact number(s)!")

    except Error as e:
        print(f"❌ Error adding student: {e}")
        con.rollback()

    finally:
        cursor.close()


# ============================
#  VIEW ALL STUDENTS (shows multiple contacts)
# ============================
def view_all_students(con):
    if con is None:
        print("❌ Connection not established!")
        return
    try:
        cursor = con.cursor()
        cursor.execute("""
            SELECT s.Student_ID, CONCAT(s.First_Name, ' ', IFNULL(s.Last_Name, '')) AS Name,
                   s.Dept, s.Email,
                   GROUP_CONCAT(sc.Contact_Number SEPARATOR ', ') AS Contacts
            FROM Student s
            LEFT JOIN Student_Contact sc ON s.Student_ID = sc.Student_ID
            GROUP BY s.Student_ID
            ORDER BY s.Student_ID
        """)
        rows = cursor.fetchall()
        print("\n=== All Students ===")
        if rows:
            for row in rows:
                contacts = row[4] if row[4] else "—"
                print(f"ID: {row[0]} | Name: {row[1]} | Dept: {row[2]} | Email: {row[3]} | Contacts: {contacts}")
        else:
            print("No student records found.")

    except Error as e:
        print(f"❌ Error retrieving students: {e}")

    finally:
        cursor.close()


# ============================
#  UPDATE STUDENT
# ============================
def update_student(con):
    if con is None:
        print("❌ Connection not established!")
        return
    try:
        cursor = con.cursor()
        student_id = input("Enter Student ID to update: ").strip()

        print("Enter new details (leave blank to keep unchanged):")
        dept = input("New Department: ").strip()
        email = input("New Email: ").strip()
        new_contacts_input = input("New Contact Numbers (comma-separated, leave blank to skip): ").strip()

        # Update Student fields
        if dept:
            cursor.execute("UPDATE Student SET Dept = %s WHERE Student_ID = %s", (dept, student_id))
        if email:
            cursor.execute("UPDATE Student SET Email = %s WHERE Student_ID = %s", (email, student_id))

        # Update contacts if provided
        if new_contacts_input:
            cursor.execute("DELETE FROM Student_Contact WHERE Student_ID = %s", (student_id,))
            new_contacts = [c.strip() for c in new_contacts_input.split(",") if c.strip()]
            for contact in new_contacts:
                cursor.execute("""
                    INSERT INTO Student_Contact (Contact_Number, Student_ID)
                    VALUES (%s, %s)
                """, (contact, student_id))

        con.commit()
        print("✅ Student updated successfully!")

    except Error as e:
        print(f"❌ Error updating student: {e}")
        con.rollback()

    finally:
        cursor.close()


# ============================
#  DELETE STUDENT
# ============================
def delete_student(con):
    if con is None:
        print("❌ Connection not established!")
        return
    try:
        cursor = con.cursor()
        student_id = input("Enter Student ID to delete: ").strip()

        cursor.execute("DELETE FROM Student WHERE Student_ID = %s", (student_id,))
        con.commit()

        if cursor.rowcount > 0:
            print("✅ Student deleted successfully!")
        else:
            print("No student found with that ID.")

    except Error as e:
        print(f"❌ Error deleting student: {e}")
        con.rollback()

    finally:
        cursor.close()


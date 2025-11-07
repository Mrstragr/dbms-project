from mysql.connector import Error

# ============================
#  ADD FACULTY (supports multiple contacts)
# ============================
def add_faculty(con):
    if con is None:
        print("❌ Connection not established!")
        return
    try:
        cursor = con.cursor()

        print("\n=== Add New Faculty ===")
        first_name = input("First Name: ").strip()
        last_name = input("Last Name (optional): ").strip() or None
        dept = input("Department: ").strip()
        email = input("Email: ").strip()
        role = input("Role: ").strip()

        # Insert into Faculty table
        cursor.execute("""
            INSERT INTO Faculty (First_Name, Last_Name, Dept, Email, Role)
            VALUES (%s, %s, %s, %s, %s)
        """, (first_name, last_name, dept, email, role))
        faculty_id = cursor.lastrowid

        # Handle multiple contacts
        print("\nEnter contact numbers (comma-separated if multiple):")
        contacts_input = input("Contacts: ").strip()
        if contacts_input:
            contacts = [c.strip() for c in contacts_input.split(",") if c.strip()]
            for contact in contacts:
                cursor.execute("""
                    INSERT INTO Faculty_Contact (Contact_Number, Faculty_ID)
                    VALUES (%s, %s)
                """, (contact, faculty_id))

        con.commit()
        print("✅ Faculty added successfully with contact number(s)!")

    except Error as e:
        print(f"❌ Error adding faculty: {e}")
        con.rollback()

    finally:
        cursor.close()


# ============================
#  VIEW ALL FACULTY (shows multiple contacts)
# ============================
def view_all_faculty(con):
    if con is None:
        print("❌ Connection not established!")
        return
    try:
        cursor = con.cursor()
        cursor.execute("""
            SELECT f.Faculty_ID, CONCAT(f.First_Name, ' ', IFNULL(f.Last_Name, '')) AS Name,
                   f.Dept, f.Email, f.Role,
                   GROUP_CONCAT(fc.Contact_Number SEPARATOR ', ')
            FROM Faculty f
            LEFT JOIN Faculty_Contact fc ON f.Faculty_ID = fc.Faculty_ID
            GROUP BY f.Faculty_ID
            ORDER BY f.Faculty_ID
        """)
        rows = cursor.fetchall()
        print("\n=== All Faculty ===")
        if rows:
            for row in rows:
                contacts = row[5] if row[5] else "—"
                print(f"ID: {row[0]} | Name: {row[1]} | Dept: {row[2]} | Email: {row[3]} | Role: {row[4]} | Contacts: {contacts}")
        else:
            print("No faculty records found.")

    except Error as e:
        print(f"❌ Error retrieving faculty: {e}")

    finally:
        cursor.close()


# ============================
#  UPDATE FACULTY
# ============================
def update_faculty(con):
    if con is None:
        print("❌ Connection not established!")
        return
    try:
        cursor = con.cursor()
        faculty_id = input("Enter Faculty ID to update: ").strip()

        print("Enter new details (leave blank to keep unchanged):")
        dept = input("New Department: ").strip()
        role = input("New Role: ").strip()
        new_contacts_input = input("New Contact Numbers (comma-separated, leave blank to skip): ").strip()

        if dept:
            cursor.execute("UPDATE Faculty SET Dept = %s WHERE Faculty_ID = %s", (dept, faculty_id))
        if role:
            cursor.execute("UPDATE Faculty SET Role = %s WHERE Faculty_ID = %s", (role, faculty_id))

        if new_contacts_input:
            # Remove old contacts and add new ones
            cursor.execute("DELETE FROM Faculty_Contact WHERE Faculty_ID = %s", (faculty_id,))
            new_contacts = [c.strip() for c in new_contacts_input.split(",") if c.strip()]
            for contact in new_contacts:
                cursor.execute("""
                    INSERT INTO Faculty_Contact (Contact_Number, Faculty_ID)
                    VALUES (%s, %s)
                """, (contact, faculty_id))

        con.commit()
        print("✅ Faculty updated successfully!")

    except Error as e:
        print(f"❌ Error updating faculty: {e}")
        con.rollback()

    finally:
        cursor.close()


# ============================
#  DELETE FACULTY
# ============================
def delete_faculty(con):
    if con is None:
        print("❌ Connection not established!")
        return
    try:
        cursor = con.cursor()
        faculty_id = input("Enter Faculty ID to delete: ").strip()

        cursor.execute("DELETE FROM Faculty WHERE Faculty_ID = %s", (faculty_id,))
        con.commit()

        if cursor.rowcount > 0:
            print("✅ Faculty deleted successfully!")
        else:
            print("No faculty found with that ID.")

    except Error as e:
        print(f"❌ Error deleting faculty: {e}")
        con.rollback()

    finally:
        cursor.close()

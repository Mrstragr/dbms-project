from mysql.connector import Error
from datetime import date

# ============================
#  ADD BOOKING 
# ============================
def add_booking(con):
    if con is None:
        print("❌ Connection not established!")
        return

    try:
        cursor = con.cursor()

        print("\n=== Add New Booking ===")

        # ---------- SHOW AVAILABLE EQUIPMENT ----------
        cursor.execute("""
            SELECT Equipment_ID, Name, Type, Status 
            FROM Equipment 
            WHERE Status = 'Available'
            ORDER BY Equipment_ID
        """)
        available = cursor.fetchall()

        if available:
            print("\nAvailable Equipment:")
            print("ID | Name | Type | Status")
            print("-----------------------------------------")
            for eq in available:
                print(f"{eq[0]} | {eq[1]} | {eq[2]} | {eq[3]}")
        else:
            print("No equipment currently available for booking!")
            return

        # ---------- TAKE INPUT ----------
        equipment_id = input("\nEnter Equipment ID to book: ").strip()
        student_id = input("Student ID: ").strip()
        faculty_id = input("Faculty ID (optional): ").strip() or None
        booking_date = date.today()
        issue_date = input("Issue Date (YYYY-MM-DD): ").strip()
        return_date = input("Expected Return Date (YYYY-MM-DD): ").strip() or None
        status = "Booked"

        # ---------- VALIDATION ----------
        # Check if Equipment exists
        cursor.execute("SELECT Name FROM Equipment WHERE Equipment_ID = %s", (equipment_id,))
        equipment = cursor.fetchone()
        if not equipment:
            print("❌ Invalid Equipment ID!")
            return

        # Check if Student exists
        cursor.execute("SELECT First_Name FROM Student WHERE Student_ID = %s", (student_id,))
        student = cursor.fetchone()
        if not student:
            print("❌ Invalid Student ID!")
            return

        # Check if Faculty exists (optional)
        if faculty_id:
            cursor.execute("SELECT First_Name FROM Faculty WHERE Faculty_ID = %s", (faculty_id,))
            faculty = cursor.fetchone()
            if not faculty:
                print("❌ Invalid Faculty ID!")
                return

        # Check if Equipment is already booked and not returned
        cursor.execute("""
            SELECT Booking_ID FROM Booking
            WHERE Equipment_ID = %s AND Status IN ('Booked', 'Issued')
        """, (equipment_id,))
        active_booking = cursor.fetchone()
        if active_booking:
            print(f"⚠️ Equipment ID {equipment_id} is already booked or issued! Cannot proceed.")
            return

        # ---------- INSERT BOOKING ----------
        cursor.execute("""
            INSERT INTO Booking (Equipment_ID, Student_ID, Faculty_ID, Booking_Date, Issue_Date, Return_Date, Status)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (equipment_id, student_id, faculty_id, booking_date, issue_date, return_date, status))

        # Update equipment status to 'Unavailable'
        cursor.execute("""
            UPDATE Equipment SET Status = 'Unavailable'
            WHERE Equipment_ID = %s
        """, (equipment_id,))

        con.commit()
        print(f"✅ Booking added successfully for Equipment: {equipment[0]} (ID {equipment_id})")

    except Error as e:
        print(f"❌ Error adding booking: {e}")
        con.rollback()

    finally:
        cursor.close()


# ============================
#  VIEW ALL BOOKINGS
# ============================
def view_all_bookings(con):
    if con is None:
        print("❌ Connection not established!")
        return

    try:
        cursor = con.cursor()
        cursor.execute("""
            SELECT 
                b.Booking_ID,
                e.Equipment_ID,
                e.Name AS Equipment_Name,
                CONCAT(s.First_Name, ' ', IFNULL(s.Last_Name, '')) AS Student_Name,
                CONCAT(f.First_Name, ' ', IFNULL(f.Last_Name, '')) AS Faculty_Name,
                b.Booking_Date, b.Issue_Date, b.Return_Date, b.Status
            FROM Booking b
            JOIN Equipment e ON b.Equipment_ID = e.Equipment_ID
            JOIN Student s ON b.Student_ID = s.Student_ID
            LEFT JOIN Faculty f ON b.Faculty_ID = f.Faculty_ID
            ORDER BY b.Booking_ID DESC
        """)

        rows = cursor.fetchall()
        print("\n=== All Bookings ===")
        if rows:
            for row in rows:
                print(f"""
Booking ID   : {row[0]}
Equipment     : {row[2]} (ID: {row[1]})
Student       : {row[3]}
Faculty       : {row[4] if row[4] else "—"}
Booking Date  : {row[5]}
Issue Date    : {row[6]}
Return Date   : {row[7] if row[7] else "—"}
Status        : {row[8]}
-----------------------------------------
                """)
        else:
            print("No booking records found.")

    except Error as e:
        print(f"❌ Error retrieving bookings: {e}")

    finally:
        cursor.close()


# ============================
#  UPDATE BOOKING
# ============================
def update_booking(con):
    if con is None:
        print("❌ Connection not established!")
        return

    try:
        cursor = con.cursor()
        booking_id = input("Enter Booking ID to update: ").strip()

        cursor.execute("SELECT Equipment_ID, Status FROM Booking WHERE Booking_ID = %s", (booking_id,))
        booking = cursor.fetchone()
        if not booking:
            print("❌ No booking found with that ID.")
            return

        equipment_id = booking[0]

        print("\nEnter new details (leave blank to keep unchanged):")
        new_return_date = input("New Return Date (YYYY-MM-DD): ").strip()
        new_status = input("New Status (Booked / Issued / Returned / Lost): ").strip()

        if new_return_date:
            cursor.execute("UPDATE Booking SET Return_Date = %s WHERE Booking_ID = %s",
                           (new_return_date, booking_id))
        if new_status:
            cursor.execute("UPDATE Booking SET Status = %s WHERE Booking_ID = %s",
                           (new_status, booking_id))

            # Auto update equipment availability
            if new_status.lower() == "returned":
                cursor.execute("UPDATE Equipment SET Status = 'Available' WHERE Equipment_ID = %s", (equipment_id,))
            elif new_status.lower() in ("booked", "issued"):
                cursor.execute("UPDATE Equipment SET Status = 'Unavailable' WHERE Equipment_ID = %s", (equipment_id,))

        con.commit()
        print("✅ Booking updated successfully!")

    except Error as e:
        print(f"❌ Error updating booking: {e}")
        con.rollback()

    finally:
        cursor.close()


# ============================
#  DELETE BOOKING
# ============================
def delete_booking(con):
    if con is None:
        print("❌ Connection not established!")
        return

    try:
        cursor = con.cursor()
        booking_id = input("Enter Booking ID to delete: ").strip()

        cursor.execute("SELECT Equipment_ID FROM Booking WHERE Booking_ID = %s", (booking_id,))
        booking = cursor.fetchone()
        if not booking:
            print("❌ No booking found with that ID.")
            return

        equipment_id = booking[0]

        cursor.execute("DELETE FROM Booking WHERE Booking_ID = %s", (booking_id,))
        con.commit()

        cursor.execute("UPDATE Equipment SET Status = 'Available' WHERE Equipment_ID = %s", (equipment_id,))
        con.commit()

        print("✅ Booking deleted successfully and equipment marked Available!")

    except Error as e:
        print(f"❌ Error deleting booking: {e}")
        con.rollback()

    finally:
        cursor.close()

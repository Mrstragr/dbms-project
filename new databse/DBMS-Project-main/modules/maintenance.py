import mysql.connector as db
from mysql.connector import Error


# -------------------------------
# ADD NEW MAINTENANCE RECORD
# -------------------------------
def add_maintenance(con):
    if con is None:
        print("❌ Connection not established!")
        return
    try:
        cursor = con.cursor()
        print("\n=== Add Maintenance Record ===")
        equipment_id = input("Enter Equipment ID: ").strip()
        issue_date = input("Enter Issue Reported Date (YYYY-MM-DD): ").strip()
        fix_date = input("Enter Fix Date (YYYY-MM-DD) or press Enter if not fixed yet: ").strip()
        issue_desc = input("Enter Issue Description: ").strip()
        status = input("Enter Status (Pending/In Progress/Resolved): ").strip()

        if fix_date == "":
            fix_date = None

        query = """
            INSERT INTO Maintenance (Equipment_ID, Issue_Reported_Date, Fix_Date, Issue_Description, Status)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (equipment_id, issue_date, fix_date, issue_desc, status))
        con.commit()
        print("✅ Maintenance record added successfully!")

    except Error as e:
        print(f"Error adding maintenance record: {e}")

    finally:
        cursor.close()


# -------------------------------
# VIEW ALL MAINTENANCE RECORDS
# -------------------------------
def view_all_maintenance(con):
    if con is None:
        print("❌ Connection not established!")
        return
    try:
        cursor = con.cursor()
        cursor.execute("""
            SELECT m.Maintenance_ID, e.Equipment_Name, m.Equipment_ID,
                   m.Issue_Reported_Date, m.Fix_Date, m.Issue_Description, m.Status
            FROM Maintenance m
            LEFT JOIN Equipment e ON m.Equipment_ID = e.Equipment_ID
            ORDER BY m.Maintenance_ID DESC
        """)
        rows = cursor.fetchall()

        print("\n=== All Maintenance Records ===")
        if rows:
            for row in rows:
                print(f"""
Maintenance ID : {row[0]}
Equipment         : {row[1]} (ID: {row[2]})
Issue Reported On : {row[3]}
Fix Date          : {row[4] if row[4] else "—"}
Description       : {row[5]}
Status            : {row[6]}
-----------------------------------------
                """)
        else:
            print("No maintenance records found.")

    except Error as e:
        print(f"Error retrieving maintenance records: {e}")

    finally:
        cursor.close()


# -------------------------------
# FILTER MAINTENANCE RECORDS BY STATUS
# -------------------------------
def filter_maintenance_by_status(con):
    if con is None:
        print("❌ Connection not established!")
        return
    try:
        cursor = con.cursor()
        print("\nFilter by Status:")
        print("1 → Pending")
        print("2 → In Progress")
        print("3 → Resolved")
        choice = input("Enter your choice: ").strip()

        status_map = {'1': 'Pending', '2': 'In Progress', '3': 'Resolved'}
        status = status_map.get(choice)

        if not status:
            print("❌ Invalid choice.")
            return

        query = """
            SELECT m.Maintenance_ID, e.Equipment_Name, m.Equipment_ID,
                   m.Issue_Reported_Date, m.Fix_Date, m.Issue_Description, m.Status
            FROM Maintenance m
            LEFT JOIN Equipment e ON m.Equipment_ID = e.Equipment_ID
            WHERE m.Status = %s
            ORDER BY m.Maintenance_ID DESC
        """
        cursor.execute(query, (status,))
        rows = cursor.fetchall()

        print(f"\n=== {status} Maintenance Records ===")
        if rows:
            for row in rows:
                print(f"""
Maintenance ID : {row[0]}
Equipment         : {row[1]} (ID: {row[2]})
Issue Reported On : {row[3]}
Fix Date          : {row[4] if row[4] else "—"}
Description       : {row[5]}
Status            : {row[6]}
-----------------------------------------
                """)
        else:
            print(f"No {status} maintenance records found.")

    except Error as e:
        print(f"Error filtering maintenance records: {e}")

    finally:
        cursor.close()


# -------------------------------
# UPDATE MAINTENANCE RECORD
# -------------------------------
def update_maintenance(con):
    if con is None:
        print("❌ Connection not established!")
        return
    try:
        cursor = con.cursor()
        maintenance_id = input("Enter Maintenance ID to update: ").strip()

        cursor.execute("SELECT * FROM Maintenance WHERE Maintenance_ID = %s", (maintenance_id,))
        if cursor.fetchone() is None:
            print("❌ No maintenance record found with that ID.")
            return

        print("\nWhat do you want to update?")
        print("1. Fix Date")
        print("2. Issue Description")
        print("3. Status")

        choice = input("Enter your choice: ")

        if choice == '1':
            fix_date = input("Enter new Fix Date (YYYY-MM-DD): ").strip()
            cursor.execute("UPDATE Maintenance SET Fix_Date=%s WHERE Maintenance_ID=%s", (fix_date, maintenance_id))
        elif choice == '2':
            desc = input("Enter updated Issue Description: ").strip()
            cursor.execute("UPDATE Maintenance SET Issue_Description=%s WHERE Maintenance_ID=%s", (desc, maintenance_id))
        elif choice == '3':
            status = input("Enter new Status (Pending/In Progress/Resolved): ").strip()
            cursor.execute("UPDATE Maintenance SET Status=%s WHERE Maintenance_ID=%s", (status, maintenance_id))
        else:
            print("Invalid choice.")
            return

        con.commit()
        print("✅ Maintenance record updated successfully!")

    except Error as e:
        print(f"Error updating maintenance record: {e}")

    finally:
        cursor.close()


# -------------------------------
# DELETE MAINTENANCE RECORD
# -------------------------------
def delete_maintenance(con):
    if con is None:
        print("❌ Connection not established!")
        return
    try:
        cursor = con.cursor()
        maintenance_id = input("Enter Maintenance ID to delete: ").strip()
        confirm = input("Are you sure you want to delete this record? (y/n): ")

        if confirm.lower() == 'y':
            cursor.execute("DELETE FROM Maintenance WHERE Maintenance_ID = %s", (maintenance_id,))
            con.commit()
            print("✅ Maintenance record deleted successfully!")
        else:
            print("Deletion cancelled.")
    except Error as e:
        print(f"Error deleting maintenance record: {e}")
    finally:
        cursor.close()



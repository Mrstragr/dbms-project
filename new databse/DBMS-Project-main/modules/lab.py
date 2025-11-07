import mysql.connector as db
from mysql.connector import Error


# ====================================================
# LAB MANAGEMENT
# ====================================================

# -------------------------------
# ADD NEW LAB
# -------------------------------
def add_lab(con):
    if con is None:
        print("❌ Connection not established!")
        return
    try:
        cursor = con.cursor()
        print("\n=== Add New Lab ===")
        lab_name = input("Enter Lab Name: ").strip()
        location = input("Enter Lab Location: ").strip()
        incharge_id = input("Enter Incharge Faculty ID (or press Enter if none): ").strip()

        if incharge_id == "":
            incharge_id = None

        query = "INSERT INTO Lab (Lab_Name, Location, Incharge_ID) VALUES (%s, %s, %s)"
        cursor.execute(query, (lab_name, location, incharge_id))
        con.commit()
        print("✅ Lab added successfully!")

    except Error as e:
        print(f"Error adding lab: {e}")
    finally:
        cursor.close()


# -------------------------------
# VIEW ALL LABS
# -------------------------------
def view_all_labs(con):
    if con is None:
        print("❌ Connection not established!")
        return
    try:
        cursor = con.cursor()
        cursor.execute("""
            SELECT l.Lab_ID, l.Lab_Name, l.Location, 
                   CONCAT(f.First_Name, ' ', IFNULL(f.Last_Name, '')) AS Incharge
            FROM Lab l
            LEFT JOIN Faculty f ON l.Incharge_ID = f.Faculty_ID
        """)
        labs = cursor.fetchall()

        print("\n=== All Labs ===")
        if labs:
            for lab in labs:
                incharge = lab[3] if lab[3] else "—"
                print(f"\n🧪 Lab ID: {lab[0]}")
                print(f"   Name: {lab[1]}")
                print(f"   Location: {lab[2]}")
                print(f"   Incharge: {incharge}")

                # Fetch lab assistants for this lab
                cursor.execute("""
                    SELECT Assistant_ID, CONCAT(First_Name, ' ', IFNULL(Last_Name, '')) AS Name
                    FROM Lab_Assistant
                    WHERE Lab_ID = %s
                """, (lab[0],))
                assistants = cursor.fetchall()
                count = len(assistants)

                if assistants:
                    print(f"   Assistants ({count}):")
                    for a in assistants:
                        print(f"      - {a[1]} (ID: {a[0]})")
                else:
                    print("   Assistants: None (0)")
        else:
            print("No labs found.")
    except Error as e:
        print(f"Error retrieving labs: {e}")
    finally:
        cursor.close()


# -------------------------------
# UPDATE LAB DETAILS
# -------------------------------
def update_lab(con):
    if con is None:
        print("❌ Connection not established!")
        return
    try:
        cursor = con.cursor()
        lab_id = input("Enter Lab ID to update: ").strip()

        cursor.execute("SELECT * FROM Lab WHERE Lab_ID = %s", (lab_id,))
        if cursor.fetchone() is None:
            print("❌ No lab found with that ID.")
            return

        print("\nWhat do you want to update?")
        print("1. Lab Name")
        print("2. Location")
        print("3. Incharge Faculty ID")
        choice = input("Enter choice: ").strip()

        if choice == '1':
            new_name = input("Enter new Lab Name: ").strip()
            cursor.execute("UPDATE Lab SET Lab_Name = %s WHERE Lab_ID = %s", (new_name, lab_id))
        elif choice == '2':
            new_location = input("Enter new Location: ").strip()
            cursor.execute("UPDATE Lab SET Location = %s WHERE Lab_ID = %s", (new_location, lab_id))
        elif choice == '3':
            new_incharge = input("Enter new Incharge Faculty ID (or press Enter to remove): ").strip()
            if new_incharge == "":
                cursor.execute("UPDATE Lab SET Incharge_ID = NULL WHERE Lab_ID = %s", (lab_id,))
            else:
                cursor.execute("UPDATE Lab SET Incharge_ID = %s WHERE Lab_ID = %s", (new_incharge, lab_id))
        else:
            print("Invalid choice.")
            return

        con.commit()
        print("✅ Lab updated successfully!")

    except Error as e:
        print(f"Error updating lab: {e}")
    finally:
        cursor.close()


# -------------------------------
# DELETE LAB
# -------------------------------
def delete_lab(con):
    if con is None:
        print("❌ Connection not established!")
        return
    try:
        cursor = con.cursor()
        lab_id = input("Enter Lab ID to delete: ").strip()
        confirm = input("Are you sure you want to delete this lab? (y/n): ").strip()
        if confirm.lower() == 'y':
            cursor.execute("DELETE FROM Lab WHERE Lab_ID = %s", (lab_id,))
            con.commit()
            print("✅ Lab deleted successfully!")
        else:
            print("Deletion cancelled.")
    except Error as e:
        print(f"Error deleting lab: {e}")
    finally:
        cursor.close()




# ====================================================
# LAB ASSISTANT MANAGEMENT
# ====================================================

# -------------------------------
# ADD LAB ASSISTANT
# -------------------------------
def add_lab_assistant(con):
    if con is None:
        print("❌ Connection not established!")
        return
    try:
        cursor = con.cursor()
        print("\n=== Add Lab Assistant ===")
        fname = input("Enter First Name: ").strip()
        lname = input("Enter Last Name (optional): ").strip()
        email = input("Enter Email: ").strip()
        lab_id = input("Enter Lab ID (or press Enter if unassigned): ").strip()

        if lab_id == "":
            lab_id = None

        query = """
            INSERT INTO Lab_Assistant (First_Name, Last_Name, Email, Lab_ID)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (fname, lname, email, lab_id))
        con.commit()
        print("✅ Lab Assistant added successfully!")
    except Error as e:
        print(f"Error adding assistant: {e}")
    finally:
        cursor.close()


# -------------------------------
# VIEW ALL LAB ASSISTANTS
# -------------------------------
def view_all_assistants(con):
    if con is None:
        print("❌ Connection not established!")
        return
    try:
        cursor = con.cursor()
        cursor.execute("""
            SELECT a.Assistant_ID, CONCAT(a.First_Name, ' ', IFNULL(a.Last_Name, '')) AS Name,
                   a.Email, IFNULL(l.Lab_Name, '—') AS Lab
            FROM Lab_Assistant a
            LEFT JOIN Lab l ON a.Lab_ID = l.Lab_ID
        """)
        rows = cursor.fetchall()

        print("\n=== All Lab Assistants ===")
        if rows:
            for row in rows:
                print(f"ID: {row[0]} | Name: {row[1]} | Email: {row[2]} | Lab: {row[3]}")
        else:
            print("No assistants found.")
    except Error as e:
        print(f"Error retrieving assistants: {e}")
    finally:
        cursor.close()


# -------------------------------
# UPDATE LAB ASSISTANT
# -------------------------------
def update_lab_assistant(con):
    if con is None:
        print("❌ Connection not established!")
        return
    try:
        cursor = con.cursor()
        assistant_id = input("Enter Assistant ID to update: ").strip()

        cursor.execute("SELECT * FROM Lab_Assistant WHERE Assistant_ID = %s", (assistant_id,))
        if cursor.fetchone() is None:
            print("❌ No assistant found with that ID.")
            return

        print("\nWhat do you want to update?")
        print("1. Name")
        print("2. Email")
        print("3. Assigned Lab")
        choice = input("Enter choice: ").strip()

        if choice == '1':
            fname = input("Enter new First Name: ").strip()
            lname = input("Enter new Last Name (optional): ").strip()
            cursor.execute("UPDATE Lab_Assistant SET First_Name=%s, Last_Name=%s WHERE Assistant_ID=%s", (fname, lname, assistant_id))
        elif choice == '2':
            email = input("Enter new Email: ").strip()
            cursor.execute("UPDATE Lab_Assistant SET Email=%s WHERE Assistant_ID=%s", (email, assistant_id))
        elif choice == '3':
            lab_id = input("Enter new Lab ID (or press Enter to remove): ").strip()
            if lab_id == "":
                cursor.execute("UPDATE Lab_Assistant SET Lab_ID=NULL WHERE Assistant_ID=%s", (assistant_id,))
            else:
                cursor.execute("UPDATE Lab_Assistant SET Lab_ID=%s WHERE Assistant_ID=%s", (lab_id, assistant_id))
        else:
            print("Invalid choice.")
            return

        con.commit()
        print("✅ Lab Assistant updated successfully!")
    except Error as e:
        print(f"Error updating assistant: {e}")
    finally:
        cursor.close()


# -------------------------------
# DELETE LAB ASSISTANT
# -------------------------------
def delete_lab_assistant(con):
    if con is None:
        print("❌ Connection not established!")
        return
    try:
        cursor = con.cursor()
        assistant_id = input("Enter Assistant ID to delete: ").strip()
        confirm = input("Are you sure you want to delete this assistant? (y/n): ").strip()
        if confirm.lower() == 'y':
            cursor.execute("DELETE FROM Lab_Assistant WHERE Assistant_ID=%s", (assistant_id,))
            con.commit()
            print("✅ Assistant deleted successfully!")
        else:
            print("Deletion cancelled.")
    except Error as e:
        print(f"Error deleting assistant: {e}")
    finally:
        cursor.close()

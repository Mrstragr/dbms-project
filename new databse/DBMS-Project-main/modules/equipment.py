import mysql.connector as db
# from modules.connection import create_connection, close_connection

# -------------------------------
# ADD NEW EQUIPMENT
# -------------------------------
def add_equipment(con):
    if con is None:
        print("❌ Connection not established!")
        return
    cursor = con.cursor()    

    try:
        name = input("Enter Equipment Name: ")
        category = input("Enter Category: ")
        condition = input("Enter Equipment Condition: ")
        purchase_date = input("Enter Purchase Date (YYYY-MM-DD): ")
        status = input("Enter Status: ")
        lab_id = input("Enter Lab ID (press Enter if not assigned): ")

        # Convert lab_id to None if blank
        lab_id = int(lab_id) if lab_id.strip() else None

        sql = """
        INSERT INTO Equipment (Name, Category, Equipment_Condition, Purchase_Date, Status, Lab_ID)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (name, category, condition, purchase_date, status, lab_id))
        con.commit()
        print("✅ Equipment added successfully!")

    except db.Error as err:
        print(f"❌ Error: {err}")
    finally:
        cursor.close()


# -------------------------------
# VIEW ALL EQUIPMENT
# -------------------------------
def view_all_equipment(con):
    if con is None:
        print("❌ Connection not established!")
        return
    cursor = con.cursor()

    try:
        cursor.execute("SELECT * FROM Equipment")
        rows = cursor.fetchall()

        if not rows:
            print("No equipment found.")
            return

        print("\n===== Equipment List =====")
        for row in rows:
            print(f"ID: {row[0]} | Name: {row[1]} | Category: {row[2]} | Condition: {row[3]} | "
                  f"Purchase Date: {row[4]} | Status: {row[5]} | Lab ID: {row[6]}")

    except db.Error as err:
        print(f"❌ Error: {err}")
    finally:
        cursor.close()


# -------------------------------
# UPDATE EQUIPMENT
# -------------------------------
def update_equipment(con):
    if con is None:
        print("❌ Connection not established!")
        return
    cursor = con.cursor()

    try:
        eq_id = int(input("Enter Equipment ID to update: "))

        print("\nChoose field to update:")
        print("1. Name")
        print("2. Category")
        print("3. Condition")
        print("4. Purchase Date")
        print("5. Status")
        print("6. Lab ID")

        choice = int(input("Enter your choice: "))

        field_map = {
            1: "Name",
            2: "Category",
            3: "Equipment_Condition",
            4: "Purchase_Date",
            5: "Status",
            6: "Lab_ID"
        }

        if choice not in field_map:
            print("Invalid choice!")
            return

        new_value = input(f"Enter new value for {field_map[choice]}: ")

        if field_map[choice] == "Lab_ID":
            new_value = int(new_value) if new_value.strip() else None

        sql = f"UPDATE Equipment SET {field_map[choice]} = %s WHERE Equipment_ID = %s"
        cursor.execute(sql, (new_value, eq_id))
        con.commit()

        if cursor.rowcount == 0:
            print("No record found with that ID.")
        else:
            print("✅ Equipment updated successfully!")

    except db.Error as err:
        print(f"❌ Error: {err}")
    finally:
        cursor.close()


# -------------------------------
# DELETE EQUIPMENT
# -------------------------------
def delete_equipment(con):
    if con is None:
        print("❌ Connection not established!")
        return
    cursor = con.cursor()

    try:
        eq_id = int(input("Enter Equipment ID to delete: "))
        confirm = input("Are you sure you want to delete this equipment? (y/n): ").lower()
        if confirm != 'y':
            print("❌ Deletion cancelled.")
            return

        cursor.execute("DELETE FROM Equipment WHERE Equipment_ID = %s", (eq_id,))
        con.commit()

        if cursor.rowcount == 0:
            print("No equipment found with that ID.")
        else:
            print("✅ Equipment deleted successfully!")

    except db.Error as err:
        print(f"❌ Error: {err}")
    finally:
        cursor.close()

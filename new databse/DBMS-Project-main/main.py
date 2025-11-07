from modules.connection import create_connection, close_connection
from modules.equipment import add_equipment, view_all_equipment, update_equipment, delete_equipment
from modules.lab import add_lab, view_all_labs, update_lab, delete_lab, add_lab_assistant, view_all_assistants, update_lab_assistant, delete_lab_assistant
from modules.faculty import add_faculty, view_all_faculty, update_faculty, delete_faculty
from modules.student import add_student, view_all_students, update_student, delete_student
from modules.booking import add_booking, view_all_bookings, update_booking, delete_booking
from modules.maintenance import add_maintenance, view_all_maintenance, filter_maintenance_by_status, update_maintenance, delete_maintenance


# con is the connection object returned by create_connection()
con = None   # defined globally

while True:
    print("=" * 60)
    print("  SAU EQUIPMENT AND LAB RESOURCE MANAGEMENT SYSTEM")
    print("=" * 60)

    print("1 → Create Connection")
    print("2 → Close Connection")
    print("3 → Equipment Menu")
    print("4 → Lab Menu")
    print("5 → Faculty Menu")
    print("6 → Student Menu")
    print("7 → Booking Menu")
    print("8 → Maintenance Menu")

    try:
        ch = int(input("\nEnter your choice: "))
    except ValueError:
        print("❌ Please enter a valid number.")
        continue

    if ch == 1:
        con = create_connection()   # Try to connect
        if con:
            print("Database connected successfully!")
        else:
            print("Failed to connect to the database.")

    elif ch == 2:
        if con is None:
            print("❌ Please establish a database connection first!")
            continue
        else:
            print("Closing the connection safely...")
            close_connection(con)
            con = None  # This ensures if the user tries any option again after closing, it won’t accidentally use a closed connection.
    
    elif ch == 3:
        if con is None:
            print("❌ Please establish a database connection first!")
            continue

        while True:
            print("\n=== Equipment Menu ===")
            print("1 → Add Equipment")
            print("2 → View All")
            print("3 → Update Equipment")
            print("4 → Delete Equipment")
            print("5 → Back to Main Menu")

            try:
                ch = int(input("Enter your choice: "))
            except ValueError:
                print("❌ Please enter a valid number.")
                continue

            if ch == 1:
                add_equipment(con)
            elif ch == 2:
                view_all_equipment(con)
            elif ch == 3:
                update_equipment(con)
            elif ch == 4:
                delete_equipment(con)
            elif ch == 5:
                break
            else:
                print("Invalid choice! Please try again.")
                continue

    elif ch == 4:
        if con is None:
            print("❌ Please establish a database connection first!")
            continue

        while True:
            print("\n===LAB MANAGEMENT MENU ===")
            print("1 → Manage Labs")
            print("2 → Manage Lab Assistants")
            print("3 → Back to Main Menu")

            try:
                sub_choice = int(input("Enter your choice: "))
            except ValueError:
                print("❌ Please enter a valid number.")
                continue

            # Lab submenu
            if sub_choice == 1:
                while True:
                    print("\n--- LAB MENU ---")
                    print("1 → Add Lab")
                    print("2 → View All Labs")
                    print("3 → Update Lab")
                    print("4 → Delete Lab")
                    print("5 → Back")

                    try:
                        lab_choice = int(input("Enter your choice: "))
                    except ValueError:
                        print("❌ Invalid input! Please enter a number.")
                        continue

                    if lab_choice == 1:
                        add_lab(con)
                    elif lab_choice == 2:
                        view_all_labs(con)
                    elif lab_choice == 3:
                        update_lab(con)
                    elif lab_choice == 4:
                        delete_lab(con)
                    elif lab_choice == 5:
                        break
                    else:
                        print("Invalid option! Try again.")

            # Lab assistant submenu
            elif sub_choice == 2:
                while True:
                    print("\n--- LAB ASSISTANT MENU ---")
                    print("1 → Add Lab Assistant")
                    print("2 → View All Assistants")
                    print("3 → Update Assistant")
                    print("4 → Delete Assistant")
                    print("5 → Back")

                    try:
                        asst_choice = int(input("Enter your choice: "))
                    except ValueError:
                        print("❌ Invalid input! Please enter a number.")
                        continue

                    if asst_choice == 1:
                        add_lab_assistant(con)
                    elif asst_choice == 2:
                        view_all_assistants(con)
                    elif asst_choice == 3:
                        update_lab_assistant(con)
                    elif asst_choice == 4:
                        delete_lab_assistant(con)
                    elif asst_choice == 5:
                        break
                    else:
                        print("Invalid option! Try again.")

            elif sub_choice == 3:
                break

            else:
                print("Invalid option! Please select from 1-3.")

    elif ch == 5:
        if con is None:
            print("❌ Please establish a database connection first!")
            continue

        while True:
            print("\n=== Faculty Menu ===")
            print("1 → Add Faculty")
            print("2 → View All Faculty")
            print("3 → Update Faculty")
            print("4 → Delete Faculty")
            print("5 → Back to Main Menu")

            try:
                ch = int(input("Enter your choice: "))
            except ValueError:
                print("❌ Please enter a valid number.")
                continue

            if ch == 1:
                add_faculty(con)
            elif ch == 2:
                view_all_faculty(con)
            elif ch == 3:
                update_faculty(con)
            elif ch == 4:
                delete_faculty(con)
            elif ch == 5:
                break
            else:
                print("Invalid choice! Please try again.")
                continue

    elif ch == 6:
        if con is None:
            print("❌ Please establish a database connection first!")
            continue

        while True:
            print("\n=== Student Menu ===")
            print("1 → Add Student")
            print("2 → View All Students")
            print("3 → Update Student")
            print("4 → Delete Student")
            print("5 → Back to Main Menu")

            try:
                ch = int(input("Enter your choice: "))
            except ValueError:
                print("❌ Please enter a valid number.")
                continue

            if ch == 1:
                add_student(con)
            elif ch == 2:
                view_all_students(con)
            elif ch == 3:
                update_student(con)
            elif ch == 4:
                delete_student(con)
            elif ch == 5:
                break
            else:
                print("Invalid choice! Please try again.")
                continue

    elif ch == 7:
        if con is None:
            print("❌ Please establish a database connection first!")
            continue

        while True:
            print("\n=== Booking Menu ===")
            print("1 → Add Booking")
            print("2 → View All Bookings")
            print("3 → Update Booking")
            print("4 → Delete Booking")
            print("5 → Back to Main Menu")

            try:
                ch = int(input("Enter your choice: "))
            except ValueError:
                print("❌ Please enter a valid number.")
                continue

            if ch == 1:
                add_booking(con)
            elif ch == 2:
                view_all_bookings(con)
            elif ch == 3:
                update_booking(con)
            elif ch == 4:
                delete_booking(con)
            elif ch == 5:
                break
            else:
                print("Invalid choice! Please try again.")
                continue

    elif ch == 8:
        if con is None:
            print("❌ Please establish a database connection first!")
            continue

        while True:
            print("\n=== Maintenance Menu ===")
            print("1 → Add Maintenance Record")
            print("2 → View All Maintenance Records")
            print("3 → Filter by Status (Pending/In Progress/Resolved)")
            print("4 → Update Maintenance Record")
            print("5 → Delete Maintenance Record")
            print("6 → Back to Main Menu")

            try:
                choice = int(input("Enter your choice: "))
            except ValueError:
                print("❌ Please enter a valid number.")
                continue

            if choice == 1:
                add_maintenance(con)
            elif choice == 2:
                view_all_maintenance(con)
            elif choice == 3:
                filter_maintenance_by_status(con)
            elif choice == 4:
                update_maintenance(con)
            elif choice == 5:
                delete_maintenance(con)
            elif choice == 6:
                break
            else:
                print("Invalid option! Try again.")
                
    else:
        print("Invalid choice! Please try again.")
        continue











# con = create_connection()   # Try to connect

# if con:
#     print("Database connected successfully!")
#     close_connection(con)   # Close the connection
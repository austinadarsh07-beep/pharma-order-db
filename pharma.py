import mysql.connector
import random
'''
# ---------------- DATABASE CONNECTION ----------------
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password123",
    database="project"
)
cursor = connection.cursor()

# ---------------- DISPLAY ALL MEDICINES ----------------
def show_all_medicines():
    cursor.execute("SELECT * FROM Medicines")
    medicines = cursor.fetchall()

    print("\n" + "="*70)
    print("{:<5} {:<20} {:<15} {:<10} {:<10} {:<10}".format(
        "ID", "Name", "Brand", "Stock", "Price", "Expiry"
    ))
    print("="*70)

    for m in medicines:
        print("{:<5} {:<20} {:<15} {:<10} {:<10} {:<10}".format(
            m[0], m[1], m[2], m[3], m[4], str(m[5])
        ))
    print("="*70)

# ---------------- ADMIN FUNCTIONS ----------------
def add_medicine():
    print("\nADD MEDICINE")
    name = input("Medicine Name: ")
    brand = input("Brand: ")
    stock = int(input("Stock Quantity: "))
    price = float(input("Price: "))
    expiry = input("Expiry Date (YYYY-MM-DD): ")

    query = """
    INSERT INTO Medicines VALUES (
        (SELECT IFNULL(MAX(MedicineID),0)+1 FROM Medicines),
        '{}','{}',{},{},'{}'
    )
    """.format(name, brand, stock, price, expiry)

    cursor.execute(query)
    connection.commit()
    print("\nMedicine added successfully!")

def remove_medicine():
    show_all_medicines()
    mid = int(input("Enter Medicine ID to remove: "))
    cursor.execute("DELETE FROM Medicines WHERE MedicineID = {}".format(mid))
    connection.commit()
    print("Medicine removed successfully!")

def update_medicine():
    show_all_medicines()
    mid = int(input("Enter Medicine ID to update: "))
    print("1. Update Stock\n2. Update Price")
    choice = input("Choice: ")

    if choice == "1":
        new_stock = int(input("New Stock: "))
        cursor.execute(
            "UPDATE Medicines SET QuantityInStock = {} WHERE MedicineID = {}".format(new_stock, mid)
        )
    elif choice == "2":
        new_price = float(input("New Price: "))
        cursor.execute(
            "UPDATE Medicines SET Price = {} WHERE MedicineID = {}".format(new_price, mid)
        )

    connection.commit()
    print("Medicine updated successfully!")

def admin_menu():
    print("\nADMIN LOGIN")
    aid = input("Admin ID: ")
    passcode = input("Passcode: ")

    cursor.execute(
        "SELECT * FROM Admin WHERE AdminID='{}' AND Passcode='{}'".format(aid, passcode)
    )
    admin = cursor.fetchone()

    if not admin:
        print("Invalid admin credentials!")
        return

    print("\nWelcome Admin,", admin[1])

    while True:
        print("\n1. Add Medicine")
        print("2. Remove Medicine")
        print("3. Update Medicine")
        print("4. Logout")

        ch = input("Choice: ")

        if ch == "1":
            add_medicine()
        elif ch == "2":
            remove_medicine()
        elif ch == "3":
            update_medicine()
        elif ch == "4":
            break
        else:
            print("Invalid choice!")

# ---------------- CUSTOMER FUNCTIONS ----------------
def order_medicine():
    show_all_medicines()
    mid = int(input("Medicine ID: "))
    qty = int(input("Quantity: "))
    name = input("Customer Name: ")
    address = input("Address: ")

    while True:
        contact = input("Contact Number (10 digits): ")
        if contact.isdigit() and len(contact) == 10:
            break
        print("Invalid contact number!")

    cursor.execute(
        "SELECT QuantityInStock, Price FROM Medicines WHERE MedicineID={}".format(mid)
    )
    med = cursor.fetchone()

    if not med or med[0] < qty:
        print("Insufficient stock!")
        return

    total = med[1] * qty

    cursor.execute(
        "INSERT INTO Customers (Name,Address,ContactNumber,MedicineID) VALUES "
        "('{}','{}','{}',{})".format(name, address, contact, mid)
    )
    cid = cursor.lastrowid

    order_id = random.randint(1000000000, 9999999999)

    cursor.execute(
        "INSERT INTO Orders VALUES ({},{},{},NOW(),{},{})".format(
            order_id, cid, mid, qty, total
        )
    )

    cursor.execute(
        "UPDATE Medicines SET QuantityInStock = QuantityInStock - {} WHERE MedicineID={}".format(qty, mid)
    )

    connection.commit()
    print("\nOrder placed successfully!")
    print("Order ID:", order_id)
    print("Total Price: ₹", total)

def view_orders():
    cname = input("Enter Customer Name: ")

    cursor.execute("""
        SELECT o.OrderID, o.OrderDate, o.Quantity, o.TotalPrice
        FROM Orders o
        JOIN Customers c ON o.CustomerID = c.CustomerID
        WHERE c.Name = '{}'
    """.format(cname))

    orders = cursor.fetchall()

    if not orders:
        print("No orders found!")
        return

    print("\nOrder Details")
    print("="*50)
    for o in orders:
        print("Order ID:", o[0], "| Date:", o[1], "| Qty:", o[2], "| Total:", o[3])
    print("="*50)

def cancel_order():
    cname = input("Customer Name: ")
    oid = input("Order ID: ")

    cursor.execute("""
        SELECT o.CustomerID, o.MedicineID, o.Quantity
        FROM Orders o
        JOIN Customers c ON o.CustomerID=c.CustomerID
        WHERE o.OrderID={} AND c.Name='{}'
    """.format(oid, cname))

    data = cursor.fetchone()

    if not data:
        print("Order not found!")
        return

    cursor.execute(
        "UPDATE Medicines SET QuantityInStock = QuantityInStock + {} WHERE MedicineID={}".format(
            data[2], data[1]
        )
    )

    cursor.execute("DELETE FROM Orders WHERE OrderID={}".format(oid))
    cursor.execute("DELETE FROM Customers WHERE CustomerID={}".format(data[0]))
    connection.commit()

    print("Order cancelled successfully!")

# ---------------- MAIN MENU ----------------
def main_menu():
    while True:
        print("\nPHARMACY MANAGEMENT SYSTEM")
        print("1. Admin")
        print("2. Customer")
        print("3. Exit")

        choice = input("Choice: ")

        if choice == "1":
            admin_menu()
        elif choice == "2":
            while True:
                print("\n1. View Medicines")
                print("2. Order Medicine")
                print("3. View Orders")
                print("4. Cancel Order")
                print("5. Back")

                c = input("Choice: ")

                if c == "1":
                    show_all_medicines()
                elif c == "2":
                    order_medicine()
                elif c == "3":
                    view_orders()
                elif c == "4":
                    cancel_order()
                elif c == "5":
                    break
                else:
                    print("Invalid choice!")
        elif choice == "3":
            print("Thank you!")
            connection.close()
            break
        else:
            print("Invalid choice!")

# ---------------- RUN PROGRAM ----------------
main_menu()
'''
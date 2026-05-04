import mysql.connector

class DatabaseManager:
    def __init__(self):
        # Establish the connection
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",        # Update with your MySQL username
            password="root",        # Update with your MySQL password
            database="cafe_management"
        )
        # Create the cursor attribute here
        self.cursor = self.conn.cursor()

    def record_sale(self, name, qty, total, time_str):
        try:
            # 1. Insert into transactions
            query_insert = "INSERT INTO transactions (item_name, quantity, total_price, sale_date) VALUES (%s, %s, %s, %s)"
            self.cursor.execute(query_insert, (name, qty, total, time_str))
            
            # 2. Update stock in menu_items
            query_update = "UPDATE menu_items SET stock_qty = stock_qty - %s WHERE item_name = %s"
            self.cursor.execute(query_update, (qty, name))
            
            self.conn.commit()
        except Exception as e:
            print(f"Error recording sale: {e}")
            self.conn.rollback()

    # Ensure these methods also use self.cursor
    def fetch_menu_items(self):
        self.cursor.execute("SELECT * FROM menu_items")
        return self.cursor.fetchall()

    def fetch_transactions(self):
        self.cursor.execute("SELECT sale_date, item_name, quantity, total_price FROM transactions")
        return self.cursor.fetchall()
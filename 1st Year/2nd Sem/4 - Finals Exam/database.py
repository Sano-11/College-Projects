import mysql.connector
from tkinter import messagebox

class DatabaseManager:
    def __init__(self):
        try:
            # Update these credentials to match your local MySQL setup
            self.db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="cafe_management"
            )
            self.cursor = self.db.cursor()
            self.create_tables()
        except mysql.connector.Error as err:
            messagebox.showerror("Connection Error", f"Could not connect to MySQL: {err}")

    def create_tables(self):
        """Ensures the required tables exist in the database."""
        # Table for menu items
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS menu_items (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                price DECIMAL(10, 2) NOT NULL,
                stock INT DEFAULT 0,
                category_id INT
            )
        """)
        
        # Table for transactions (Fixes image_57047e.png error)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS sales (
                id INT AUTO_INCREMENT PRIMARY KEY,
                date VARCHAR(255) NOT NULL,
                items TEXT NOT NULL,
                total DECIMAL(10, 2) NOT NULL
            )
        """)
        self.db.commit()

    def fetch_menu_items(self):
        """Retrieves all products for the Dashboard and Inventory views."""
        self.cursor.execute("SELECT * FROM menu_items")
        return self.cursor.fetchall()

    def fetch_sales(self):
        """Retrieves order history for the Transaction Records view."""
        self.cursor.execute("SELECT * FROM sales ORDER BY id DESC")
        return self.cursor.fetchall()

    def update_stock(self, product_id, change):
        """Increments or decrements stock levels in real-time."""
        query = "UPDATE products SET stock = stock + %s WHERE product_id = %s"
        self.cursor.execute(query, (change, product_id))
        self.db.commit()

    def add_sale(self, date, items, total):
        """Records a completed checkout. (Fixes image_575a02.png error)"""
        try:
            query = "INSERT INTO sales (date, items, total) VALUES (%s, %s, %s)"
            values = (date, items, total)
            self.cursor.execute(query, values)
            self.db.commit()
        except mysql.connector.Error as err:
            print(f"Error saving sale: {err}")
            self.db.rollback()
            raise err

    def __del__(self):
        if hasattr(self, 'db') and self.db.is_connected():
            self.cursor.close()
            self.db.close()
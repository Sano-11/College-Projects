import mysql.connector
from tkinter import messagebox

class DatabaseManager:
    def __init__(self):
        try:
            self.db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="cafe_management"
            )
            self.cursor = self.db.cursor()
            # We don't need create_tables() here if you ran the SQL script in Workbench,
            # but keeping it safe and updated to 'products'
            self.create_tables()
        except mysql.connector.Error as err:
            messagebox.showerror("Connection Error", f"Could not connect to MySQL: {err}")

    def create_tables(self):
        """Ensures the required tables exist using names that match the POS code."""
        # Table for products (Matches image_560083.png requirement)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                price DECIMAL(10, 2) NOT NULL,
                stock INT DEFAULT 0,
                category_id INT
            )
        """)
        
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
        """Retrieves all products. Updated to query 'products' table."""
        self.cursor.execute("SELECT * FROM products")
        return self.cursor.fetchall()

    def fetch_sales(self):
        self.cursor.execute("SELECT * FROM sales ORDER BY id DESC")
        return self.cursor.fetchall()

    def update_stock(self, product_id, change):
        """Fixed query to use 'id' instead of 'product_id' to match schema."""
        query = "UPDATE products SET stock = stock + %s WHERE id = %s"
        self.cursor.execute(query, (change, product_id))
        self.db.commit()

    def add_sale(self, date, items, total):
        try:
            query = "INSERT INTO sales (date, items, total) VALUES (%s, %s, %s)"
            values = (date, items, total)
            self.cursor.execute(query, values)
            self.db.commit()
        except mysql.connector.Error as err:
            self.db.rollback()
            raise err

    def execute_query(self, query, params=None):
        """Helper for the Edit and Delete functions in MainApp."""
        self.cursor.execute(query, params or ())
        self.db.commit()

    def __del__(self):
        if hasattr(self, 'db') and self.db.is_connected():
            self.cursor.close()
            self.db.close()
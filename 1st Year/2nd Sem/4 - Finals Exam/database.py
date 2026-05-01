import mysql.connector

class DatabaseManager:
    """Handles all MySQL interactions (Encapsulation)."""
    def __init__(self):
        self.config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'root', # Update this to your MySQL password
            'database': 'cafe_management'
        }
    def fetch_transactions(self):
        cursor = self.connection.cursor()
    # Adjust table/column names to match your MySQL script
        cursor.execute("SELECT sale_date, item_name, quantity, total_price FROM transactions ORDER BY sale_date DESC")
        return cursor.fetchall()
    
    def _connect(self):
        return mysql.connector.connect(**self.config)

    # --- CATEGORY CRUD ---
    def fetch_categories(self):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM categories")
        result = cursor.fetchall()
        conn.close()
        return result

    def add_category(self, name):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO categories (category_name) VALUES (%s)", (name,))
        conn.commit()
        conn.close()

    # --- MENU ITEM CRUD ---
    def fetch_menu_items(self):
        conn = self._connect()
        cursor = conn.cursor()
        query = """
            SELECT m.item_id, m.item_name, m.price, m.stock_qty, c.category_name 
            FROM menu_items m 
            JOIN categories c ON m.category_id = c.category_id
        """
        cursor.execute(query)
        result = cursor.fetchall()
        conn.close()
        return result

    def add_item(self, name, price, stock, cat_id):
        conn = self._connect()
        cursor = conn.cursor()
        query = "INSERT INTO menu_items (item_name, price, stock_qty, category_id) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (name, price, stock, cat_id))
        conn.commit()
        conn.close()

    def update_item(self, item_id, name, price, stock):
        conn = self._connect()
        cursor = conn.cursor()
        query = "UPDATE menu_items SET item_name=%s, price=%s, stock_qty=%s WHERE item_id=%s"
        cursor.execute(query, (name, price, stock, item_id))
        conn.commit()
        conn.close()

    def delete_item(self, item_id):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM menu_items WHERE item_id = %s", (item_id,))
        conn.commit()
        conn.close()
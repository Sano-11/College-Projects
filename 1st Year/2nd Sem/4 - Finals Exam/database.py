import mysql.connector

class DatabaseManager:
    def __init__(self):
        self.config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'root', # Ensure this matches your MySQL password
            'database': 'cafe_management'
        }

    def _connect(self):
        return mysql.connector.connect(**self.config)

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

    def fetch_transactions(self):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT sale_date, item_name, quantity, total_price FROM transactions ORDER BY sale_date DESC")
        result = cursor.fetchall()
        conn.close()
        return result

    def add_item(self, name, price, stock, cat_id=1):
        conn = self._connect()
        cursor = conn.cursor()
        query = "INSERT INTO menu_items (item_name, price, stock_qty, category_id) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (name, price, stock, cat_id))
        conn.commit()
        conn.close()

    def update_item_full(self, item_id, name, price, stock):
        conn = self._connect()
        cursor = conn.cursor()
        query = "UPDATE menu_items SET item_name = %s, price = %s, stock_qty = %s WHERE item_id = %s"
        cursor.execute(query, (name, price, stock, item_id))
        conn.commit()
        conn.close()

    def record_sale(self, item_name, qty, total):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO transactions (item_name, quantity, total_price) VALUES (%s, %s, %s)", (item_name, qty, total))
        cursor.execute("UPDATE menu_items SET stock_qty = stock_qty - %s WHERE item_name = %s", (qty, item_name))
        conn.commit()
        conn.close()

    def delete_item(self, item_id):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM menu_items WHERE item_id = %s", (item_id,))
        conn.commit()
        conn.close()
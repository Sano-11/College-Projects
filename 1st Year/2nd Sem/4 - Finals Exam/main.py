import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from database import DatabaseManager

# =================================================================
# BUG FIX: LABEL DESTRUCTION (Python 3.13 Compatibility)
# =================================================================
def universal_safe_destroy(self):
    if not hasattr(self, '_font'): self._font = None
    try:
        if hasattr(self, "canvas"): self.canvas.delete(self.canvas_id)
        super(ctk.CTkLabel, self).destroy()
    except: pass
ctk.CTkLabel.destroy = universal_safe_destroy

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Bean & Brew POS System")
        self.withdraw()
        self.after(10, lambda: self.state('zoomed'))
        
        self.primary_green = "#276C4C"
        self.sidebar_white = "#FFFFFF"
        self.border_gray = "#D1D1D6"
        ctk.set_appearance_mode("light")
        
        self.db = DatabaseManager()
        self.cart = {} 
        self.nav_btns = {}

        self.grid_columnconfigure(0, weight=0) 
        self.grid_columnconfigure(1, weight=2) 
        self.grid_columnconfigure(2, weight=0, minsize=320) 
        self.grid_rowconfigure(0, weight=1)

        self.setup_sidebar()
        self.setup_cart_panel()
        
        self.container = ctk.CTkScrollableFrame(self, fg_color="transparent", corner_radius=0)
        self.container.grid(row=0, column=1, sticky="nsew", padx=20, pady=30)

        self.show_dashboard()
        self.deiconify()

    def setup_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=220, fg_color=self.sidebar_white, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        ctk.CTkLabel(self.sidebar, text="☕\nBEAN & BREW", font=("SF Pro Display", 26, "bold"), 
                    text_color=self.primary_green).pack(pady=(60, 50))

        menu_items = [("Dashboard", "show_dashboard", "🏠"), 
                     ("Inventory Manager", "show_inventory_manager", "📦"), 
                     ("Transaction Records", "show_sales_history", "📋")]

        for text, func, icon in menu_items:
            btn = ctk.CTkButton(self.sidebar, text=f"  {icon}  {text}", height=50, corner_radius=10,
                                fg_color="transparent", text_color="#1C1C1E", font=("SF Pro Text", 14, "bold"), 
                                anchor="w", command=getattr(self, func))
            btn.pack(pady=5, padx=15, fill="x")
            self.nav_btns[text] = btn

    def setup_cart_panel(self):
        self.cart_panel = ctk.CTkFrame(self, fg_color=self.sidebar_white, corner_radius=0, border_width=1, border_color=self.border_gray)
        self.cart_panel.grid(row=0, column=2, sticky="nsew")
        
        ctk.CTkLabel(self.cart_panel, text="Current Order", font=("SF Pro Display", 22, "bold")).pack(pady=(40, 20))
        self.cart_scroll = ctk.CTkScrollableFrame(self.cart_panel, fg_color="transparent")
        self.cart_scroll.pack(fill="both", expand=True, padx=10)
        
        footer = ctk.CTkFrame(self.cart_panel, fg_color="transparent")
        footer.pack(fill="x", side="bottom", padx=20, pady=30)
        self.total_lbl = ctk.CTkLabel(footer, text="Total: ₱0.00", font=("SF Pro Text", 28, "bold"), text_color=self.primary_green)
        self.total_lbl.pack(pady=(0, 20))
        ctk.CTkButton(footer, text="Checkout", height=60, corner_radius=30, fg_color=self.primary_green, 
                      font=("SF Pro Text", 16, "bold"), command=self.process_checkout).pack(fill="x")

    def show_dashboard(self):
        self.clear_view()
        self.update_nav("Dashboard")
        
        pill_container = ctk.CTkFrame(self.container, fg_color="transparent")
        pill_container.pack(fill="x", pady=(10, 40))
        header_pill = ctk.CTkFrame(pill_container, fg_color=self.primary_green, corner_radius=50, height=120)
        header_pill.pack(expand=True)
        ctk.CTkLabel(header_pill, text="MENU DASHBOARD", font=("SF Pro Display", 44, "bold"), text_color="white").pack(padx=120, pady=30)
        
        grid_main = ctk.CTkFrame(self.container, fg_color="transparent")
        grid_main.pack(fill="both", expand=True)
        grid_main.columnconfigure((0, 1, 2, 3), weight=1)
        
        items = self.db.fetch_menu_items() 
        for i, item in enumerate(items):
            card = ctk.CTkFrame(grid_main, height=340, fg_color=self.sidebar_white, corner_radius=25, border_width=1, border_color=self.border_gray)
            card.grid(row=i//4, column=i%4, padx=10, pady=10, sticky="nsew")
            card.grid_propagate(False)
            
            ctk.CTkLabel(card, text=item[1], font=("SF Pro Text", 18, "bold"), wraplength=150).pack(pady=(35, 5))
            ctk.CTkLabel(card, text=f"₱{item[2]:.2f}", font=("SF Pro Text", 16), text_color=self.primary_green).pack()
            ctk.CTkLabel(card, text=f"Stock: {item[3]}", text_color="gray", font=("SF Pro Text", 12)).pack(pady=5)
            
            btn_state = "normal" if item[3] > 0 else "disabled"
            ctk.CTkButton(card, text="Add to Order" if item[3] > 0 else "Out of Stock", fg_color=self.primary_green, 
                          corner_radius=15, height=40, state=btn_state, font=("SF Pro Text", 13, "bold"),
                          command=lambda n=item[1], p=item[2]: self.add_to_cart(n, p)).pack(side="bottom", pady=25, padx=20, fill="x")

    def show_inventory_manager(self):
        self.clear_view()
        self.update_nav("Inventory Manager")
        ctk.CTkLabel(self.container, text="Inventory Database", font=("SF Pro Display", 32, "bold")).pack(anchor="w", padx=10, pady=(0, 25))
        
        # Add Item Form
        form = ctk.CTkFrame(self.container, fg_color=self.sidebar_white, corner_radius=15, border_width=1, border_color=self.border_gray)
        form.pack(fill="x", padx=10, pady=(0, 20))
        row_in = ctk.CTkFrame(form, fg_color="transparent")
        row_in.pack(fill="x", padx=20, pady=20)
        
        e_n = ctk.CTkEntry(row_in, placeholder_text="Product Name", width=250, height=40)
        e_n.pack(side="left", padx=5)
        e_p = ctk.CTkEntry(row_in, placeholder_text="Price", width=100, height=40)
        e_p.pack(side="left", padx=5)
        e_s = ctk.CTkEntry(row_in, placeholder_text="Stock", width=100, height=40)
        e_s.pack(side="left", padx=5)
        
        def save():
            if e_n.get():
                try:
                    self.db.add_item(e_n.get(), float(e_p.get() or 0), int(e_s.get() or 0))
                    self.show_inventory_manager()
                except ValueError:
                    messagebox.showerror("Error", "Please enter valid numbers for Price and Stock")
        
        ctk.CTkButton(row_in, text="Add Item", fg_color=self.primary_green, width=120, height=40, font=("SF Pro Text", 14, "bold"), command=save).pack(side="left", padx=10)

        # Item List
        for item in self.db.fetch_menu_items():
            row = ctk.CTkFrame(self.container, fg_color=self.sidebar_white, height=85, corner_radius=12, border_width=1, border_color=self.border_gray)
            row.pack(fill="x", padx=10, pady=6)
            row.grid_propagate(False)
            
            # Configure columns for alignment
            row.grid_columnconfigure(1, weight=1) # Item name takes up remaining space
            row.grid_columnconfigure(4, minsize=100) # Fixed space for buttons
            row.grid_columnconfigure(5, minsize=100)

            # ID and Name
            ctk.CTkLabel(row, text=f"#{item[0]}", text_color="gray", width=50).grid(row=0, column=0, padx=(20, 10), pady=25)
            ctk.CTkLabel(row, text=item[1], font=("SF Pro Text", 16, "bold"), anchor="w").grid(row=0, column=1, sticky="w")
            
            # Price and Stock
            ctk.CTkLabel(row, text=f"₱{item[2]:.2f}", text_color=self.primary_green, font=("SF Pro Text", 16, "bold"), width=100).grid(row=0, column=2, padx=10)
            ctk.CTkLabel(row, text=f"Stock: {item[3]}", width=100).grid(row=0, column=3, padx=10)
            
            # Action Buttons (Now both clearly visible and aligned)
            ctk.CTkButton(row, text="Edit", fg_color="#FF9500", width=80, height=35, 
                          command=lambda v=item: self.open_edit_popup(v)).grid(row=0, column=4, padx=5)
            
            ctk.CTkButton(row, text="Remove", fg_color="#FF3B30", width=80, height=35, 
                          command=lambda i=item[0]: [self.db.delete_item(i), self.show_inventory_manager()]).grid(row=0, column=5, padx=(5, 20))
    def show_sales_history(self):
        self.clear_view(); self.update_nav("Transaction Records")
        ctk.CTkLabel(self.container, text="Transaction Records", font=("SF Pro Display", 32, "bold")).pack(anchor="w", padx=10, pady=(0, 25))
        
        # TABLE HEADER
        header = ctk.CTkFrame(self.container, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(0, 10))
        ctk.CTkLabel(header, text="Date", font=("SF Pro Text", 12, "bold"), text_color="gray", width=150, anchor="w").pack(side="left", padx=10)
        ctk.CTkLabel(header, text="Order/Items", font=("SF Pro Text", 12, "bold"), text_color="gray", anchor="w").pack(side="left", expand=True, fill="x", padx=10)
        ctk.CTkLabel(header, text="Price", font=("SF Pro Text", 12, "bold"), text_color="gray", width=80).pack(side="left", padx=10)
        ctk.CTkLabel(header, text="Qty", font=("SF Pro Text", 12, "bold"), text_color="gray", width=60).pack(side="left", padx=10)
        ctk.CTkLabel(header, text="Total", font=("SF Pro Text", 12, "bold"), text_color="gray", width=100, anchor="e").pack(side="left", padx=25)

        # LATEST FIRST: Grouping transactions by timestamp (simulating orders)
        transactions = self.db.fetch_transactions()
        orders = {}
        for s in transactions:
            timestamp = s[0]
            if timestamp not in orders: orders[timestamp] = []
            orders[timestamp].append(s)

        # Reverse keys to get latest date first
        sorted_times = sorted(orders.keys(), reverse=True)
        
        for idx, t in enumerate(sorted_times):
            order_num = len(sorted_times) - idx
            order_items = orders[t]
            
            # Card for the Order
            card = ctk.CTkFrame(self.container, fg_color=self.sidebar_white, corner_radius=12, border_width=1, border_color=self.border_gray)
            card.pack(fill="x", padx=10, pady=8)
            
            # Order Title Row
            title_row = ctk.CTkFrame(card, fg_color="transparent")
            title_row.pack(fill="x", padx=15, pady=(15, 5))
            ctk.CTkLabel(title_row, text=f"📅 {t}", width=150, anchor="w", text_color="gray").pack(side="left")
            ctk.CTkLabel(title_row, text=f"Order #{order_num}", font=("SF Pro Text", 18, "bold")).pack(side="left", padx=10)
            
            # Items List within Order
            for item in order_items:
                item_row = ctk.CTkFrame(card, fg_color="transparent")
                item_row.pack(fill="x", padx=15, pady=2)
                
                ctk.CTkLabel(item_row, text="", width=150).pack(side="left") # Spacer for date align
                ctk.CTkLabel(item_row, text=f"• {item[1]}", font=("SF Pro Text", 15), anchor="w").pack(side="left", expand=True, fill="x", padx=10)
                
                # Calculation (Assumes DB: [0]Date, [1]Name, [2]Qty, [3]Total_Paid)
                # We calculate individual price: Total_Paid / Qty
                unit_price = item[3] / item[2] if item[2] > 0 else 0
                
                ctk.CTkLabel(item_row, text=f"₱{unit_price:.2f}", width=80).pack(side="left", padx=10)
                ctk.CTkLabel(item_row, text=f"x{item[2]}", width=60).pack(side="left", padx=10)
                ctk.CTkLabel(item_row, text=f"₱{item[3]:.2f}", text_color=self.primary_green, font=("SF Pro Text", 15, "bold"), width=100, anchor="e").pack(side="left", padx=(10, 25))

    def open_edit_popup(self, item):
        pop = ctk.CTkToplevel(self); pop.title("Edit Item"); pop.geometry("400x480"); pop.attributes("-topmost", True)
        ctk.CTkLabel(pop, text="Update Product", font=("SF Pro Display", 20, "bold")).pack(pady=30)
        en = ctk.CTkEntry(pop, width=300, height=45); en.insert(0, item[1]); en.pack(pady=10)
        ep = ctk.CTkEntry(pop, width=300, height=45); ep.insert(0, item[2]); ep.pack(pady=10)
        es = ctk.CTkEntry(pop, width=300, height=45); es.insert(0, item[3]); es.pack(pady=10)
        def update():
            self.db.update_item_full(item[0], en.get(), float(ep.get()), int(es.get()))
            pop.destroy(); self.show_inventory_manager()
        ctk.CTkButton(pop, text="Update", fg_color=self.primary_green, height=50, width=200, command=update).pack(pady=30)

    def update_cart_ui(self):
        for widget in self.cart_scroll.winfo_children(): widget.destroy()
        grand_total = 0
        for name, data in self.cart.items():
            price, qty = data['price'], data['qty']
            grand_total += price * qty
            row = ctk.CTkFrame(self.cart_scroll, fg_color="#F2F2F7", corner_radius=12, height=70)
            row.pack(fill="x", pady=4, padx=2); row.pack_propagate(False)
            ctrl = ctk.CTkFrame(row, fg_color="transparent")
            ctrl.pack(side="left", padx=5)
            ctk.CTkButton(ctrl, text="-", width=24, height=24, fg_color="#D1D1D6", text_color="black", command=lambda n=name: self.change_qty(n, -1)).pack(side="left", padx=1)
            ctk.CTkLabel(ctrl, text=str(qty), font=("SF Pro Text", 12, "bold"), width=20).pack(side="left")
            ctk.CTkButton(ctrl, text="+", width=24, height=24, fg_color="#D1D1D6", text_color="black", command=lambda n=name: self.change_qty(n, 1)).pack(side="left", padx=1)
            ctk.CTkLabel(row, text=name, font=("SF Pro Text", 12), wraplength=100, justify="left").pack(side="left", padx=5)
            ctk.CTkLabel(row, text=f"₱{price*qty:.0f}", font=("SF Pro Text", 12, "bold"), text_color=self.primary_green).pack(side="right", padx=8)
        self.total_lbl.configure(text=f"Total: ₱{grand_total:.2f}")

    def change_qty(self, name, delta):
        if name in self.cart:
            self.cart[name]['qty'] += delta
            if self.cart[name]['qty'] <= 0: del self.cart[name]
            self.update_cart_ui()

    def add_to_cart(self, name, price):
        if name in self.cart: self.cart[name]['qty'] += 1
        else: self.cart[name] = {'price': price, 'qty': 1}
        self.update_cart_ui()

    def clear_view(self):
        for child in self.container.winfo_children(): child.destroy()
        self.container._parent_canvas.yview_moveto(0)

    def update_nav(self, active_text):
        for name, btn in self.nav_btns.items():
            btn.configure(fg_color=self.primary_green if name == active_text else "transparent", 
                          text_color="white" if name == active_text else "#1C1C1E")

    def process_checkout(self):
        if not self.cart: return
        # Logic to ensure all items in a single checkout share the exact same timestamp
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for name, data in self.cart.items():
            self.db.record_sale(name, data['qty'], data['price'] * data['qty'], now)
        self.cart = {}; self.update_cart_ui()
        messagebox.showinfo("Success", "Order Finalized!")
        self.show_dashboard()

    def record_sale(self, name, qty, total, time_str): # Now accepts 5 (self + 4)
        self.cursor.execute("INSERT INTO transactions VALUES (?, ?, ?, ?)", (time_str, name, qty, total))
        self.cursor.execute("UPDATE menu SET stock = stock - ? WHERE name = ?", (qty, name))
        self.conn.commit()

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from database import DatabaseManager

# =================================================================
# BUG FIX: LABEL DESTRUCTION (Python 3.13 Compatibility)
# =================================================================
def universal_safe_destroy(self):
    if not hasattr(self, '_font'): 
        self._font = None
    try:
        if hasattr(self, "canvas"): 
            self.canvas.delete(self.canvas_id)
        super(ctk.CTkLabel, self).destroy()
    except: 
        pass
ctk.CTkLabel.destroy = universal_safe_destroy

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Bean & Brew POS System")
        self.withdraw()
        self.after(10, lambda: self.state('zoomed'))
        
        # UI Constants
        self.primary_green = "#276C4C"
        self.sidebar_white = "#FFFFFF"
        self.border_gray = "#D1D1D6"
        ctk.set_appearance_mode("light")
        
        # Category Definitions
        self.categories = {
            1: "Espresso Drinks",
            2: "Non-Caffeine",
            3: "Pastries",
            4: "Signature Cold Brew",
            5: "Iced Refreshers"
        }
        
        # Initialize Logic
        self.db = DatabaseManager()
        self.cart = {} 
        self.nav_btns = {}
        
        # Dropdown state: False means start collapsed[cite: 1]
        self.expanded_categories = {cat_id: False for cat_id in self.categories.keys()}

        # Layout Configuration
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

    def create_section_header(self, text):
        """Creates a centered pill with a fixed width and left-aligned text."""
        pill_container = ctk.CTkFrame(self.container, fg_color="transparent")
        pill_container.pack(fill="x", pady=(10, 40))
        
        # Fixed width (e.g., 800) ensures consistency across all pages
        header_pill = ctk.CTkFrame(pill_container, 
                                   fg_color=self.primary_green, 
                                   corner_radius=50, 
                                   height=120, 
                                   width=800)
        header_pill.pack(expand=True) # Keeps the pill itself centered in the view
        header_pill.pack_propagate(False) # Prevents the pill from shrinking to the text size
        
        # anchor="w" (West) aligns the text to the left within the fixed-width pill
        ctk.CTkLabel(header_pill, 
                    text=text, 
                    font=("SF Pro Display", 44, "bold"), 
                    text_color="white",
                    anchor="w").pack(fill="both", expand=True, padx=60)
        
    def show_dashboard(self):
        self.clear_view()
        self.update_nav("Dashboard")
        self.create_section_header("MENU DASHBOARD") #[cite: 1]
        
        items = self.db.fetch_menu_items()
        for cat_id, cat_name in self.categories.items():
            cat_items = [item for item in items if item[4] == cat_id]
            if not cat_items: continue

            # Category Visual Separator[cite: 1]
            header_frame = ctk.CTkFrame(self.container, fg_color="transparent")
            header_frame.pack(fill="x", pady=(20, 10))
            ctk.CTkLabel(header_frame, text=cat_name, font=("SF Pro Display", 24, "bold"), 
                        text_color=self.primary_green).pack(side="left", padx=10)
            ctk.CTkFrame(header_frame, fg_color=self.border_gray, height=2).pack(side="left", fill="x", expand=True, padx=10)

            grid_main = ctk.CTkFrame(self.container, fg_color="transparent")
            grid_main.pack(fill="both", expand=True, padx=10, pady=5)
            grid_main.columnconfigure((0, 1, 2, 3), weight=1)
            
            for i, item in enumerate(cat_items):
                card = ctk.CTkFrame(grid_main, height=340, fg_color=self.sidebar_white, 
                                   corner_radius=25, border_width=1, border_color=self.border_gray)
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
        self.create_section_header("INVENTORY DATABASE") #[cite: 1]
        
        items = self.db.fetch_menu_items()
        for cat_id, cat_name in self.categories.items():
            cat_items = [item for item in items if item[4] == cat_id]
            if not cat_items: continue
                
            is_expanded = self.expanded_categories.get(cat_id, False) #[cite: 1]
            icon = "▼" if is_expanded else "▶"
            
            # Clickable Dropdown Header[cite: 1]
            header_btn = ctk.CTkButton(self.container, text=f"{icon}  {cat_name.upper()}", 
                                      font=("SF Pro Text", 14, "bold"), fg_color="#F2F2F7",
                                      text_color="#1C1C1E", hover_color=self.border_gray, height=45,
                                      anchor="w", corner_radius=8, command=lambda c=cat_id: self.toggle_category(c))
            header_btn.pack(fill="x", padx=10, pady=(10, 2))

            if is_expanded:
                item_container = ctk.CTkFrame(self.container, fg_color="transparent")
                item_container.pack(fill="x", padx=10, pady=0)
                for item in cat_items:
                    row = ctk.CTkFrame(item_container, fg_color=self.sidebar_white, height=85, 
                                       corner_radius=12, border_width=1, border_color=self.border_gray)
                    row.pack(fill="x", pady=4); row.pack_propagate(False)
                    row.grid_columnconfigure(1, weight=1)

                    ctk.CTkLabel(row, text=f"#{item[0]}", text_color="gray", width=50).pack(side="left", padx=20)
                    ctk.CTkLabel(row, text=item[1], font=("SF Pro Text", 16, "bold")).pack(side="left", padx=10)
                    ctk.CTkLabel(row, text=f"₱{item[2]:.2f}", text_color=self.primary_green, font=("SF Pro Text", 16, "bold")).pack(side="left", padx=30)
                    ctk.CTkLabel(row, text=f"Stock: {item[3]}", width=100).pack(side="left", padx=10)
                    
                    ctk.CTkButton(row, text="Remove", fg_color="#FF3B30", width=80, height=35, 
                                  command=lambda i=item[0]: [self.db.delete_item(i), self.show_inventory_manager()]).pack(side="right", padx=20)
                    ctk.CTkButton(row, text="Edit", fg_color="#FF9500", width=80, height=35, 
                                  command=lambda v=item: self.open_edit_popup(v)).pack(side="right", padx=5)

    def toggle_category(self, cat_id):
        self.expanded_categories[cat_id] = not self.expanded_categories.get(cat_id, False) #[cite: 1]
        self.show_inventory_manager()

    def show_sales_history(self):
        self.clear_view()
        self.update_nav("Transaction Records")
        self.create_section_header("TRANSACTION RECORDS") #[cite: 1]
        
        transactions = self.db.fetch_transactions()
        orders = {}
        for s in transactions:
            timestamp = s[0]
            if timestamp not in orders: orders[timestamp] = []
            orders[timestamp].append(s)

        for idx, t in enumerate(sorted(orders.keys(), reverse=True)):
            card = ctk.CTkFrame(self.container, fg_color=self.sidebar_white, corner_radius=12, border_width=1, border_color=self.border_gray)
            card.pack(fill="x", padx=10, pady=8)
            title_row = ctk.CTkFrame(card, fg_color="transparent")
            title_row.pack(fill="x", padx=15, pady=15)
            ctk.CTkLabel(title_row, text=f"📅 {t}", width=150, anchor="w", text_color="gray").pack(side="left")
            ctk.CTkLabel(title_row, text=f"Order Detail", font=("SF Pro Text", 18, "bold")).pack(side="left", padx=10)
            
            for item in orders[t]:
                item_row = ctk.CTkFrame(card, fg_color="transparent")
                item_row.pack(fill="x", padx=15, pady=2)
                ctk.CTkLabel(item_row, text=f"• {item[1]}", font=("SF Pro Text", 15), anchor="w").pack(side="left", expand=True, fill="x", padx=160)
                ctk.CTkLabel(item_row, text=f"x{item[2]}", width=60).pack(side="left", padx=10)
                ctk.CTkLabel(item_row, text=f"₱{item[3]:.2f}", text_color=self.primary_green, font=("SF Pro Text", 15, "bold"), width=100).pack(side="left")

    def open_edit_popup(self, item):
        pop = ctk.CTkToplevel(self); pop.title("Edit Item"); pop.geometry("400x480"); pop.attributes("-topmost", True)
        ctk.CTkLabel(pop, text="Update Product", font=("SF Pro Display", 20, "bold")).pack(pady=30)
        en = ctk.CTkEntry(pop, width=300, height=45); en.insert(0, item[1]); en.pack(pady=10)
        ep = ctk.CTkEntry(pop, width=300, height=45); ep.insert(0, str(item[2])); ep.pack(pady=10)
        es = ctk.CTkEntry(pop, width=300, height=45); es.insert(0, str(item[3])); es.pack(pady=10)
        def update():
            self.db.update_item_full(item[0], en.get(), float(ep.get()), int(es.get()))
            pop.destroy(); self.show_inventory_manager()
        ctk.CTkButton(pop, text="Update", fg_color=self.primary_green, height=50, width=200, command=update).pack(pady=30)

    def process_checkout(self):
        if not self.cart: return
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for name, data in self.cart.items():
            self.db.record_sale(name, data['qty'], data['price'] * data['qty'], now)
        self.cart = {}; self.update_cart_ui()
        messagebox.showinfo("Success", "Order Finalized!"); self.show_dashboard()

    def update_cart_ui(self):
        for widget in self.cart_scroll.winfo_children(): widget.destroy()
        grand_total = 0
        for name, data in self.cart.items():
            price, qty = data['price'], data['qty']
            grand_total += price * qty
            row = ctk.CTkFrame(self.cart_scroll, fg_color="#F2F2F7", corner_radius=12, height=70)
            row.pack(fill="x", pady=4, padx=2); row.pack_propagate(False)
            ctk.CTkLabel(row, text=name, font=("SF Pro Text", 12), wraplength=100).pack(side="left", padx=10)
            ctk.CTkLabel(row, text=f"x{qty}", font=("SF Pro Text", 12, "bold")).pack(side="left", padx=5)
            ctk.CTkLabel(row, text=f"₱{price*qty:.0f}", font=("SF Pro Text", 12, "bold"), text_color=self.primary_green).pack(side="right", padx=8)
        self.total_lbl.configure(text=f"Total: ₱{grand_total:.2f}")

    def add_to_cart(self, name, price):
        if name in self.cart: self.cart[name]['qty'] += 1
        else: self.cart[name] = {'price': price, 'qty': 1}
        self.update_cart_ui()

    def clear_view(self):
        for child in self.container.winfo_children(): child.destroy()
        self.container._parent_canvas.yview_moveto(0)

    def update_nav(self, active_text):
        for name, btn in self.nav_btns.items():
            is_active = (name == active_text)
            btn.configure(fg_color=self.primary_green if is_active else "transparent", 
                          text_color="white" if is_active else "#1C1C1E")

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
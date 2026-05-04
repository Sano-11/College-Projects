import customtkinter as ctk
from tkinter import messagebox, simpledialog
from datetime import datetime
from database import DatabaseManager

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Window Configuration & Scaling
        self.title("Bean & Brew POS System | MSEUF CS Project")
        self.withdraw()
        self.after(10, lambda: self.state('zoomed'))
        
        # Theme & Styling Constants
        self.primary_green = "#276C4C"
        self.bg_gray = "#F2F2F7" 
        self.border_gray = "#D1D1D6"
        self.tax_rate = 0.12 
        self.b_width = 3 # Global Border Width requirement
        
        ctk.set_appearance_mode("light")
        self.configure(fg_color=self.bg_gray)
        
        # Data & State Management
        self.db = DatabaseManager()
        self.cart = {} 
        self.nav_btns = {}
        self.categories = {
            1: "Espresso Drinks", 
            2: "Non-Caffeine", 
            3: "Pastries", 
            4: "Signature Cold Brew", 
            5: "Iced Refreshers"
        }
        self.expanded_categories = {cat_id: False for cat_id in self.categories.keys()}
        self.current_filter = "All"

        # Main Layout Configuration
        self.grid_columnconfigure(0, weight=0, minsize=260) 
        self.grid_columnconfigure(1, weight=1) 
        self.grid_columnconfigure(2, weight=0, minsize=340) 
        self.grid_rowconfigure(0, weight=1)

        self.setup_sidebar()
        
        # Main Content Scrollable Container
        self.container = ctk.CTkScrollableFrame(self, fg_color="transparent", corner_radius=0)
        self.container.grid(row=0, column=1, sticky="nsew", padx=20, pady=30)
        
        self.setup_cart_panel() 
        self.show_dashboard()
        self.deiconify()

    def setup_sidebar(self):
        """Builds the primary navigation sidebar."""
        self.sidebar = ctk.CTkFrame(self, width=260, fg_color="white", corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.logo_label = ctk.CTkLabel(
            self.sidebar, 
            text="☕\nBEAN & BREW", 
            font=("SF Pro Display", 26, "bold"), 
            text_color=self.primary_green
        )
        self.logo_label.pack(pady=(60, 50))

        menu_items = [
            ("Dashboard", "show_dashboard", "🏠"), 
            ("Inventory Manager", "show_inventory_manager", "📦"), 
            ("Transaction Records", "show_sales_history", "📋")
        ]
        
        for text, func, icon in menu_items:
            btn = ctk.CTkButton(
                self.sidebar, text=f"  {icon}  {text}", height=55, corner_radius=12, 
                fg_color="transparent", text_color="#1C1C1E", font=("SF Pro Text", 15, "bold"), 
                anchor="w", command=getattr(self, func)
            )
            btn.pack(pady=5, padx=20, fill="x")
            self.nav_btns[text] = btn

        self.logout_btn = ctk.CTkButton(
            self.sidebar, text="  🚪  Logout Admin", height=50, corner_radius=12, 
            fg_color="#FFE5E5", text_color="#FF3B30", font=("SF Pro Text", 14, "bold"), 
            hover_color="#FFD1D1", command=self.quit
        )
        self.logout_btn.pack(side="bottom", pady=30, padx=20, fill="x")

    def setup_cart_panel(self):
        """Builds the 340px thin rounded cart panel."""
        wrapper = ctk.CTkFrame(self, fg_color="transparent")
        wrapper.grid(row=0, column=2, sticky="nsew", padx=(0, 20), pady=30)
        
        self.cart_panel = ctk.CTkFrame(
            wrapper, fg_color="white", corner_radius=30, 
            border_width=self.b_width, border_color=self.border_gray
        )
        self.cart_panel.pack(fill="both", expand=True)
        
        ctk.CTkLabel(self.cart_panel, text="🛒 Current Order", font=("SF Pro Display", 22, "bold")).pack(pady=(30, 15))
        self.cart_scroll = ctk.CTkScrollableFrame(self.cart_panel, fg_color="transparent")
        self.cart_scroll.pack(fill="both", expand=True, padx=10)
        
        footer = ctk.CTkFrame(self.cart_panel, fg_color="transparent")
        footer.pack(fill="x", side="bottom", padx=20, pady=25)
        
        self.tax_lbl = ctk.CTkLabel(footer, text="Tax (12%): ₱0.00", font=("SF Pro", 13), text_color="#8E8E93")
        self.tax_lbl.pack(anchor="w")
        self.total_lbl = ctk.CTkLabel(footer, text="₱0.00", font=("SF Pro", 28, "bold"), text_color=self.primary_green)
        self.total_lbl.pack(pady=(2, 15), anchor="w")
        
        ctk.CTkButton(
            footer, text="Complete Checkout", height=55, corner_radius=15, 
            fg_color=self.primary_green, font=("SF Pro Text", 15, "bold"), command=self.checkout
        ).pack(fill="x")

    def show_dashboard(self, filter_text=""):
        self.clear_view()
        self.update_nav("Dashboard")
        
        h = ctk.CTkFrame(self.container, fg_color="transparent")
        h.pack(fill="x", pady=(10, 25), padx=10)
        ctk.CTkLabel(h, text="Welcome back, Admin! 👋", font=("SF Pro Text", 14), text_color="gray").pack(anchor="w")
        ctk.CTkLabel(h, text="Menu Dashboard", font=("SF Pro Display", 38, "bold")).pack(anchor="w")
        
        row_search = ctk.CTkFrame(self.container, fg_color="transparent")
        row_search.pack(fill="x", padx=10, pady=(0, 20))
        
        self.dash_search = ctk.CTkEntry(row_search, placeholder_text="🔍 Search products...", height=45, corner_radius=12, border_width=self.b_width)
        self.dash_search.pack(side="left", fill="x", expand=True, padx=(0, 10))
        if filter_text: self.dash_search.insert(0, filter_text)
        self.dash_search.bind("<KeyRelease>", lambda e: self.show_dashboard(self.dash_search.get()))

        ctk.CTkButton(
            row_search, text="▽", width=45, height=45, corner_radius=12, 
            fg_color="white", border_width=self.b_width, border_color=self.border_gray, 
            text_color="black", command=self.open_filter_menu
        ).pack(side="right")

        items = self.db.fetch_menu_items()
        for cat_id, cat_name in self.categories.items():
            if self.current_filter != "All" and cat_name != self.current_filter: continue
            cat_items = [i for i in items if i[4] == cat_id and filter_text.lower() in i[1].lower()]
            if not cat_items: continue
            
            ctk.CTkLabel(self.container, text=f"☕ {cat_name}", font=("SF Pro Display", 20, "bold")).pack(anchor="w", padx=10, pady=(15, 5))
            grid = ctk.CTkFrame(self.container, fg_color="transparent")
            grid.pack(fill="x", padx=10)
            grid.columnconfigure((0, 1, 2), weight=1)
            
            for i, item in enumerate(cat_items):
                card = ctk.CTkFrame(grid, height=230, fg_color="white", corner_radius=15, border_width=self.b_width, border_color=self.border_gray)
                card.grid(row=i//3, column=i%3, padx=8, pady=8, sticky="nsew")
                card.grid_propagate(False)
                
                stock_color = "#FF3B30" if item[3] <= 5 else "#8E8E93"
                ctk.CTkLabel(card, text=f"Stock: {item[3]}", font=("SF Pro", 10, "bold"), text_color=stock_color).pack(anchor="e", padx=12, pady=(10, 0))
                ctk.CTkLabel(card, text=item[1], font=("SF Pro", 16, "bold"), wraplength=140).pack(pady=(10, 2))
                ctk.CTkLabel(card, text=f"₱{float(item[2]):,.2f}", font=("SF Pro", 14)).pack()
                
                ctk.CTkButton(
                    card, text="Add to Order", height=35, 
                    fg_color=self.primary_green if item[3] > 0 else "#D1D1D6", 
                    state="normal" if item[3] > 0 else "disabled", command=lambda n=item[1], p=item[2], i=item[0]: self.update_cart(n, p, 1, i)
                ).pack(side="bottom", pady=15, padx=15, fill="x")

    def show_inventory_manager(self, filter_text=""):
        self.clear_view()
        self.update_nav("Inventory Manager")
        ctk.CTkLabel(self.container, text="Inventory Database", font=("SF Pro Display", 38, "bold")).pack(anchor="w", padx=10, pady=(10, 20))
        
        self.inv_search = ctk.CTkEntry(self.container, placeholder_text="🔍 Search inventory...", height=45, corner_radius=12, border_width=self.b_width)
        self.inv_search.pack(fill="x", padx=10, pady=(0, 20))
        if filter_text: self.inv_search.insert(0, filter_text)
        self.inv_search.bind("<KeyRelease>", lambda e: self.show_inventory_manager(self.inv_search.get()))

        items = self.db.fetch_menu_items()
        for cat_id, cat_name in self.categories.items():
            cat_items = [i for i in items if i[4] == cat_id and filter_text.lower() in i[1].lower()]
            if not cat_items: continue
            
            is_exp = self.expanded_categories[cat_id]
            ctk.CTkButton(
                self.container, text=f"{'▼' if is_exp else '▶'}  {cat_name}", 
                font=("SF Pro", 16, "bold"), fg_color="transparent", text_color="black", 
                anchor="w", command=lambda c=cat_id: self.toggle_category(c)
            ).pack(fill="x", padx=10, pady=5)
            
            if is_exp:
                tbl = ctk.CTkFrame(self.container, fg_color="white", corner_radius=15, border_width=self.b_width, border_color=self.border_gray)
                tbl.pack(fill="x", padx=10, pady=5)
                for item in cat_items:
                    row = ctk.CTkFrame(tbl, fg_color="transparent", height=70)
                    row.pack(fill="x", padx=15, pady=8)
                    ctk.CTkLabel(row, text=item[1], font=("SF Pro", 14, "bold"), width=180, anchor="w").pack(side="left")
                    
                    s_ctrl = ctk.CTkFrame(row, fg_color="transparent")
                    s_ctrl.pack(side="left", padx=10)
                    ctk.CTkButton(s_ctrl, text="-", width=30, height=30, fg_color=self.primary_green, command=lambda i=item: self.adjust_stock(i[0], -1)).pack(side="left", padx=2)
                    ctk.CTkLabel(s_ctrl, text=str(item[3]), width=40, font=("SF Pro", 14, "bold")).pack(side="left")
                    ctk.CTkButton(s_ctrl, text="+", width=30, height=30, fg_color=self.primary_green, command=lambda i=item: self.adjust_stock(i[0], 1)).pack(side="left", padx=2)
                    
                    ctk.CTkButton(row, text="Edit", width=60, height=30, fg_color="#E5E5E7", text_color="black", command=lambda i=item: self.edit_item(i)).pack(side="right", padx=5)
                    ctk.CTkButton(row, text="Del", width=60, height=30, fg_color="#FF3B30", command=lambda i=item[0]: self.delete_item(i)).pack(side="right", padx=5)

    def show_sales_history(self):
        self.clear_view()
        self.update_nav("Transaction Records")
        ctk.CTkLabel(self.container, text="Transaction History", font=("SF Pro Display", 38, "bold")).pack(anchor="w", padx=10, pady=(10, 25))
        
        sales = self.db.fetch_sales()
        for sale in sales:
            pill = ctk.CTkFrame(self.container, fg_color="white", corner_radius=15, border_width=self.b_width, border_color=self.border_gray)
            pill.pack(fill="x", padx=10, pady=8)
            head = ctk.CTkFrame(pill, fg_color="#F8F8F8", height=40)
            head.pack(fill="x", padx=2, pady=2)
            ctk.CTkLabel(head, text=f"Order #{sale[0]}", font=("SF Pro", 12, "bold")).pack(side="left", padx=15)
            ctk.CTkLabel(head, text=sale[1], font=("SF Pro", 11), text_color="gray").pack(side="right", padx=15)
            ctk.CTkLabel(pill, text=sale[2], font=("SF Pro", 14), wraplength=550, justify="left").pack(anchor="w", padx=20, pady=10)
            ctk.CTkLabel(pill, text=f"Total: ₱{sale[3]:,.2f}", font=("SF Pro", 18, "bold"), text_color=self.primary_green).pack(anchor="e", padx=20, pady=(0, 10))

    def render_cart(self):
        for widget in self.cart_scroll.winfo_children(): widget.destroy()
        subtotal = 0.0
        for name, data in self.cart.items():
            row = ctk.CTkFrame(self.cart_scroll, fg_color="#F8F8F8", corner_radius=12, border_width=self.b_width, border_color="#E5E5E5")
            row.pack(fill="x", pady=4, padx=5)
            ctk.CTkButton(row, text="🗑️", width=30, height=30, fg_color="transparent", text_color="#FF3B30", command=lambda n=name: self.delete_from_cart(n)).pack(side="left", padx=8)
            
            info = ctk.CTkFrame(row, fg_color="transparent")
            info.pack(side="left", fill="both", expand=True, padx=5, pady=8)
            ctk.CTkLabel(info, text=name, font=("SF Pro", 12, "bold"), anchor="w").pack(fill="x")
            ctk.CTkLabel(info, text=f"₱{data['price']:,.2f}", font=("SF Pro", 11), text_color=self.primary_green, anchor="w").pack(fill="x")
            
            ctrl = ctk.CTkFrame(row, fg_color="white", corner_radius=6)
            ctrl.pack(side="right", padx=8)
            ctk.CTkButton(ctrl, text="−", width=24, height=24, fg_color=self.primary_green, command=lambda n=name, p=data['price'], i=data['id']: self.update_cart(n, p, -1, i)).pack(side="left")
            ctk.CTkLabel(ctrl, text=str(data['qty']), font=("SF Pro", 11, "bold"), width=22).pack(side="left")
            ctk.CTkButton(ctrl, text="+", width=24, height=24, fg_color=self.primary_green, command=lambda n=name, p=data['price'], i=data['id']: self.update_cart(n, p, 1, i)).pack(side="left")
            subtotal += data['price'] * data['qty']
        
        self.tax_lbl.configure(text=f"Tax (12%): ₱{(subtotal * self.tax_rate):,.2f}")
        self.total_lbl.configure(text=f"₱{(subtotal * 1.12):,.2f}")

    def update_cart(self, n, p, d, i):
        if n in self.cart:
            self.cart[n]['qty'] += d
            if self.cart[n]['qty'] <= 0: del self.cart[n]
        elif d > 0: self.cart[n] = {'price': float(p), 'qty': 1, 'id': i}
        self.render_cart()

    def open_filter_menu(self):
        m = ctk.CTkToplevel(self)
        m.title("Filter Categories")
        m.geometry("250x380")
        m.attributes("-topmost", True)
        for opt in ["All"] + list(self.categories.values()):
            ctk.CTkButton(m, text=opt, height=40, command=lambda o=opt: self.set_filter(o, m)).pack(fill="x", padx=20, pady=5)

    def set_filter(self, opt, win):
        self.current_filter = opt
        win.destroy()
        self.show_dashboard()

    def edit_item(self, item):
        new_price = simpledialog.askfloat("Edit Product", f"New price for {item[1]}:", initialvalue=item[2])
        if new_price:
            self.db.execute_query("UPDATE products SET price=%s WHERE id=%s", (new_price, item[0]))
            self.show_inventory_manager()

    def delete_item(self, pid):
        if messagebox.askyesno("Confirm", "Permanently delete this product?"):
            self.db.execute_query("DELETE FROM products WHERE id=%s", (pid,))
            self.show_inventory_manager()

    def checkout(self):
        if not self.cart: 
            return messagebox.showwarning("POS", "Cart is empty!")
    
        try:
        # 1. Pre-Check: Verify all items have sufficient stock
            items_in_db = {item[0]: item for item in self.db.fetch_menu_items()} #
        
            for item_name, item_data in self.cart.items():
                pid = item_data['id']
                requested_qty = item_data['qty']
                current_stock = items_in_db[pid][3] # Index 3 is stock column
            
                if requested_qty > current_stock:
                    messagebox.showerror("Stock Error", 
                        f"Insufficient stock for {item_name}.\n"
                        f"Requested: {requested_qty}\n"
                        f"Available: {current_stock}")
                    return # Stop the checkout entirely

        # 2. Process Checkout (Only if stock is sufficient)
            summary = ", ".join([f"{v['qty']}x {k}" for k,v in self.cart.items()])
            total = sum([v['qty'] * v['price'] for v in self.cart.values()]) * 1.12 #
        
            for item_name, item_data in self.cart.items():
                self.db.update_stock(item_data['id'], -item_data['qty']) #[cite: 3]
            
            self.db.add_sale(datetime.now().strftime("%Y-%m-%d %H:%M"), summary, total) #[cite: 3]
        
            messagebox.showinfo("POS", "Transaction Completed!")
            self.cart = {}
            self.render_cart()
            self.show_dashboard()
        
        except Exception as e:
            messagebox.showerror("Error", f"Checkout failed: {e}")

    def adjust_stock(self, pid, d): self.db.update_stock(pid, d); self.show_inventory_manager()
    def toggle_category(self, cid): self.expanded_categories[cid] = not self.expanded_categories[cid]; self.show_inventory_manager()
    def delete_from_cart(self, name): 
        if name in self.cart: del self.cart[name]
        self.render_cart()
    def clear_view(self): [c.destroy() for c in self.container.winfo_children()]
    def update_nav(self, txt):
        for n, b in self.nav_btns.items():
            act = (n == txt)
            b.configure(fg_color=self.primary_green if act else "transparent", text_color="white" if act else "black")

if __name__ == "__main__": 
    MainApp().mainloop()
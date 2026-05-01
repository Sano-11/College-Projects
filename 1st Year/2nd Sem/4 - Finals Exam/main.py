import customtkinter as ctk
from tkinter import messagebox
import pywinstyles

# --- DATABASE BRIDGE ---
class DatabaseManager:
    def fetch_menu_items(self):
        # Restored the full 10-item list for a complete grid[cite: 1]
        return [
            (1, "Caffe Americano", 120.0, 100, "Coffee"), (2, "Vanilla Latte", 155.0, 45, "Coffee"),
            (3, "Espresso", 90.0, 50, "Coffee"), (4, "Caramel Macchiato", 165.0, 30, "Coffee"),
            (5, "Iced Matcha", 145.0, 20, "Tea"), (6, "Croissant", 85.0, 15, "Pastry"),
            (7, "Blueberry Muffin", 95.0, 12, "Pastry"), (8, "Hot Choco", 110.0, 40, "Non-Caffeine"),
            (9, "Spanish Latte", 170.0, 25, "Coffee"), (10, "Cold Brew", 130.0, 50, "Coffee")
        ]
    
    def fetch_categories(self):
        return [(1, "Coffee"), (2, "Pastries"), (3, "Tea"), (4, "Non-Caffeine")]
    
    def fetch_transactions(self):
        return [
            ("2026-05-01 10:30", "Caffe Americano", 2, 240.00),
            ("2026-05-01 11:45", "Spanish Latte", 1, 170.00),
            ("2026-05-01 12:15", "Iced Matcha", 1, 145.00)
        ]

ctk.set_appearance_mode("light")

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Bean & Brew POS System")
        self.after(0, lambda: self.state('zoomed'))
        
        self.db = DatabaseManager()
        self.cart = [] 

        # --- DESIGN SYSTEM ---
        self.primary_green = "#276C4C"
        self.bg_color = "#F0F0F5"
        self.pill_border_weight = 4 
        self.shadow_color = "#D1D1D6"
        
        self.configure(fg_color=self.bg_color) 
        pywinstyles.apply_style(self, "mica")

        # Layout Weights: Sidebar(0) | Main(1) | Cart(0)[cite: 1]
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0, minsize=340) # Smaller, fixed-width cart[cite: 1]
        self.grid_rowconfigure(0, weight=1)

        # 1. NAVIGATION SIDEBAR
        self.sidebar = ctk.CTkFrame(self, width=240, fg_color="white", corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        # Reduced Logo Size[cite: 1]
        self.logo_label = ctk.CTkLabel(self.sidebar, text="☕\nBEAN & BREW", 
                                      font=("SF Pro Display", 22, "bold"), justify="center")
        self.logo_label.pack(pady=(60, 40))

        self.nav_btns = {}
        for btn_name in ["Dashboard", "Inventory Manager", "Sales History"]:
            self.nav_btns[btn_name] = self.create_nav_btn(btn_name)

        # 2. MAIN CONTENT AREA
        self.container = ctk.CTkScrollableFrame(self, fg_color="transparent", corner_radius=0)
        self.container.grid(row=0, column=1, sticky="nsew", padx=10)
        
        # 3. CART SIDEBAR (Fixed and Thinner)[cite: 1]
        self.right_panel = ctk.CTkFrame(self, fg_color="white", corner_radius=0, border_width=1, border_color=self.shadow_color)
        self.right_panel.grid(row=0, column=2, sticky="nsew")
        
        # Header
        ctk.CTkLabel(self.right_panel, text="Current Order", font=("SF Pro Display", 24, "bold")).pack(pady=(40, 20))
        
        # Scrollable Cart Items
        self.cart_scroll = ctk.CTkScrollableFrame(self.right_panel, fg_color="transparent")
        self.cart_scroll.pack(fill="both", expand=True, padx=20)
        
        # PINNED CHECKOUT AREA (Prevents button from disappearing)[cite: 1]
        self.checkout_area = ctk.CTkFrame(self.right_panel, fg_color="white", height=220)
        self.checkout_area.pack(fill="x", side="bottom", padx=25, pady=25)
        self.checkout_area.pack_propagate(False) # Maintain fixed height
        
        self.total_lbl = ctk.CTkLabel(self.checkout_area, text="Total: ₱0.00", 
                                      font=("SF Pro Text", 28, "bold"), text_color=self.primary_green)
        self.total_lbl.pack(pady=10)
        
        self.checkout_btn = ctk.CTkButton(self.checkout_area, text="Review & Checkout", height=65, 
                                          corner_radius=32, font=("SF Pro Text", 16, "bold"),
                                          fg_color=self.primary_green, command=self.open_checkout)
        self.checkout_btn.pack(fill="x", pady=10)

        self.show_dashboard()

    def create_nav_btn(self, text):
        cmds = {"Dashboard": self.show_dashboard, "Inventory Manager": self.show_inventory, "Sales History": self.show_sales_history}
        btn = ctk.CTkButton(self.sidebar, text=text, command=cmds[text], 
                            height=52, corner_radius=15, fg_color="transparent", 
                            text_color="#1C1C1E", font=("SF Pro Text", 15, "bold"), anchor="w")
        btn.pack(pady=5, padx=25, fill="x")
        return btn

    def show_dashboard(self):
        for name, btn in self.nav_btns.items():
            is_active = (name == "Dashboard")
            btn.configure(fg_color=self.primary_green if is_active else "transparent", 
                          text_color="white" if is_active else "#1C1C1E")
            
        for w in self.container.winfo_children(): w.destroy()
        
        # Header for the main view
        ctk.CTkLabel(self.container, text="Menu Selection", font=("SF Pro Display", 28, "bold")).pack(anchor="w", padx=35, pady=(30, 10))
        
        # Grid System matched to image_3ef218.png[cite: 1]
        grid = ctk.CTkFrame(self.container, fg_color="transparent")
        grid.pack(fill="both", expand=True, padx=25, pady=10)
        grid.columnconfigure((0, 1, 2), weight=1, uniform="menu_grid") 

        items = self.db.fetch_menu_items()
        for i, item in enumerate(items):
            card = ctk.CTkFrame(grid, height=290, fg_color="white", corner_radius=35, 
                                border_width=self.pill_border_weight, border_color=self.shadow_color)
            card.grid(row=i//3, column=i%3, padx=12, pady=12, sticky="nsew")
            card.grid_propagate(False)
            
            ctk.CTkLabel(card, text=item[1], font=("SF Pro Display", 19, "bold"), wraplength=180).pack(pady=(45, 5))
            ctk.CTkLabel(card, text=f"₱{item[2]:.2f}", font=("SF Pro Text", 17), text_color=self.primary_green).pack()
            
            ctk.CTkButton(card, text="Add to Cart", width=160, height=45, corner_radius=22, 
                          fg_color=self.primary_green, font=("SF Pro Text", 14, "bold"),
                          command=lambda n=item[1], p=item[2]: self.update_cart(n, p)).pack(side="bottom", pady=35)

    def update_cart(self, name, price):
        self.cart.append((name, price))
        row = ctk.CTkFrame(self.cart_scroll, fg_color="#F8F8F8", corner_radius=10)
        row.pack(fill="x", pady=4)
        ctk.CTkLabel(row, text=name, font=("SF Pro Text", 14), padx=15).pack(side="left", pady=10)
        ctk.CTkLabel(row, text=f"₱{price:.2f}", font=("SF Pro Text", 14, "bold"), padx=15).pack(side="right", pady=10)
        
        total = sum(i[1] for i in self.cart)
        self.total_lbl.configure(text=f"Total: ₱{total:.2f}")

    def show_inventory(self):
        for name, btn in self.nav_btns.items():
            is_active = (name == "Inventory Manager")
            btn.configure(fg_color=self.primary_green if is_active else "transparent", 
                          text_color="white" if is_active else "#1C1C1E")
            
        for w in self.container.winfo_children(): w.destroy()
        
        content = ctk.CTkFrame(self.container, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=40, pady=40)

        ctk.CTkLabel(content, text="Inventory Management", font=("SF Pro Display", 32, "bold")).pack(anchor="w")
        
        # Add Item Form[cite: 1]
        form = ctk.CTkFrame(content, fg_color="white", corner_radius=25, border_width=1, border_color=self.shadow_color)
        form.pack(fill="x", pady=30)
        
        fields = [("Item Name", "e.g. Mocha Latte"), ("Price", "₱ 0.00"), ("Initial Stock", "Quantity")]
        self.entries = {}
        for label, placeholder in fields:
            lbl = ctk.CTkLabel(form, text=label, font=("SF Pro Text", 13, "bold"))
            lbl.pack(pady=(20, 5), padx=40, anchor="w")
            entry = ctk.CTkEntry(form, placeholder_text=placeholder, height=50, corner_radius=15, fg_color="#F9F9F9")
            entry.pack(pady=(0, 10), padx=40, fill="x")
            self.entries[label] = entry

        ctk.CTkButton(content, text="Add New Item to Menu", height=60, corner_radius=30, 
                      fg_color=self.primary_green, font=("SF Pro Text", 16, "bold")).pack(pady=20, fill="x")

    def show_sales_history(self):
        for name, btn in self.nav_btns.items():
            is_active = (name == "Sales History")
            btn.configure(fg_color=self.primary_green if is_active else "transparent", 
                          text_color="white" if is_active else "#1C1C1E")
            
        for w in self.container.winfo_children(): w.destroy()
        
        logs = self.db.fetch_transactions()
        ctk.CTkLabel(self.container, text="Sales History", font=("SF Pro Display", 32, "bold")).pack(pady=40, padx=45, anchor="w")
        
        for date, item, qty, total in logs:
            pill = ctk.CTkFrame(self.container, fg_color="white", corner_radius=25, height=90, 
                                border_width=1, border_color=self.shadow_color)
            pill.pack(fill="x", padx=45, pady=10)
            pill.pack_propagate(False)
            
            info_frame = ctk.CTkFrame(pill, fg_color="transparent")
            info_frame.pack(side="left", padx=30, fill="y")
            
            ctk.CTkLabel(info_frame, text=item, font=("SF Pro Text", 18, "bold")).pack(anchor="w", pady=(15, 0))
            ctk.CTkLabel(info_frame, text=date, font=("SF Pro Text", 12), text_color="gray").pack(anchor="w")
            
            ctk.CTkLabel(pill, text=f"₱{total:.2f}", font=("SF Pro Display", 22, "bold"), 
                        text_color=self.primary_green).pack(side="right", padx=40)

    def open_checkout(self):
        if not self.cart:
            messagebox.showwarning("Cart Empty", "Please add items to the cart first.")
            return
        
        # Receipt Modal[cite: 1]
        pay_win = ctk.CTkToplevel(self)
        pay_win.title("Checkout Summary")
        pay_win.geometry("500x750")
        pay_win.attributes("-topmost", True)
        pay_win.configure(fg_color="white")
        
        ctk.CTkLabel(pay_win, text="ORDER RECEIPT", font=("SF Pro Display", 24, "bold")).pack(pady=(40, 20))
        
        receipt_frame = ctk.CTkFrame(pay_win, fg_color="#F8F8F8", corner_radius=20, border_width=1, border_color="#E5E5E5")
        receipt_frame.pack(fill="both", expand=True, padx=40, pady=10)
        
        receipt_text = ctk.CTkTextbox(receipt_frame, font=("Courier New", 14), fg_color="transparent")
        receipt_text.pack(fill="both", expand=True, padx=20, pady=20)
        
        total = sum(i[1] for i in self.cart)
        receipt_text.insert("end", f"{'Item':<20} {'Price':>10}\n")
        receipt_text.insert("end", "-"*32 + "\n")
        for n, p in self.cart:
            receipt_text.insert("end", f"{n[:18]:<20} ₱{p:>9.2f}\n")
        receipt_text.configure(state="disabled")

        ctk.CTkLabel(pay_win, text=f"Total Amount: ₱{total:.2f}", font=("SF Pro Display", 26, "bold"), 
                     text_color=self.primary_green).pack(pady=20)
        
        cash_in = ctk.CTkEntry(pay_win, placeholder_text="Enter Cash Amount", height=60, width=320, 
                               corner_radius=30, justify="center", font=("SF Pro Text", 18))
        cash_in.pack(pady=10)
        
        def process_payment():
            try:
                tendered = float(cash_in.get())
                if tendered < total:
                    messagebox.showerror("Error", "Insufficient cash.")
                else:
                    messagebox.showinfo("Success", f"Transaction Complete!\nChange: ₱{tendered - total:.2f}")
                    self.cart = []
                    for w in self.cart_scroll.winfo_children(): w.destroy()
                    self.total_lbl.configure(text="Total: ₱0.00")
                    pay_win.destroy()
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number.")

        ctk.CTkButton(pay_win, text="CONFIRM & PRINT", height=65, width=320, corner_radius=32, 
                      fg_color=self.primary_green, font=("SF Pro Text", 16, "bold"), 
                      command=process_payment).pack(pady=40)

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
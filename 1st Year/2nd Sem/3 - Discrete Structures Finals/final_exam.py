import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import math
import csv

class SecureCommMSEUF:
    def __init__(self, root):
        self.root = root
        self.root.title("SecureComm Pro - Discrete Structures")
        self.root.geometry("1280x820")
        self.root.configure(bg="#F1F5F9") # Neutral background to make white cards "pop"

        # --- MSEUF Identity Palette ---
        self.colors = {
            "maroon": "#7B1113",     
            "gold": "#FFC107",       
            "bg": "#F1F5F9",         # Light slate background
            "card": "#FFFFFF",       # High-contrast white for cards
            "border": "#E2E8F0",     # Subtle gray for card edges
            "text_main": "#1E293B",
            "text_muted": "#64748B",
            "white": "#FFFFFF"
        }

        # --- 1. Global Header (Stays Flat) ---
        self.header = tk.Frame(root, bg=self.colors["maroon"], height=70)
        self.header.pack(side="top", fill="x")
        self.header.pack_propagate(False)

        header_inner = tk.Frame(self.header, bg=self.colors["maroon"])
        header_inner.pack(fill="both", expand=True, padx=32)

        tk.Label(header_inner, text="SecureComm Pro", font=("Inter", 20, "bold"), 
                 bg=self.colors["maroon"], fg=self.colors["white"]).pack(side="left")
        
        user_info = tk.Frame(header_inner, bg=self.colors["maroon"])
        user_info.pack(side="right")
        tk.Label(user_info, text="Allen Jerrome M. Tolete |", font=("Inter", 10, "bold"), 
                 bg=self.colors["maroon"], fg=self.colors["white"]).pack(anchor="e")
        tk.Label(user_info, text="MSEUF Lucena | BS Computer Science", font=("Inter", 9), 
                 bg=self.colors["maroon"], fg=self.colors["gold"]).pack(anchor="e")

        # --- Main Workspace (The "Floor") ---
        self.workspace = tk.Frame(root, bg=self.colors["bg"])
        self.workspace.pack(expand=True, fill="both", padx=32, pady=32)

        # --- 2. Sidebar Card ---
        # highlightthickness=1 + border color creates the "card" effect
        self.sidebar = tk.Frame(self.workspace, bg=self.colors["card"], width=320, 
                                highlightthickness=1, highlightbackground=self.colors["border"])
        self.sidebar.pack(side="left", fill="y", padx=(0, 24))
        self.sidebar.pack_propagate(False)

        tk.Label(self.sidebar, text="Configuration", font=("Inter", 12, "bold"), 
                 bg=self.colors["card"], fg=self.colors["maroon"]).pack(anchor="w", padx=24, pady=(24, 16))

        self.add_input("Affine Multiplier (a)", "17", "key_a")
        self.add_input("Affine Shift (b)", "20", "key_b")

        # Buttons nested inside the sidebar card
        self.btn_import = tk.Button(self.sidebar, text="Import CSV Dataset", command=self.import_csv, 
                                    bg=self.colors["maroon"], fg="white", font=("Inter", 10, "bold"), 
                                    relief="flat", cursor="hand2")
        self.btn_import.pack(fill="x", padx=24, pady=(24, 8), ipady=12)

        self.btn_export = tk.Button(self.sidebar, text="Export Secure Ballots", command=self.export_csv, 
                                    bg=self.colors["gold"], fg=self.colors["maroon"], font=("Inter", 10, "bold"), 
                                    relief="flat", cursor="hand2")
        self.btn_export.pack(fill="x", padx=24, pady=8, ipady=12)

        # --- 3. Main Content Card ---
        self.content_card = tk.Frame(self.workspace, bg=self.colors["card"], 
                                     highlightthickness=1, highlightbackground=self.colors["border"])
        self.content_card.pack(side="right", expand=True, fill="both")

        # --- 4. Inner Header Card (The Maroon Strip) ---
        self.content_header = tk.Frame(self.content_card, bg=self.colors["maroon"], height=55)
        self.content_header.pack(fill="x")
        self.content_header.pack_propagate(False)
        
        tk.Label(self.content_header, text="Data Transmission Record", font=("Inter", 11, "bold"), 
                 bg=self.colors["maroon"], fg=self.colors["white"]).pack(side="left", padx=24)
        
        self.status_msg = tk.Label(self.content_header, text="Dataset: 0 records loaded", font=("Inter", 9), 
                                   bg=self.colors["maroon"], fg=self.colors["gold"])
        self.status_msg.pack(side="right", padx=24)

        # --- 5. Structured Table Container ---
        self.table_frame = tk.Frame(self.content_card, bg=self.colors["card"])
        self.table_frame.pack(expand=True, fill="both", padx=24, pady=24)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", font=("Inter", 10), rowheight=40, fieldbackground="white", borderwidth=0)
        style.configure("Treeview.Heading", font=("Inter", 9, "bold"), background="#F8FAFC", foreground=self.colors["maroon"], relief="flat")
        
        self.tree = ttk.Treeview(self.table_frame, columns=("Original", "Encrypted"), show="headings")
        self.tree.heading("Original", text="   ORIGINAL DOMAIN DATA")
        self.tree.heading("Encrypted", text="   ENCRYPTED CODOMAIN (SECURE)")
        self.tree.column("Original", width=400, anchor="w")
        self.tree.column("Encrypted", width=400, anchor="w")
        
        self.tree.pack(expand=True, fill="both")

    def add_input(self, label, default, var_name):
        f = tk.Frame(self.sidebar, bg=self.colors["card"])
        f.pack(fill="x", padx=24, pady=8)
        tk.Label(f, text=label, font=("Inter", 9, "bold"), bg=self.colors["card"], fg=self.colors["text_muted"]).pack(anchor="w", pady=(0, 4))
        e = tk.Entry(f, font=("Inter", 11), bg="#F8FAFC", relief="flat", 
                     highlightthickness=1, highlightbackground=self.colors["border"], fg=self.colors["maroon"])
        e.insert(0, default)
        e.pack(fill="x", ipady=10)
        setattr(self, var_name, e)

    # ... (Encryption, Import, and Export methods remain the same)
    def affine_encrypt(self, text, a, b):
        res = ""
        for char in text.upper():
            if char.isalpha():
                p = ord(char) - 65
                res += chr(((a * p + b) % 26) + 65)
            else:
                res += char
        return res

    def import_csv(self):
        try:
            a, b = int(self.key_a.get()), int(self.key_b.get())
            if math.gcd(a, 26) != 1:
                messagebox.showerror("Discrete Math Warning", "Multiplier 'a' must be coprime to 26.")
                return
            path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
            if not path: return
            for i in self.tree.get_children(): self.tree.delete(i)
            with open(path, mode='r') as f:
                reader = csv.reader(f)
                count = 0
                for row in reader:
                    if row:
                        orig = row[0]
                        enc = self.affine_encrypt(orig, a, b)
                        self.tree.insert("", "end", values=(f"  {orig}", f"  {enc}"))
                        count += 1
            self.status_msg.config(text=f"Dataset: {count} records loaded")
        except:
            messagebox.showerror("Error", "Check your keys or file format.")

    def export_csv(self):
        if not self.tree.get_children(): return
        path = filedialog.asksaveasfilename(defaultextension=".csv")
        if not path: return
        with open(path, mode='w', newline='') as f:
            writer = csv.writer(f)
            for i in self.tree.get_children():
                writer.writerow([v.strip() for v in self.tree.item(i)['values']])
        messagebox.showinfo("Success", "Security export complete.")

if __name__ == "__main__":
    root = tk.Tk()
    app = SecureCommMSEUF(root)
    root.mainloop()
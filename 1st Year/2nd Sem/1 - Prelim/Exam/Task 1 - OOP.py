import tkinter as tk
from tkinter import messagebox, ttk

class Book:
    def __init__(self, title, author, isbn, is_available=True):
        self._title = title
        self._author = author
        self._isbn = isbn
        self._is_available = is_available
    
    def get_title(self): return self._title
    def get_author(self): return self._author
    def get_isbn(self): return self._isbn
    def is_available(self): return self._is_available
    def set_available(self, status): self._is_available = status

class Library:
    def __init__(self):
        self._books = []
        self.load_sample_books()
    
    def load_sample_books(self):
        # Fixed syntax errors from source (missing commas)
        sample_books = [
            ("Python Crash Course", "Rommel Robert Florido", "978-1593279288"),
            ("Clean Code", "Lanz Isaac Olaes", "978-0132350884"),
            ("The Pragmatic Programmer", "Ernesto Lucas Mateo", "978-0201616224"),
            ("Head First Design Patterns", "Steven Wayne Chua", "978-0596007126"),
            ("Automate the Boring Stuff", "Pete Andre Ron Borromeo", "978-1593275990"),
            ("Introduction to Algorithms", "Nadine Endrenal", "978-0262033848"),
            ("Grokking Algorithms", "Charish Aiwyne De Ocampo", "978-1617292231"),
            ("Fluent Python", "Sean Kavin Fermo", "978-1492056348"),
            ("Data Algorithms", "Brian Miguel Rabe", "978-1516487521"),
            ("Fluent Python", "Aldryn Untalan", "978-1234567890")
        ]
        for title, author, isbn in sample_books:
            self._books.append(Book(title, author, isbn))

    def get_books(self):
        return self._books

    def add_book(self, book):
        self._books.append(book)

    def toggle_status(self, isbn):
        for book in self._books:
            if book.get_isbn() == isbn:
                book.set_available(not book.is_available())
                return True
        return False

class LibraryGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Enverga University - Library Manager")
        self.root.state('zoomed')
        self.root.configure(bg="#f4f4f7")
        
        self.library = Library()
        self.style = ttk.Style()
        self.setup_styles()
        
        # --- SCROLLABLE CONTAINER ---
        self.main_canvas = tk.Canvas(self.root, bg="#f4f4f7", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.main_canvas.yview)
        self.scrollable_frame = tk.Frame(self.main_canvas, bg="#f4f4f7")

        self.scrollable_frame.bind(
            "<Configure>", 
            lambda e: self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))
        )
        self.canvas_window = self.main_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.main_canvas.bind('<Configure>', self._on_canvas_configure)
        
        self.root.bind_all("<MouseWheel>", self._on_mousewheel)
        self.root.bind_all("<Button-4>", self._on_mousewheel)
        self.root.bind_all("<Button-5>", self._on_mousewheel)

        self.main_canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")
        self.main_canvas.pack(side="left", fill="both", expand=True)

        self.setup_ui()
        self.refresh_list()

    def _on_mousewheel(self, event):
        if event.num == 4 or (hasattr(event, 'delta') and event.delta > 0):
            self.main_canvas.yview_scroll(-1, "units")
        elif event.num == 5 or (hasattr(event, 'delta') and event.delta < 0):
            self.main_canvas.yview_scroll(1, "units")

    def _on_canvas_configure(self, event):
        self.main_canvas.itemconfig(self.canvas_window, width=event.width)

    def setup_styles(self):
        self.style.theme_use('clam')
        self.style.configure("Treeview", background="white", fieldbackground="white", 
                             rowheight=50, font=("Segoe UI", 11), borderwidth=0)
        self.style.configure("Treeview.Heading", font=("Segoe UI Bold", 11), 
                             background="#800000", foreground="white", relief="flat")
        self.style.map("Treeview.Heading", background=[('active', '#660000')])
        self.style.map("Treeview", background=[('selected', '#f2d7d7')], 
                       foreground=[('selected', '#800000')])
        
        self.style.configure("Primary.TButton", font=("Segoe UI Bold", 10), background="#800000", foreground="white", padding=8, width=20)
        self.style.configure("Secondary.TButton", font=("Segoe UI Semibold", 10), background="#e9ecef", foreground="#333", padding=8, width=20)
        self.style.configure("Danger.TButton", font=("Segoe UI Bold", 10), background="#fdf2f2", foreground="#c92a2a", padding=8, width=18)

    def setup_ui(self):
        # MAIN HEADER
        header = tk.Frame(self.scrollable_frame, bg="#800000", height=130)
        header.pack(fill="x")
        tk.Label(header, text="UNIVERSITY LIBRARY SYSTEM", bg="#800000", fg="white", 
                 font=("Segoe UI Bold", 32)).pack(pady=(30, 5))
        tk.Label(header, text="Library Management Portal", bg="#800000", fg="#ffcccc", 
                 font=("Segoe UI", 12, "italic")).pack(pady=(0, 30))

        content = tk.Frame(self.scrollable_frame, bg="#f4f4f7")
        content.pack(fill="both", expand=True, padx=100, pady=30)

        # --- COMPACT INPUT CARD ---
        input_card = tk.Frame(content, bg="white", highlightbackground="#ced4da", highlightthickness=1)
        input_card.pack(fill="x", pady=(0, 30))

        # Maroon Header for the Card 
        input_header = tk.Frame(input_card, bg="#800000")
        input_header.pack(fill="x")
        tk.Label(input_header, text="ADD NEW RECORD", bg="#800000", fg="white",
                 font=("Segoe UI Bold", 11)).pack(pady=10) # White text 

        # Body of the Card [cite: 15]
        input_body = tk.Frame(input_card, bg="white", padx=40, pady=20)
        input_body.pack(fill="x")
        input_body.grid_columnconfigure((0, 1, 2), weight=1)

        fields = [("Book Title", "title"), ("Author Name", "author"), ("ISBN Code", "isbn")]
        self.entries = {}
        for i, (label_text, key) in enumerate(fields):
            container = tk.Frame(input_body, bg="white")
            container.grid(row=0, column=i, padx=15, pady=5)
            
            tk.Label(container, text=label_text.upper(), bg="white", 
                     font=("Segoe UI Bold", 8), fg="#adb5bd").pack(anchor="center")
            
            entry = ttk.Entry(container, width=30) # Slightly shorter for compactness [cite: 17]
            entry.pack(pady=(5, 0), ipady=3)
            self.entries[key] = entry

        # Button Container
        btn_container = tk.Frame(input_body, bg="white")
        btn_container.grid(row=1, column=0, columnspan=3, pady=(25, 5), sticky="ew")
        
        actions_frame = tk.Frame(btn_container, bg="white")
        actions_frame.pack(side="left")
        ttk.Button(actions_frame, text="ADD TO COLLECTION", style="Primary.TButton", command=self.add_book).pack(side="left", padx=(0, 10))
        ttk.Button(actions_frame, text="CHANGE STATUS", style="Secondary.TButton", command=self.toggle_status).pack(side="left", padx=10)
        ttk.Button(btn_container, text="WIPE DATABASE", style="Danger.TButton", command=self.clear_all).pack(side="right")

        # --- TABLE CARD ---
        table_card = tk.Frame(content, bg="white", padx=30, pady=25,
                              highlightbackground="#ced4da", highlightthickness=1)
        table_card.pack(fill="both", expand=True)

        search_frame = tk.Frame(table_card, bg="white")
        search_frame.pack(fill="x", pady=(0, 20))
        tk.Label(search_frame, text="FILTER BY ISBN:", bg="white", font=("Segoe UI Bold", 9), fg="#495057").pack(side="left", padx=(0, 10))
        self.search_entry = ttk.Entry(search_frame, width=40)
        self.search_entry.pack(side="left", ipady=2)
        self.search_entry.bind("<KeyRelease>", lambda e: self.refresh_list())

        columns = ("title", "author", "isbn", "status")
        self.tree = ttk.Treeview(table_card, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.tree.heading(col, text=col.upper())
        
        # Alignment logic
        self.tree.column("title", width=400, anchor="w")
        self.tree.column("author", width=250, anchor="w")
        self.tree.column("isbn", width=180, anchor="center")
        self.tree.column("status", width=180, anchor="center")

        self.tree.tag_configure('available', foreground='#2f9e44', font=("Segoe UI Semibold", 11))
        self.tree.tag_configure('checkedout', foreground='#e03131', font=("Segoe UI Semibold", 11))
        self.tree.tag_configure('even', background='#fcfcfc')

        self.tree.pack(side="left", fill="both", expand=True)
        list_sb = ttk.Scrollbar(table_card, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=list_sb.set)
        list_sb.pack(side="right", fill="y")

    def refresh_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        query = self.search_entry.get().lower()
        for i, book in enumerate(self.library.get_books()):
            if query in book.get_isbn().lower():
                status = "●  Available" if book.is_available() else "○  Checked Out"
                tag = 'available' if book.is_available() else 'checkedout'
                row_tag = (tag, 'even' if i % 2 == 0 else 'odd')
                self.tree.insert("", "end", values=(book.get_title(), book.get_author(), 
                                                   book.get_isbn(), status), tags=row_tag)

    def add_book(self):
        t, a, i = self.entries['title'].get(), self.entries['author'].get(), self.entries['isbn'].get()
        if t and a and i:
            self.library.add_book(Book(t, a, i))
            for e in self.entries.values():
                e.delete(0, tk.END)
            self.refresh_list()
        else:
            messagebox.showwarning("Incomplete", "Please fill all fields.")

    def toggle_status(self):
        selected = self.tree.focus()
        if not selected:
            return
        isbn = self.tree.item(selected)['values'][2]
        self.library.toggle_status(isbn)
        self.refresh_list()

    def clear_all(self):
        if messagebox.askyesno("Confirm", "Wipe all library data?"):
            self.library._books.clear()
            self.refresh_list()

if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryGUI(root)
    root.mainloop()
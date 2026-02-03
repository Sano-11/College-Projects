import re
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from collections import Counter
import random
import itertools
import threading
import time

class LeadApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Text File Generator & Data Analyzer")
        self.root.state('zoomed') 
        
        # LIGHT MODE COLORS
        self.bg_main = "#f0f2f5"      # Light grey background
        self.bg_card = "#ffffff"      # Pure white for containers
        self.fg_text = "#2c3e50"      # Dark slate for text
        self.border_col = "#dcdde1"   # Light border
        self.blue = "#3498db"         # Soft blue accent
        self.green = "#2ecc71"        # Emerald green accent
        
        self.root.configure(bg=self.bg_main)

        # --- HEADER ---
        header = tk.Frame(root, bg="#2c3e50", pady=20)
        header.pack(fill="x")
        tk.Label(header, text="TEXT FILE GENERATOR & DATA ANALYZER", 
                 font=('Segoe UI Bold', 22), bg="#2c3e50", fg="white").pack()

        self.setup_scrollable_frames()
        self.setup_generator_ui()
        self.setup_auditor_ui()

    def setup_scrollable_frames(self):
        self.canvas = tk.Canvas(self.root, bg=self.bg_main, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=self.bg_main)
        
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", width=self.root.winfo_screenwidth())
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

    def setup_generator_ui(self):
        tk.Label(self.scrollable_frame, text="STEP 1: INPUT NAMES FOR COMBINATIONS", 
                 font=("Segoe UI Bold", 10), bg=self.bg_main, fg="#7f8c8d").pack(pady=(30, 5))

        # ENTRY BOXES WITH LIGHT THEME
        self.name_entries = []
        for i in range(5):
            entry = tk.Entry(self.scrollable_frame, width=50, font=("Segoe UI", 12), bd=0, 
                             bg=self.bg_card, fg=self.fg_text, insertbackground="black",
                             highlightthickness=1, highlightbackground=self.border_col, justify="center")
            entry.pack(pady=4, ipady=8)
            self.name_entries.append(entry)

        self.progress = ttk.Progressbar(self.scrollable_frame, mode='indeterminate', length=300)
        self.progress.pack(pady=10)

        tk.Button(self.scrollable_frame, text="📂 GENERATE & RANDOMIZE LEADS", command=self.start_gen_thread,
                  bg=self.blue, fg="white", font=("Segoe UI Bold", 11), padx=40, pady=10, bd=0, cursor="hand2").pack(pady=10)

    def setup_auditor_ui(self):
        tk.Label(self.scrollable_frame, text="STEP 2: DATA ANALYSIS (REGEX ENGINE)", 
                 font=("Segoe UI Bold", 10), bg=self.bg_main, fg="#7f8c8d").pack(pady=(30, 5))

        # TEXT BOX (PLACEHOLDERS)
        self.text_display = tk.Text(self.scrollable_frame, height=10, width=80, font=('Consolas', 11), 
                                    bg=self.bg_card, fg="#2d3436", bd=0, padx=20, pady=20, 
                                    highlightthickness=1, highlightbackground=self.border_col)
        self.text_display.pack(pady=10)
        self.text_display.insert("1.0", "Paste leads here or generate above...")

        # BUTTONS
        btn_frame = tk.Frame(self.scrollable_frame, bg=self.bg_main)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="🚀 RUN REGEX ANALYSIS", command=self.analyze_emails, 
                  bg=self.green, fg="white", font=("Segoe UI Bold", 11), padx=30, pady=10, bd=0, cursor="hand2").pack(side="left", padx=10)
        
        tk.Button(btn_frame, text="📋 COPY TO CLIPBOARD", command=self.copy_to_clipboard, 
                  bg="#e67e22", fg="white", font=("Segoe UI Bold", 11), padx=30, pady=10, bd=0, cursor="hand2").pack(side="left", padx=10)

        self.res_label = tk.Label(self.scrollable_frame, text="Awaiting Data...", 
                                  font=('Segoe UI Semilight', 13), bg=self.bg_main, fg=self.fg_text)
        self.res_label.pack(pady=(10, 50))

    def start_gen_thread(self):
        self.progress.start(10)
        threading.Thread(target=self.generate_file, daemon=True).start()

    def generate_file(self):
        all_words = []
        for n in self.name_entries:
            val = n.get().strip()
            if val: all_words.extend(val.split())

        if len(all_words) < 2:
            self.root.after(0, lambda: [self.progress.stop(), messagebox.showwarning("Error", "Need more names!")])
            return

        time.sleep(0.5) 
        domains = ["gmail.com", "outlook.com", "mseuf.edu.ph", "techcorp.io"]
        name_combinations = list(itertools.permutations(all_words, 2))
        
        data = [f"Lead ID {random.randint(100, 999)}: {p[0]} {p[1]} ({p[0].lower()}.{p[1].lower()}@{random.choice(domains)})" 
                for p in name_combinations]

        self.root.after(0, self.finish_generation, data)

    def finish_generation(self, data):
        self.progress.stop()
        self.text_display.delete("1.0", tk.END)
        self.text_display.insert(tk.END, "\n".join(data))
        messagebox.showinfo("Success", f"Generated {len(data)} unique combinations.")

    def copy_to_clipboard(self):
        content = self.text_display.get("1.0", tk.END).strip()
        self.root.clipboard_clear()
        self.root.clipboard_append(content)
        messagebox.showinfo("Clipboard", "Data copied successfully!")

    def analyze_emails(self):
        content = self.text_display.get("1.0", tk.END).strip()
        emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", content)
        ids = re.findall(r"Lead ID \d+", content) #

        if not emails: return

        counts = Counter([e.split('@')[1] for e in emails])
        top_domain, freq = counts.most_common(1)[0]
        
        # CLASSIFICATION LOGIC
        status = "MSEUF (Academic List)" if top_domain == "mseuf.edu.ph" else f"{top_domain.split('.')[0].title()} (General Market List)"

        report = (
            f"📊 TOTAL LEAD ID COUNTER: {len(ids)}\n"
            f"🏢 TOP DOMAIN: {top_domain} ({freq} hits)\n"
            f"🎯 LEAD CLASSIFICATION: {status}"
        )
        self.res_label.config(text=report)

if __name__ == "__main__":
    root = tk.Tk()
    app = LeadApp(root)
    root.mainloop()
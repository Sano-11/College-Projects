import re
import tkinter as tk
from tkinter import filedialog, messagebox
from collections import Counter
import random
import itertools

class IntelligenceSuite:
    def __init__(self, root):
        self.root = root
        self.root.title("Unified Lead Generation & Intelligence Suite")
        self.root.state('zoomed') 
        self.root.configure(bg="#f0f2f5")

        # --- SHARED HEADER ---
        header = tk.Frame(root, bg="#2c3e50", pady=20)
        header.pack(fill="x")
        tk.Label(header, text="Text File Generator & Data Analyzer", 
                 font=('Segoe UI Bold', 20), bg="#2c3e50", fg="white").pack()

        # --- SCROLLABLE CONTAINER ---
        self.main_container = tk.Frame(root, bg="#f0f2f5")
        self.main_container.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(self.main_container, bg="#f0f2f5", highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.main_container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#f0f2f5")

        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        self.canvas.bind('<Configure>', self._on_canvas_configure)
        self.root.bind_all("<MouseWheel>", lambda e: self.canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.setup_generator_ui()
        self.setup_auditor_ui()

    def _on_canvas_configure(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    def setup_generator_ui(self):
        tk.Label(self.scrollable_frame, text="SECTION 1: Email Data Text File Generator ", 
                 font=("Segoe UI Bold", 10), bg="#f0f2f5", fg="#7f8c8d").pack(pady=(30, 10))

        grid_container = tk.Frame(self.scrollable_frame, bg="#f0f2f5")
        grid_container.pack(pady=10)

        self.name_entries = []
        for i in range(5):
            ne = tk.Entry(grid_container, width=50, font=("Segoe UI", 11), bd=0, 
                          highlightthickness=1, highlightbackground="#dcdde1", justify="center")
            ne.pack(pady=5, ipady=8)
            self.name_entries.append(ne)

        tk.Button(self.scrollable_frame, text="📂 GENERATE RANDOMIZED COMBINATIONS.TXT", command=self.generate_file,
                  bg="#3498db", fg="white", font=("Segoe UI Bold", 10), padx=40, pady=12, bd=0).pack(pady=25)

    def setup_auditor_ui(self):
        tk.Label(self.scrollable_frame, text="SECTION 2: Data Analysis", 
                 font=("Segoe UI Bold", 10), bg="#f0f2f5", fg="#7f8c8d").pack(pady=(40, 10))

        preview_frame = tk.Frame(self.scrollable_frame, bg="#f0f2f5")
        preview_frame.pack(fill="x", padx=150)

        self.text_display = tk.Text(preview_frame, height=12, font=('Consolas', 10), 
                                    bd=0, padx=15, pady=15, highlightthickness=1, highlightbackground="#dcdde1")
        self.text_display.pack(fill="x")

        self.btn_analyze = tk.Button(self.scrollable_frame, text="🚀 RUN REGEX ANALYSIS", command=self.analyze_emails, 
                                     bg="#2ecc71", fg="white", font=("Segoe UI Bold", 11), padx=60, pady=15, bd=0)
        self.btn_analyze.pack(pady=25)

        self.res_label = tk.Label(self.scrollable_frame, text="Waiting for analysis...", justify="center", 
                                  font=('Segoe UI Semilight', 11), bg="#f0f2f5", fg="#2c3e50")
        self.res_label.pack(pady=(0, 100))

    def generate_file(self):
        all_words = []
        for n in self.name_entries:
            val = n.get().strip()
            if val:
                all_words.extend(val.split())

        if len(all_words) < 2:
            messagebox.showwarning("Input Error", "Enter more names.")
            return

        domains = ["gmail.com", "outlook.com", "mseuf.edu.ph", "techcorp.io"]
        data_lines = []
        
        name_combinations = list(itertools.permutations(all_words, 2))

        for pair in name_combinations:
            user_handle = f"{pair[0].lower()}.{pair[1].lower()}"
            domain = random.choice(domains) 
            lead_id = random.randint(100, 999)
            data_lines.append(f"Lead ID {lead_id}: {pair[0]} {pair[1]} ({user_handle}@{domain})")

        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, 'w') as f:
                f.write("\n".join(data_lines))
            
            self.text_display.delete(1.0, tk.END)
            self.text_display.insert(tk.END, "\n".join(data_lines))

    def analyze_emails(self):
        content = self.text_display.get(1.0, tk.END).strip()
        if not content:
            return
            
        lead_ids = re.findall(r"Lead ID \d+", content)
        emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", content)

        if not emails:
            return

        total_ids = len(lead_ids)
        domains_found = [email.split('@')[1] for email in emails]
        
        counts = Counter(domains_found)
        most_common_domain, max_freq = counts.most_common(1)[0]
        
        # --- UPDATED CLASSIFICATION FORMAT ---
        domain_name = most_common_domain.split('.')[0].title()
        if most_common_domain == "mseuf.edu.ph":
            target_status = "MSEUF (Academic List)"
        else:
            target_status = f"{domain_name} (General Market List)"

        usernames = [email.split('@')[0] for email in emails]
        avg_len = sum(len(u) for u in usernames) / len(usernames)
        shortest_domain = min(domains_found, key=len)

        report = (
            f"📊 TOTAL LEAD ID COUNTER: {total_ids}\n"
            f"🏢 TOP DOMAIN (MAX):      {most_common_domain} ({max_freq} hits)\n"
            f"📏 AVG USERNAME LENGTH:  {avg_len:.1f} characters\n"
            f"🎯 LEAD CLASSIFICATION:  {target_status}\n"
            f"🔍 SHORTEST DOMAIN (MIN): {shortest_domain}"
        )
        self.res_label.config(text=report)

if __name__ == "__main__":
    root = tk.Tk()
    app = IntelligenceSuite(root)
    root.mainloop()
import re
import tkinter as tk
from tkinter import filedialog, messagebox
from collections import Counter
import random
import itertools

class LeadApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Text File Generator & Data Analyzer")
        self.root.state('zoomed') 
        # DARK MODE COLORS
        self.bg_dark = "#1e1e2e"      # Deep Navy/Charcoal
        self.fg_light = "#cdd6f4"     # Soft White
        self.accent_dark = "#181825"  # Darker contrast
        self.border_col = "#45475a"   # Muted slate border
        
        self.root.configure(bg=self.bg_dark)

        # --- SHARED HEADER ---
        header = tk.Frame(root, bg="#11111b", pady=25)
        header.pack(fill="x")
        tk.Label(header, text="TEXT FILE GENERATOR & DATA ANALYZER", 
                 font=('Segoe UI Bold', 22), bg="#11111b", fg="#89b4fa").pack()

        # --- SCROLLABLE CONTAINER ---
        self.main_container = tk.Frame(root, bg=self.bg_dark)
        self.main_container.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(self.main_container, bg=self.bg_dark, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.main_container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=self.bg_dark)

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
        tk.Label(self.scrollable_frame, text="SECTION 1: COMBINATORIAL GENERATOR", 
                 font=("Segoe UI Bold", 10), bg=self.bg_dark, fg="#bac2de").pack(pady=(30, 10))

        grid_container = tk.Frame(self.scrollable_frame, bg=self.bg_dark)
        grid_container.pack(pady=10)

        self.name_entries = []
        for i in range(5):
            ne = tk.Entry(grid_container, width=50, font=("Segoe UI", 12), bd=0, 
                          bg=self.accent_dark, fg=self.fg_light, insertbackground="white",
                          highlightthickness=1, highlightbackground=self.border_col, justify="center")
            ne.pack(pady=6, ipady=10)
            self.name_entries.append(ne)

        tk.Button(self.scrollable_frame, text="📂 GENERATE RANDOMIZED TEXT FILE", command=self.generate_file,
                  bg="#317air", fg="white", activebackground="#89b4fa", font=("Segoe UI Bold", 11), 
                  padx=40, pady=12, bd=0, cursor="hand2").pack(pady=25)

    def setup_auditor_ui(self):
        tk.Label(self.scrollable_frame, text="SECTION 2: DATA ANALYZER (REGEX)", 
                 font=("Segoe UI Bold", 10), bg=self.bg_dark, fg="#bac2de").pack(pady=(40, 10))

        preview_frame = tk.Frame(self.scrollable_frame, bg=self.bg_dark)
        preview_frame.pack(fill="x", padx=150)

        self.text_display = tk.Text(preview_frame, height=12, font=('Consolas', 11), 
                                    bg=self.accent_dark, fg="#a6e3a1", bd=0, padx=20, pady=20, 
                                    insertbackground="white", highlightthickness=1, highlightbackground=self.border_col)
        self.text_display.pack(fill="x")

        self.btn_analyze = tk.Button(self.scrollable_frame, text="🚀 RUN REGEX ANALYSIS", command=self.analyze_emails, 
                                     bg="#a6e3a1", fg="#11111b", activebackground="#94e2d5", 
                                     font=("Segoe UI Bold", 12), padx=70, pady=15, bd=0, cursor="hand2")
        self.btn_analyze.pack(pady=25)

        self.res_label = tk.Label(self.scrollable_frame, text="Waiting for analysis...", justify="center", 
                                  font=('Segoe UI Semilight', 13), bg=self.bg_dark, fg=self.fg_light)
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

        total_ids = len(lead_ids) #
        domains_found = [email.split('@')[1] for email in emails]
        counts = Counter(domains_found)
        most_common_domain, max_freq = counts.most_common(1)[0]
        
        domain_name = most_common_domain.split('.')[0].title()
        if most_common_domain == "mseuf.edu.ph":
            target_status = "MSEUF (Academic List)"
        else:
            target_status = f"{domain_name} (General Market List)" #

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
    app = LeadApp(root)
    root.mainloop()
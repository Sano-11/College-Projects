# Activity 4 - Accessing File (CSV) with GUI
# Student: Allen
# Course: BS Computer Science
# School: MSEUF Lucena
#
# Description:
#   Part I  - CSV Record Management System with Tkinter UI
#   Part II - Data Analysis and Visualization using pandas and matplotlib

import os
import csv
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime

import pandas as pd
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# --------------------------------------------------
# File paths (CSV files are in the same folder as this script)
# --------------------------------------------------
script_dir = os.path.dirname(os.path.abspath(__file__))
DATASET_FILE = os.path.join(script_dir, "ai_job_replacement_2020_2026_v2.csv")
RECORDS_FILE = os.path.join(script_dir, "custom_records.csv")

# --------------------------------------------------
# Colors and Fonts (MSEUF theme: Maroon, White, Yellow)
# --------------------------------------------------
MAROON  = "#7B0D1E"
MAROON2 = "#5C0A16"
YELLOW  = "#F5C518"
WHITE   = "#FFFFFF"
LGRAY   = "#F5F5F5"
GRAY    = "#DDDDDD"
DGRAY   = "#555555"
BLACK   = "#111111"

FONT       = ("Arial", 10)
FONT_BOLD  = ("Arial", 10, "bold")
FONT_TITLE = ("Arial", 14, "bold")
FONT_SMALL = ("Arial", 9)


# ==================================================
# PART I - OOP: Data classes and CSV handling
# ==================================================

class JobRecord:
    FIELDS = ["ID", "Job Role", "Industry", "Country",
              "Year", "Risk %", "AI Score", "Salary (USD)", "Notes", "Date Added"]

    def __init__(self, rid, job_role, industry, country,
                 year, risk, ai_score, salary, notes="", date_added=None):
        self.rid        = str(rid).strip()
        self.job_role   = str(job_role).strip()
        self.industry   = str(industry).strip()
        self.country    = str(country).strip()
        self.year       = str(year).strip()
        self.risk       = str(risk).strip()
        self.ai_score   = str(ai_score).strip()
        self.salary     = str(salary).strip()
        self.notes      = str(notes).strip()
        self.date_added = date_added or datetime.now().strftime("%Y-%m-%d %H:%M")

    def to_dict(self):
        return {
            "ID": self.rid,
            "Job Role": self.job_role,
            "Industry": self.industry,
            "Country": self.country,
            "Year": self.year,
            "Risk %": self.risk,
            "AI Score": self.ai_score,
            "Salary (USD)": self.salary,
            "Notes": self.notes,
            "Date Added": self.date_added
        }

    @classmethod
    def from_dict(cls, d):
        return cls(
            d["ID"], d["Job Role"], d["Industry"], d["Country"],
            d["Year"], d["Risk %"], d["AI Score"], d["Salary (USD)"],
            d.get("Notes", ""), d.get("Date Added", "")
        )


class CSVRepository:
    def __init__(self, filepath):
        self.filepath = filepath
        self._create_if_not_exists()

    def _create_if_not_exists(self):
        if not os.path.exists(self.filepath):
            with open(self.filepath, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=JobRecord.FIELDS)
                writer.writeheader()

    def load_all(self):
        records = []
        with open(self.filepath, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                records.append(JobRecord.from_dict(row))
        return records

    def save_all(self, records):
        with open(self.filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=JobRecord.FIELDS)
            writer.writeheader()
            for r in records:
                writer.writerow(r.to_dict())

    def append_record(self, record):
        with open(self.filepath, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=JobRecord.FIELDS)
            writer.writerow(record.to_dict())

    def id_exists(self, rid):
        return any(r.rid == str(rid) for r in self.load_all())


class RecordManager:
    def __init__(self, repo):
        self.repo = repo

    def add_record(self, rid, job_role, industry, country,
                   year, risk, ai_score, salary, notes):
        if self.repo.id_exists(rid):
            return False, f"ID '{rid}' already exists."
        new_rec = JobRecord(rid, job_role, industry, country,
                            year, risk, ai_score, salary, notes)
        self.repo.append_record(new_rec)
        return True, f"Record added! (ID: {rid})"

    def get_all_records(self):
        return self.repo.load_all()

    def search_by_id(self, rid):
        for r in self.repo.load_all():
            if r.rid == str(rid):
                return r
        return None

    def search_by_name(self, query):
        query = query.lower()
        return [r for r in self.repo.load_all()
                if query in r.job_role.lower() or query in r.country.lower()]

    def delete_record(self, rid):
        records = self.repo.load_all()
        filtered = [r for r in records if r.rid != str(rid)]
        if len(filtered) == len(records):
            return False, f"No record found with ID '{rid}'."
        self.repo.save_all(filtered)
        return True, f"Record '{rid}' deleted."


# ==================================================
# MAIN APPLICATION
# ==================================================

class App(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("AI Job Displacement - Record Management System")
        self.geometry("1100x700")
        self.configure(bg=LGRAY)
        self.resizable(True, True)

        self.repo    = CSVRepository(RECORDS_FILE)
        self.manager = RecordManager(self.repo)
        self.df      = self._load_dataset()

        self._setup_styles()
        self._build_header()
        self._build_tabs()

    def _load_dataset(self):
        if os.path.exists(DATASET_FILE):
            df = pd.read_csv(DATASET_FILE)
            df.columns = df.columns.str.strip()
            return df
        return pd.DataFrame()

    def _setup_styles(self):
        style = ttk.Style(self)
        style.theme_use("clam")

        style.configure("TNotebook",       background=LGRAY, borderwidth=0)
        style.configure("TNotebook.Tab",   background=GRAY, foreground=BLACK,
                        font=FONT_BOLD,    padding=[16, 8])
        style.map("TNotebook.Tab",
                  background=[("selected", MAROON)],
                  foreground=[("selected", WHITE)])

        style.configure("Treeview",         background=WHITE, foreground=BLACK,
                        fieldbackground=WHITE, rowheight=24, font=FONT_SMALL)
        style.configure("Treeview.Heading", background=MAROON, foreground=WHITE,
                        font=FONT_BOLD,    relief="flat")
        style.map("Treeview",
                  background=[("selected", MAROON)],
                  foreground=[("selected", WHITE)])

        style.configure("TScrollbar", background=GRAY, troughcolor=LGRAY)
        style.configure("TFrame",     background=LGRAY)
        style.configure("TLabel",     background=LGRAY, foreground=BLACK, font=FONT)
        style.configure("TEntry",     font=FONT)

    def _build_header(self):
        header = tk.Frame(self, bg=MAROON, height=60)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        tk.Label(header,
                 text="  AI Job Displacement Analytics System",
                 bg=MAROON, fg=WHITE,
                 font=("Arial", 15, "bold")).pack(side="left", padx=10, pady=12)

        tk.Label(header,
                 text="MSEUF Lucena  |  BS Computer Science  ",
                 bg=MAROON, fg=YELLOW,
                 font=FONT_SMALL).pack(side="right", padx=10)

        if not self.df.empty:
            tk.Label(header,
                     text=f"Dataset: {len(self.df):,} records loaded  |  ",
                     bg=MAROON, fg=WHITE,
                     font=FONT_SMALL).pack(side="right")

    def _build_tabs(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.tab_records  = tk.Frame(self.notebook, bg=LGRAY)
        self.tab_dataset  = tk.Frame(self.notebook, bg=LGRAY)
        self.tab_analysis = tk.Frame(self.notebook, bg=LGRAY)
        self.tab_charts   = tk.Frame(self.notebook, bg=LGRAY)

        self.notebook.add(self.tab_records,  text="  My Records  ")
        self.notebook.add(self.tab_dataset,  text="  View Dataset  ")
        self.notebook.add(self.tab_analysis, text="  Data Analysis  ")
        self.notebook.add(self.tab_charts,   text="  Charts  ")

        self._build_records_tab()
        self._build_dataset_tab()
        self._build_analysis_tab()
        self._build_charts_tab()

        self.notebook.bind("<<NotebookTabChanged>>", self._on_tab_change)

    def _on_tab_change(self, event):
        tab = self.notebook.index(self.notebook.select())
        if tab == 2:
            self._run_analysis()
        elif tab == 3:
            self._render_chart()

    def _make_btn(self, parent, text, bg, fg, command):
        return tk.Button(parent, text=text, bg=bg, fg=fg,
                         font=FONT_BOLD, relief="flat",
                         padx=8, pady=6, cursor="hand2",
                         activebackground=MAROON2, activeforeground=WHITE,
                         command=command)


    # ==================================================
    # TAB 1 - My Records
    # ==================================================

    def _build_records_tab(self):
        left = tk.Frame(self.tab_records, bg=WHITE, bd=1, relief="solid")
        left.pack(side="left", fill="y", padx=(0, 6), pady=0, ipadx=10, ipady=10)

        tk.Label(left, text="Add New Record", bg=WHITE, fg=MAROON,
                 font=FONT_TITLE).grid(row=0, column=0, columnspan=2,
                                       pady=(10, 12), padx=12, sticky="w")

        fields = [
            ("ID",           "rid"),
            ("Job Role",     "job_role"),
            ("Industry",     "industry"),
            ("Country",      "country"),
            ("Year",         "year"),
            ("Risk %",       "risk"),
            ("AI Score",     "ai_score"),
            ("Salary (USD)", "salary"),
            ("Notes",        "notes"),
        ]
        self.form_entries = {}
        for i, (label, key) in enumerate(fields, start=1):
            tk.Label(left, text=label + ":", bg=WHITE, fg=DGRAY,
                     font=FONT_SMALL).grid(row=i, column=0, padx=12, pady=3, sticky="w")
            entry = tk.Entry(left, font=FONT, width=22, bg=LGRAY, relief="solid", bd=1)
            entry.grid(row=i, column=1, padx=12, pady=3)
            self.form_entries[key] = entry

        btn_frame = tk.Frame(left, bg=WHITE)
        btn_frame.grid(row=len(fields)+1, column=0, columnspan=2,
                       pady=12, padx=12, sticky="ew")

        self._make_btn(btn_frame, "Add Record",   MAROON,    WHITE, self._add_record).pack(fill="x", pady=2)
        self._make_btn(btn_frame, "Delete by ID", "#B22222", WHITE, self._delete_record).pack(fill="x", pady=2)
        self._make_btn(btn_frame, "Clear Form",   GRAY,      BLACK, self._clear_form).pack(fill="x", pady=2)

        tk.Frame(left, bg=GRAY, height=1).grid(
            row=len(fields)+2, column=0, columnspan=2, sticky="ew", padx=12, pady=8)

        tk.Label(left, text="Search Records", bg=WHITE, fg=MAROON,
                 font=FONT_BOLD).grid(row=len(fields)+3, column=0, columnspan=2,
                                      padx=12, sticky="w")

        self.search_var = tk.StringVar()
        tk.Entry(left, textvariable=self.search_var, font=FONT, width=22,
                 bg=LGRAY, relief="solid", bd=1).grid(
            row=len(fields)+4, column=0, columnspan=2, padx=12, pady=4, sticky="ew")

        search_btns = tk.Frame(left, bg=WHITE)
        search_btns.grid(row=len(fields)+5, column=0, columnspan=2, padx=12, sticky="ew")
        self._make_btn(search_btns, "By ID",   YELLOW, BLACK, self._search_by_id).pack(side="left", fill="x", expand=True, padx=(0, 2))
        self._make_btn(search_btns, "By Name", YELLOW, BLACK, self._search_by_name).pack(side="left", fill="x", expand=True)

        self._make_btn(left, "Show All Records", GRAY, BLACK,
                       self._refresh_records_table).grid(
            row=len(fields)+6, column=0, columnspan=2, padx=12, pady=(6, 0), sticky="ew")

        self.status_label = tk.Label(left, text="", bg=WHITE, fg="green",
                                     font=FONT_SMALL, wraplength=230, justify="left")
        self.status_label.grid(row=len(fields)+7, column=0, columnspan=2,
                               padx=12, pady=6, sticky="w")

        right = tk.Frame(self.tab_records, bg=WHITE, bd=1, relief="solid")
        right.pack(side="left", fill="both", expand=True)

        hdr = tk.Frame(right, bg=MAROON)
        hdr.pack(fill="x")
        tk.Label(hdr, text="  My Records  (custom_records.csv)",
                 bg=MAROON, fg=WHITE, font=FONT_BOLD).pack(side="left", pady=6)

        cols = JobRecord.FIELDS
        self.records_tree = ttk.Treeview(right, columns=cols, show="headings")
        col_widths = [45, 130, 100, 90, 50, 55, 65, 90, 110, 120]
        for col, w in zip(cols, col_widths):
            self.records_tree.heading(col, text=col)
            self.records_tree.column(col, width=w, minwidth=40)

        vsb = ttk.Scrollbar(right, orient="vertical",   command=self.records_tree.yview)
        hsb = ttk.Scrollbar(right, orient="horizontal", command=self.records_tree.xview)
        self.records_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.records_tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")
        hsb.pack(side="bottom", fill="x")

        self.records_tree.tag_configure("odd",  background="#FFF0F0")
        self.records_tree.tag_configure("even", background=WHITE)

        self._refresh_records_table()

    def _refresh_records_table(self):
        self.records_tree.delete(*self.records_tree.get_children())
        for i, r in enumerate(self.manager.get_all_records()):
            tag = "odd" if i % 2 else "even"
            self.records_tree.insert("", "end", values=[
                r.rid, r.job_role, r.industry, r.country,
                r.year, r.risk, r.ai_score, r.salary,
                r.notes, r.date_added
            ], tags=(tag,))

    def _set_status(self, msg, ok=True):
        self.status_label.config(text=msg, fg="green" if ok else "red")

    def _add_record(self):
        v = {k: e.get().strip() for k, e in self.form_entries.items()}
        required = ["rid", "job_role", "industry", "country",
                    "year", "risk", "ai_score", "salary"]
        if any(not v[k] for k in required):
            self._set_status("Please fill in all required fields.", ok=False)
            return
        ok, msg = self.manager.add_record(
            v["rid"], v["job_role"], v["industry"], v["country"],
            v["year"], v["risk"], v["ai_score"], v["salary"], v["notes"])
        self._set_status(msg, ok)
        if ok:
            self._clear_form()
            self._refresh_records_table()

    def _delete_record(self):
        rid = self.form_entries["rid"].get().strip()
        if not rid:
            self._set_status("Enter an ID in the ID field to delete.", ok=False)
            return
        if messagebox.askyesno("Confirm Delete", f"Delete record with ID '{rid}'?"):
            ok, msg = self.manager.delete_record(rid)
            self._set_status(msg, ok)
            if ok:
                self._refresh_records_table()

    def _clear_form(self):
        for entry in self.form_entries.values():
            entry.delete(0, "end")
        self.status_label.config(text="")

    def _search_by_id(self):
        q = self.search_var.get().strip()
        result = self.manager.search_by_id(q)
        self.records_tree.delete(*self.records_tree.get_children())
        if result:
            self.records_tree.insert("", "end", values=[
                result.rid, result.job_role, result.industry, result.country,
                result.year, result.risk, result.ai_score, result.salary,
                result.notes, result.date_added])
            self._set_status(f"Found record: {q}")
        else:
            self._set_status(f"No record with ID '{q}'.", ok=False)

    def _search_by_name(self):
        q = self.search_var.get().strip()
        results = self.manager.search_by_name(q)
        self.records_tree.delete(*self.records_tree.get_children())
        for i, r in enumerate(results):
            tag = "odd" if i % 2 else "even"
            self.records_tree.insert("", "end", values=[
                r.rid, r.job_role, r.industry, r.country,
                r.year, r.risk, r.ai_score, r.salary,
                r.notes, r.date_added], tags=(tag,))
        self._set_status(f"{len(results)} result(s) found for '{q}'.", ok=bool(results))


    # ==================================================
    # TAB 2 - View Dataset
    # ==================================================

    def _build_dataset_tab(self):
        filter_bar = tk.Frame(self.tab_dataset, bg=MAROON)
        filter_bar.pack(fill="x")

        tk.Label(filter_bar, text="  Filter by Industry:",
                 bg=MAROON, fg=WHITE, font=FONT_SMALL).pack(side="left", padx=(10, 2), pady=8)

        industries = ["All"] + (sorted(self.df["industry"].unique().tolist()) if not self.df.empty else [])
        self.ds_industry_var = tk.StringVar(value="All")
        ttk.Combobox(filter_bar, textvariable=self.ds_industry_var,
                     values=industries, width=14, state="readonly",
                     font=FONT_SMALL).pack(side="left", padx=4, pady=6)

        tk.Label(filter_bar, text="Year:",
                 bg=MAROON, fg=WHITE, font=FONT_SMALL).pack(side="left", padx=(10, 2))

        years = ["All"] + (sorted(self.df["year"].unique().tolist()) if not self.df.empty else [])
        self.ds_year_var = tk.StringVar(value="All")
        ttk.Combobox(filter_bar, textvariable=self.ds_year_var,
                     values=years, width=8, state="readonly",
                     font=FONT_SMALL).pack(side="left", padx=4, pady=6)

        self._make_btn(filter_bar, "Apply Filter", YELLOW, BLACK,
                       self._filter_dataset).pack(side="left", padx=10)

        self.ds_count_label = tk.Label(filter_bar, text="", bg=MAROON, fg=YELLOW, font=FONT_SMALL)
        self.ds_count_label.pack(side="right", padx=12)

        if self.df.empty:
            tk.Label(self.tab_dataset,
                     text="Dataset file not found.\nMake sure 'ai_job_replacement_2020_2026_v2.csv' is in the same folder as this script.",
                     bg=LGRAY, fg=DGRAY, font=FONT).pack(expand=True)
            return

        table_frame = tk.Frame(self.tab_dataset, bg=LGRAY)
        table_frame.pack(fill="both", expand=True)

        cols = list(self.df.columns)
        self.ds_tree = ttk.Treeview(table_frame, columns=cols, show="headings")
        for col in cols:
            self.ds_tree.heading(col, text=col.replace("_", " ").title())
            self.ds_tree.column(col, width=110, minwidth=60)

        vsb = ttk.Scrollbar(table_frame, orient="vertical",   command=self.ds_tree.yview)
        hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=self.ds_tree.xview)
        self.ds_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.ds_tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")
        hsb.pack(side="bottom", fill="x")

        self.ds_tree.tag_configure("odd",  background="#FFF0F0")
        self.ds_tree.tag_configure("even", background=WHITE)

        self._load_dataset_table(self.df)

    def _load_dataset_table(self, df):
        self.ds_tree.delete(*self.ds_tree.get_children())
        for i, (_, row) in enumerate(df.iterrows()):
            tag = "odd" if i % 2 else "even"
            self.ds_tree.insert("", "end", values=list(row), tags=(tag,))
        self.ds_count_label.config(text=f"Showing {len(df):,} records  ")

    def _filter_dataset(self):
        df = self.df.copy()
        if self.ds_industry_var.get() != "All":
            df = df[df["industry"] == self.ds_industry_var.get()]
        if self.ds_year_var.get() != "All":
            df = df[df["year"] == int(self.ds_year_var.get())]
        self._load_dataset_table(df)


    # ==================================================
    # TAB 3 - Data Analysis
    # ==================================================

    def _build_analysis_tab(self):
        ctrl = tk.Frame(self.tab_analysis, bg=MAROON)
        ctrl.pack(fill="x")

        tk.Label(ctrl, text="  Data Analysis  |  Year:",
                 bg=MAROON, fg=WHITE, font=FONT_BOLD).pack(side="left", pady=8, padx=4)

        years = ["All"] + (sorted(self.df["year"].unique().tolist()) if not self.df.empty else [])
        self.an_year_var = tk.StringVar(value="All")
        ttk.Combobox(ctrl, textvariable=self.an_year_var,
                     values=years, width=8, state="readonly",
                     font=FONT_SMALL).pack(side="left", padx=4, pady=6)

        tk.Label(ctrl, text="Industry:",
                 bg=MAROON, fg=WHITE, font=FONT_SMALL).pack(side="left", padx=(10, 2))

        industries = ["All"] + (sorted(self.df["industry"].unique().tolist()) if not self.df.empty else [])
        self.an_industry_var = tk.StringVar(value="All")
        ttk.Combobox(ctrl, textvariable=self.an_industry_var,
                     values=industries, width=14, state="readonly",
                     font=FONT_SMALL).pack(side="left", padx=4, pady=6)

        self._make_btn(ctrl, "Run Analysis", YELLOW, BLACK,
                       self._run_analysis).pack(side="left", padx=10)

        out_frame = tk.Frame(self.tab_analysis, bg=LGRAY)
        out_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.analysis_text = tk.Text(
            out_frame, bg=WHITE, fg=BLACK,
            font=("Courier New", 10), relief="solid", bd=1,
            padx=12, pady=10, wrap="none"
        )
        vsb = ttk.Scrollbar(out_frame, command=self.analysis_text.yview)
        hsb = ttk.Scrollbar(out_frame, orient="horizontal", command=self.analysis_text.xview)
        self.analysis_text.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.analysis_text.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")
        hsb.pack(side="bottom", fill="x")

        self.analysis_text.tag_configure("title",   foreground=MAROON,  font=("Courier New", 11, "bold"))
        self.analysis_text.tag_configure("section", foreground=MAROON2, font=("Courier New", 10, "bold"))
        self.analysis_text.tag_configure("gray",    foreground=DGRAY)
        self.analysis_text.tag_configure("good",    foreground="green")
        self.analysis_text.tag_configure("bad",     foreground="red")

        if not self.df.empty:
            self._run_analysis()

    def _run_analysis(self):
        self.analysis_text.config(state="normal")
        self.analysis_text.delete("1.0", "end")

        df = self.df.copy()
        if df.empty:
            self.analysis_text.insert("end", "\nNo dataset loaded.\n", "bad")
            self.analysis_text.config(state="disabled")
            return

        if self.an_year_var.get() != "All":
            df = df[df["year"] == int(self.an_year_var.get())]
        if self.an_industry_var.get() != "All":
            df = df[df["industry"] == self.an_industry_var.get()]

        def write(text, tag=""):
            self.analysis_text.insert("end", text, tag)

        sep = "-" * 65

        write("\n  AI Job Displacement - Data Analysis Report\n", "title")
        write(f"  Year = {self.an_year_var.get()}  |  Industry = {self.an_industry_var.get()}\n", "gray")
        write(f"  Records in filter: {len(df):,}\n\n", "gray")

        # Q1
        write("  Q1: What is the average automation risk per industry?\n", "section")
        write(f"  {sep}\n", "gray")
        q1 = df.groupby("industry")["automation_risk_percent"].mean().sort_values(ascending=False).round(2)
        write(f"  {'Industry':<22} {'Avg Risk %':>10}\n")
        for ind, val in q1.items():
            tag = "bad" if val > 55 else ("good" if val < 35 else "")
            write(f"  {ind:<22} {val:>10.2f}\n", tag)

        # Q2
        write(f"\n  Q2: Which countries have the highest average AI replacement score?\n", "section")
        write(f"  {sep}\n", "gray")
        q2 = df.groupby("country")["ai_replacement_score"].mean().sort_values(ascending=False).round(2)
        write(f"  {'Country':<18} {'Avg AI Score':>14}\n")
        for country, val in q2.items():
            write(f"  {country:<18} {val:>14.2f}\n")

        # Q3
        write(f"\n  Q3: How does automation risk category affect average salary change?\n", "section")
        write(f"  {sep}\n", "gray")
        q3 = df.groupby("automation_risk_category")["salary_change_percent"].mean().round(2)
        write(f"  {'Risk Category':<18} {'Avg Salary Change %':>20}\n")
        for cat, val in q3.items():
            tag = "bad" if val < 0 else "good"
            write(f"  {cat:<18} {val:>20.2f}%\n", tag)

        # Q4
        write(f"\n  Q4: How have AI adoption levels changed year by year?\n", "section")
        write(f"  {sep}\n", "gray")
        q4 = df.groupby("year")[["ai_adoption_level", "reskilling_urgency_score"]].mean().round(2)
        write(f"  {'Year':<8} {'AI Adoption Avg':>16} {'Reskilling Urgency Avg':>24}\n")
        for yr, row in q4.iterrows():
            write(f"  {int(yr):<8} {row['ai_adoption_level']:>16.2f} {row['reskilling_urgency_score']:>24.2f}\n")

        # Q5
        write(f"\n  Q5: What are the top 10 job roles with the highest salary before AI?\n", "section")
        write(f"  {sep}\n", "gray")
        q5 = df.groupby("job_role")["salary_before_usd"].mean().sort_values(ascending=False).head(10).round(2)
        write(f"  {'Job Role':<28} {'Avg Salary Before (USD)':>24}\n")
        for role, val in q5.items():
            write(f"  {role:<28} ${val:>23,.2f}\n")

        # Bonus
        write(f"\n  Bonus: Correlation - Skill Gap Index, Wage Volatility, AI Disruption\n", "section")
        write(f"  {sep}\n", "gray")
        cols_corr = ["skill_gap_index", "wage_volatility_index", "ai_disruption_intensity"]
        if all(c in df.columns for c in cols_corr):
            corr = df[cols_corr].corr().round(3)
            write(f"\n{corr.to_string()}\n")

        write(f"\n  {sep}\n", "gray")
        write(f"  Done. {len(df):,} records analyzed.\n\n", "good")
        self.analysis_text.config(state="disabled")


    # ==================================================
    # TAB 4 - Charts
    # ==================================================

    def _build_charts_tab(self):
        ctrl = tk.Frame(self.tab_charts, bg=MAROON)
        ctrl.pack(fill="x")

        tk.Label(ctrl, text="  Select Chart:",
                 bg=MAROON, fg=WHITE, font=FONT_BOLD).pack(side="left", pady=8, padx=8)

        self.chart_var = tk.StringVar(value="Overview")
        chart_options = [
            "Overview",
            "Risk by Industry",
            "Salary Before vs After",
            "Trend Over Years",
            "Top Job Roles"
        ]
        self._chart_buttons = {}
        for opt in chart_options:
            btn = tk.Button(
                ctrl, text=opt,
                bg=MAROON2, fg=WHITE,
                font=FONT_SMALL, relief="flat",
                padx=10, pady=5, cursor="hand2",
                bd=2,
                command=lambda o=opt: self._select_chart(o)
            )
            btn.pack(side="left", padx=4, pady=8)
            self._chart_buttons[opt] = btn

        # Highlight the default selected button
        self._chart_buttons["Overview"].config(bg=YELLOW, fg=BLACK)

        self._make_btn(ctrl, "Save Chart", YELLOW, BLACK,
                       self._save_chart).pack(side="right", padx=10)

        self.chart_area = tk.Frame(self.tab_charts, bg=WHITE)
        self.chart_area.pack(fill="both", expand=True)

    def _select_chart(self, option):
        self.chart_var.set(option)
        for opt, btn in self._chart_buttons.items():
            if opt == option:
                btn.config(bg=YELLOW, fg=BLACK)
            else:
                btn.config(bg=MAROON2, fg=WHITE)
        self._render_chart()

    def _render_chart(self):
        if self.df.empty:
            return
        df = self.df
        choice = self.chart_var.get()

        plt.rcParams.update({
            "figure.facecolor": WHITE,
            "axes.facecolor":   "#FFF8F8",
            "axes.edgecolor":   GRAY,
            "text.color":       BLACK,
            "axes.labelcolor":  DGRAY,
            "xtick.color":      DGRAY,
            "ytick.color":      DGRAY,
            "axes.titlecolor":  MAROON,
            "grid.color":       GRAY,
            "font.family":      "sans-serif",
        })

        fig = plt.Figure(figsize=(10, 6), tight_layout=True)

        if   choice == "Overview":              self._chart_overview(fig, df)
        elif choice == "Risk by Industry":      self._chart_risk(fig, df)
        elif choice == "Salary Before vs After": self._chart_salary(fig, df)
        elif choice == "Trend Over Years":      self._chart_trend(fig, df)
        elif choice == "Top Job Roles":         self._chart_jobs(fig, df)

        for widget in self.chart_area.winfo_children():
            widget.destroy()
        canvas = FigureCanvasTkAgg(fig, master=self.chart_area)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        self._current_fig = fig

    def _save_chart(self):
        if not hasattr(self, "_current_fig"):
            messagebox.showinfo("No Chart", "Go to the Charts tab first to generate a chart.")
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG Image", "*.png"), ("All Files", "*.*")])
        if path:
            self._current_fig.savefig(path, dpi=150, bbox_inches="tight")
            messagebox.showinfo("Saved", f"Chart saved:\n{path}")

    def _chart_overview(self, fig, df):
        axes = fig.subplots(2, 2)
        fig.suptitle("Overview Dashboard", color=MAROON, fontsize=13, fontweight="bold")

        ax = axes[0, 0]
        rc = df["automation_risk_category"].value_counts()
        ax.pie(rc.values, labels=rc.index, autopct="%1.1f%%",
               colors=[MAROON, YELLOW, "#CCCCCC"], startangle=120,
               wedgeprops=dict(edgecolor=WHITE, linewidth=2))
        ax.set_title("Automation Risk Categories")

        ax = axes[0, 1]
        by_ind = df.groupby("industry")["ai_replacement_score"].mean().sort_values()
        ax.barh(by_ind.index, by_ind.values, color=MAROON, edgecolor=WHITE)
        ax.set_title("Avg AI Replacement Score by Industry")
        ax.set_xlabel("Score")

        ax = axes[1, 0]
        trend = df.groupby("year")[["ai_adoption_level", "reskilling_urgency_score"]].mean()
        ax.plot(trend.index, trend["ai_adoption_level"], marker="o",
                color=MAROON, label="AI Adoption", linewidth=2)
        ax.plot(trend.index, trend["reskilling_urgency_score"], marker="s",
                color=YELLOW, label="Reskilling Urgency", linewidth=2)
        ax.set_title("AI Adoption vs Reskilling Urgency")
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)

        ax = axes[1, 1]
        ax.scatter(df["automation_risk_percent"], df["salary_change_percent"],
                   alpha=0.3, s=10, color=MAROON)
        ax.axhline(0, color="red", linestyle="--", linewidth=1)
        ax.set_title("Automation Risk vs Salary Change %")
        ax.set_xlabel("Automation Risk %")
        ax.set_ylabel("Salary Change %")

    def _chart_risk(self, fig, df):
        ax = fig.add_subplot(111)
        fig.suptitle("Automation Risk % by Industry (Box Plot)",
                     color=MAROON, fontsize=13, fontweight="bold")
        industries = sorted(df["industry"].unique())
        data = [df[df["industry"] == ind]["automation_risk_percent"].dropna().values
                for ind in industries]
        bp = ax.boxplot(data, labels=industries, patch_artist=True,
                        medianprops=dict(color=YELLOW, linewidth=2))
        for patch in bp["boxes"]:
            patch.set_facecolor(MAROON)
            patch.set_alpha(0.6)
        ax.set_ylabel("Automation Risk %")
        ax.grid(True, axis="y", alpha=0.3)
        plt.setp(ax.get_xticklabels(), rotation=20, ha="right", fontsize=9)

    def _chart_salary(self, fig, df):
        axes = fig.subplots(1, 2)
        fig.suptitle("Salary Impact of AI Automation",
                     color=MAROON, fontsize=13, fontweight="bold")

        ax = axes[0]
        grp = df.groupby("country")[["salary_before_usd", "salary_after_usd"]].mean().sort_values("salary_before_usd")
        x = range(len(grp))
        w = 0.38
        ax.bar([i - w/2 for i in x], grp["salary_before_usd"] / 1000, w,
               label="Before", color=MAROON, alpha=0.85)
        ax.bar([i + w/2 for i in x], grp["salary_after_usd"] / 1000, w,
               label="After",  color=YELLOW, alpha=0.85)
        ax.set_xticks(list(x))
        ax.set_xticklabels(grp.index, rotation=30, ha="right", fontsize=8)
        ax.set_ylabel("Avg Salary (USD '000)")
        ax.set_title("Salary Before vs After by Country")
        ax.legend(fontsize=8)
        ax.grid(True, axis="y", alpha=0.3)

        ax = axes[1]
        change = df["salary_change_percent"].dropna()
        ax.hist(change, bins=40, color=MAROON, edgecolor=WHITE, alpha=0.85)
        ax.axvline(change.mean(), color=YELLOW, linestyle="--", linewidth=2,
                   label=f"Mean: {change.mean():.1f}%")
        ax.axvline(0, color="red", linestyle="--", linewidth=1, label="0% (no change)")
        ax.set_title("Distribution of Salary Change %")
        ax.set_xlabel("Salary Change %")
        ax.set_ylabel("Count")
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)

    def _chart_trend(self, fig, df):
        ax = fig.add_subplot(111)
        fig.suptitle("Key Metrics Trend Over Years (2020-2026)",
                     color=MAROON, fontsize=13, fontweight="bold")
        metrics = {
            "ai_replacement_score":     (MAROON,    "AI Replacement Score"),
            "reskilling_urgency_score":  (YELLOW,    "Reskilling Urgency"),
            "skill_gap_index":           ("#888888", "Skill Gap Index"),
            "wage_volatility_index":     ("#CC6600", "Wage Volatility"),
        }
        for col, (color, label) in metrics.items():
            trend = df.groupby("year")[col].mean()
            ax.plot(trend.index, trend.values, marker="o", color=color,
                    label=label, linewidth=2, markersize=5)
        ax.set_xlabel("Year")
        ax.set_ylabel("Average Score")
        ax.legend(fontsize=9)
        ax.grid(True, alpha=0.3)
        ax.set_xticks(sorted(df["year"].unique()))

    def _chart_jobs(self, fig, df):
        axes = fig.subplots(1, 2)
        fig.suptitle("Top 10 Job Roles Comparison",
                     color=MAROON, fontsize=13, fontweight="bold")

        top_risk = df.groupby("job_role")["automation_risk_percent"].mean().sort_values(ascending=False).head(10)
        ax = axes[0]
        ax.barh(top_risk.index[::-1], top_risk.values[::-1],
                color=MAROON, edgecolor=WHITE, alpha=0.85)
        ax.set_title("Highest Automation Risk")
        ax.set_xlabel("Avg Automation Risk %")
        ax.grid(True, axis="x", alpha=0.3)

        top_sal = df.groupby("job_role")["salary_before_usd"].mean().sort_values(ascending=False).head(10)
        ax = axes[1]
        ax.barh(top_sal.index[::-1], top_sal.values[::-1] / 1000,
                color=YELLOW, edgecolor=WHITE, alpha=0.85)
        ax.set_title("Highest Salary Before AI")
        ax.set_xlabel("Avg Salary (USD '000)")
        ax.grid(True, axis="x", alpha=0.3)


# ==================================================
# Entry point
# ==================================================
if __name__ == "__main__":
    app = App()
    app.mainloop()

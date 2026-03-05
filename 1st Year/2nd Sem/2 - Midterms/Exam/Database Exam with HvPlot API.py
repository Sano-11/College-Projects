"""
PART I: CSV Record Management System
=====================================
A fully OOP-based student record management system.
Supports: Add, Display All, Search, and Delete records.
Data is persisted in a CSV file.
"""

import csv
import os
from datetime import datetime


# ─────────────────────────────────────────────
# Data Model
# ─────────────────────────────────────────────

class StudentRecord:
    """Represents a single student record."""

    FIELDS = ["ID", "Name", "Age", "Course", "Grade", "Date Added"]

    def __init__(self, record_id, name, age, course, grade, date_added=None):
        self.record_id = str(record_id).strip()
        self.name = str(name).strip()
        self.age = str(age).strip()
        self.course = str(course).strip()
        self.grade = str(grade).strip()
        self.date_added = date_added or datetime.now().strftime("%Y-%m-%d %H:%M")

    def to_dict(self):
        return {
            "ID": self.record_id,
            "Name": self.name,
            "Age": self.age,
            "Course": self.course,
            "Grade": self.grade,
            "Date Added": self.date_added,
        }

    @classmethod
    def from_dict(cls, d):
        return cls(
            record_id=d["ID"],
            name=d["Name"],
            age=d["Age"],
            course=d["Course"],
            grade=d["Grade"],
            date_added=d["Date Added"],
        )

    def __str__(self):
        return (
            f"  ID         : {self.record_id}\n"
            f"  Name       : {self.name}\n"
            f"  Age        : {self.age}\n"
            f"  Course     : {self.course}\n"
            f"  Grade      : {self.grade}\n"
            f"  Date Added : {self.date_added}"
        )


# ─────────────────────────────────────────────
# CSV Repository
# ─────────────────────────────────────────────

class CSVRepository:
    """Handles all CSV read/write operations."""

    def __init__(self, filepath):
        self.filepath = filepath
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        if not os.path.exists(self.filepath):
            with open(self.filepath, "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=StudentRecord.FIELDS)
                writer.writeheader()

    def load_all(self):
        records = []
        with open(self.filepath, "r", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                records.append(StudentRecord.from_dict(row))
        return records

    def save_all(self, records):
        with open(self.filepath, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=StudentRecord.FIELDS)
            writer.writeheader()
            for r in records:
                writer.writerow(r.to_dict())

    def append_record(self, record):
        with open(self.filepath, "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=StudentRecord.FIELDS)
            writer.writerow(record.to_dict())

    def id_exists(self, record_id):
        return any(r.record_id == str(record_id) for r in self.load_all())


# ─────────────────────────────────────────────
# Record Manager (Business Logic)
# ─────────────────────────────────────────────

class RecordManager:
    """Handles all business logic for student records."""

    def __init__(self, repository):
        self.repo = repository

    def add_record(self, record_id, name, age, course, grade):
        if self.repo.id_exists(record_id):
            return False, f"Error: A record with ID '{record_id}' already exists."
        record = StudentRecord(record_id, name, age, course, grade)
        self.repo.append_record(record)
        return True, f"Record for '{name}' added successfully."

    def get_all_records(self):
        return self.repo.load_all()

    def search_by_id(self, record_id):
        for r in self.repo.load_all():
            if r.record_id == str(record_id):
                return r
        return None

    def search_by_name(self, name_query):
        query = name_query.lower()
        return [r for r in self.repo.load_all() if query in r.name.lower()]

    def delete_record(self, record_id):
        records = self.repo.load_all()
        filtered = [r for r in records if r.record_id != str(record_id)]
        if len(filtered) == len(records):
            return False, f"No record found with ID '{record_id}'."
        self.repo.save_all(filtered)
        return True, f"Record with ID '{record_id}' deleted successfully."


# ─────────────────────────────────────────────
# UI / Display Helpers
# ─────────────────────────────────────────────

class UI:
    """Handles all user interface interactions."""

    DIVIDER = "=" * 55
    THIN_DIV = "-" * 55

    @staticmethod
    def clear():
        os.system("cls" if os.name == "nt" else "clear")

    @staticmethod
    def header(title):
        print(f"\n{UI.DIVIDER}")
        print(f"  {title}")
        print(UI.DIVIDER)

    @staticmethod
    def success(msg):
        print(f"\n  ✔  {msg}")

    @staticmethod
    def error(msg):
        print(f"\n  ✘  {msg}")

    @staticmethod
    def info(msg):
        print(f"\n  ℹ  {msg}")

    @staticmethod
    def input_field(prompt):
        return input(f"  {prompt}: ").strip()

    @staticmethod
    def print_record(record, index=None):
        prefix = f"  Record #{index}" if index else "  Record"
        print(f"\n{UI.THIN_DIV}")
        if index:
            print(prefix)
            print(UI.THIN_DIV)
        print(record)

    @staticmethod
    def print_table(records):
        if not records:
            UI.info("No records found.")
            return
        header = f"{'ID':<8} {'Name':<20} {'Age':<5} {'Course':<20} {'Grade':<7} {'Date Added'}"
        print(f"\n  {UI.THIN_DIV}")
        print(f"  {header}")
        print(f"  {UI.THIN_DIV}")
        for r in records:
            row = f"{r.record_id:<8} {r.name:<20} {r.age:<5} {r.course:<20} {r.grade:<7} {r.date_added}"
            print(f"  {row}")
        print(f"  {UI.THIN_DIV}")
        print(f"  Total records: {len(records)}")

    @staticmethod
    def pause():
        input("\n  Press Enter to continue...")


# ─────────────────────────────────────────────
# Application Controller
# ─────────────────────────────────────────────

class Application:
    """Main application controller."""

    CSV_FILE = "students.csv"

    def __init__(self):
        self.repo = CSVRepository(self.CSV_FILE)
        self.manager = RecordManager(self.repo)

    def run(self):
        while True:
            self._show_menu()
            choice = UI.input_field("Enter your choice")
            if choice == "1":
                self._add_record()
            elif choice == "2":
                self._display_all()
            elif choice == "3":
                self._search_record()
            elif choice == "4":
                self._delete_record()
            elif choice == "5":
                print("\n  Goodbye!\n")
                break
            else:
                UI.error("Invalid choice. Please select 1–5.")
                UI.pause()

    def _show_menu(self):
        UI.header("Student Record Management System")
        print("  [1] Add New Record")
        print("  [2] Display All Records")
        print("  [3] Search Record")
        print("  [4] Delete Record")
        print("  [5] Exit")
        print(UI.DIVIDER)

    def _add_record(self):
        UI.header("Add New Student Record")
        record_id = UI.input_field("Student ID")
        name     = UI.input_field("Full Name")
        age      = UI.input_field("Age")
        course   = UI.input_field("Course")
        grade    = UI.input_field("Grade (e.g. A, B+, 90)")

        if not all([record_id, name, age, course, grade]):
            UI.error("All fields are required. Record not saved.")
        else:
            ok, msg = self.manager.add_record(record_id, name, age, course, grade)
            UI.success(msg) if ok else UI.error(msg)
        UI.pause()

    def _display_all(self):
        UI.header("All Student Records")
        records = self.manager.get_all_records()
        UI.print_table(records)
        UI.pause()

    def _search_record(self):
        UI.header("Search Student Record")
        print("  [1] Search by ID")
        print("  [2] Search by Name")
        sub = UI.input_field("Select search type")

        if sub == "1":
            record_id = UI.input_field("Enter Student ID")
            result = self.manager.search_by_id(record_id)
            if result:
                UI.print_record(result)
            else:
                UI.error(f"No record found with ID '{record_id}'.")

        elif sub == "2":
            name_query = UI.input_field("Enter Name (partial allowed)")
            results = self.manager.search_by_name(name_query)
            if results:
                UI.info(f"{len(results)} match(es) found:")
                UI.print_table(results)
            else:
                UI.error(f"No records matching '{name_query}'.")
        else:
            UI.error("Invalid search type.")
        UI.pause()

    def _delete_record(self):
        UI.header("Delete Student Record")
        record_id = UI.input_field("Enter Student ID to delete")
        record = self.manager.search_by_id(record_id)
        if not record:
            UI.error(f"No record found with ID '{record_id}'.")
        else:
            UI.print_record(record)
            confirm = UI.input_field("\n  Confirm delete? (yes/no)")
            if confirm.lower() in ("yes", "y"):
                ok, msg = self.manager.delete_record(record_id)
                UI.success(msg) if ok else UI.error(msg)
            else:
                UI.info("Deletion cancelled.")
        UI.pause()


# ─────────────────────────────────────────────
# Entry Point
# ─────────────────────────────────────────────

if __name__ == "__main__":
    app = Application()
    app.run()
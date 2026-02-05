# University Library System & Data Analyzer Suite

A comprehensive Python desktop application suite developed for **Enverga University**. This project demonstrates advanced implementation of **Object-Oriented Programming (OOP)** and **Regular Expressions (RegEx)** to solve practical administrative and data-driven tasks.

---

## 📚 Module 1: University Library System

### Description
A professional management portal designed to streamline the tracking of book inventories and records. Built with Python's **Tkinter** library, it features a modern interface that allows administrators to manage titles, authors, and ISBN codes with ease.

### Key Features
* **Inventory Management**: Add new book records including Title, Author, and ISBN.
* **Real-time Availability Tracking**: Toggle status between "Available" (green indicator) and "Checked Out" (red indicator).
* **Live Filtering**: Instant database search functionality based on ISBN codes.
* **Database Control**: Features a "Wipe Database" option for total management resets.

### Technical Architecture (OOP)
The system is built on a clean architecture using three primary classes:
* **`Book` Class**: Encapsulates individual book data and availability using protected attributes and getter/setter methods.
* **`Library` Class**: The backend engine that manages a collection of `Book` objects through **composition**.
* **`LibraryGUI` Class**: The presentation layer that handles the window lifecycle, styles, and user interactions.

---

## 🔍 Module 2: Text File Generator & Data Analyzer

### Description
A high-performance desktop utility designed for automated lead generation and data processing. It uses combinatorial logic to synthesize datasets and Regular Expressions to audit them within a professional Tkinter interface.

### Key Features
* **Lead Generation**: Synthesizes unique lead identifiers and emails from user-provided names using `itertools.permutations`.
* **Multi-threaded Engine**: Offloads heavy generation tasks to a background thread to prevent UI freezing.
* **RegEx Analysis Engine**: Scrapes the dataset in real-time to calculate lead counts and identify dominant domains.
* **Smart Classification**: Automatically labels lists as "Academic" (e.g., `mseuf.edu.ph`) or "General Market" based on frequency analysis.

### Libraries Used
* `re`: Regular Expression matching for data scraping.
* `itertools`: Combinatorial mathematics for lead generation.
* `threading`: Asynchronous background processing.
* `collections.Counter`: Frequency analysis for domain classification.

---

## 🚀 Installation & Usage
1. **Requirements**: Ensure Python 3.x is installed. 
2. **Run Library System**: Execute the script to manage books via the "Add New Record" card and the interactive table.
3. **Run Data Analyzer**: Enter names into the generator fields, click **"Generate & Randomize Leads"**, and use **"Run RegEx Analysis"** to view statistical reports.

---

## 👤 Author
* **Allen Jerrome M. Tolete**
* **Course**: CP102-M001
# AI Job Displacement Analytics System

A comprehensive Python-based desktop application and data analysis suite developed for the CP102 Database Exam at Manuel S. Enverga University Foundation (MSEUF). This project focuses on managing and visualizing the "AI Job Replacement 2020-2026" dataset to understand the impact of automation on the global workforce.

## Overview

The system consists of two primary components designed to handle a dataset of 15,000 records:
1.  **CSV Record Management System**: A GUI-based application for CRUD operations (Create, Read, Update, Delete) and real-time analytics.
2.  **Data Analysis Suite**: A deep-dive exploration using Pandas and Matplotlib to answer key industry questions regarding AI adoption and salary volatility.

## Features

### 1. Record Management (CRUD)
* **Custom Records**: Add, delete, and search for specific job records in a local `custom_records.csv` file.
* **Data Integrity**: Built-in ID validation to prevent duplicate entries.
* **Search Engine**: Filter records by Unique ID or Job Role/Country names.

### 2. Dataset Exploration & Filtering
* **Live Viewer**: Browse the master dataset with over 15,000 entries.
* **Dynamic Filters**: Filter the entire dataset by Industry or Year to narrow down specific trends.

### 3. Data Analytics Dashboard
Automated analysis of five core questions:
* Average automation risk per industry.
* Top countries by AI replacement scores.
* Impact of automation risk on salary changes.
* Annual trends in AI adoption vs. reskilling urgency.
* Top 10 highest-paying roles before AI intervention.

### 4. Interactive Visualizations
Integrated Matplotlib charts including:
* **Risk Distribution**: Pie charts for automation risk categories.
* **Industry Comparison**: Horizontal bar charts for AI scores.
* **Temporal Trends**: Line graphs showing the rise of AI adoption.
* **Correlation Analysis**: Scatter plots for risk vs. salary change.

## Tech Stack

* **Language**: Python 3
* **GUI Framework**: Tkinter (Themed with MSEUF Maroon, Yellow, and White)
* **Data Handling**: Pandas, CSV module
* **Visualization**: Matplotlib (TkAgg backend)
* **Architecture**: Object-Oriented Programming (OOP) with Repository Pattern

## Project Structure

* `main.py`: The primary GUI application.
* `ai_job_replacement_2020_2026_v2.csv`: The master dataset.
* `custom_records.csv`: Local storage for user-generated records.
* `analysis_notebook.ipynb`: Jupyter Notebook for extended data exploration.

## Installation & Usage

1.  **Clone the repository**:
    ```bash
    git clone [https://github.com/yourusername/ai-job-displacement.git](https://github.com/yourusername/ai-job-displacement.git)
    ```
2.  **Install dependencies**:
    ```bash
    pip install pandas matplotlib
    ```
3.  **Run the application**:
    ```bash
    python main.py
    ```

## Academic Context
* **Institution**: Manuel S. Enverga University Foundation (MSEUF)
* **Course**: BS Computer Science
* **Subject**: CP102 - Database Exam (Midterms)
* **Developer**: Allen Jerrome M. Tolete

---
*Developed for educational purposes to demonstrate the integration of GUI, OOP, and Data Analytics.*
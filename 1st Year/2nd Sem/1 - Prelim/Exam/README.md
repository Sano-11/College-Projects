# University Library Management System

## **Program Description**
This program is a professional **University Library Management System** designed for Enverga University to streamline the tracking of book inventories and records. The system features a modern, user-friendly graphical interface built with Python’s Tkinter library, allowing administrators to manage a collection of titles with specific attributes including Book Title, Author Name, and ISBN Code. The application implements a comprehensive **Object-Oriented Architecture** using composition, where a central `Library` class manages a collection of `Book` objects. Each `Book` object encapsulates its own data and availability status, while the `Library` class handles high-level operations such as adding new records and toggling the checkout status of items.



---

## **How it Works (Operational Logic)**
The program operates by separating data management from the visual interface, following a structure similar to the Model-View-Controller (MVC) pattern.

### **A. Data Modeling (The `Book` Class)**
The `Book` class serves as the blueprint for every book in the system, utilizing **Encapsulation** to protect data.
* **Attributes**: It stores `_title`, `_author`, and `_isbn` as protected attributes to prevent unauthorized direct access.
* **Methods**: It uses getter methods like `get_title()` and `get_isbn()` to retrieve information and setter methods like `set_available()` to modify the book's state.

### **B. Logic Management (The `Library` Class)**
The `Library` class acts as the internal database and logic controller.
* **Composition**: It maintains a list called `_books` that stores instances of `Book` objects.
* **Operations**: It includes logic to `add_book()` to the collection and a `toggle_status()` function that searches for a book by its unique ISBN to update its availability.

### **C. User Interface (The `LibraryGUI` Class)**
The GUI layer handles user interaction and visualizes the library data using the Tkinter library.
* **Event Handling**: When a user clicks "ADD TO COLLECTION," the GUI triggers a method that pulls text from the input fields and sends it to the `Library` controller.
* **Dynamic View**: The `refresh_list()` function clears the current table and repopulates it with the latest data, applying color-coded tags for "Available" (green) or "Checked Out" (red) status.



---

## **Key Features**
* **Encapsulated Data**: All book attributes are protected, ensuring data integrity through controlled access methods.
* **Real-time Search**: A "Filter by ISBN" feature allows users to search through the database instantly as they type.
* **Interactive Table**: A styled `Treeview` provides alternating row colors and distinct status indicators for better scannability.
* **Scrollable Layout**: A canvas-based scrolling system ensures the interface remains usable even as the library collection grows.

---

## **Areas for Improvement**
While the current version of the University Library System is fully functional, there are several technical enhancements that could further professionalize the application:
* **Data Persistence**: Currently, any new books added are stored only in volatile memory and are lost once the program is closed. Integrating a local SQLite database would allow the system to save and reload the collection across different sessions.
* **Input Validation**: Enhancing the `add_book` method to ensure that ISBN codes follow a specific numerical format and to prevent duplicate entries from being added to the database.

---

## **Technical Reflection**
Developing this system provided a valuable opportunity to apply theoretical **Object-Oriented Programming (OOP)** concepts to a practical scenario. By structuring the program into distinct `Book`, `Library`, and `LibraryGUI` classes, the project demonstrates how **Composition** allows complex systems to be built from simpler, reusable components. Implementing **Encapsulation** was particularly insightful, as using protected attributes and getter/setter methods demonstrated how to protect internal data while still providing a controlled interface for the GUI. Overall, this project highlights the importance of a "Separation of Concerns" architecture.

---
**Author:** Sano
**Course:** CP102

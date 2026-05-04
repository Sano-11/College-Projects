-- 1. Database Initialization
CREATE DATABASE IF NOT EXISTS cafe_management;
USE cafe_management;

-- 2. Clean up to ensure a fresh start
DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS menu_items;
DROP TABLE IF EXISTS categories;

-- 3. Create Categories Table
CREATE TABLE categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(50) NOT NULL UNIQUE
);

-- 4. Create Menu Items Table
CREATE TABLE menu_items (
    item_id INT AUTO_INCREMENT PRIMARY KEY,
    item_name VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    stock_qty INT DEFAULT 0,
    category_id INT,
    CONSTRAINT fk_category FOREIGN KEY (category_id) 
    REFERENCES categories(category_id) ON DELETE CASCADE
);

-- 5. Create Transaction History Table
CREATE TABLE transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    item_name VARCHAR(255) NOT NULL,
    quantity INT NOT NULL,
    total_price DECIMAL(10, 2) NOT NULL,
    sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 6. Insert Categories
INSERT INTO categories (category_name) VALUES 
('Espresso Drinks'), 
('Non-Caffeine'), 
('Pastries'), 
('Signature Cold Brew'),
('Iced Refreshers');

-- 7. Insert Seed Data (20 Items)
INSERT INTO menu_items (item_name, price, stock_qty, category_id) VALUES 
-- Espresso Drinks (Category 1)
('Americano', 120.00, 100, 1),
('Vanilla Latte', 155.00, 45, 1),
('Caramel Macchiato', 165.00, 30, 1),
('White Chocolate Mocha', 175.00, 25, 1),
('Spanish Latte', 160.00, 40, 1),
('Hazelnut Latte', 155.00, 35, 1),
('Cortado', 140.00, 20, 1),

-- Non-Caffeine (Category 2)
('Matcha Latte', 170.00, 25, 2),
('Strawberry Milk', 150.00, 15, 2),
('Hojicha Latte', 170.00, 20, 2),
('Dark Chocolate Cocoa', 145.00, 30, 2),

-- Pastries (Category 3)
('Butter Croissant', 85.00, 20, 3),
('Pain au Chocolat', 95.00, 12, 3),
('Blueberry Cheesecake', 185.00, 10, 3),
('Ham & Cheese Croissant', 120.00, 15, 3),
('Glazed Donut', 65.00, 24, 3),
('Chocolate Chip Cookie', 55.00, 40, 3),

-- Signature Cold Brew (Category 4)
('Nitro Cold Brew', 180.00, 12, 4),

-- Iced Refreshers (Category 5)
('Passionfruit Tea', 130.00, 50, 5),
('Peach Iced Tea', 125.00, 45, 5);
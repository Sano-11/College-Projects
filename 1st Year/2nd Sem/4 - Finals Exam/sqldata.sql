-- 1. Database Creation
CREATE DATABASE IF NOT EXISTS cafe_management;
USE cafe_management;

-- 2. Clear existing tables to ensure a fresh start
DROP TABLE IF EXISTS menu_items;
DROP TABLE IF EXISTS categories;

-- 3. Create Tables with Relationships
CREATE TABLE categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE menu_items (
    item_id INT AUTO_INCREMENT PRIMARY KEY,
    item_name VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    stock_qty INT DEFAULT 0,
    category_id INT,
    CONSTRAINT fk_category FOREIGN KEY (category_id) 
    REFERENCES categories(category_id) ON DELETE CASCADE
);

-- 4. Sample Dataset (READ)
INSERT INTO categories (category_name) VALUES 
('Espresso Drinks'), ('Non-Caffeine'), ('Pastries'), ('Signature Cold Brew');

INSERT INTO menu_items (item_name, price, stock_qty, category_id) VALUES 
('Caffe Americano', 120.00, 100, 1),
('Vanilla Latte', 155.00, 45, 1),
('Matcha Latte', 170.00, 25, 2),
('Butter Croissant', 85.00, 20, 3),
('Nitro Cold Brew', 180.00, 12, 4);
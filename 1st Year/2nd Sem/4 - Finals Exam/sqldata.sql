-- ============================================================
-- Bean & Brew Cafe — Final Fixed Database Schema
-- ============================================================

CREATE DATABASE IF NOT EXISTS cafe_management;
USE cafe_management;

-- Clean slate to prevent name conflicts
DROP TABLE IF EXISTS sales;
DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS categories;

-- 1. Categories
CREATE TABLE categories (
    category_id   INT          AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(50)  NOT NULL UNIQUE
);

-- 2. Products (Renamed from menu_items to match your Python code)
CREATE TABLE products (
    id          INT            AUTO_INCREMENT PRIMARY KEY,
    name        VARCHAR(255)   NOT NULL,
    price       DECIMAL(10,2)  NOT NULL,
    stock       INT            DEFAULT 0,
    category_id INT,
    CONSTRAINT fk_category FOREIGN KEY (category_id)
        REFERENCES categories(category_id) ON DELETE CASCADE
);

-- 3. Sales (Using the structure your Python checkout needs)
CREATE TABLE sales (
    id     INT AUTO_INCREMENT PRIMARY KEY,
    date   VARCHAR(255) NOT NULL,
    items  TEXT NOT NULL,
    total  DECIMAL(10, 2) NOT NULL
);

-- 4. Categories Seed
INSERT INTO categories (category_name) VALUES
    ('Espresso Drinks'),
    ('Non-Caffeine'),
    ('Pastries'),
    ('Signature Cold Brew'),
    ('Iced Refreshers');

-- 5. Products Seed (Mapping your 20 items to the new table name)
INSERT INTO products (name, price, stock, category_id) VALUES
    ('Americano', 120.00, 100, 1),
    ('Vanilla Latte', 155.00, 45, 1),
    ('Caramel Macchiato', 165.00, 30, 1),
    ('White Chocolate Mocha', 175.00, 25, 1),
    ('Spanish Latte', 160.00, 40, 1),
    ('Hazelnut Latte', 155.00, 35, 1),
    ('Cortado', 140.00, 20, 1),
    ('Matcha Latte', 170.00, 25, 2),
    ('Strawberry Milk', 150.00, 15, 2),
    ('Hojicha Latte', 170.00, 20, 2),
    ('Dark Chocolate Cocoa', 145.00, 30, 2),
    ('Butter Croissant', 85.00, 20, 3),
    ('Pain au Chocolat', 95.00, 12, 3),
    ('Blueberry Cheesecake', 185.00, 10, 3),
    ('Ham & Cheese Croissant', 120.00, 15, 3),
    ('Glazed Donut', 65.00, 24, 3),
    ('Chocolate Chip Cookie', 55.00, 40, 3),
    ('Nitro Cold Brew', 180.00, 12, 4),
    ('Passionfruit Tea', 130.00, 50, 5),
    ('Peach Iced Tea', 125.00, 45, 5);
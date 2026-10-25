-- SpendWise database schema (MySQL 8 / MariaDB 10.4+)
CREATE DATABASE IF NOT EXISTS spendwise CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE spendwise;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_deleted_at DATETIME DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS income (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    source VARCHAR(100) NOT NULL,
    amount DECIMAL(12,2) NOT NULL,
    category VARCHAR(50) NOT NULL,
    income_date DATE NOT NULL,
    account VARCHAR(50) DEFAULT 'Bank Account',
    recurring BOOLEAN DEFAULT FALSE,
    frequency VARCHAR(20) DEFAULT NULL,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS expenses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    description VARCHAR(150) NOT NULL,
    amount DECIMAL(12,2) NOT NULL,
    category VARCHAR(50) NOT NULL,
    expense_date DATE NOT NULL,
    payment_method VARCHAR(50) DEFAULT 'Other',
    recurring BOOLEAN DEFAULT FALSE,
    frequency VARCHAR(20) DEFAULT NULL,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS budgets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    category VARCHAR(50) NOT NULL,
    amount DECIMAL(12,2) NOT NULL,
    period ENUM('Monthly','Weekly','Yearly') NOT NULL DEFAULT 'Monthly',
    budget_month DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_budgets_user (user_id),
    INDEX idx_budgets_month (budget_month),
    INDEX idx_budgets_category (category)
);

CREATE TABLE IF NOT EXISTS goals (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    name VARCHAR(150) NOT NULL,
    target_amount DECIMAL(12,2) NOT NULL,
    saved_amount DECIMAL(12,2) NOT NULL DEFAULT 0.00,
    deadline DATE DEFAULT NULL,
    category VARCHAR(50) NOT NULL DEFAULT 'Savings',
    icon VARCHAR(20) DEFAULT '🎯',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_goals_user (user_id),
    INDEX idx_goals_deadline (deadline)
);

CREATE TABLE IF NOT EXISTS user_preferences (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL UNIQUE,
    currency VARCHAR(10) NOT NULL DEFAULT 'INR',
    date_format VARCHAR(20) NOT NULL DEFAULT 'DD/MM/YYYY',
    dark_mode BOOLEAN NOT NULL DEFAULT FALSE,
    compact_layout BOOLEAN NOT NULL DEFAULT FALSE,
    show_summary BOOLEAN NOT NULL DEFAULT TRUE,
    show_goals BOOLEAN NOT NULL DEFAULT TRUE,
    budget_alerts BOOLEAN NOT NULL DEFAULT TRUE,
    goal_reminders BOOLEAN NOT NULL DEFAULT TRUE,
    monthly_summary BOOLEAN NOT NULL DEFAULT TRUE,
    security_notifications BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS notifications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    type VARCHAR(40) NOT NULL,
    title VARCHAR(120) NOT NULL,
    message VARCHAR(500) NOT NULL,
    severity VARCHAR(10) NOT NULL DEFAULT 'info',
    reference_id INT NOT NULL DEFAULT 0,
    period VARCHAR(20) NOT NULL DEFAULT '',
    is_read TINYINT(1) NOT NULL DEFAULT 0,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uniq_notification (user_id, type, reference_id, period),
    INDEX idx_user_unread (user_id, is_read),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

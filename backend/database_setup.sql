-- Database setup script for Mini Games Casino
-- Run this script to create the database

CREATE DATABASE IF NOT EXISTS mini_games_db;

USE mini_games_db;

-- Tables will be automatically created by Flask-SQLAlchemy
-- when the application runs for the first time via db.create_all()

-- Optional: Create a user for the application
-- CREATE USER IF NOT EXISTS 'minigames'@'localhost' IDENTIFIED BY 'your_password_here';
-- GRANT ALL PRIVILEGES ON mini_games_db.* TO 'minigames'@'localhost';
-- FLUSH PRIVILEGES;

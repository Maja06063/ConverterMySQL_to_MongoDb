-- Tworzenie bazy danych
CREATE DATABASE IF NOT EXISTS moja_baza_danych;
USE moja_baza_danych;

-- Tworzenie tabeli użytkowników
CREATE TABLE IF NOT EXISTS Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE
);

-- Tworzenie tabeli postów
CREATE TABLE IF NOT EXISTS Posts (
    post_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    content TEXT NOT NULL,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

-- Tworzenie tabeli komentarzy
CREATE TABLE IF NOT EXISTS Comments (
    comment_id INT AUTO_INCREMENT PRIMARY KEY,
    content TEXT NOT NULL,
    post_id INT,
    user_id INT,
    FOREIGN KEY (post_id) REFERENCES Posts(post_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

-- Tworzenie tabeli tagów
CREATE TABLE IF NOT EXISTS Tags (
    tag_id INT AUTO_INCREMENT PRIMARY KEY,
    tag_name VARCHAR(50) NOT NULL UNIQUE
);

-- Tworzenie tabeli łączącej posty z tagami (wiele do wielu)
CREATE TABLE IF NOT EXISTS PostTags (
    post_id INT,
    tag_id INT,
--PRIMARY KEY (post_id, tag_id),
    FOREIGN KEY (post_id) REFERENCES Posts(post_id),
    FOREIGN KEY (tag_id) REFERENCES Tags(tag_id)
);

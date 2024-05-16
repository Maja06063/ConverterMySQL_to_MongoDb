-- Tworzenie bazy danych
CREATE DATABASE IF NOT EXISTS databaseConverter;
USE databaseConverter;

CREATE TABLE IF NOT EXISTS DaneSystemowe (
    loginn VARCHAR(16) NOT NULL PRIMARY KEY,
    haslo CHAR(32) NOT NULL,
    rodzaj_konta ENUM('rodzic', 'uczen', 'nauczyciel') NOT NULL,
    email VARCHAR(32)
);

CREATE TABLE IF NOT EXISTS DaneOsobowe (
    loginn VARCHAR(16) NOT NULL PRIMARY KEY,
    imie NVARCHAR(20) NOT NULL,
    nazwisko NVARCHAR(52) NOT NULL
);

CREATE TABLE IF NOT EXISTS Opiekunowie (
    ID INT(3) NOT NULL PRIMARY KEY AUTO_INCREMENT,
    rodzaj_opiekuna VARCHAR(60) NOT NULL
);

CREATE TABLE IF NOT EXISTS Miejscowosc (
    ID INT(3) NOT NULL PRIMARY KEY AUTO_INCREMENT,
    nazwa NVARCHAR(30) NOT NULL
);

CREATE TABLE IF NOT EXISTS Ulica (
    ID INT(3) NOT NULL PRIMARY KEY AUTO_INCREMENT,
    nazwa NVARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS CzasLekcji (
    ID INT(5) NOT NULL PRIMARY KEY AUTO_INCREMENT,
    data_lekcji DATE NOT NULL,
    godz_rozp TIME NOT NULL,
    godz_zak TIME NOT NULL
);

CREATE TABLE IF NOT EXISTS Przedmiot (
    ID INT(2) NOT NULL PRIMARY KEY AUTO_INCREMENT,
    nazwa NVARCHAR(32) NOT NULL
);

CREATE TABLE IF NOT EXISTS Nauczyciel (
    ID INT(2) NOT NULL PRIMARY KEY AUTO_INCREMENT,
    czy_wychowawca BOOLEAN NOT NULL,
    loginn VARCHAR(16) NOT NULL,
    FOREIGN KEY (loginn) REFERENCES DaneSystemowe (loginn)
);

CREATE TABLE IF NOT EXISTS Klasa (
    ID INT(2) NOT NULL PRIMARY KEY AUTO_INCREMENT,
    nazwa CHAR(2) NOT NULL,
    nauczyciel_id INT(2) NOT NULL,
    FOREIGN KEY (nauczyciel_id) REFERENCES Nauczyciel (ID)
);

CREATE TABLE IF NOT EXISTS NauczycielPrzedmiotu (
    ID INT(3) NOT NULL PRIMARY KEY AUTO_INCREMENT,
    nauczyciel_id INT(2) NOT NULL,
    przedmiot_id INT(2) NOT NULL,
    FOREIGN KEY (nauczyciel_id) REFERENCES Nauczyciel (ID),
    FOREIGN KEY (przedmiot_id) REFERENCES Przedmiot (ID)
);

CREATE TABLE IF NOT EXISTS UliceMiejscowosci (
    ID INT(6) NOT NULL PRIMARY KEY AUTO_INCREMENT,
    miejscowosc_id INT(3) NOT NULL,
    ulica_id INT(3) NOT NULL,
    FOREIGN KEY (miejscowosc_id) REFERENCES Miejscowosc (ID),
    FOREIGN KEY (ulica_id) REFERENCES Ulica (ID)
);

CREATE TABLE IF NOT EXISTS Adres (
    ID INT(3) NOT NULL PRIMARY KEY AUTO_INCREMENT,
    ulica_miejscowosci INT(6) NOT NULL,
    nr_domu VARCHAR(10) NOT NULL,
    nr_mieszkania VARCHAR(4),
    kod_pocztowy INT(5) NOT NULL,
    FOREIGN KEY (ulica_miejscowosci) REFERENCES UliceMiejscowosci (ID)
);

CREATE TABLE IF NOT EXISTS Rodzic (
    ID INT(3) NOT NULL PRIMARY KEY AUTO_INCREMENT,
    nr_telefonu VARCHAR(12) NOT NULL,
    loginn VARCHAR(16) NOT NULL,
    opiekunowie_id INT(3) NOT NULL,
    rola ENUM('rodzic', 'opiekun_prawny') NOT NULL,
    adres_id INT(3) NOT NULL,
    FOREIGN KEY (loginn) REFERENCES DaneOsobowe (loginn),
    FOREIGN KEY (adres_id) REFERENCES Adres (ID)
);

CREATE TABLE IF NOT EXISTS Uczen (
    ID INT(3) NOT NULL PRIMARY KEY AUTO_INCREMENT,
    pesel CHAR(11) NOT NULL,
    drugie_imie NVARCHAR(20) NOT NULL,
    wiek INT(3) NOT NULL,
    plec ENUM('mezczyzna', 'kobieta') NOT NULL,
    adres_id INT(3) NOT NULL,
    klasa_id INT(2) NOT NULL,
    opiekun_id INT(3) NOT NULL,
    loginn VARCHAR(16) NOT NULL,
    FOREIGN KEY (adres_id) REFERENCES Adres (ID),
    FOREIGN KEY (klasa_id) REFERENCES Klasa (ID),
    FOREIGN KEY (opiekun_id) REFERENCES Opiekunowie (ID),
    FOREIGN KEY (loginn) REFERENCES DaneOsobowe (loginn)
);

CREATE TABLE IF NOT EXISTS Ocena (
    ID INT(6) NOT NULL PRIMARY KEY AUTO_INCREMENT,
    stopien ENUM('1', '2', '3', '4', '5', '6') NOT NULL,
    waga INT(1) NOT NULL,
    poprawiona_ocena INT(1) NOT NULL,
    waga_poprawionej INT(1) NOT NULL,
    opis NVARCHAR(100),
    data_oceny DATE NOT NULL,
    uczen_id INT(3) NOT NULL,
    nauczyciel_przedmiotu_id INT(3) NOT NULL,
    FOREIGN KEY (uczen_id) REFERENCES Uczen (ID),
    FOREIGN KEY (nauczyciel_przedmiotu_id) REFERENCES NauczycielPrzedmiotu (ID)
);

CREATE TABLE IF NOT EXISTS GrupaLekcji (
    ID INT(3) NOT NULL PRIMARY KEY AUTO_INCREMENT,
    nauczyciel_przedmiotu_id INT(3) NOT NULL,
    klasa_id INT(2) NOT NULL,
    FOREIGN KEY (nauczyciel_przedmiotu_id) REFERENCES NauczycielPrzedmiotu (ID),
    FOREIGN KEY (klasa_id) REFERENCES Klasa (ID)
);

CREATE TABLE IF NOT EXISTS Lekcja (
    ID INT(5) NOT NULL PRIMARY KEY AUTO_INCREMENT,
    grupa_lekcji_id INT(3) NOT NULL,
    temat NVARCHAR(250) NOT NULL,
    czas_lekcji_id INT(5) NOT NULL,
    sala INT(2) NOT NULL,
    FOREIGN KEY (grupa_lekcji_id) REFERENCES GrupaLekcji (ID),
    FOREIGN KEY (czas_lekcji_id) REFERENCES CzasLekcji (ID)
);

CREATE TABLE IF NOT EXISTS Obecnosc (
    ID INT(7) NOT NULL PRIMARY KEY AUTO_INCREMENT,
    status_ob ENUM('obecny', 'nieobecny') NOT NULL,
    uczen_id INT(3) NOT NULL,
    lekcja_id INT(5) NOT NULL,
    FOREIGN KEY (uczen_id) REFERENCES Uczen (ID),
    FOREIGN KEY (lekcja_id) REFERENCES Lekcja (ID)
);

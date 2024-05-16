-- DaneSystemowe
INSERT INTO DaneSystemowe (loginn, haslo, rodzaj_konta, email) VALUES
('jan.kowalski', 'haslo123', 'uczen', 'jan.kowalski@example.com'),
('anna.nowak', 'qwerty', 'nauczyciel', 'anna.nowak@example.com'),
('marek.kowalczyk', 'abc123', 'rodzic', 'marek.kowalczyk@example.com');

-- DaneOsobowe
INSERT INTO DaneOsobowe (loginn, imie, nazwisko) VALUES
('jan.kowalski', 'Jan', 'Kowalski'),
('anna.nowak', 'Anna', 'Nowak'),
('marek.kowalczyk', 'Marek', 'Kowalczyk');

-- Opiekunowie
INSERT INTO Opiekunowie (rodzaj_opiekuna) VALUES
('Tata'),
('Mama'),
('Dziadek');

-- Miejscowosc
INSERT INTO Miejscowosc (nazwa) VALUES
('Warszawa'),
('Kraków'),
('Poznań');

-- Ulica
INSERT INTO Ulica (nazwa) VALUES
('Krakowska'),
('Warszawska'),
('Poznańska');

-- CzasLekcji
INSERT INTO CzasLekcji (data_lekcji, godz_rozp, godz_zak) VALUES
('2024-05-16', '08:00:00', '09:30:00'),
('2024-05-16', '09:45:00', '11:15:00'),
('2024-05-16', '11:30:00', '13:00:00');

-- Przedmiot
INSERT INTO Przedmiot (nazwa) VALUES
('Matematyka'),
('Fizyka'),
('Chemia');

-- Nauczyciel
INSERT INTO Nauczyciel (czy_wychowawca, loginn) VALUES
(1, 'anna.nowak');

-- Klasa
INSERT INTO Klasa (nazwa, nauczyciel_id) VALUES
('1A', 1),
('1B', 1),
('1C', 1);

-- NauczycielPrzedmiotu
INSERT INTO NauczycielPrzedmiotu (nauczyciel_id, przedmiot_id) VALUES
(1, 1),
(1, 2),
(1, 3);

-- UliceMiejscowosci
INSERT INTO UliceMiejscowosci (miejscowosc_id, ulica_id) VALUES
(1, 1),
(2, 2),
(3, 3);

-- Adres
INSERT INTO Adres (ulica_miejscowosci, nr_domu, kod_pocztowy) VALUES
(1, '10', '00-001'),
(2, '20', '30-002'),
(3, '30', '60-003');

-- Rodzic
INSERT INTO Rodzic (nr_telefonu, loginn, opiekunowie_id, rola, adres_id) VALUES
('123456789', 'marek.kowalczyk', 1, 'rodzic', 1),
('987654321', 'anna.nowak', 2, 'opiekun_prawny', 2),
('111222333', 'jan.kowalski', 3, 'opiekun_prawny', 3);

-- Uczen
INSERT INTO Uczen (pesel, drugie_imie, wiek, plec, adres_id, klasa_id, opiekun_id, loginn) VALUES
('12345678901', 'Adam', 13, 'mezczyzna', 1, 1, 1, 'jan.kowalski'),
('98765432109', 'Ewa', 14, 'kobieta', 2, 2, 2, 'anna.nowak'),
('11122233309', 'Piotr', 13, 'mezczyzna', 3, 3, 3, 'marek.kowalczyk');

-- Ocena
INSERT INTO Ocena (stopien, waga, poprawiona_ocena, waga_poprawionej, opis, data_oceny, uczen_id, nauczyciel_przedmiotu_id) VALUES
('5', 2, 0, 0, 'Bardzo dobry', '2024-05-16', 1, 1),
('4', 1, 0, 0, 'Dobry', '2024-05-16', 2, 2),
('3', 1, 0, 0, 'Dostateczny', '2024-05-16', 3, 3);

-- GrupaLekcji
INSERT INTO GrupaLekcji (nauczyciel_przedmiotu_id, klasa_id) VALUES
(1, 1),
(2, 2),
(3, 3);

-- Lekcja
INSERT INTO Lekcja (grupa_lekcji_id, temat, czas_lekcji_id, sala) VALUES
(1, 'Równania kwadratowe', 1, 101),
(2, 'Siły w przyrodzie', 2, 202),
(3, 'Reakcje chemiczne', 3, 303);

-- Obecnosc
INSERT INTO Obecnosc (status_ob, uczen_id, lekcja_id) VALUES
('obecny', 1, 1),
('obecny', 2, 2),
('nieobecny', 3, 3);

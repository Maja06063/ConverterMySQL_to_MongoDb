-- Wstawianie danych do tabeli Users
INSERT INTO Users (username, email) VALUES
('jan_kowalski', 'jan.kowalski@example.com'),
('anna_nowak', 'anna.nowak@example.com'),
('adam_michalski', 'adam.michalski@example.com');

-- Wstawianie danych do tabeli Posts
INSERT INTO Posts (title, content, user_id) VALUES
('Pierwszy post', 'Treść pierwszego posta...', 1),
('Drugi post', 'Treść drugiego posta...', 2),
('Trzeci post', 'Treść trzeciego posta...', 3);

-- Wstawianie danych do tabeli Comments
INSERT INTO Comments (content, post_id, user_id) VALUES
('To jest komentarz do pierwszego posta.', 1, 2),
('To jest komentarz do drugiego posta.', 2, 3),
('To jest komentarz do trzeciego posta.', 3, 1);

-- Wstawianie danych do tabeli Tags
INSERT INTO Tags (tag_name) VALUES
('SQL'),
('Bazy danych'),
('Programowanie');

-- Wstawianie danych do tabeli PostTags
INSERT INTO PostTags (post_id, tag_id) VALUES
(1, 1),
(1, 2),
(2, 2),
(3, 3),
(3, 1);

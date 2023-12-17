-- Запрос на полную выборку данных
SELECT * FROM provider;

-- Запрос на выборку данных без повторений
SELECT DISTINCT inn, name, address
FROM provider;

-- Запрос на выборку первых 10 записей
SELECT inn, name, address
FROM provider
LIMIT 10;

-- Запрос на выборку последних 15 записей
SELECT *
FROM provider
ORDER BY id DESC
LIMIT 15;

-- Запросы на выполнение функций Average, Max, Min
SELECT AVG(price) AS average_price
FROM product;

SELECT MAX(quantity) AS max_quantity
FROM product;

SELECT MIN(weight) AS min_weight
FROM product;

-- запрос на возвращение определенного кортежа по первичному ключу
SELECT *
FROM natural_person
WHERE natural_person_id = 1;

-- запросы на возвращение значения по условиям больше, меньше и между
SELECT *
FROM product
WHERE quantity > 100;

SELECT *
FROM product
WHERE price < 50;

SELECT *
FROM product
WHERE weight BETWEEN 5 AND 10;

-- запросы на возвращении всех кортежей по условию с использованием оператора LIKE и ESCAPE
SELECT *
FROM natural_person
WHERE forename LIKE '%a%';

SELECT *
FROM natural_person
WHERE forename LIKE '%^_%' ESCAPE '^';

-- запрос на возвращение кортежей со сложным условием на основе логических операторов И, ИЛИ, НЕ
SELECT *
FROM product
WHERE (weight > 1.70 OR receipt_date > '2023-09-01') AND quantity > 15;

SELECT *
FROM waybill
WHERE NOT product_quantity = 0;


-- запрос с использованием оператора NOT NULL в условии отбора
SELECT *
FROM natural_person
WHERE phone_number IS NOT NULL;

-- Запрос с простыми условиями, условиями, содержащими IN или BETWEEN
SELECT *
FROM product
WHERE price IN (189.00, 493.50, 997.50);

SELECT *
FROM product
WHERE price BETWEEN (189.00, 493.50, 997.50);


-- Запросы с сортировкой по нескольким полям, направлениям
SELECT *
FROM product
ORDER BY product_name ASC, price DESC;

-- Запросы с использованием групповых операций (группировка статистические функции, отбор по групповым функциям)
SELECT place, SUM(price) AS total_price
FROM product
GROUP BY place;

SELECT place, SUM(price) AS total_cost
FROM product
GROUP BY place
HAVING SUM (price) > 6000;

-- Запросы с операцией над множествами (обязательно используя сортировку)
SELECT email
FROM natural_person
UNION
SELECT email
FROM legal_person
ORDER BY email ASC;

SELECT email
FROM natural_person
UNION ALL
SELECT email
FROM legal_person
ORDER BY email ASC;

-- Запросы на обновление
UPDATE natural_person
SET email = 'new_email@example.com'
WHERE natural_person_id = 1;

UPDATE provider
SET address = 'New Address'
WHERE provider_id = 1;

-- Запросы на удаление
DELETE FROM natural_person
WHERE natural_person_id = 1;

DELETE FROM provider
WHERE id IN (
    SELECT provider_id
    FROM product
    WHERE price < 50
);

-- Запросы на вставку
INSERT INTO legal_person (inn, name, phone, email, delivery_address, representative_forename) 
VALUES ('789456123', 'OOO SNG', '79095273752', 'email@email.com', 'surgut', 'Ivanov');

INSERT INTO natural_person (passport, forename, phone, email, delivery_address) 
VALUES ('4894165', 'Komarov', '79084893526', 'email@email.com', 'minsk');


-- Создание таблицы
CREATE TABLE Client (
    client_id SERIAL PRIMARY KEY,
    second_name VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    date_of_birth DATE NOT NULL
);

-- Заполнение данными
INSERT INTO Client (second_Name, name, date_of_birth) VALUES
    ('Иванов', 'Иван', '1955-12-19'),
    ('Петров', 'Петр', '1956-12-23'),
    ('Сидоров', 'Николай', '1957-12-09'),
    ('Кузнецов', 'Сергей', '1958-12-02'),
    ('Смирнов', 'Алексей', '1962-12-02'),
    ('Васильев', 'Василий', '1964-12-28'),
    ('Павлов', 'Павел', '1965-12-17'),
    ('Семенов', 'Семен', '1966-12-14'),
    ('Голубев', 'Глеб', '1967-12-11'),
    ('Виноградов', 'Виктор', '1968-12-24'),
    ('Богданов', 'Борис', '1970-12-05'),
    ('Воробьев', 'Валерий', '1971-12-21'),
    ('Федоров', 'Федор', '1972-12-18'),
    ('Михайлов', 'Михаил', '1973-12-07'),
    ('Беляев', 'Белла', '1974-12-20'),
    ('Тарасов', 'Тарас', '1976-12-13'),
    ('Белов', 'Борислав', '1977-12-03'),
    ('Комаров', 'Константин', '1978-12-22'),
    ('Орлов', 'Орест', '1980-12-01'),
    ('Киселев', 'Кирилл', '1981-12-26'),
    ('Макаров', 'Макар', '1982-12-15'),
    ('Андреев', 'Андрей', '1984-12-09'),
    ('Ковалев', 'Константин', '1985-12-02'),
    ('Ильин', 'Илья', '1986-12-25'),
    ('Гусев', 'Геннадий', '1988-12-19'),
    ('Титов', 'Тимофей', '1989-12-12'),
    ('Кузьмин', 'Кузьма', '1990-12-06'),
    ('Кудрявцев', 'Кузьма', '1993-12-18'),
    ('Баранов', 'Борис', '1995-12-21'),
    ('Куликов', 'Кирилл', '1998-12-24');

SELECT
    CONCAT("second_name", ' ', LEFT("name", 1), '.') AS "ФИО",
    DATE_PART('year', AGE(NOW(), "date_of_birth")) AS "Возраст",
    "date_of_birth" AS "Дата рождения",
    "date_of_birth" + INTERVAL '1 year' * DATE_PART('year', AGE(NOW(), "date_of_birth")) AS "Дата юбилея"
FROM Client
WHERE
  DATE_PART('month', "date_of_birth") = DATE_PART('month', NOW() + INTERVAL '1 MONTH')
  AND DATE_PART('year', AGE(NOW(), "date_of_birth"))::integer % 5 = 4;
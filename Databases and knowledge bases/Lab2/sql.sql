SELECT * FROM provider;

SELECT DISTINCT inn, provider_name, address
FROM provider;


SELECT inn, provider_name, address
FROM provider
LIMIT 10;



-- Пример для столбца price в таблице product
SELECT AVG(price) AS average_price
FROM product;

-- Пример для столбца quantity в таблице product
SELECT MAX(quantity) AS max_quantity
FROM product;

-- Пример для столбца weight в таблице product
SELECT MIN(weight) AS min_weight
FROM product;

-- Пример для таблицы natural_person
SELECT *
FROM natural_person
WHERE natural_person_id = 1;

-- Пример для таблицы product, выбор продуктов с количеством больше 100
SELECT *
FROM product
WHERE quantity > 100;

-- Пример для таблицы product, выбор продуктов с ценой меньше 50
SELECT *
FROM product
WHERE price < 50;

-- Пример для таблицы product, выбор продуктов с весом между 5 и 10
SELECT *
FROM product
WHERE weight BETWEEN 5 AND 10;

-- Пример для таблицы natural_person, выбор физических лиц с именем, начинающимся на "Иван"
SELECT *
FROM natural_person
WHERE natural_customer_name LIKE 'Иван%';

-- Пример с использованием ESCAPE для поиска значений, содержащих символ "%"
SELECT *
FROM table_name
WHERE column_name LIKE '%\%%' ESCAPE '\';

-- Пример для таблицы natural_person, выбор физических лиц с указанным номером телефона
SELECT *
FROM natural_person
WHERE phone_number IS NOT NULL;

SELECT *
FROM product
WHERE price IN (50, 75, 100);

SELECT *
FROM product
WHERE price IN (50, 75, 100);

-- Сортировка по нескольким полям (product_name в алфовитном порядке, price по убыванию)
SELECT *
FROM product
ORDER BY product_name ASC, price DESC;

-- С использованием статических функций
SELECT customer_id, AVG(total_cost) AS avg_cost, SUM(total_cost) AS total_cost
FROM orders
GROUP BY customer_id;

-- С использованием груповых функций
SELECT customer_id, SUM(total_cost) AS total_cost
FROM orders
GROUP BY customer_id
HAVING SUM(total_cost) > 1000;

-- Использование UNION (объединение множеств)
SELECT email
FROM natural_person
UNION
SELECT email
FROM legal_person
ORDER BY email ASC;

-- Использование UNION ALL (объединение множеств с дубликатами)
SELECT email
FROM natural_person
UNION ALL
SELECT email
FROM legal_person
ORDER BY email ASC;

-- Пример обновления email для конкретного natural_person_id
UPDATE natural_person
SET email = 'new_email@example.com'
WHERE natural_person_id = 1;

-- Пример обновления phone_number для конкретного legal_person_id
UPDATE legal_person
SET phone_number = 1234567890
WHERE legal_person_id = 1;

-- Пример обновления address для конкретного provider_id
UPDATE provider
SET address = 'New Address'
WHERE provider_id = 1;

-- Пример обновления цены и количества для конкретного product_id
UPDATE product
SET price = 99.99, quantity = 50
WHERE product_id = 1;

-- Пример обновления общей стоимости и количества товара для конкретного orders_id
UPDATE orders
SET total_cost = 500.00, product_quantity = 10
WHERE orders_id = 1;

-- Пример удаления конкретного natural_person_id
DELETE FROM natural_person
WHERE natural_person_id = 1;

-- Пример удаления конкретного legal_person_id
DELETE FROM legal_person
WHERE legal_person_id = 1;

-- Пример удаления provider по условию из подзапроса
DELETE FROM provider
WHERE provider_id IN (
    SELECT provider_id
    FROM product
    WHERE price < 50
);

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
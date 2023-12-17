-- Создание или замена функции fill_data
CREATE OR REPLACE FUNCTION fill_data() RETURNS void AS $$
DECLARE
    i INTEGER := 0;
BEGIN
    WHILE i < 1000 LOOP
        -- Исправленные операторы INSERT для таблицы legal_person
        INSERT INTO legal_person (inn, name, phone, email, delivery_address, representative_forename) 
        VALUES ('inn' || i, 'legal_customer_name' || i, 'phone_number' || i, 'email' || i, 'delivery_address' || i, 'representative_name' || i);

        -- Исправленные операторы INSERT для таблицы natural_person
        INSERT INTO natural_person (passport, forename, phone, email, delivery_address) 
        VALUES ('passport_details' || i, 'natural_customer_name' || i, 'phone_number' || i, 'email' || i, 'delivery_address' || i);

        -- Исправленные операторы INSERT для таблицы provider
        INSERT INTO provider (inn, name, address) 
        VALUES ('provider_inn' || i, 'provider_name' || i, 'provider_address' || i);

        -- Исправленные операторы INSERT для таблицы product
        INSERT INTO product (place, name, receipt_date, article, quantity, price, weight) 
        VALUES (i, 'product_name' || i, CURRENT_DATE, 'article' || i, i, i * 10.5, i * 0.1);

        -- Исправленные операторы INSERT для таблицы waybill
        INSERT INTO waybill (article_product, product_quantity) 
        VALUES ('article' || i, i);

        i := i + 1;
    END LOOP;
END;
$$ LANGUAGE plpgsql;

-- Вызов функции fill_data
SELECT fill_data();

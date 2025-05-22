-- Создание таблицы natural_person
CREATE TABLE natural_person (
    id SERIAL PRIMARY KEY,
    passport VARCHAR(255) UNIQUE,
    forename VARCHAR(255),
    phone VARCHAR(255),
    email VARCHAR(255),
    delivery_address VARCHAR(255)
);

-- Создание таблицы legal_person
CREATE TABLE legal_person (
    id SERIAL PRIMARY KEY,
    inn VARCHAR(255) UNIQUE,
    name VARCHAR(255),
    phone VARCHAR(255),
    email VARCHAR(255),
    delivery_address VARCHAR(255),
	representative_forename VARCHAR(255)
);

-- Создание таблицы provider
CREATE TABLE provider (
    id SERIAL PRIMARY KEY,
    inn VARCHAR(255) UNIQUE,
    name VARCHAR(255),
    address VARCHAR(255)
);

-- Создание таблицы product
CREATE TABLE product (
    id SERIAL PRIMARY KEY,
    place INTEGER UNIQUE,
    provider_id INTEGER REFERENCES provider(id),
    provider_name VARCHAR(255),
    name VARCHAR(255),
    receipt_date DATE,
    article VARCHAR(255) UNIQUE,
    quantity INT,
    price DECIMAL(10, 2),
    weight DECIMAL(5, 2)
);

-- Создание таблицы orders
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    order_number INTEGER UNIQUE,
    weight DECIMAL(5, 2),
    registration_date DATE,
    cost DECIMAL(10, 2),
    customer_id INTEGER,
    customer_category VARCHAR(50) CHECK (customer_category IN ('Юр. лицо', 'Физ. лицо')),
    CONSTRAINT fk_legal_person FOREIGN KEY (customer_id) REFERENCES legal_person(id) DEFERRABLE INITIALLY DEFERRED,
    CONSTRAINT fk_natural_person FOREIGN KEY (customer_id) REFERENCES natural_person(id) DEFERRABLE INITIALLY DEFERRED,
    CONSTRAINT check_customer_id CHECK (
        (customer_category = 'Юр. лицо' AND customer_id IS NOT NULL) OR
        (customer_category = 'Физ. лицо' AND customer_id IS NOT NULL)
    )
);

-- Создание таблицы waybill
CREATE TABLE waybill (
    id SERIAL PRIMARY KEY,
    article_product VARCHAR(255) REFERENCES product(article),
    product_quantity INTEGER,
	orders_number INTEGER REFERENCES orders(order_number),
	doc_number INTEGER
);
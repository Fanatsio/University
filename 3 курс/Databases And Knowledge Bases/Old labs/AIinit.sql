-- Таблица "Физ. лицо"
CREATE TABLE fiz_lico (
    id SERIAL PRIMARY KEY,
    passport_number VARCHAR(20) UNIQUE NOT NULL,
    phone_number VARCHAR(20),
    delivery_address TEXT,
    email VARCHAR(255) UNIQUE
);

-- Таблица "Юр. лицо"
CREATE TABLE yur_lico (
    id SERIAL PRIMARY KEY,
    inn VARCHAR(12) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    delivery_address TEXT,
    phone_number VARCHAR(20),
    email VARCHAR(255) UNIQUE,
    representative_name VARCHAR(255)
);

-- Таблица "Заказ"
CREATE TABLE zakaz (
    id SERIAL PRIMARY KEY,
    order_number VARCHAR(20) UNIQUE NOT NULL,
    fiz_lico_id INTEGER,
    yur_lico_id INTEGER,
    total_cost DECIMAL(10,2) NOT NULL,
    order_date DATE NOT NULL,
    CONSTRAINT fk_fiz FOREIGN KEY (fiz_lico_id) REFERENCES fiz_lico(id) ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT fk_yur FOREIGN KEY (yur_lico_id) REFERENCES yur_lico(id) ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT chk_customer CHECK (
        (fiz_lico_id IS NOT NULL AND yur_lico_id IS NULL) OR
        (fiz_lico_id IS NULL AND yur_lico_id IS NOT NULL)
    )
);

-- Таблица "Поставщик"
CREATE TABLE postavshik (
    id SERIAL PRIMARY KEY,
    inn VARCHAR(12) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    address TEXT
);

-- Таблица "Товар"
CREATE TABLE tovar (
    id SERIAL PRIMARY KEY,
    product_code VARCHAR(20) UNIQUE NOT NULL,
    storage_location VARCHAR(255) NOT NULL,
    arrival_date DATE NOT NULL,
    name VARCHAR(255) NOT NULL,
    unit_weight DECIMAL(10,2) NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    stock_quantity INTEGER NOT NULL,
    supplier_inn VARCHAR(12) NOT NULL,
    CONSTRAINT fk_supplier FOREIGN KEY (supplier_inn) REFERENCES postavshik(inn) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Таблица "Накладная"
CREATE TABLE nakladnaya (
    id SERIAL PRIMARY KEY,
    product_code VARCHAR(20) NOT NULL,
    order_number VARCHAR(20) NOT NULL,
    document_number VARCHAR(20) UNIQUE NOT NULL,
    product_quantity INTEGER NOT NULL,
    creation_date DATE NOT NULL,
    product_weight DECIMAL(10,2) NOT NULL,
    CONSTRAINT fk_product FOREIGN KEY (product_code) REFERENCES tovar(product_code) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_order FOREIGN KEY (order_number) REFERENCES zakaz(order_number) ON DELETE CASCADE ON UPDATE CASCADE
);
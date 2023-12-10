CREATE TABLE natural_person (
    natural_person_id SERIAL PRIMARY KEY,
    passport_details INTEGER UNIQUE NOT NULL,
    phone_number INTEGER NOT NULL,
    natural_customer_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    delivery_address VARCHAR(255) NOT NULL
);

CREATE TABLE legal_person (
    legal_person_id SERIAL PRIMARY KEY,
    inn INTEGER UNIQUE NOT NULL,
    legal_customer_name VARCHAR(255) NOT NULL,
    phone_number INTEGER NOT NULL,
    email VARCHAR(255) NOT NULL,
    delivery_address VARCHAR(255) NOT NULL
);

CREATE TABLE provider (
    provider_id SERIAL PRIMARY KEY,
    inn INTEGER UNIQUE NOT NULL,
    provider_name VARCHAR(255) NOT NULL,
    address VARCHAR(255) NOT NULL
);

CREATE TABLE product (
    product_id SERIAL PRIMARY KEY,
    place INTEGER UNIQUE NOT NULL,
    provider_name VARCHAR(255) REFERENCES provider(provider_name),
    product_name VARCHAR(255) NOT NULL,
    receipt_date DATE,
    quantity INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    weight DECIMAL(5, 2) NOT NULL
);

CREATE TABLE orders (
    orders_id SERIAL PRIMARY KEY,
    order_number INTEGER UNIQUE NOT NULL,
    category_customer VARCHAR(50) NOT NULL CHECK (category_customer IN ('Юр. лицо', 'Физ. лицо')),
    name_customer VARCHAR(255),
    CONSTRAINT fk_legal_person FOREIGN KEY (name_customer) REFERENCES legal_person(legal_customer_name) DEFERRABLE INITIALLY DEFERRED,
    CONSTRAINT fk_natural_person FOREIGN KEY (name_customer) REFERENCES natural_person(natural_customer_name) DEFERRABLE INITIALLY DEFERRED,
    CONSTRAINT check_name_customer CHECK (
        (category_customer = 'Юр. лицо' AND name_customer IS NOT NULL) OR
        (category_customer = 'Физ. лицо' AND name_customer IS NOT NULL)
    )
);
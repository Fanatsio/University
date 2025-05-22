CREATE TABLE natural_person (
    natural_person_id SERIAL PRIMARY KEY,
    natural_person_passport INTEGER UNIQUE,
    natural_person_name VARCHAR(255),
    natural_person_phone VARCHAR(255) UNIQUE,
    natural_person_email VARCHAR(255) UNIQUE,
    natural_person_address VARCHAR(255)
);

CREATE TABLE legal_person (
    legal_person_id SERIAL PRIMARY KEY,
    legal_person_inn VARCHAR(255) UNIQUE,
    legal_person_name VARCHAR(255),
    legal_person_phone VARCHAR(255) UNIQUE,
    legal_person_email VARCHAR(255) UNIQUE,
    legal_person_address VARCHAR(255)
);

CREATE TABLE provider (
    provider_id SERIAL PRIMARY KEY,
    provider_inn VARCHAR(255) UNIQUE,
    provider_name VARCHAR(255),
    provider_address VARCHAR(255)
);

CREATE TABLE material (
    material_id SERIAL PRIMARY KEY,
    material_colour VARCHAR(255),
    material_name VARCHAR(255),
    material_type VARCHAR(255),
    material_quantity INTEGER,
    provider_inn VARCHAR(255) REFERENCES provider(provider_inn),
    material_cost DECIMAL(10, 2)
);

CREATE TABLE accessories (
    accessories_id SERIAL PRIMARY KEY,
    accessories_name VARCHAR(255),
    accessories_colour VARCHAR(255),
    accessories_type VARCHAR(255),
    accessories_quantity INTEGER,
    provider_inn VARCHAR(255) REFERENCES provider(provider_inn),
    accessories_cost DECIMAL(10, 2)
);

CREATE TABLE furniture (
    furniture_id SERIAL PRIMARY KEY,
    furniture_colour VARCHAR(255),
    furniture_article INTEGER UNIQUE,
    id_material INTEGER REFERENCES material(material_id),
    furniture_type VARCHAR(255),
    furniture_size DECIMAL(5, 2),
    furniture_name VARCHAR(255),
    id_accessories INTEGER REFERENCES accessories(accessories_id)
);

CREATE TABLE orders (
    orders_id SERIAL PRIMARY KEY,
    orders_registration_date DATE,
    orders_total_cost DECIMAL(10, 2),
	order_number INTEGER UNIQUE,
    category_customer VARCHAR(50) CHECK (category_customer IN ('Юр. лицо', 'Физ. лицо')),
    orders_status VARCHAR(255),
    customer_id INTEGER,
    CONSTRAINT fk_legal_person FOREIGN KEY (customer_id) REFERENCES legal_person(legal_person_id) DEFERRABLE INITIALLY DEFERRED,
    CONSTRAINT fk_natural_person FOREIGN KEY (customer_id) REFERENCES natural_person(natural_person_id) DEFERRABLE INITIALLY DEFERRED,
    CONSTRAINT check_customer_id CHECK (
        (category_customer = 'Юр. лицо' AND customer_id IS NOT NULL) OR
        (category_customer = 'Физ. лицо' AND customer_id IS NOT NULL)
    )
);

CREATE TABLE waybill (
    waybill_id SERIAL PRIMARY KEY,
    waybill_number INTEGER UNIQUE,
    article_furniture INTEGER REFERENCES furniture(furniture_article),
    furniture_quantity INTEGER,
    orders_number INTEGER REFERENCES orders(order_number)
);

CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(50) NOT NULL
);
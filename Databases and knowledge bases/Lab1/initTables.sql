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
    provider_id INTEGER REFERENCES provider(provider_id),
    product_name VARCHAR(255) NOT NULL,
    receipt_date DATE,
    quantity INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    weight DECIMAL(5, 2) NOT NULL,
    provider_name VARCHAR(255),
    CONSTRAINT fk_provider FOREIGN KEY (provider_id) REFERENCES provider(provider_id)
);

-- Заполним provider_name при помощи триггера
CREATE OR REPLACE FUNCTION update_provider_name()
RETURNS TRIGGER AS $$
BEGIN
    NEW.provider_name := (
        SELECT provider_name FROM provider WHERE provider.provider_id = NEW.provider_id
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_provider_name_trigger
BEFORE INSERT OR UPDATE ON product
FOR EACH ROW
EXECUTE FUNCTION update_provider_name();

CREATE TABLE orders (
    orders_id SERIAL PRIMARY KEY,
    order_number INTEGER UNIQUE NOT NULL,
    product_id INTEGER,
    product_name VARCHAR(255),
    product_quantity INT NOT NULL,
    weight DECIMAL(5, 2) NOT NULL,
    registration_date DATE,
    total_cost DECIMAL(10, 2) NOT NULL,
    category_customer VARCHAR(50) NOT NULL CHECK (category_customer IN ('Юр. лицо', 'Физ. лицо')),
    customer_id INTEGER,
    customer_name VARCHAR(255),
    CONSTRAINT fk_product FOREIGN KEY (product_id) REFERENCES product(product_id),
    CONSTRAINT fk_legal_person FOREIGN KEY (customer_id) REFERENCES legal_person(legal_person_id) DEFERRABLE INITIALLY DEFERRED,
    CONSTRAINT fk_natural_person FOREIGN KEY (customer_id) REFERENCES natural_person(natural_person_id) DEFERRABLE INITIALLY DEFERRED,
    CONSTRAINT check_customer_id CHECK (
        (category_customer = 'Юр. лицо' AND customer_id IS NOT NULL) OR
        (category_customer = 'Физ. лицо' AND customer_id IS NOT NULL)
    ),
    CONSTRAINT check_customer_name CHECK (
        (category_customer = 'Юр. лицо' AND customer_name IS NOT NULL) OR
        (category_customer = 'Физ. лицо' AND customer_name IS NOT NULL)
    )
);

CREATE OR REPLACE FUNCTION update_product_name()
RETURNS TRIGGER AS $$
BEGIN
    NEW.product_name := (
        SELECT product_name FROM product WHERE product.product_id = NEW.product_id
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_product_name_trigger
BEFORE INSERT OR UPDATE ON orders
FOR EACH ROW
EXECUTE FUNCTION update_product_name();
CREATE TABLE natural_person (
    natural_person_id SERIAL PRIMARY KEY,
    passport_details VARCHAR(255) UNIQUE NOT NULL,
    phone_number VARCHAR(255) NOT NULL,
    natural_customer_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    delivery_address VARCHAR(255) NOT NULL
);

CREATE TABLE legal_person (
    legal_person_id SERIAL PRIMARY KEY,
    inn VARCHAR(255) UNIQUE NOT NULL,
    legal_customer_name VARCHAR(255) NOT NULL,
    phone_number VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    delivery_address VARCHAR(255) NOT NULL,
	representative_name VARCHAR(255) NOT NULL
);

CREATE TABLE provider (
    provider_id SERIAL PRIMARY KEY,
    inn VARCHAR(255) UNIQUE NOT NULL,
    provider_name VARCHAR(255) NOT NULL,
    address VARCHAR(255) NOT NULL
);

CREATE TABLE product (
    product_id SERIAL PRIMARY KEY,
    place INTEGER UNIQUE NOT NULL,
    provider_id INTEGER REFERENCES provider(provider_id),
    product_name VARCHAR(255) NOT NULL,
    receipt_date DATE,
    article VARCHAR(255) UNIQUE NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    weight DECIMAL(5, 2) NOT NULL,
    provider_name VARCHAR(255),
    CONSTRAINT fk_provider FOREIGN KEY (provider_id) REFERENCES provider(provider_id)
);

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
    weight DECIMAL(5, 2) NOT NULL,
    registration_date DATE,
    total_cost DECIMAL(10, 2) NOT NULL,
    category_customer VARCHAR(50) NOT NULL CHECK (category_customer IN ('Юр. лицо', 'Физ. лицо')),
    customer_id INTEGER,
    customer_name VARCHAR(255),
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

CREATE TABLE waybill (
    waibill_id SERIAL PRIMARY KEY,
    article_product VARCHAR(255) REFERENCES product(article),
    product_quantity INTEGER NOT NULL,
	orders_number INTEGER REFERENCES orders(order_number)
);
CREATE TABLE natural_person (
    id SERIAL PRIMARY KEY,
    passport VARCHAR(255) UNIQUE NOT NULL,
    forename VARCHAR(255) NOT NULL,
    phone VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    delivery_address VARCHAR(255) NOT NULL
);

CREATE TABLE legal_person (
    id SERIAL PRIMARY KEY,
    inn VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    phone VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    delivery_address VARCHAR(255) NOT NULL,
	representative_forename VARCHAR(255) NOT NULL
);

CREATE TABLE provider (
    id SERIAL PRIMARY KEY,
    inn VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    address VARCHAR(255) NOT NULL
);

CREATE TABLE product (
    id SERIAL PRIMARY KEY,
    place INTEGER UNIQUE NOT NULL,
    provider_id INTEGER REFERENCES provider(provider_id),
    provider_name VARCHAR(255),
    CONSTRAINT fk_provider FOREIGN KEY (provider_id) REFERENCES provider(provider_id),
    name VARCHAR(255) NOT NULL,
    receipt_date DATE,
    article VARCHAR(255) UNIQUE NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    weight DECIMAL(5, 2) NOT NULL,
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
    id SERIAL PRIMARY KEY,
    order_number INTEGER UNIQUE NOT NULL,
    weight DECIMAL(5, 2) NOT NULL,
    registration_date DATE,
    cost DECIMAL(10, 2) NOT NULL,
    customer_id INTEGER,
    customer_category VARCHAR(50) NOT NULL CHECK (category_customer IN ('Юр. лицо', 'Физ. лицо')),
    CONSTRAINT fk_legal_person FOREIGN KEY (customer_id) REFERENCES legal_person(legal_person_id) DEFERRABLE INITIALLY DEFERRED,
    CONSTRAINT fk_natural_person FOREIGN KEY (customer_id) REFERENCES natural_person(natural_person_id) DEFERRABLE INITIALLY DEFERRED,
    CONSTRAINT check_customer_id CHECK (
        (category_customer = 'Юр. лицо' AND customer_id IS NOT NULL) OR
        (category_customer = 'Физ. лицо' AND customer_id IS NOT NULL)
    )
);

CREATE TABLE waybill (
    id SERIAL PRIMARY KEY,
    article_product VARCHAR(255) REFERENCES product(article),
    product_quantity INTEGER NOT NULL,
	orders_number INTEGER REFERENCES orders(order_number)
);
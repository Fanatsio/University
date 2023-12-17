CREATE OR REPLACE FUNCTION fill_data() RETURNS void AS $$
DECLARE
    i INTEGER := 0;
BEGIN
    WHILE i < 1000 LOOP
        INSERT INTO legal_person (inn, legal_customer_name, phone_number, email, delivery_address, representative_name) 
		VALUES ('legal_customer' || i, 'phone_number' || i, 'email' || i, 'delivery_address' || i, 'representative_name' || i);
		INSERT INTO natural_person (passport_details, phone_number, natural_customer_name, email, delivery_address) 
		VALUES ('passport_details' || i, 'phone_number' || i, 'natural_customer_name' || i, 'email' || i, 'delivery_address' || i);
		INSERT INTO product (place, product_name, receipt_date, article, quantity, price, weight) 
		VALUES ('passport_details' || i, 'phone_number' || i, 'natural_customer_name' || i, 'email' || i, 'delivery_address' || i);
        i := i + 1;
    END LOOP;
END;
$$ LANGUAGE plpgsql;

SELECT fill_data();
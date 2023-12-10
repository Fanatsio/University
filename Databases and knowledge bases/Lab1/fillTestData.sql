CREATE OR REPLACE FUNCTION fill_provider_name() RETURNS void AS $$
DECLARE
    i INTEGER := 0;
BEGIN
    WHILE i < 1000 LOOP -- создаст 1000 записей
        INSERT INTO provider (provider_name) VALUES ('provider ' || i);
        i := i + 1;
    END LOOP;
END;
$$ LANGUAGE plpgsql;


SELECT fill_provider_name();
-- Database: warehouse

-- DROP DATABASE IF EXISTS warehouse;

CREATE DATABASE warehouse
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'Russian_Russia.1251'
    LC_CTYPE = 'Russian_Russia.1251'
    LOCALE_PROVIDER = 'libc'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;
	
CREATE TABLE natural_person (
	natural_person_id SERIAL PRIMARY KEY,
	passport_details INTEGER UNIQUE NOT NULL,
	phone_number INTEGER NOT NULL,
	natural_customer_name VARCHAR NOT NULL,
	email VARCHAR NOT NULL,
	delivery_address VARCHAR NOT NULL
)

CREATE TABLE legal_person (
	legal_person_id SERIAL PRIMARY KEY,
	inn INTEGER UNIQUE NOT NULL,
	legal_customer_name VARCHAR NOT NULL,
	phone_number INTEGER NOT NULL,
	email VARCHAR NOT NULL,
	delivery_address VARCHAR NOT NULL
)

CREATE TABLE provider (
	provider_id SERIAL PRIMARY KEY,
	inn INTEGER UNIQUE NOT NULL,
	provider_name VARCHAR NOT NULL
	address VARCHAR NOT NULL
)

CREATE TABLE product (
	product_id SERIAL PRIMARY KEY,
	place VARCHAR NOT NULL,
	provider_name VARCHAR REFERENCES provider(provider_name),
	product_name VARCHAR,
	receipt_date DATE
	quantity INT NOT NULL
	price DECIMAL(10, 2) NOT NULL
	weight DECIMAL(5, 2) NOT NULL
)
	
CREATE TABLE orders (
	orders_id SERIAL PRIMARY KEY,
	order_number INTEGER UNIQUE NOT NULL,
	name_customer VARCHAR REFERENCES 
)
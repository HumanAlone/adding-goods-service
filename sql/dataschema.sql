-- Схема БД

CREATE TABLE categories (
	id INTEGER NOT NULL, 
	name VARCHAR(255) NOT NULL, 
	parent_id INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(parent_id) REFERENCES categories (id) ON DELETE SET NULL
);

CREATE TABLE clients (
	id INTEGER NOT NULL, 
	name VARCHAR(255) NOT NULL, 
	address VARCHAR(512), 
	PRIMARY KEY (id)
);

CREATE TABLE products (
	id INTEGER NOT NULL, 
	name VARCHAR(255) NOT NULL, 
	quantity INTEGER NOT NULL, 
	price DECIMAL(10, 2) NOT NULL, 
	category_id INTEGER, 
	PRIMARY KEY (id), 
	CONSTRAINT check_quantity_positive CHECK (quantity >= 0), 
	CONSTRAINT check_price_positive CHECK (price >= 0), 
	FOREIGN KEY(category_id) REFERENCES categories (id) ON DELETE SET NULL
);

CREATE TABLE orders (
	id INTEGER NOT NULL, 
	client_id INTEGER NOT NULL, 
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
	PRIMARY KEY (id), 
	FOREIGN KEY(client_id) REFERENCES clients (id) ON DELETE CASCADE
);

CREATE TABLE order_items (
	id INTEGER NOT NULL, 
	order_id INTEGER NOT NULL, 
	product_id INTEGER NOT NULL, 
	quantity INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	CONSTRAINT uq_order_product UNIQUE (order_id, product_id), 
	CONSTRAINT check_order_quantity_positive CHECK (quantity > 0), 
	FOREIGN KEY(order_id) REFERENCES orders (id) ON DELETE CASCADE, 
	FOREIGN KEY(product_id) REFERENCES products (id) ON DELETE CASCADE
);

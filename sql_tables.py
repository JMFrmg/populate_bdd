TABLE_COLUMNS = tables_columns = {
                    "customer": ["id", "country"],
                    "product": ["id", "description", "price"],
                    "customer_order": ["id", "invoice_nb", "invoice_date", "customer_id"],
                    "order_detail": ["id", "quantity", "order_id", "product_id"]
                }

CREATE_TABLES = {"customer": """CREATE TABLE customer (
	                id INTEGER NOT NULL, 
	                country VARCHAR, 
	                PRIMARY KEY (id)
                );""",

                "customer_order": """CREATE TABLE customer_order (
                    id INTEGER NOT NULL, 
                    invoice_nb INTEGER, 
                    invoice_date DATE,
                    customer_id INTEGER, 
                    PRIMARY KEY (id), 
                    FOREIGN KEY(customer_id) REFERENCES customer (id)
                );""",

                "product": """CREATE TABLE product (
                    id INTEGER NOT NULL, 
                    description VARCHAR, 
                    price FLOAT, 
                    PRIMARY KEY (id)
                );""",

                "order_detail": """CREATE TABLE order_detail (
                    id INTEGER NOT NULL, 
                    quantity INTEGER, 
                    order_id INTEGER, 
                    product_id INTEGER, 
                    PRIMARY KEY (id), 
                    FOREIGN KEY(order_id) REFERENCES "order" (id), 
                    FOREIGN KEY(product_id) REFERENCES product (id)
                );"""

                }


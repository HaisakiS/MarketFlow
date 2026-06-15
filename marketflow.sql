CREATE TABLE price_sources (
    id_source INTEGER PRIMARY KEY AUTOINCREMENT,
    source_name TEXT NOT NULL UNIQUE,
    type TEXT DEFAULT 'Supplier'
);

CREATE TABLE price_history (
    id_history INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT NOT NULL,
    variant TEXT DEFAULT 'Unique',
    recorded_price REAL NOT NULL,
    record_date TEXT DEFAULT CURRENT_DATE,
    id_source INTEGER,
    notes TEXT,
    FOREIGN KEY (id_source) REFERENCES price_sources (id_source)
);


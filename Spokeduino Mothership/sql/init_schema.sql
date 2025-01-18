PRAGMA foreign_keys = ON;

-- Manufacturers table
CREATE TABLE manufacturers
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

-- Tensiometer table
CREATE TABLE tensiometers
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

-- Spoke types table
CREATE TABLE types
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT NOT NULL UNIQUE
);

-- Spokes table
CREATE TABLE spokes
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    manufacturer_id INTEGER NOT NULL,
    type_id INTEGER NOT NULL,
    gauge INTEGER NOT NULL,
    weight DECIMAL(2, 1) DEFAULT 0.0,
    name TEXT NOT NULL,
    dimensions TEXT NOT NULL,
    comment TEXT DEFAULT '',
    FOREIGN KEY (manufacturer_id)
        REFERENCES manufacturers(id)
        ON DELETE CASCADE,
    FOREIGN KEY (type_id)
        REFERENCES types(id)
        ON DELETE CASCADE
);

-- Measurement sets table
CREATE TABLE measurement_sets
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    spoke_id INTEGER NOT NULL,
    tensiometer_id INTEGER NOT NULL,
    comment TEXT DEFAULT '',
    ts DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (tensiometer_id)
        REFERENCES tensiometers(id)
        ON DELETE CASCADE,
    FOREIGN KEY (spoke_id)
        REFERENCES spokes(id)
        ON DELETE CASCADE
);

-- Measurements table
CREATE TABLE measurements
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    set_id INTEGER NOT NULL,
    tension DECIMAL(5, 2) NOT NULL,
    deflection DECIMAL(5, 2) NOT NULL,
    FOREIGN KEY (set_id)
        REFERENCES measurement_sets(id)
        ON DELETE CASCADE
);

-- Settings table
CREATE TABLE settings
(
	key TEXT PRIMARY KEY,
	value TEXT
);

-- Indexes for optimization
CREATE INDEX idx_manufacturer_id ON spokes(manufacturer_id);
CREATE INDEX idx_type_id ON spokes(type_id);
CREATE INDEX idx_tensiometer_id ON measurements(tensiometer_id);
CREATE INDEX idx_spoke_id ON measurements(spoke_id);

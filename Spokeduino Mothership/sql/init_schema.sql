PRAGMA foreign_keys = ON;

-- Manufacturers table
CREATE TABLE manufacturers 
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

-- Tensioners table
CREATE TABLE tensioners
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

-- Measurements table
CREATE TABLE measurements
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tensioner_id INTEGER NOT NULL,
    spoke_id INTEGER NOT NULL,
    tension_300N DECIMAL(5, 2) DEFAULT 0.00,
    tension_400N DECIMAL(5, 2) DEFAULT 0.00,
    tension_500N DECIMAL(5, 2) DEFAULT 0.00,
    tension_600N DECIMAL(5, 2) DEFAULT 0.00,
    tension_700N DECIMAL(5, 2) DEFAULT 0.00,
    tension_800N DECIMAL(5, 2) DEFAULT 0.00,
    tension_900N DECIMAL(5, 2) DEFAULT 0.00,
    tension_1000N DECIMAL(5, 2) DEFAULT 0.00,
    tension_1100N DECIMAL(5, 2) DEFAULT 0.00,
    tension_1200N DECIMAL(5, 2) DEFAULT 0.00,
    tension_1300N DECIMAL(5, 2) DEFAULT 0.00,
    tension_1400N DECIMAL(5, 2) DEFAULT 0.00,
    tension_1500N DECIMAL(5, 2) DEFAULT 0.00,
    tension_1600N DECIMAL(5, 2) DEFAULT 0.00,
    formula TEXT DEFAULT '',
    comment TEXT DEFAULT '',
    FOREIGN KEY (tensioner_id) 
        REFERENCES tensioners(id)
        ON DELETE CASCADE,
    FOREIGN KEY (spoke_id) 
        REFERENCES spokes(id)
        ON DELETE CASCADE
);

-- Indexes for optimization
CREATE INDEX idx_manufacturer_id ON spokes(manufacturer_id);
CREATE INDEX idx_type_id ON spokes(type_id);
CREATE INDEX idx_tensioner_id ON measurements(tensioner_id);
CREATE INDEX idx_spoke_id ON measurements(spoke_id);

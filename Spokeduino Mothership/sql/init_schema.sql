PRAGMA foreign_keys = ON;

CREATE TABLE tensiometers
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE spoke_manufacturers
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE spoke_types
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT NOT NULL UNIQUE
);

CREATE TABLE spoke_models
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
        REFERENCES spoke_manufacturers(id)
        ON DELETE CASCADE,
    FOREIGN KEY (type_id)
        REFERENCES spoke_types(id)
        ON DELETE CASCADE
);

CREATE TABLE spoke_measurement_sets
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
        REFERENCES spoke_models(id)
        ON DELETE CASCADE
);

CREATE TABLE spoke_measurements
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    set_id INTEGER NOT NULL,
    tension DECIMAL(5, 2) NOT NULL,
    deflection DECIMAL(5, 2) NOT NULL,
    FOREIGN KEY (set_id)
        REFERENCES spoke_measurement_sets(id)
        ON DELETE CASCADE
);

CREATE TABLE hub_manufacturers
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE axle_types
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE boost_classifications
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE hub_models
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    manufacturer_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    axle_type_id INTEGER NOT NULL, -- FK to axle_types
    old INTEGER NOT NULL, -- Over Locknut Dimension
    pcd_left DECIMAL(5, 2) NOT NULL, -- Pitch Circle Diameter (Left)
    pcd_right DECIMAL(5, 2) NOT NULL, -- Pitch Circle Diameter (Right)
    wl DECIMAL(5, 2), -- Flange distance to center (Left)
    wr DECIMAL(5, 2), -- Flange distance to center (Right)
    spoke_hole_diameter_left DECIMAL(3, 2) DEFAULT 2.5, -- Defaults to 2.5mm
    spoke_hole_diameter_right DECIMAL(3, 2) DEFAULT 2.5,    
    is_front BOOLEAN NOT NULL DEFAULT True, -- True = Front Hub, False = Rear Hub
    is_disc BOOLEAN NOT NULL DEFAULT True, -- True = Disc Brake, False = Rim Brake
    is_centerlock BOOLEAN NOT NULL DEFAULT True, -- True = Center Lock, False = 6-Bolt
    is_jbend BOOLEAN NOT NULL, -- True = J-Bend, False = Straightpull
    comment TEXT DEFAULT '',
    FOREIGN KEY (manufacturer_id) REFERENCES hub_manufacturers(id) ON DELETE CASCADE,
    FOREIGN KEY (axle_type_id) REFERENCES axle_types(id) ON DELETE CASCADE    
);

CREATE TABLE rim_manufacturers
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE rim_models
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    manufacturer_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    etrto_bsd INTEGER NOT NULL, -- Bead Seat Diameter (622, 584, etc.)
    etrto_width INTEGER NOT NULL, -- Internal width (19, 21, etc.)
    outer_width DECIMAL(5, 2), -- External rim width
    erd DECIMAL(5, 2) NOT NULL, -- Effective Rim Diameter
    nipple_offset_left DECIMAL(5, 2) DEFAULT 0.00, -- Left side offset
    nipple_offset_right DECIMAL(5, 2) DEFAULT 0.00, -- Right side offset
    rim_depth DECIMAL(5, 2) NOT NULL, -- Needed for deep-section spoke calculations
    is_disc BOOLEAN NOT NULL DEFAULT True, -- True = Disc Brake, False = Rim Brake
    comment TEXT DEFAULT '',
    FOREIGN KEY (manufacturer_id) REFERENCES rim_manufacturers(id) ON DELETE CASCADE  
);

CREATE TABLE etrto_description
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    etrto_bsd INTEGER NOT NULL, -- Bead Seat Diameter (559, 584, 622)
    name TEXT NOT NULL, -- "26", "27.5", "29", etc.    
    is_default BOOLEAN DEFAULT FALSE -- Marks the most common description
);

CREATE TABLE settings
(
	key TEXT PRIMARY KEY,
	value TEXT
);

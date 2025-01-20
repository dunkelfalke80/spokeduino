INSERT INTO measurement_sets (spoke_id, tensiometer_id, comment) 
VALUES 
(1, 1, 'Gute Daten'),
(1, 1, 'Falsche Daten'),
(1, 1, 'Schlechte daten');

INSERT INTO measurements (set_id, tension, deflection) 
VALUES 
(1, 1500, 3.10), 
(1, 1400, 3.05),
(1, 1300, 3.01),
(1, 1200, 2.95),
(1, 1100, 2.89),
(1, 1000, 2.82),
(1, 900, 2.76),
(1, 800, 2.67),
(1, 700, 2.57),
(1, 600, 2.49),
(1, 500, 2.34),
(1, 400, 2.20);

INSERT INTO measurements (set_id, tension, deflection) 
VALUES 
(2, 1500, 3.14), 
(2, 1400, 3.10),
(2, 1300, 3.05),
(2, 1200, 3.00),
(2, 1100, 2.94),
(2, 1000, 2.87),
(2, 900, 2.80),
(2, 800, 2.73),
(2, 700, 2.64),
(2, 600, 2.53),
(2, 500, 2.43),
(2, 400, 2.28);


INSERT INTO measurements (set_id, tension, deflection) 
VALUES 
(3, 1500, 3.18), 
(3, 1400, 3.14),
(3, 1300, 3.07),
(3, 1200, 3.02),
(3, 1100, 2.92),
(3, 1000, 2.86),
(3, 900, 2.78),
(3, 800, 2.70),
(3, 700, 2.60),
(3, 600, 2.52),
(3, 500, 2.36),
(3, 400, 2.21);
PRAGMA foreign_keys = ON;

INSERT INTO manufacturers (id, name) VALUES
(0, 'Custom'),
(1, 'Sapim'),
(2, 'DT Swiss'),
(3, 'Pillar'),
(4, 'cnSpoke'),
(5, 'Alpina'),
(6, 'Wheelsmith'),
(7, 'Berd');

INSERT INTO tensiometers (id, name) VALUES
(0, 'Toopre TL-P3'),
(1, 'Toopre TL-P11'),
(2, 'ZTTO TC-02');

INSERT INTO types (id, type) VALUES
(0, 'Straight gauge'),
(1, 'Single-butted'),
(2, 'Double-butted'),
(3, 'Triple-butted'),
(4, 'Quadruple-butted'),
(5, 'Aero'),
(6, 'Titanium'),
(7, 'Carbon'),
(8, 'Flexible'),
(9, 'Alloy');

INSERT INTO spokes (manufacturer_id, type_id, gauge, weight, name, dimensions) VALUES

-- Generic --------------------------------------------
--  Straight gauge
(0, 0, 13, 8.5, 'Generic straight gauge 13G', '2.3'),
(0, 0, 14, 6.7, 'Generic straight gauge 14G', '2.0'),
(0, 0, 15, 5.5, 'Generic straight gauge 15G', '1.8'),
--  Double butted
(0, 2, 14, 5.7, 'Generic double butted', '2.0/1.8/2.0'),

-- Sapim ----------------------------------------------
--  Straight gauge
(1, 0, 12, 10.8, 'Zinc', '2.6'),
(1, 0, 13, 8.5, 'Zinc', '2.3'),
(1, 0, 14, 6.7, 'Zinc', '2.0'),
(1, 0, 12, 10.8, 'Leader', '2.6'),
(1, 0, 13, 8.5, 'Leader', '2.3'),
(1, 0, 14, 6.7, 'Leader', '2.0'),
(1, 0, 15, 5.5, 'Leader', '1.8'),
--  Butted
(1, 1, 13, 9.0, 'E-Strong', '2.6/2.3'),
(1, 1, 14, 7.0, 'Strong', '2.3/2.0'),
--  Double butted
(1, 2, 12, 9.5, 'E-Race', '2.6/2.3/2.6'),
(1, 2, 13, 6.0, 'Race', '2.3/2.0/2.3'),
(1, 2, 14, 5.7, 'Race', '2.0/1.8/2.0'),
(1, 2, 14, 5.2, 'Sprint', '2.0/1.7/2.0'),
(1, 2, 14, 4.8, 'D-Light', '2.0/1.65/2.0'),
(1, 2, 14, 5.3, 'E-Light', '2.2/1.7/2.0'),
(1, 2, 14, 4.4, 'Laser', '2.0/1.5/2.0'),
(1, 2, 15, 3.6, 'Super Spoke', '1.8/1.4/1.8'),
--  Triple butted
(1, 3, 14, 5.9, 'Force', '2.2/2.0/1.8/2.0'),
--  Aero
(1, 5, 13, 8.8, 'CX', '2.3/3.2-1.5/2.3'),
(1, 5, 14, 6.6, 'CX', '2.0/2.8-1.3/2.0'),
(1, 5, 14, 4.4, 'CX-Ray', '2.0/2.2-0.9/2.0'),
(1, 5, 14, 5.2, 'CX-Sprint', '2.0/2.2-1.2/2.0'),
(1, 5, 14, 4.3, 'CX-Delta', '2.0/2.2-0.9/2.0'),
(1, 5, 13, 8.7, 'CX-Wing', '2.3/4.5-0.9/2.3'),
(1, 5, 14, 6.8, 'CX-Wing', '2.0/3.5-0.9/2.0'),
(1, 5, 14, 5.8, 'CX-Force', '2.2/2.3-1.3/2.0'),
(1, 5, 13, 6.0, 'CX-Speed', '2.3/2.3-1.26/2.3'),
(1, 5, 14, 5.6, 'CX-Speed', '2.0/2.6-1.2/2.0'),
(1, 5, 14, 7.1, 'CX-Ultra', '2.3/3.5-0.9/2.0'),
(1, 5, 14, 7.1, 'CX-Extra', '2.3/2.8-1.3/2.0'),
(1, 5, 14, 3.6, 'CX-Super', '1.8/2.0-0.8/1.8'),

-- DT Swiss -------------------------------------------
--  Straight gauge
(2, 0, 14, 6.9, 'Champion', '2.0'),
(2, 0, 15, 5.6, 'Champion', '1.8'),
--  Butted
(2, 1, 14, 6.5, 'Alpine', '2.34/2.0'),
--  Double butted
(2, 2, 14, 6.0, 'Competition', '2.0/1.8/2.0'),
(2, 2, 15, 4.9, 'Competition', '1.8/1.6/1.8'),
(2, 2, 14, 4.9, 'Competition Race', '2.0/1.6/2.0'),
(2, 2, 14, 4.4, 'Revolution', '2.0/1.5/2.0'),
--  Triple butted
(2, 3, 14, 6.5, 'Alpine III', '2.34/2.0/1.85/2.0'),
(2, 3, 15, 5.0, 'Supercomp', '2.0/1.8/1.7/1.8'),
--  Aero
(2, 5, 14, 6.0, 'Aero Comp', '2.0/2.3-1.25/2.0'),
(2, 5, 14, 4.0, 'Aerolite', '2.5/2.0-0.9/1.5/2.0'),
(2, 5, 14, 4.0, 'Revolite', '2.3/2.0-1.3/1.57/2.0'),
(2, 5, 14, 5.7, 'Complite', '2.3/2.0-1.5/1.75/2.0'),
(2, 5, 15, 5.5, 'Aero Speed', '1.8/2.3-1.2/1.8'),

-- Pillar ---------------------------------------------
--  Straight gauge
(3, 0, 12, 10.9, 'P12', '2.6'),
(3, 0, 13, 8.5, 'P13', '2.3'),
(3, 0, 14, 6.5, 'P14', '2.0'),
(3, 0, 15, 5.5, 'P15', '1.8'),
(3, 0, 14, 8.5, 'P13/P14', '2.3'),
(3, 0, 14, 8.5, 'S13/S14', '2.3'),
--  Butted
(3, 1, 13, 9.0, 'PSB23', '2.6/2.3'),
(3, 1, 14, 6.8, 'PSB34', '2.3/2.0'),
(3, 1, 15, 5.6, 'PSB45', '2.0/1.8'),
--  Double butted
(3, 2, 12, 9.2, 'PDB1213', '2.6/2.3/2.6'),
(3, 2, 13, 7.0, 'PDB1314', '2.3/2.0/2.3'),
(3, 2, 14, 5.7, 'PDB1415', '2.0/1.8/2.0'),
(3, 2, 14, 4.7, 'PDB1416', '2.0/1.6/2.0'),
(3, 2, 14, 4.3, 'PDB1417', '2.0/1.5/2.0'),
--  Triple butted
(3, 3, 14, 6.3, 'PTB380', '2.3/2.0/1.8/2.0'),
(3, 3, 14, 5.3, 'PTB270', '2.2/2.0/1.7/2.0'),
(3, 3, 14, 4.3, 'PSR TB2015', '2.2/2.0/1.5/2.0'),
(3, 3, 14, 4.7, 'PSR TB2016', '2.2/2.0/1.6/2.0'),
(3, 3, 14, 5.2, 'PSR TB2017', '2.2/2.0/1.7/2.0'),
(3, 3, 14, 5.7, 'PSR TB2018', '2.2/2.0/1.8/2.0'),
--  Quadruple butted
(3, 4, 14, 6.3, 'PSR QB5380', '2.5/2.3/1.8/2.0'),
(3, 4, 14, 5.8, 'PSR QB4270', '2.4/2.3/1.7/2.0'),
--  Aero
(3, 5, 14, 6.5, 'PA 1423', '2.0/2.3-1.5/2.0'),
(3, 5, 14, 6.5, 'PA 1432', '2.0/3.2-1.0/2.0'),
(3, 5, 15, 5.5, 'PA 1528', '1.8/2.8-1.0/1.8'),
(3, 5, 14, 4.3, 'PBA 1420', '2.0/2.0-0.95/2.0'),
(3, 5, 14, 4.7, 'PBA 1422', '2.0/2.2-0.95/2.0'),
(3, 5, 14, 5.7, 'PBA 1425', '2.0/2.5-1.05/2.0'),
(3, 5, 14, 6.5, 'PSR AERO 1423', '2.2/2.3-1.5/2.0'),
(3, 5, 14, 6.5, 'PSR AERO 1432', '2.2/3.2-1.0/2.0'),
(3, 5, 15, 5.5, 'PSR AERO 1525', '2.0/2.8-1.0/1.8'),
(3, 5, 14, 4.3, 'PSR XTRA 1420', '2.2/2.0-0.95/2.0'),
(3, 5, 14, 4.7, 'PSR XTRA 1422', '2.2/2.2-0.95/2.0'),
(3, 5, 14, 5.2, 'PSR XTRA 1424', '2.2/2.4-1.05/2.0'),
(3, 5, 14, 5.7, 'PSR XTRA 1425', '2.2/2.5-1.05/2.0'),
(3, 5, 13, 6.5, '13g Wing 25', '2.3/2.5-1.4/2.3'),
(3, 5, 14, 4.3, 'PSR WING 20', '2.2/2.0-1.2/2.0'),
(3, 5, 14, 4.7, 'PSR WING 21', '2.2/2.1-1.3/2.0'),
(3, 5, 14, 5.2, 'PSR WING 22', '2.2/2.2-1.4/2.0'),
(3, 5, 14, 5.7, 'PSR WING 23', '2.2/2.3-1.45/2.0'),

-- cnSpoke --------------------------------------------
--  Straight gauge
(4, 0, 12, 10.7, 'STD 12', '2.6'),
(4, 0, 13, 8.6, 'STD 13', '2.3'),
(4, 0, 14, 6.5, 'STD 14C', '2.0'),
(4, 0, 15, 5.3, 'STD 15C', '1.8'),
(4, 0, 12, 10.7, 'UCP 12', '2.6'),
(4, 0, 13, 8.6, 'UCP 13', '2.3'),
(4, 0, 14, 6.7, 'UCP 14C', '2.0'),
(4, 0, 15, 5.3, 'UCP 15C', '1.8'),
(4, 0, 13, 8.7, 'MAC 13', '2.3'),
(4, 0, 14, 6.6, 'MAC 14', '2.0'),
(4, 0, 15, 5.5, 'MAC 15', '1.8'),
(4, 0, 13, 8.5, 'mac 134T', '2.3'),
--  Butted
(4, 2, 13, 6.6, 'mac OPTIME 344', '2.3/2.0'),
(4, 2, 14, 5.5, 'mac OPTIME 455', '2.0/1.8'),
--  Double butted
(4, 2, 14, 4.2, 'mac DB 474', '2.0/1.5/2.0'),
(4, 2, 14, 4.7, 'mac DB 464', '2.0/1.6/2.0'),
(4, 2, 14, 5.2, 'mac DB 404', '2.0/1.7/2.0'),
(4, 2, 14, 5.6, 'mac DB 454', '2.0/1.8/2.0'),
(4, 2, 15, 3.8, 'mac DB 545', '1.8/1.4/1.8'),
(4, 2, 15, 4.4, 'mac DB 565', '1.8/1.6/1.8'),
(4, 2, 13, 8.61, 'XT233', '2.5/2.3'),
(4, 2, 14, 6.45, 'XT344', '2.2/2.0'),
--  Triple butted
(4, 3, 13, 5.6, 'mac TB 354', '2.3/2.0/1.8/2.3'),
(4, 3, 13, 5.2, 'mac TB 304', '2.3/2.0/1.7/2.3'),
(4, 3, 14, 4.1, 'mac TB 475', '2.0/1.8/1.5/2.0'),
(4, 3, 14, 5.0, 'mac TB 405', '2.0/1.8/1.7/2.0'),
--  Aero
(4, 5, 14, 3.3, 'mac Aero 330', '1.8/2.0-0.9/2.0'),
(4, 5, 14, 3.6, 'mac Aero 360', '2.0/2.0-0.9/2.0'),
(4, 5, 13, 8.6, 'mac Aero 373', '3.2/2.3-1.5/2.3'),
(4, 5, 13, 8.6, 'mac Aero 374T', '3.2/2.3-1.4/2.0'),
(4, 5, 13, 8.6, 'mac Aero 383', '4.3/2.3-1.3/2.3'),
(4, 5, 13, 8.5, 'mac Aero 384T', '4.3/2.3-1.3/2.0'),
(4, 5, 13, 8.6, 'mac Aero 393', '5.0/2.3-1.1/2.3'),
(4, 5, 13, 8.5, 'mac Aero 394T', '5.0/2.3-1.1/2.0'),
(4, 5, 14, 4.7, 'mac Aero 416', '2.2/2.0-1.0/2.0'),
(4, 5, 14, 5.1, 'mac Aero 417', '2.2/2.0-1.1/2.0'),
(4, 5, 14, 5.6, 'mac Aero 418', '2.2/2.0-1.2/2.0'),
(4, 5, 14, 4.2, 'mac Aero 424', '2.2/2.0-0.9/2.0'),
(4, 5, 14, 6.5, 'mac Aero 474', '2.3/2.0-1.5/2.0'),
(4, 5, 14, 6.5, 'mac Aero 494', '3.0/2.0-1.2/2.0'),
(4, 5, 14, 6.5, 'mac Aero 494C', '3.5/2.0-1.1/2.0'),
(4, 5, 15, 4.4, 'mac Aero 565', '2.2/1.8-1.0/1.8'),
(4, 5, 15, 5.4, 'mac Aero 585', '2.3/1.8-1.2/1.8'),
(4, 5, 15, 5.4, 'mac Aero 595', '3.0/1.8-1.0/1.8'),
(4, 5, 13, 5.6, 'mac Aries 384', '2.5/2.3-1.2/2.0'),
(4, 5, 13, 6.6, 'mac Bravo 374', '2.3/2.3-1.5/2.0'),
(4, 5, 15, 6.5, 'mac Bravo 394', '3.0/2.3-1.2/2.0'),
(4, 5, 14, 3.6, 'XTA 360', '2.0/2.0-0.9/2.0'),
(4, 5, 14, 4.2, 'XTA 424', '2.0/2.2-0.9/2.0'),
(4, 5, 14, 4.7, 'XTA 416', '2.0/2.2-1.0/2.0'),
--  Titanium
(4, 6, 14, 3.7, 'Ti-14C', '2.0'),
(4, 6, 14, 3.6, 'Ti-Aero', '2.0/3.0/2.0'),
(4, 6, 14, 2.8, 'Ti-Duo Aero', '2.0/2.3/2.0'),
(4, 6, 14, 2.8, 'Ti-Duo', '2.0/1.7/2.0'),

-- Alpina ---------------------------------------------
--  Straight gauge
(5, 0, 13, 8.5, 'One XL', '2.33'),
(5, 0, 13, 8.5, 'One XXL', '2.33'),
(5, 0, 14, 6.5, 'One', '2.0'),
--  Butted
(5, 1, 13, 8.9, 'Spark XL', '2.62/2.33'),
(5, 1, 14, 6.7, 'Spark', '2.33/2.0'),
--  Double butted
(5, 2, 14, 5.7, 'Basicite', '2.0/1.8/2.0'),
(5, 2, 14, 5.7, 'Extralite', '2.0/1.7/2.0'),
(5, 2, 14, 4.3, 'Superlite', '2.0/1.6/2.0'),
(5, 2, 14, 4.3, 'Ultralite', '2.0/1.5/2.0'),
--  Quadruple butted
(5, 4, 14, 3.3, 'Hyperlite', '2.0/1.5/1.3/1.5/2.0'),
--  Aero
(5, 5, 13, 6.5, 'One Aero XL', '2.33'),
(5, 5, 13, 8.5, 'One Flat XL', '2.33'),
(5, 5, 14, 6.5, 'One Aero', '2.0'),
(5, 5, 14, 6.5, 'One Flat', '2.0'),
(5, 5, 14, 5.7, 'Basicite Aero', '2.0/1.8/2.0'),
(5, 5, 14, 5.7, 'Extralite Aero', '2.0/1.7/2.0'),
(5, 5, 14, 5.7, 'Extralite Flat', '2.0/1.7/2.0'),
(5, 5, 14, 4.3, 'Superlite Aero', '2.0/1.6/2.0'),
(5, 5, 14, 4.3, 'Superlite Flat', '2.0/1.6/2.0'),
(5, 5, 14, 4.3, 'Ultralite Aero', '2.0/1.5/2.0'),
(5, 5, 14, 3.3, 'Hyperlite Aero', '2.0/1.5/1.3/1.5/2.0'),

-- Wheelsmith -----------------------------------------
--  Straight gauge
(6, 0, 14, 6.8, '2.0', '2.0'),
(6, 0, 14, 6.7, 'SS14', '2.0'),
(6, 0, 15, 5.3, 'SS15', '1.8'),
--  Butted
(6, 2, 13, 6.9, 'DH13', '2.3/2.0'),
--  Double butted
(6, 2, 14, 5.7, '2.0DB', '2.0/1.7/2.0'),
(6, 2, 15, 4.6, '1.8DB', '1.8/1.55/2.0'),
(6, 2, 14, 5.4, 'DB14', '2.0/1.7/2.0'),
(6, 2, 15, 4.4, 'DB15', '1.8/1.55/1.8'),
(6, 2, 14, 4.3, 'XL14', '2.0/1.5/2.0'),
(6, 2, 15, 4.00, 'XL15', '1.8/1.5/1.8'),
--  Aero
(6, 5, 15, 4.4, 'AE15', '1.8/2.2-1.2/1.8'),

-- Berd -----------------------------------------------
--  Flexible
(7, 8, 14, 2.4, 'PolyLight', '1.8');

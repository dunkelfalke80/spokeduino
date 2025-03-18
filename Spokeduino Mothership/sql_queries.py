class SQLQueries:
    GET_SETTINGS: str = """
                SELECT
                    key, value
                FROM settings"""

    GET_SINGLE_SETTING: str = """
                SELECT
                    value
                FROM
                    settings
                WHERE
                    key = ?"""

    GET_TENSIOMETERS: str = """
                SELECT
                    id, name
                FROM
                    tensiometers"""

    GET_SPOKE_MANUFACTURERS: str = """
                SELECT
                    id, name
                FROM
                    spoke_manufacturers"""

    GET_SPOKE_TYPES = """
                SELECT
                    id, type
                FROM
                    spoke_types"""

    GET_SPOKES: str = """
                SELECT
                    s.id, s.name, t.type, s.gauge,
                    s.weight, s.dimensions, s.comment
                FROM
                    spoke_models s
                JOIN
                    spoke_types t
                ON
                    s.type_id = t.id"""

    GET_SPOKES_BY_MANUFACTURER: str = \
        GET_SPOKES + " WHERE s.manufacturer_id = ?"

    GET_SPOKES_BY_ID: str = \
        GET_SPOKES + " WHERE s.id = ?"

    GET_MEASUREMENT_SETS: str = """
                SELECT
                    id, comment, strftime('%Y-%m-%d %H:%M', ts) AS ts
                FROM
                    spoke_measurement_sets
                WHERE
                    spoke_id = ? AND tensiometer_id = ?
                ORDER BY
                    id
                ASC"""

    GET_MEASUREMENTS: str = """
                SELECT
                    set_id, tension, deflection
                FROM
                    spoke_measurements
                WHERE
                    set_id IN"""

    GET_MEASUREMENTS_BY_ID: str = """
                SELECT
                    tension, deflection
                FROM
                    spoke_measurements
                WHERE
                    set_id = ?
                ORDER BY
                    tension
                ASC"""

    GET_HUB_MANUFACTURERS: str = """
                SELECT
                    id, name
                FROM
                    hub_manufacturers"""

    GET_HUBS: str = """
                SELECT
                    h.id, h.name, hm.name as manufacturer, a.name as axle_type,
                    h.old, h.pcd_left, h.pcd_right, h.wl, h.wr,
                    h.spoke_hole_diameter_left, h.spoke_hole_diameter_right,
                    b.name as boost_classification, h.is_front,
                    h.is_disc, h.is_centerlock, h.is_jbend, h.comment
                FROM
                    hub_models h
                JOIN hub_manufacturers hm ON h.manufacturer_id = hm.id
                JOIN axle_types a ON h.axle_type_id = a.id
                JOIN boost_classifications b
                ON h.boost_classification_id = b.id"""

    GET_HUBS_BY_MANUFACTURER: str = \
        GET_HUBS + " WHERE s.manufacturer_id = ?"

    GET_HUBS_BY_ID: str = \
        GET_HUBS + " WHERE s.id = ?"

    GET_RIM_MANUFACTURERS: str = """
                SELECT
                    id, name
                FROM
                    rim_manufacturers"""

    GET_RIMS: str = """
                SELECT
                    r.id, r.name, rm.name as manufacturer,
                    r.etrto_bsd, r.etrto_width, r.outer_width, r.erd,
                    r.nipple_offset_left, r.nipple_offset_right,
                    r.rim_depth, r.is_disc, r.comment
                FROM
                    rim_models r
                JOIN rim_manufacturers rm ON r.manufacturer_id = rm.id"""

    GET_RIMS_BY_MANUFACTURER: str = \
        GET_RIMS + " WHERE s.manufacturer_id = ?"

    GET_RIMS_BY_ID: str = \
        GET_RIMS + " WHERE s.id = ?"

    GET_AXLE_TYPES: str = """
                SELECT
                    id, name
                FROM
                    axle_types"""

    GET_BOOST_CLASSIFICATIONS: str = """
                SELECT
                    id, name
                FROM
                    boost_classifications"""

    GET_ETRTO_DESCRIPTIONS: str = """
                SELECT
                    etrto_bsd, name, is_default
                FROM
                    etrto_description"""

    ADD_MEASUREMENT: str = """
                INSERT INTO
                    spoke_measurements (set_id, tension, deflection)
                VALUES
                    (?, ?, ?)"""

    ADD_MEASUREMENT_SET: str = """
                INSERT INTO
                    spoke_measurement_sets (spoke_id, tensiometer_id, comment)
                VALUES
                    (?, ?, ?)"""

    ADD_TENSIOMETER: str = """
                INSERT INTO
                    tensiometers (name)
                VALUES
                    (?)"""

    ADD_SPOKE_MANUFACTURER: str = """
                INSERT INTO
                    spoke_manufacturers (name)
                VALUES
                    (?)"""

    ADD_SPOKE: str = """
                INSERT INTO
                    spoke_models(manufacturer_id, name, type_id,
                    gauge, weight, dimensions, comment)
                VALUES
                    (?, ?, ?, ?, ?, ?, ?)"""

    ADD_HUB_MANUFACTURER: str = """
                INSERT INTO
                    hub_manufacturers (name)
                VALUES
                    (?)"""

    ADD_HUB: str = """
                INSERT INTO hub_models (
                    manufacturer_id, name, axle_type_id, old,
                    pcd_left, pcd_right, wl, wr,
                    spoke_hole_diameter_left, spoke_hole_diameter_right,
                    boost_classification_id, is_front, is_disc,
                    is_centerlock, is_jbend, comment
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""

    ADD_RIM_MANUFACTURER: str = """
                INSERT INTO
                    rim_manufacturers (name)
                VALUES
                    (?)"""

    ADD_RIM: str = """
                INSERT INTO rim_models (
                    manufacturer_id, name, etrto_bsd, etrto_width, outer_width,
                    erd, nipple_offset_left, nipple_offset_right, rim_depth,
                    is_disc, comment
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""

    MODIFY_SPOKE: str = """
                UPDATE
                    spoke_models
                SET
                    name = ?, type_id = ?, gauge = ?,
                    weight = ?, dimensions = ?, comment = ?
                WHERE id = ?"""

    MODIFY_HUB: str = """
                UPDATE hub_models
                SET
                    manufacturer_id = ?, name = ?, axle_type_id = ?, old = ?,
                    pcd_left = ?, pcd_right = ?, wl = ?, wr = ?,
                    spoke_hole_diameter_left = ?,
                    spoke_hole_diameter_right = ?,
                    boost_classification_id = ?, is_front = ?, is_disc = ?,
                    is_centerlock = ?, is_jbend = ?, comment = ?
                WHERE id = ?"""

    MODIFY_RIM: str = """
                UPDATE rim_models
                SET
                    manufacturer_id = ?, name = ?, etrto_bsd = ?,
                    etrto_width = ?, outer_width = ?, erd = ?,
                    nipple_offset_left = ?, nipple_offset_right = ?,
                    rim_depth = ?, is_disc = ?, comment = ?
                WHERE id = ?"""

    DELETE_SPOKE: str = """
                DELETE FROM
                        spoke_models
                    WHERE
                        id = ?"""

    DELETE_HUB: str = """
                DELETE FROM
                        hub_models
                    WHERE
                        id = ?"""

    DELETE_RIM: str = """
                DELETE FROM
                        rim_models
                    WHERE
                        id = ?"""

    DELETE_MEASUREMENT: str = """
                DELETE FROM
                    spoke_measurements
                WHERE
                    id = ?"""

    DELETE_MEASUREMENT_SET: str = """
                DELETE FROM
                    spoke_measurement_sets
                WHERE
                    id = ?"""

    UPSERT_SETTING: str = """
                INSERT INTO
                    settings (key, value)
                VALUES
                    (?, ?)
                ON CONFLICT(key) DO UPDATE SET
                    value=excluded.value"""

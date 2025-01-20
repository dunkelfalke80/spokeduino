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

    GET_MANUFACTURERS: str = """
                SELECT
                    id, name
                FROM
                    manufacturers"""

    GET_TYPES = """
                SELECT
                    id, type
                FROM
                    types"""

    GET_SPOKES: str = """
                SELECT
                    s.id, s.name, t.type, s.gauge,
                    s.weight, s.dimensions, s.comment
                FROM
                    spokes s
                JOIN
                    types t
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
                    measurement_sets
                WHERE
                    spoke_id = ? AND tensiometer_id = ?"""

    GET_MEASUREMENTS: str = """
                SELECT
                    tension, deflection
                FROM
                    measurements
                WHERE
                    set_id IN"""

    ADD_MEASUREMENT: str = """
                INSERT INTO
                    measurements (set_id, tension, deflection)
                VALUES
                    (?, ?, ?)"""

    ADD_TENSIOMETER: str = """
                INSERT INTO
                    tensiometers (name)
                VALUES
                    (?)"""

    ADD_MANUFACTURER: str = """
                INSERT INTO
                    manufacturers (name)
                VALUES
                    (?)"""

    ADD_SPOKE: str = """
                INSERT INTO
                    spokes(manufacturer_id, name, type_id,
                    gauge, weight, dimensions, comment)
                VALUES
                    (?, ?, ?, ?, ?, ?, ?)"""

    MODIFY_SPOKE: str = """
                UPDATE
                    spokes
                SET
                    name = ?, type_id = ?, gauge = ?,
                    weight = ?, dimensions = ?, comment = ?
                WHERE id = ?"""

    DELETE_SPOKE: str = """
                DELETE FROM
                        spokes
                    WHERE
                        id = ?"""

    DELETE_MEASUREMENT: str = """
                DELETE FROM
                    measurements
                WHERE
                    id = ?"""

    UPSERT_SETTING: str = """
                INSERT INTO
                    settings (key, value)
                VALUES
                    (?, ?)
                ON CONFLICT(key) DO UPDATE SET
                    value=excluded.value"""

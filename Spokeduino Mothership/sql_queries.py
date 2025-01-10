class SQLQueries:
    GET_TENSIOMETERS: str = """
                SELECT
                    id, name
                FROM
                    tensioners"""

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
                    s.name, t.type, s.gauge, s.weight,
                    s.dimensions, s.comment, s.id
                FROM
                    spokes s
                JOIN
                    types t
                ON
                    s.type_id = t.id"""

    GET_SPOKES_BY_MANUFACTURER: str = \
        GET_SPOKES + " WHERE s.manufacturer_id = ?"

    GET_SPOKES_BY_ID: str  = \
        GET_SPOKES + " WHERE s.id = ?"

    GET_MEASUREMENTS: str = """
                SELECT
                    tension_300N, tension_400N, tension_500N,
                    tension_600N, tension_700N, tension_800N,
                    tension_900N, tension_1000N, tension_1100N,
                    tension_1200N, tension_1300N, tension_1400N,
                    tension_1500N, id
                FROM
                    measurements
                WHERE
                    spoke_id = ?
                AND
                    tensioner_id = ?"""

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

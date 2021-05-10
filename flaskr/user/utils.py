from database.db import cursor


# Returns true if a id exists
def id_exists(table: str, id_entity: int) -> bool:
    sql = f"SELECT id FROM {table} WHERE id = %s;"
    result = cursor.execute(sql, [id_entity])
    return True if result > 0 else False

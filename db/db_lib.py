import sqlite3

def connection(db_name: str):
    """Maakt een connectie met de database en retourneert de verbinding."""
    return sqlite3.connect(db_name)

def execute_script(db_name: str, sql: str):

    conn = connection(db_name)

    cursor = conn.cursor()
    cursor.executescript(sql)

    conn.commit()
    conn.close()



def query(db_name: str, sql: str, params: tuple = ()):
    """Voert een query uit en retourneert de cursor en databaseverbinding."""
    conn = connection(db_name)
    conn.execute("PRAGMA foreign_keys = ON;")
    cursor = conn.cursor()
    cursor.execute(sql, params)
    return conn, cursor

def fetch_one(db_name: str, sql: str, params: tuple = ()):
    """Haalt één resultaat op uit de database."""
    conn, cursor = query(db_name, sql, params)
    result = cursor.fetchone()
    conn.close()
    return result

def fetch_all(db_name: str, sql: str, params: tuple = ()):
    """Haalt alle resultaten op uit de database."""
    conn, cursor = query(db_name, sql, params)
    results = cursor.fetchall()  # Correcte methode
    conn.close()
    return results

def insert(db_name: str, sql: str, params: tuple = ()) -> int:
    """Voegt een rij toe en retourneert het ID van de nieuwe rij."""
    conn, cursor = query(db_name, sql, params)
    lastId = cursor.lastrowid
    conn.commit()
    conn.close()
    return lastId

def delete(db_name: str, sql: str, params: tuple = ()) -> int:
    """Verwijdert rijen en retourneert het aantal verwijderde rijen."""
    conn, cursor = query(db_name, sql, params)
    rows_deleted = cursor.rowcount  # Aantal verwijderde rijen
    conn.commit()
    conn.close()
    return rows_deleted

def update(db_name: str, sql: str, params: tuple = ()) -> int:
    """Werk één of meer rijen bij en retourneer het aantal gewijzigde rijen."""
    conn, cursor = query(db_name, sql, params)
    rows_updated = cursor.rowcount  # Aantal gewijzigde rijen
    conn.commit()
    conn.close()
    return rows_updated

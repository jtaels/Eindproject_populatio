from dbfread import DBF
import sqlite3

# Verbind met je database
conn = sqlite3.connect("C:\\bevolkingsregister\\bevolkingsregister.db")
cur = conn.cursor()

# Gemeente toevoegen als ze nog niet bestaat
def get_or_create_gemeente(naam, postcode, provincie="onbekend"):
    cur.execute("SELECT id FROM gemeenten WHERE postcode = ?", (postcode,))
    row = cur.fetchone()
    if row:
        return row[0]
    cur.execute(
        "INSERT INTO gemeenten (naam, postcode, provincie) VALUES (?, ?, ?)",
        (naam, postcode, provincie)
    )
    conn.commit()
    return cur.lastrowid

# Adres invoegen
def voeg_adres_toe(record):
    straat = record.get("straatnm", "").strip()
    huisnummer = record.get("huisnr", "").strip()
    busnummer = record.get("busnr", "").strip()
    postcode = record.get("postcode", "").strip()
    gemeente = record.get("gemeentenm", "").strip()

    if not straat or not huisnummer or not postcode or not gemeente:
        print("Onvolledige data, overslaan:", record)
        return

    gemeente_id = get_or_create_gemeente(gemeente, postcode)
    cur.execute(
        """
        INSERT INTO adressen (straatnaam, huisnummer, busnummer, gemeente_id)
        VALUES (?, ?, ?, ?)
        """,
        (straat, huisnummer, busnummer, gemeente_id)
    )
    conn.commit()

# Inlezen van DBF-bestand
table = DBF('datasets/Adres.dbf', encoding='latin1')  # 'cp1252' indien nodig
for record in table:
    voeg_adres_toe(record)

print("Import afgerond.")

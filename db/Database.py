import db.db_lib as db_lib

class Database:

    def __init__(self,dbName:str):

        self._dbName = dbName

    def _createGemeenteSQL(self) -> str:
        
        return '''

            CREATE TABLE IF NOT EXISTS "gemeenten" (
                "id"	INTEGER NOT NULL,
                "naam"	TEXT NOT NULL,
                "postcode"	TEXT UNIQUE,
                "provincie"	TEXT NOT NULL,
                PRIMARY KEY("id" AUTOINCREMENT)
            );

        '''

    def _createAdressenSQL(self) -> str:

        return '''
        
            CREATE TABLE IF NOT EXISTS "adressen" (
                "id" INTEGER NOT NULL,
                "straatnaam" TEXT NOT NULL,
                "huisnummer" TEXT,
                "busnummer" TEXT,
                "gemeente_id" INT NOT NULL,
                PRIMARY KEY("id" AUTOINCREMENT),
                FOREIGN KEY("gemeente_id") REFERENCES "gemeenten"("id") ON DELETE RESTRICT
            );
        
        '''

    def _createPersonenSQL(self) -> str:

        return '''

            CREATE TABLE IF NOT EXISTS "personen" (
                "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                "voornaam" TEXT NOT NULL,
                "achternaam" TEXT,
                "geboortedatum" DATE,
                "geboorteplaats_id" INTEGER,
                "overlijdensdatum" DATE,
                "overlijdensplaats_id" INTEGER,
                "overlijdensoorzaak" TEXT,
                "bevolkingsregisternummer" TEXT UNIQUE,
                FOREIGN KEY("geboorteplaats_id") REFERENCES "gemeenten"("id") ON DELETE RESTRICT,
                FOREIGN KEY("overlijdensplaats_id") REFERENCES "gemeenten"("id") ON DELETE RESTRICT
            );
        '''

    def _createPersoonRelatieSQL(self) -> str:

        return '''
        
            CREATE TABLE IF NOT EXISTS "persoonRelaties" (
                "id" INTEGER PRIMARY KEY AUTOINCREMENT,
                "persoon_id_1" INTEGER NOT NULL,
                "persoon_id_2" INTEGER NOT NULL,
                "relatie_type" TEXT NOT NULL, -- Relatie type bv vader, moeder, partner, gescheiden
                FOREIGN KEY("persoon_id_1") REFERENCES "personen"("id") ON DELETE CASCADE,
                FOREIGN KEY("persoon_id_2") REFERENCES "personen"("id") ON DELETE CASCADE
            );
                    
        '''

    def _createPersoonAdresSQL(self) -> str:

        return '''

            CREATE TABLE IF NOT EXISTS "persoonAdressen" (
                "id" INTEGER PRIMARY KEY AUTOINCREMENT,
                "persoon_id" INTEGER NOT NULL,
                "adres_id" INTEGER NOT NULL,
                "adres_type" TEXT NOT NULL, -- hoofdverblijf, tweedeverblijf
                "van" DATE,
                "tot" DATE,
                FOREIGN KEY("persoon_id") REFERENCES "personen"("id") ON DELETE CASCADE,
                FOREIGN KEY("adres_id") REFERENCES "adressen"("id") ON DELETE RESTRICT
            );

        '''

    def _createUsersSQL(self):

        return '''
        
            CREATE TABLE IF NOT EXISTS "users" (
                "id" INTEGER PRIMARY KEY AUTOINCREMENT, -- Unieke ID voor elke gebruiker
                "gebruikersnaam" TEXT NOT NULL UNIQUE,  -- Gebruikersnaam (moet uniek zijn)
                "wachtwoord" TEXT NOT NULL,            -- Wachtwoord van de gebruiker (kan gehasht worden)
                "rol" INTEGER NOT NULL,                   -- De rol van de gebruiker (bijv. admin, medewerker)
                "twee_fa_secret" TEXT,                 -- Secret voor 2FA (bijv. TOTP, Authenticator-app)
                "twee_fa_enabled" BOOLEAN DEFAULT 0,   -- Boolean om aan te geven of 2FA is ingeschakeld (0 = niet ingeschakeld, 1 = ingeschakeld)
                "laatst_ingelogd" TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Tijdstip van laatste login
                "aangemaakt" TIMESTAMP DEFAULT CURRENT_TIMESTAMP      -- Tijdstip van aanmaken van de gebruiker
            );
                    
        '''

    def _generateTables(self):

        return (self._createGemeenteSQL() +
               self._createAdressenSQL() +
               self._createPersonenSQL() +
               self._createPersoonRelatieSQL() +
               self._createPersoonAdresSQL() +
               self._createUsersSQL())

    def connection(self):

        db_lib.execute_script(self._dbName,self._generateTables())

        return self

    def execute_script(self, sql: str):
        return db_lib.execute_script(self._dbName,sql)

    def query(self, sql: str, params: tuple = ()):
        return db_lib.query(self._dbName, sql,params)

    def fetch_one(self, sql: str, params: tuple = ()):
        return db_lib.fetch_one(self._dbName, sql, params)

    def fetch_all(self, sql: str, params: tuple = ()):
        return db_lib.fetch_all(self._dbName, sql, params)

    def insert(self, sql: str, params: tuple = ()) -> int:
        return db_lib.insert(self._dbName, sql, params)

    def delete(self,sql: str, params: tuple = ()) -> int:
        return db_lib.delete(self._dbName, sql, params)

    def update(self,sql: str, params: tuple = ()) -> int:
        return db_lib.update(self._dbName, sql, params)
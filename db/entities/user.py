class User:

    def __init__(self, id, gebruikersnaam, wachtwoord, rol, twee_fa_secret, twee_fa_enabled, laatst_ingelogd, aangemaakt):
        self.id = id
        self.gebruikersnaam = gebruikersnaam
        self.wachtwoord = wachtwoord
        self.rol = rol
        self.twee_fa_secret = twee_fa_secret
        self.twee_fa_enabled = twee_fa_enabled
        self.laatst_ingelogd = laatst_ingelogd
        self.aangemaakt = aangemaakt
from faker import Faker
import random
from datetime import datetime

faker = Faker('nl_BE')  # Belgische data

def generate_rijksregisternummer(geboortedatum: datetime):
    # Rijksregisternummer format: YYMMDDXXXCC
    geboorte_str = geboortedatum.strftime('%y%m%d')
    volgnummer = random.randint(1, 997)
    volgnummer_str = f'{volgnummer:03d}'

    # Controlegetal berekenen
    base = f'{geboorte_str}{volgnummer_str}'
    # Voeg 2 voor 2000 toe
    if geboortedatum.year >= 2000:
        controlegetal = 97 - (int('2' + base) % 97)
    else:
        controlegetal = 97 - (int(base) % 97)

    return f'{geboorte_str}-{volgnummer_str}-{controlegetal:02d}'

# 👇 Genereer 10 nep-personen
for _ in range(100):
    voornaam = faker.first_name()
    achternaam = faker.last_name()
    geboortedatum = faker.date_of_birth(minimum_age=18, maximum_age=95)
    geboorteplaats_id = random.randint(1, 50)  # Aantal gemeenten in jouw db?
    overlijdensdatum = None if random.random() > 0.3 else faker.date_between(start_date=geboortedatum)
    overlijdensplaats_id = geboorteplaats_id if overlijdensdatum else None
    overlijdensoorzaak = None
    rijksregisternummer = generate_rijksregisternummer(geboortedatum)

    print(f"('{voornaam}', '{achternaam}', '{geboortedatum}', {geboorteplaats_id}, "
          f"{repr(overlijdensdatum)}, {overlijdensplaats_id}, '{overlijdensoorzaak}', '{rijksregisternummer}'),")

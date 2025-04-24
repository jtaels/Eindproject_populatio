from fpdf import FPDF
from datetime import datetime

class AdresHistoriekPdfGenerator:
    def __init__(self, persoon_naam: str):
        self.persoon_naam = persoon_naam
        self.addresses = []

    def add_address(self, adres: dict):
        self.addresses.append(adres)

    def set_addresses(self, adressen: list):
        self.addresses.extend(adressen)

    def sorteer_op_van(self,adressen):
        def parse_datum_safe(datum):
            if not datum:
                return datetime.min  # Sorteert lege datums helemaal vooraan
            try:
                return datetime.strptime(datum, "%d-%m-%Y")
            except ValueError:
                return datetime.min

        return sorted(adressen, key=lambda a: parse_datum_safe(getattr(a, "van", None)))

    def generate(self, output_path: str = "adres_historiek.pdf"):
        pdf = FPDF(orientation="L", unit="mm", format="A4")  # Liggend A4
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.cell(0, 10, txt=f"Adres Historiek van {self.persoon_naam}", ln=True, align='C')
        pdf.ln(10)

        # Kolomtitels
        pdf.set_font("Arial", "B", 10)
        headers = ["Van - Tot", "Type", "Straatnaam", "Nr", "Bus", "Gemeente", "Provincie"]
        col_widths = [50, 40, 50, 15, 15, 45, 45]

        for i, header in enumerate(headers):
            pdf.cell(col_widths[i], 10, header, border=1)
        pdf.ln()

        # Adresgegevens
        pdf.set_font("Arial", "", 10)

        sorted_addresses = self.sorteer_op_van(self.addresses)

        for address in sorted_addresses:
            row = [
                f"{getattr(address, 'van', '') or ''} - {getattr(address, 'tot', '') or ''}",
                getattr(address, "adres_type", "") or "",
                getattr(address.adres, "straatnaam", "") if address.adres else "",
                getattr(address.adres, "huisnummer", "") if address.adres else "",
                getattr(address.adres, "busnummer", "") if address.adres else "",
                getattr(address.adres.gemeente, "naam", "") if address.adres and address.adres.gemeente else "",
                getattr(address.adres.gemeente, "provincie", "") if address.adres and address.adres.gemeente else "",
            ]

            for i, col in enumerate(row):
                pdf.cell(col_widths[i], 10, str(col), border=1)
            pdf.ln()

        pdf.output(output_path)

from datetime import datetime

def error_array_to_str(errors) -> str:

    error_str = ""

    for error in errors:
        error_str += error + "\n"

    return error_str


def parse_date(date_str):
    """Zet een datumstring om naar een datetime-object als deze niet leeg is."""
    return datetime.strptime(date_str, "%Y-%m-%d") if date_str else None


def format_date_for_system(date_obj):
    """Formatteer een datetime object naar het gewenste formaat (d-m-Y)."""
    return date_obj.strftime("%d-%m-%Y") if date_obj else None
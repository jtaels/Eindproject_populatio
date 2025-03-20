def error_array_to_str(errors) -> str:

    error_str = ""

    for error in errors:
        error_str += error + "\n"

    return error_str
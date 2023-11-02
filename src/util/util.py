def parse_bool(string: str) -> bool:
    if string.lower() == "true":
        return True
    elif string.lower() == "false":
        return False
    else:
        raise ValueError(f"Cannot parse {string} to boolean")
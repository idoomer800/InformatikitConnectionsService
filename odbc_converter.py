import configparser
import json
from pathlib import Path


def odbc_to_dict(file_path: str) -> dict:
    """
    Parse an ODBC .dsn / .ini file into a nested dictionary.

    Args:
        file_path: Path to the ODBC file.

    Returns:
        dict  {section_name: {key: value, ...}, ...}

    Raises:
        FileNotFoundError: if the file does not exist.
        ValueError: if the file cannot be parsed.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"ODBC file not found: {file_path}")

    parser = configparser.ConfigParser()
    # Preserve original key casing (configparser lower-cases by default)
    parser.optionxform = str

    try:
        parser.read(path, encoding="utf-8")
    except configparser.Error as exc:
        raise ValueError(f"Failed to parse ODBC file: {exc}") from exc

    result = {}
    for section in parser.sections():
        result[section] = dict(parser[section])

    return result


def dict_to_odbc(data: dict, file_path: str) -> None:
    """
    Write a nested dictionary to an ODBC .dsn / .ini file.

    Args:
        data:      {section_name: {key: value, ...}, ...}
        file_path: Destination path for the ODBC file.

    Raises:
        TypeError: if `data` is not a dict of dicts.
    """
    if not isinstance(data, dict):
        raise TypeError("data must be a dictionary")

    parser = configparser.ConfigParser()
    parser.optionxform = str  # Keep original casing

    for section, values in data.items():
        if not isinstance(values, dict):
            raise TypeError(
                f"Section '{section}' must map to a dict, got {type(values).__name__}"
            )
        parser[section] = values

    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as fh:
        parser.write(fh)

    print(f"ODBC file written to: {path}")


if __name__ == "__main__":
    SOURCE_FILE = "example.ini"
    OUTPUT_FILE = "output.ini"

    # --- ODBC file → dict ---
    print("=" * 50)
    print("Reading ODBC file:", SOURCE_FILE)
    print("=" * 50)

    odbc_dict = odbc_to_dict(SOURCE_FILE)

    print(json.dumps(odbc_dict, indent=2))

    # --- dict → ODBC file ---
    print()
    print("=" * 50)
    print("Writing dictionary back to:", OUTPUT_FILE)
    print("=" * 50)

    dict_to_odbc(odbc_dict, OUTPUT_FILE)

    # Verify round-trip
    reloaded = odbc_to_dict(OUTPUT_FILE)
    assert reloaded == odbc_dict, "Round-trip mismatch!"
    print("Round-trip verification passed.")
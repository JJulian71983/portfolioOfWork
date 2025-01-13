from pathlib import Path
from os import listdir
from typing import Any, Dict
from yaml import safe_load
from utils.helper_utils import get_driver_list
from constants import PROPERTIES_DIRECTORY_PATH, ACCEPTED_EXTRACT_FREQUENCY_VALUES, ACCEPTED_EXTRACT_TYPE_VALUES, ACCEPTED_INCREMENTAL_TYPES


def validate_string_value(
        value: Any,
        value_name: str,
        filename: str,
        all_empty: bool = False
        ) -> None:
    if not isinstance(value, str):
        raise TypeError(f"{value_name} value must be a string in file {filename}.")
    if not all_empty and value in ["", None]:
        raise ValueError(f"{value_name} is missing in file {filename}.")


def validate_list_value(
        value: Any,
        value_name: str,
        filename: str,
        ) -> None:
    if not isinstance(value, list):
        raise TypeError(f"{value_name} value must be an array in file {filename}.")
    if not value:
        raise ValueError(f"{value_name} is missing in file {filename}.")


def validate_accepted_value(
        value: Any,
        value_name: str,
        filename: str
        ) -> None:
    if value_name.lower() == "database_type":
        if value.lower() not in get_driver_list():
            raise ValueError(f"{value_name} is not supported in file {filename}.")
    if value_name.lower() == "extract_frequency":
        if value.lower() not in ACCEPTED_EXTRACT_FREQUENCY_VALUES:
            raise ValueError(f"{value_name} is not supported in file {filename}.")
    if value_name.lower() == "extract_type":
        if value.lower() not in ACCEPTED_EXTRACT_TYPE_VALUES:
            raise ValueError(f"{value_name} is not supported in file {filename}.")
    if value_name.lower() == "incremental_type":
        if value.lower() not in ACCEPTED_INCREMENTAL_TYPES:
            raise ValueError(f"{value_name} is not supported in file {filename}.")


def validate_single_property_file(filepath: Path) -> None:
    with open(filepath, "r") as file:
        parsed_file = safe_load(file)
    filename = filepath.name
    # Validate database_type
    validate_string_value(parsed_file["database_type"], "Database_type", filename)
    validate_accepted_value(parsed_file["database_type"], "Database_type", filename)
    # Validate database_name
    validate_string_value(parsed_file["database_name"], "Database_name", filename)
    # Validate username
    validate_string_value(parsed_file["username"], "Username", filename)
    # Validate password
    validate_string_value(parsed_file["password"], "Password", filename)
    # Validate host
    validate_string_value(parsed_file["host"], "Host", filename)
    # Validate schemas
    validate_list_value(parsed_file["schemas"], "Schema", filename)
    for schema in parsed_file["schemas"]:
        validate_string_value(schema["name"], "Schema_name", filename)
        for table in schema["tables"]:
            # Validate table name
            validate_string_value(table["name"], "Table_name", filename)
            # Validate extract_frequency
            validate_string_value(table["extract_frequency"], "Extract_frequency", filename)
            validate_accepted_value(table["extract_frequency"], "Extract_frequency", filename)
            # Validate extract_type
            validate_string_value(table["extract_type"], "Extract_type", filename)
            validate_accepted_value(table["extract_type"], "Extract_type", filename)
            # Validate incremental_type
            if table["extract_type"] == "incremental":
                validate_accepted_value(table["incremental_type"], "Incremental_type", filename)


def check_property_files() -> str:
    properties_dir = Path(PROPERTIES_DIRECTORY_PATH)
    for entry in listdir(properties_dir):
        full_path = properties_dir / entry
        if not full_path.is_file():
            continue
        validate_single_property_file(full_path)
    return "All property files passed validation successfully."


if __name__ == "__main__":
    print(check_property_files())
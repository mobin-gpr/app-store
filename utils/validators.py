"""
Custom validators and validation utilities.

This module provides reusable validation functions for data validation
across the application.
"""

import json
from typing import Any, Dict, Optional
from django.core.exceptions import ValidationError
from django.http import HttpRequest


def validate_json_request(request: HttpRequest, required_fields: Optional[list] = None) -> Dict[str, Any]:
    """
    Validate and parse JSON request body.

    Args:
        request: Django HttpRequest object
        required_fields: List of required field names

    Returns:
        Parsed JSON data as dictionary

    Raises:
        ValidationError: If JSON is invalid or required fields are missing
    """
    if request.method != "POST":
        raise ValidationError("Only POST requests are allowed")

    try:
        data = json.loads(request.body.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        raise ValidationError("Invalid JSON data")

    if required_fields:
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            raise ValidationError(f"Missing required fields: {', '.join(missing_fields)}")

    return data


def validate_positive_integer(value: Any, field_name: str = "value") -> int:
    """
    Validate and convert value to positive integer.

    Args:
        value: Value to validate
        field_name: Name of the field (for error messages)

    Returns:
        Validated integer value

    Raises:
        ValidationError: If value is not a valid positive integer
    """
    try:
        int_value = int(value)
        if int_value <= 0:
            raise ValidationError(f"{field_name} must be a positive integer")
        return int_value
    except (ValueError, TypeError):
        raise ValidationError(f"{field_name} must be a valid integer")


def validate_choice(value: str, choices: list, field_name: str = "value") -> str:
    """
    Validate value against a list of choices.

    Args:
        value: Value to validate
        choices: List of valid choices
        field_name: Name of the field (for error messages)

    Returns:
        Validated value

    Raises:
        ValidationError: If value is not in choices
    """
    if value not in choices:
        raise ValidationError(f"{field_name} must be one of: {', '.join(choices)}")
    return value

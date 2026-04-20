# File: os_layer/schemas/command_schema.py

# ==============================
# Allowed Values
# ==============================

ALLOWED_EXECUTION_TYPES = [
    "filesystem",
    "application",
    "shell",
    "web",
    "system"
]

ALLOWED_RISK_LEVELS = [
    "low",
    "medium",
    "high"
]


# ==============================
# Intent Validation
# ==============================

def normalize_intent(intent):
    if not isinstance(intent, str):
        raise ValueError("Intent must be a string")

    intent = intent.strip().lower()

    if len(intent) < 2 or len(intent) > 100:
        raise ValueError("Intent length must be between 2 and 100")

    return intent


# ==============================
# Parameters Validation
# ==============================

def validate_parameters(parameters):
    if parameters is None:
        return {}

    if not isinstance(parameters, dict):
        raise ValueError("Parameters must be a dictionary")

    return parameters


# ==============================
# Main Command Validator
# ==============================

def validate_os_command(command):
    """
    Validates and normalizes an OS command dictionary.
    This is the ONLY format allowed to reach execution layer.
    """

    if not isinstance(command, dict):
        raise ValueError("Command must be a dictionary")

    # Block unexpected fields (same as pydantic extra="forbid")
    allowed_fields = {
        "intent",
        "parameters",
        "execution_type",
        "risk_level"
    }

    for field in command.keys():
        if field not in allowed_fields:
            raise ValueError(f"Unexpected field: {field}")

    # Validate intent
    intent = normalize_intent(command.get("intent"))

    # Validate parameters
    parameters = validate_parameters(command.get("parameters", {}))

    # Validate execution type
    execution_type = command.get("execution_type")
    if execution_type not in ALLOWED_EXECUTION_TYPES:
        raise ValueError("Invalid execution_type")

    # Validate risk level
    risk_level = command.get("risk_level")
    if risk_level not in ALLOWED_RISK_LEVELS:
        raise ValueError("Invalid risk_level")

    # Return validated command
    return {
        "intent": intent,
        "parameters": parameters,
        "execution_type": execution_type,
        "risk_level": risk_level
    }
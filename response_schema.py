# File: os_layer/schemas/response_schema.py

# ==============================
# Allowed Status Values
# ==============================

ALLOWED_STATUS = [
    "success",
    "failed"
]


# ==============================
# Response Builder
# ==============================

def create_os_response(
    status,
    output=None,
    error=None,
    command_id=None,
    execution_time=None
):
    """
    Creates and validates an OS response dictionary.
    """

    if status not in ALLOWED_STATUS:
        raise ValueError("Status must be 'success' or 'failed'")

    if error is not None and not isinstance(error, str):
        raise ValueError("Error must be a string")

    if execution_time is not None and not isinstance(execution_time, (int, float)):
        raise ValueError("Execution time must be numeric")

    response = {
        "status": status,
        "output": output,
        "error": error,
        "command_id": command_id,
        "execution_time": execution_time
    }

    return response
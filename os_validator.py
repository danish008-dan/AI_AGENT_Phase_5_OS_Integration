# File: os_layer/os_validator.py

# ==============================
# Allowed Execution Types
# ==============================
ALLOWED_EXECUTION_TYPES = [
    "filesystem",
    "shell",
    "application",
    "web",
    "system"
]

# ==============================
# Blocked Shell Patterns
# ==============================
BLOCKED_SHELL_PATTERNS = [
    "rm -rf",
    "format",
    "mkfs",
    "shutdown",
    "del /f"
]


# ==============================
# Validate OS Command
# ==============================
def validate_os_command(command: dict) -> bool:
    """
    Validates a structured OS command dictionary for safety.

    Args:
        command (dict): Command dictionary with 'execution_type' and 'parameters'.

    Returns:
        bool: True if validation passes.

    Raises:
        ValueError: If execution type is invalid or dangerous shell command detected.
    """

    execution_type = command.get("execution_type")
    if execution_type not in ALLOWED_EXECUTION_TYPES:
        raise ValueError(f"Invalid execution type: {execution_type}")

    # -----------------------------
    # Shell Command Safety Check
    # -----------------------------
    if execution_type == "shell":
        cmd = command.get("parameters", {}).get("command", "")
        for pattern in BLOCKED_SHELL_PATTERNS:
            if pattern.lower() in cmd.lower():
                raise ValueError(f"Dangerous shell command detected: {pattern}")

    return True
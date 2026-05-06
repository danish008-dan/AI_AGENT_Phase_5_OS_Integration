# File: os_layer/security/risk_assessor.py

# ==============================
# Risk Assessment
# ==============================

def requires_confirmation(command):
    """
    Determines if a command requires user confirmation based on risk level.

    Args:
        command (dict): The validated OS command dictionary.

    Returns:
        bool: True if risk_level is 'high', False otherwise.
    """

    # Ensure 'risk_level' key exists
    risk_level = command.get("risk_level")
    if risk_level is None:
        return False

    return risk_level.lower() == "high"
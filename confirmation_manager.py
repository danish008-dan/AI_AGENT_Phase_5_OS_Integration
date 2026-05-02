# os_layer/security/confirmation_manager.py

import uuid
import time

PENDING_CONFIRMATIONS = {}

def create_confirmation(command):
    token = str(uuid.uuid4())

    PENDING_CONFIRMATIONS[token] = {
        "command": command,
        "timestamp": time.time()
    }

    return token

def validate_confirmation(token):
    return PENDING_CONFIRMATIONS.pop(token, None)
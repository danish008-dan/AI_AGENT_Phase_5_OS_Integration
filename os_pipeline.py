# os_layer/os_pipeline.py

import uuid
import time

from ai.groq_translator import translate_to_structured_command
from os_router import route
from os_layer.schemas.command_schema import validate_os_command
from security.risk_assessor import requires_confirmation
from security.confirmation_manager import create_confirmation
from os_logger import log_command
from os_history import add_history

def process_command(natural_text):

    start = time.time()

    structured = translate_to_structured_command(natural_text)
    command = validate_os_command(structured)

    if requires_confirmation(command):
        token = create_confirmation(command)
        return {
            "status": "confirmation_required",
            "confirmation_token": token
        }

    result = route(command)

    execution_time = time.time() - start
    command_id = str(uuid.uuid4())

    result.update({
        "command_id": command_id,
        "execution_time": execution_time
    })

    log_command(command, result)
    add_history(result)

    return result
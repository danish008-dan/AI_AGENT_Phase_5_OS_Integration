# os_layer/os+logger.py

import logging
import json
import uuid
from datetime import datetime

logging.basicConfig(
    filename="os_audit.log",
    level=logging.INFO,
    format="%(message)s"
)

def log_command(command, response):

    entry = {
        "id": str(uuid.uuid4()),
        "timestamp": datetime.utcnow().isoformat(),
        "command": command,
        "response": response
    }

    logging.info(json.dumps(entry))
    return entry["id"]
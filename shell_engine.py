# os_layer/execution/shell_engine.py

import subprocess
from os_layer.schemas.response_schema import create_os_response

ALLOWED_COMMANDS = [
    "dir",
    "echo",
    "ipconfig"
]

def handle_shell(command):

    params = command["parameters"]
    cmd = params.get("command")

    if cmd not in ALLOWED_COMMANDS:
        return create_os_response(
            status="failed",
            error="Shell command not allowed"
        )

    elif command["intent"] == "list_directory":
        result = subprocess.run(
            "dir",
            shell=True,
            capture_output=True,
            text=True
        )
        return create_os_response(
            status="success",
            output=result.stdout[:2000]
        )

    try:
        result = subprocess.run(
            ALLOWED_COMMANDS[cmd],
            capture_output=True,
            text=True,
            timeout=10,
            shell=False
        )

        return create_os_response(
            status="success",
            output=result.stdout.strip()
        )

    except Exception as e:
        return create_os_response(
            status="failed",
            error=str(e)
        )
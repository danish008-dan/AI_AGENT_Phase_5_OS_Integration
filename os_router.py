# os_layer/os_route.py

from execution.filesystem_engine import handle_filesystem
from execution.application_engine import handle_application
from execution.shell_engine import handle_shell
from execution.system_engine import handle_system
from execution.web_engine import handle_web

ROUTER = {
    "filesystem": handle_filesystem,
    "application": handle_application,
    "shell": handle_shell,
    "system": handle_system,
    "web": handle_web
}

def route(command):
    handler = ROUTER.get(command.execution_type)
    if not handler:
        raise ValueError("Unsupported execution type")
    return handler(command)
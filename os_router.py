import time
from os_layer.schemas.command_schema import validate_os_command
from os_layer.schemas.response_schema import create_os_response
from os_layer.security.risk_assessor import requires_confirmation
from os_layer.execution.application_engine import handle_application
from os_layer.execution.filesystem_engine import handle_filesystem
from os_layer.execution.shell_engine import handle_shell
from os_layer.execution.system_engine import handle_system
from os_layer.execution.web_engine import handle_web


def route(raw_command):

    start_time = time.time()

    try:
        command = validate_os_command(raw_command)
    except Exception as e:
        return create_os_response(
            status="failed",
            error=f"Validation failed: {str(e)}"
        )

    if requires_confirmation(command):
        return create_os_response(
            status="failed",
            error="High-risk command requires confirmation"
        )

    execution_type = command.get("execution_type")

    try:

        if execution_type == "application":
            response = handle_application(command)

        elif execution_type == "web":
            response = handle_web(command)

        elif execution_type == "filesystem":
            response = handle_filesystem(command)

        elif execution_type == "system":
            response = handle_system(command)

        elif execution_type == "shell":
            response = handle_shell(command)

        else:
            response = create_os_response(
                status="failed",
                error="Unsupported execution type"
            )

    except Exception as e:
        response = create_os_response(
            status="failed",
            error=f"OS PIPELINE ERROR: {str(e)}"
        )

    execution_time = time.time() - start_time
    response["execution_time"] = round(execution_time, 4)

    return response
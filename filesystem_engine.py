import os
from os_layer.schemas.response_schema import create_os_response

def handle_filesystem(command):

    intent = command.get("intent")
    params = command.get("parameters", {})

    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

    if intent == "create_folder":

        folder_name = params.get("folder_name")

        if not folder_name or folder_name == "<default>":
            return create_os_response(
                status="failed",
                error="Folder name not specified"
            )

        safe_folder = folder_name.strip()

        try:
            full_path = os.path.join(desktop_path, safe_folder)
            os.makedirs(full_path, exist_ok=True)

            return create_os_response(
                status="success",
                output=f"Folder '{safe_folder}' created"
            )

        except Exception as e:
            return create_os_response(
                status="failed",
                error=str(e)
            )

    elif command["intent"] == "list_files":
        files = os.listdir()
        return create_os_response(
            status="success",
            output=str(files)
        )

    return create_os_response(
        status="failed",
        error="Unsupported filesystem intent"
    )
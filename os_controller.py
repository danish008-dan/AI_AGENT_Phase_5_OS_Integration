# os_layer/os_controller.py

from fastapi import APIRouter, Depends, WebSocket
from fastapi.security import HTTPBearer

from os_layer.security.confirmation_manager import validate_confirmation
from os_layer.security.jwt_manager import decode_token

from os_layer.core.os_pipeline import process_command
from os_layer.core.os_router import route

from os_layer.websocket.log_stream import connect
from os_layer.security.confirmation_manager import validate_confirmation

from os_layer.os_voice_loop import activate_os_mode, deactivate_os_mode, get_os_mode_status



router = APIRouter()

@router.post("/os/command")
def execute_os_command(payload: dict):

    try:

        user_text = payload.get("command") or payload.get("message") or payload.get("text")

        if not user_text:
            return {
                "status": "failed",
                "error": "No command provided"
            }

        result = process_command(user_text)

        # Defensive validation
        if not isinstance(result, dict):
            return {
                "status": "failed",
                "error": "Invalid pipeline response"
            }

        if "status" not in result:
            return {
                "status": "failed",
                "error": "Malformed pipeline response"
            }

        return result

    except Exception as e:

        return {
            "status": "failed",
            "error": str(e)
        }


@router.post("/os/confirm/{confirmation_token}")
def confirm_command(confirmation_token: str):

    data = validate_confirmation(confirmation_token)

    if not data:
        return {"status": "failed", "error": "Invalid or expired token"}

    result = route(data["command"])
    return result


@router.websocket("/ws/logs")
async def websocket_logs(websocket: WebSocket):
    await connect(websocket)

@router.get("/os/start")
def start_os_mode():

    activate_os_mode()

    return {
        "status": "success",
        "message": "OS mode activated"

    }

@router.get("/os/stop")
def stop_os_mode():

    deactivate_os_mode()

    return {
        "status": "success",
        "message": "OS mode deactivated"
    }
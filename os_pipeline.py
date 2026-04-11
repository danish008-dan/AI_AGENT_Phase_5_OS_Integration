# os_layer/core/os_pipeline

import time
from os_layer.ai.groq_translator import translate_to_structured_command
from os_layer.schemas.command_schema import validate_os_command
from os_layer.schemas.response_schema import create_os_response
from os_layer.security.risk_assessor import requires_confirmation
from os_layer.security.confirmation_manager import create_confirmation
from os_layer.core.os_router import route


def process_command(user_text):


    if user_text.lower().strip() in [
        "operating system mode activated",
        "operating system mode deactivated"
    ]:
        return {
            "status": "success",
            "output": "system message ignored"
        }

    start = time.time()

    try:

        print("USER COMMAND:", user_text)

        # Step 1 AI translate
        raw_command = translate_to_structured_command(user_text)

        print("AI TRANSLATED COMMAND:", raw_command)

        # Step 2 validate schema
        command = validate_os_command(raw_command)

        print("VALIDATED COMMAND:", command)

        # Step 3 risk check
        if requires_confirmation(command):

            token = create_confirmation(command)

            return create_os_response(
                status="failed",
                error="confirmation_required",
                command_id=token
            )

        print("ROUTING COMMAND")

        # Step 4 execute
        result = route(command)

        print("EXECUTION RESULT:", result)

        end = time.time()

        return create_os_response(
            status=result["status"],
            output=result.get("output"),
            error=result.get("error"),
            execution_time=end-start
        )

    except Exception as e:

        print("OS PIPELINE ERROR:", str(e))

        return create_os_response(
            status="failed",
            error=str(e)
        )

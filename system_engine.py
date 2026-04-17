# os_layer/execution/system_engine.py

"""
System Engine
-------------
This module is responsible for executing low-level system operations
based on intents received from the OS command router.

Supported Intents:
- get_system_info
- open_application
- run_command
- get_cpu_usage
- get_user_info
"""

import platform
import psutil
import subprocess
import getpass


def handle_system(command: dict) -> dict:
    """
    Main system execution handler.

    Parameters
    ----------
    command : dict
        Parsed command from OS intent router.
        Expected structure:
        {
            "intent": "intent_name",
            "parameters": { ... }
        }

    Returns
    -------
    dict
        Standard OS response format:
        {
            "status": "success" | "failed",
            "output": result data OR message,
            "error": error message (if failed)
        }
    """

    intent = command.get("intent")
    params = command.get("parameters", {})

    try:

        # ==========================================================
        # SYSTEM INFORMATION
        # Returns OS name, version, CPU usage, and memory usage
        # ==========================================================
        if intent == "get_system_info":

            return {
                "status": "success",
                "output": {
                    "os": platform.system(),
                    "version": platform.version(),
                    "cpu_usage": psutil.cpu_percent(),
                    "memory_usage": psutil.virtual_memory().percent
                }
            }

        # ==========================================================
        # GET CPU USAGE
        # Returns current CPU utilization percentage
        # ==========================================================
        elif intent == "get_cpu_usage":

            cpu = psutil.cpu_percent(interval=1)

            return {
                "status": "success",
                "output": f"CPU usage is {cpu}%"
            }

        # ==========================================================
        # GET CURRENT USER INFO
        # Returns active system username
        # ==========================================================
        elif intent == "get_user_info":

            user = getpass.getuser()

            return {
                "status": "success",
                "output": f"Current user is {user}"
            }

        # ==========================================================
        # OPEN APPLICATION
        # Launches an application using subprocess
        # ==========================================================
        elif intent == "open_application":

            app = params.get("application")

            if not app:
                return {
                    "status": "failed",
                    "error": "No application specified"
                }

            subprocess.Popen(app)

            return {
                "status": "success",
                "output": f"Opened application: {app}"
            }

        # ==========================================================
        # RUN SHELL COMMAND
        # Executes raw OS command
        # ==========================================================
        elif intent == "run_command":

            cmd = params.get("command")

            if not cmd:
                return {
                    "status": "failed",
                    "error": "No command specified"
                }

            subprocess.Popen(cmd, shell=True)

            return {
                "status": "success",
                "output": f"Executed command: {cmd}"
            }

        elif intent == "shutdown_system":

            try:
                subprocess.Popen("shutdown /s /t 5", shell=True)

                return {
                    "status": "success",
                    "output": "System shutting down in 5 seconds"
                }

            except Exception as e:
                return {
                    "status": "failed",
                    "error": str(e)
                }

        # ==========================================================
        # UNSUPPORTED INTENT
        # ==========================================================
        else:
            return {
                "status": "failed",
                "error": f"Unsupported system intent: {intent}"
            }

    # ==============================================================
    # GLOBAL ERROR HANDLER
    # ==============================================================
    except Exception as e:

        return {
            "status": "failed",
            "error": str(e)
        }
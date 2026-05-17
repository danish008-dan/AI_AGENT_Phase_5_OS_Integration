"""
File: os_layer/os_voice_loop.py

Refactored OS Mode State Controller
------------------------------------

IMPORTANT:
Backend no longer controls microphone or runs infinite voice loops.

OS Mode is now controlled by frontend browser voice recognition.
Backend is responsible ONLY for:

1. Maintaining OS mode state
2. Executing validated OS commands
3. Providing OS status

This prevents server-side microphone conflicts
and ensures web-architecture correctness.
"""

# Global OS mode state flag
os_mode_active = False


def activate_os_mode():
    """
    Activates OS mode.
    Called from /os/start endpoint.
    """
    global os_mode_active
    os_mode_active = True


def deactivate_os_mode():
    """
    Deactivates OS mode.
    Called from /os/stop endpoint.
    """
    global os_mode_active
    os_mode_active = False


def get_os_mode_status():
    """
    Returns current OS mode state.
    """
    return os_mode_active
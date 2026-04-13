from os_layer.schemas.response_schema import create_os_response
import subprocess
import webbrowser
import urllib.parse
from os_layer.execution.music_controller import play_song, stop_music, start_music, resume_music


ALLOWED_APPS = {
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "chrome": "chrome.exe",
    "command prompt": "cmd.exe",
}

def handle_application(command):

    intent = command.get("intent")
    params = command.get("parameters", {})

    app_name = params.get("app_name", "").strip().lower()

    print("APP NAME RECEIVED:", app_name)
    print("ALLOWED_APPS:", ALLOWED_APPS)

    # OPEN APPLICATION
    if intent == "open_application":

        if app_name not in ALLOWED_APPS:
            return create_os_response(
                status="failed",
                error="Application not allowed"
            )

        try:
            subprocess.Popen(ALLOWED_APPS[app_name])
            return create_os_response(
                status="success",
                output=f"{app_name} launched"
            )
        except Exception as e:
            return create_os_response(
                status="failed",
                error=str(e)
            )

    # CLOSE APPLICATION
    elif intent == "close_application":

        if app_name not in ALLOWED_APPS:
            return create_os_response(
                status="failed",
                error="Application not allowed"
            )

        try:
            subprocess.run(["taskkill", "/IM", ALLOWED_APPS[app_name], "/F"])
            return create_os_response(
                status="success",
                output=f"{app_name} closed"
            )
        except Exception as e:
            return create_os_response(
                status="failed",
                error=str(e)
            )




    # =====================================================

    # MUSIC CONTROL SYSTEM

    # =====================================================

    elif intent == "play_music":

        song = params.get("song_name", "").strip()

        try:

            if song:

                result = play_song(song)


            else:

                result = start_music()

            return create_os_response(

                status="success",

                output=result

            )


        except Exception as e:

            return create_os_response(

                status="failed",

                error=str(e)

            )



    elif intent == "start_music":

        try:

            result = start_music()

            return create_os_response(

                status="success",

                output=result

            )


        except Exception as e:

            return create_os_response(

                status="failed",

                error=str(e)

            )



    elif intent == "stop_music":

        try:

            result = stop_music()

            return create_os_response(

                status="success",

                output=result

            )


        except Exception as e:

            return create_os_response(

                status="failed",

                error=str(e)

            )



    elif intent == "resume_music":

        try:

            result = resume_music()

            return create_os_response(

                status="success",

                output=result

            )


        except Exception as e:

            return create_os_response(

                status="failed",

                error=str(e)

            )


    elif intent in ["start_music", "play_audio"]:

        webbrowser.open("https://www.youtube.com")
        return create_os_response(
            status="success",
            output="Opening YouTube"
        )

    elif intent == "stop_music":

        try:
            subprocess.run(["taskkill", "/F", "/IM", "chrome.exe"])
            return create_os_response(
                status="success",
                output="Music stopped"
            )
        except Exception as e:
            return create_os_response(
                status="failed",
                error=str(e)
            )

    else:
        return create_os_response(
            status="failed",
            error="Unsupported application intent"
        )


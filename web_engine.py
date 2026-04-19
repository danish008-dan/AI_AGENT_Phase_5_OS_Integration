import webbrowser
from os_layer.schemas.response_schema import create_os_response
import urllib.parse

def handle_web(command):

    intent = command.get("intent")
    params = command.get("parameters", {})

    # OPEN WEBSITE
    if intent == "open_website":

        url = params.get("url")
        if not url:
            return create_os_response(status="failed", error="URL missing")

        webbrowser.open(url)
        return create_os_response(
            status="success",
            output=f"Opened {url}"
        )

    # SEARCH QUERY
    elif intent in ["search_engine_query", "search_institutes"]:

        query = params.get("query") or "top institutes"
        encoded = urllib.parse.quote(query)
        url = f"https://www.google.com/search?q={encoded}"

        webbrowser.open(url)

        return create_os_response(
            status="success",
            output=f"Searched for {query}"
        )
    elif command["intent"] == "search_web":
        query = command["parameters"].get("query", "")
        url = f"https://www.google.com/search?q={query}"
        webbrowser.open(url)
        return create_os_response(
            status="success",
            output=f"Searched for {query}"
        )

    elif command["intent"] == "search_weather":
        url = "https://www.google.com/search?q=weather+today"
        webbrowser.open(url)
        return create_os_response(
            status="success",
            output="Opened weather information"
        )


    return create_os_response(
        status="failed",
        error="Unsupported web intent"
    )
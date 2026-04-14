import webbrowser
import urllib.parse
import keyboard

# =====================================================
# MUSIC STATE
# =====================================================

music_state = {
    "is_playing": False,
    "last_song": None
}

# =====================================================
# PLAY SPECIFIC SONG
# =====================================================

def play_song(song):

    query = urllib.parse.quote(song)

    url = f"https://www.youtube.com/results?search_query={query}"

    webbrowser.open(url)

    music_state["is_playing"] = True
    music_state["last_song"] = song

    return f"Searching and playing {song}"


# =====================================================
# PLAY / START MUSIC
# =====================================================

def start_music():

    if music_state["is_playing"]:

        keyboard.send("play/pause media")
        music_state["is_playing"] = True
        return "Music resumed"

    else:

        keyboard.send("play/pause media")
        music_state["is_playing"] = True
        return "Music started"


# =====================================================
# STOP MUSIC
# =====================================================

def stop_music():

    keyboard.send("play/pause media")

    music_state["is_playing"] = False

    return "Music paused"


# =====================================================
# RESUME MUSIC
# =====================================================

def resume_music():

    keyboard.send("play/pause media")

    music_state["is_playing"] = True

    return "Music resumed"
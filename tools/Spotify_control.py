import subprocess, os, time
from langchain_core.tools import tool
from logger import get_logger

log = get_logger("tool.spotify")

def _sp():
    """Get authenticated Spotify client."""
    import spotipy
    from spotipy.oauth2 import SpotifyOAuth
    return spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=os.getenv("SPOTIFY_CLIENT_ID", ""),
        client_secret=os.getenv("SPOTIFY_CLIENT_SECRET", ""),
        redirect_uri="http://localhost:8888/callback",
        scope="user-modify-playback-state user-read-playback-state user-read-currently-playing",
        cache_path=".spotify_cache"
    ))

@tool
def spotify_play(song_name: str = "") -> str:
    """Play a song on Spotify. song_name: song or artist to search and play."""
    try:
        sp = _sp()
        if song_name:
            results = sp.search(q=song_name, type="track", limit=1)
            tracks = results.get("tracks", {}).get("items", [])
            if not tracks:
                return f"Song '{song_name}' nahi mila Spotify pe."
            uri = tracks[0]["uri"]
            name = tracks[0]["name"]
            artist = tracks[0]["artists"][0]["name"]
            sp.start_playback(uris=[uri])
            return f"Playing: {name} by {artist}"
        else:
            sp.start_playback()
            return "Spotify resumed."
    except ImportError:
        return "pip install spotipy"
    except Exception as e:
        log.error(f"Spotify play error: {e}")
        return f"Spotify error: {e}"

@tool
def spotify_pause() -> str:
    """Pause Spotify playback."""
    try:
        _sp().pause_playback()
        return "Spotify paused."
    except Exception as e:
        return f"Pause failed: {e}"

@tool
def spotify_next() -> str:
    """Skip to next track on Spotify."""
    try:
        _sp().next_track()
        time.sleep(0.5)
        current = _sp().current_playback()
        if current and current.get("item"):
            name = current["item"]["name"]
            artist = current["item"]["artists"][0]["name"]
            return f"Next track: {name} by {artist}"
        return "Next track play ho gaya."
    except Exception as e:
        return f"Next failed: {e}"

@tool
def spotify_previous() -> str:
    """Go to previous track on Spotify."""
    try:
        _sp().previous_track()
        return "Previous track."
    except Exception as e:
        return f"Previous failed: {e}"

@tool
def spotify_volume(level: int) -> str:
    """Set Spotify volume. level: 0 to 100."""
    try:
        level = max(0, min(100, level))
        _sp().volume(level)
        return f"Spotify volume set to {level}%."
    except Exception as e:
        return f"Volume error: {e}"

@tool
def spotify_current_song() -> str:
    """Get the currently playing song on Spotify."""
    try:
        current = _sp().current_playback()
        if not current or not current.get("item"):
            return "Koi song nahi chal raha Spotify pe."
        item = current["item"]
        name = item["name"]
        artist = item["artists"][0]["name"]
        album = item["album"]["name"]
        progress_ms = current.get("progress_ms", 0)
        duration_ms = item.get("duration_ms", 1)
        progress_pct = int((progress_ms / duration_ms) * 100)
        is_playing = current.get("is_playing", False)
        status = "Playing" if is_playing else "Paused"
        return f"{status}: {name} by {artist} ({album}) — {progress_pct}% done"
    except Exception as e:
        return f"Error: {e}"
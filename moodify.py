from spotify import get_album_art_file
from lifx import set_mood_colors, set_default_colors
from clone import call_clone

def moodify():
  album_art, playing_on_wanted_device = get_album_art_file()

  status = None
  if playing_on_wanted_device:
    status = set_mood_colors(album_art)
    call_clone()
  else:
    stop_cron_service()
    status = set_default_colors()

  return {
    "status": status
  }
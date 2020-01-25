import os
import requests

from requests.auth import HTTPBasicAuth

from colors import get_mood_colors, get_default_color

lifx = {
  "auth": {
    "access_token": os.getenv("LIFX_ACCESS_TOKEN"), # load from env
  },
  "light_ids": {
    "left_lamp": os.getenv("LIFX_LEFT_LAMP"), # load from env
    "right_lamp": os.getenv("LIFX_RIGHT_LAMP"), # load from env
    "accent_lamp": os.getenv("LIFX_ACCENT_LAMP"), # load from env
  },
  "endpoints": {
    "set_lights": {
      "url": "https://api.lifx.com/v1/lights/states",
      "success_code": 207
    }
  },
  "consts": {
    "transition_duration": 5 # seconds
  }
}

MOOD_COLOR_OK = "Set mood colors successfully"
DEFAULT_COLOR_OK = "Set default colors successfully"
COLOR_ERROR = "Something went wrong"

def set_mood_colors(image):
  primary, accent = get_mood_colors(image)
  return MOOD_COLOR_OK if set_colors(left=primary, right=primary, accent=accent, force_on=True) else COLOR_ERROR

def set_default_colors(force_on=False):
  default_color = get_default_color()
  return DEFAULT_COLOR_OK if set_colors(left=default_color, right=default_color, accent=default_color, brightness=1, force_on=force_on) else COLOR_ERROR

def set_colors(left, right, accent, brightness=None, force_on=False):
  headers = get_lifx_headers();
  light_states = get_light_states(left, right, accent, brightness, force_on)
  resp = requests.put(url=lifx["endpoints"]["set_lights"]["url"], headers=headers, json=light_states)

  return resp.status_code == lifx["endpoints"]["set_lights"]["success_code"]

def get_light_states(left, right, accent, brightness, force_on):
  states = [
    {"selector": "id:" + lifx["light_ids"]["left_lamp"], "color": left},
    {"selector": "id:" + lifx["light_ids"]["right_lamp"], "color": right},
    {"selector": "id:" + lifx["light_ids"]["accent_lamp"], "color": accent}
  ]

  if force_on:
    states = [ dict(**state, **{"power": "on"}) for state in states ] if force_on else states
    states = [ dict(**state, **{"brightness": brightness}) for state in states ] if brightness is not None else states

  return {
    "states": states,
    "defaults": {"duration": lifx["consts"]["transition_duration"]} # 5 seconds
  }

def get_lifx_headers():
  return { "Authorization": "Bearer " + lifx["auth"]["access_token"] }

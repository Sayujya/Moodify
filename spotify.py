import os
import time
import requests

from io import BytesIO
import json

spotify = {
  "auth": {
    "access_token": None,
    "access_token_valid_till": None,
    "refresh_token": os.getenv("SPOTIFY_REFRESH_TOKEN"),
    "client_id": os.getenv("SPOTIFY_CLIENT_ID"),
    "client_secret": os.getenv("SPOTIFY_CLIENT_SECRET"),
    "auth_endpoint": "https://accounts.spotify.com/api/token",
  },
  "device": {
    "id": os.getenv("SPOTIFY_DEVICE_ID")
  },
  "endpoints": {
    "current_playing": {
      "url": "https://api.spotify.com/v1/me/player",
      "success_code": 200
    }
  }
}

def get_album_art_file():
  headers = get_headers();
  resp = requests.get(url=spotify["endpoints"]["current_playing"]["url"], headers=headers)

  if not is_playing_on_wanted_device(resp):
    return None, False

  album_art_url = get_album_art_url(resp.json())
  image = get_album_art(album_art_url)

  return image, True

def is_playing_on_wanted_device(resp):
  if not resp.status_code == spotify["endpoints"]["current_playing"]["success_code"]:
    return False
  device = resp.json()["device"]
  if device is None or "name" not in device:
    return False
  device_id = device["id"]

  return spotify["device"]["id"] == device_id

def get_headers():
  access_token = get_access_token()
  return { "Authorization": "Bearer " + access_token}

def get_access_token():
  if not is_token_valid():
    renew_token()
  return spotify["auth"]["access_token"]

def is_token_valid():
  if (spotify["auth"]["access_token"] and spotify["auth"]["access_token_valid_till"]) is None:
    print("Access token not initialized!")
    return False

  # leave a two minute buffer time
  current_time = round(time.time()) + 2*60
  if current_time > spotify["auth"]["access_token_valid_till"]:
    print("Access token expiring soon or expired!")
    return False

  return True

def renew_token():
  print("Renewing token")
  url = spotify["auth"]["auth_endpoint"]
  body = {
    "grant_type": "refresh_token",
    "refresh_token": spotify["auth"]["refresh_token"]
  }
  resp = requests.post(url=url, auth=(spotify["auth"]["client_id"], spotify["auth"]["client_secret"]), data=body)

  if resp.status_code == 200:
    resp_json = resp.json()
    current_time = round(time.time())
    spotify["auth"]["access_token_valid_till"] = current_time + resp_json["expires_in"]
    spotify["auth"]["access_token"] = resp_json["access_token"]
    print("Renewed token, valid till", spotify["auth"]["access_token_valid_till"])
  else:
    print(resp.json())

def get_album_art_url(jres):
  item = jres["item"]
  if "album" not in item:
    return None
  album = item["album"]
  if "images" not in album:
    return None
  images = album["images"]
  if images is None or len(images) == 0:
    return None
  image = images[0]
  if "url" not in image:
    return None
  album_art_url = image["url"]
  return album_art_url

def get_album_art(album_art_url):
  if album_art_url is None:
    return None

  response = requests.get(album_art_url)
  return BytesIO(response.content)

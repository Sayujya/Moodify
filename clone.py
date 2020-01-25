import os
import time
import requests

clone_url = os.getenv("CLONE_URL")
SLEEP_TIME = int(os.getenv("CLONE_WAIT_TIME")) # seconds

def call_clone():
  time.sleep(SLEEP_TIME)
  # allow the request to the clone to timeout and supress the error
  try:
    requests.get(clone_url, timeout=0.5)
  except:
    pass

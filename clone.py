import os
import time
import requests

clone_url = os.getenv("CLONE_URL")
SLEEP_TIME = int(os.getenv("CLONE_WAIT_TIME")) # seconds

def call_clone():
  time.sleep(SLEEP_TIME)
  requests.get(clone_url)

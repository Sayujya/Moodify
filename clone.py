import os
import time
import requests

clone_url = os.getenv("CLONE_URL")

def call_clone():
  time.sleep(10)
  requests.get(clone_url)

import os

from sanic import Sanic
from sanic.response import json
from moodify import moodify

app = Sanic(name="Moodify")

@app.route("/moodify")
async def test(request):
  return json(moodify())

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=int(os.environ["PORT"]))

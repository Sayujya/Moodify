# Moodify

### What is this?
It's just lipstick over some APIs and some hacky stuff so that:  
1. I can ask Google Assistant to set the color of my lights to match the album art of the song that's playing from Spotify on my living room chromecast  
2. And do so without me having to pay money for servers and what not

### Why though?
I dunno. This was written over two nights so don't judge it too hard please. :)

### What's hacky about it?
Everything. Except the Spotify side I think. If I had to pick one, I would say it's the fact that the servers call each other with very short timeouts to simulate a tight polling scenario.  

Here's the flow of API calls. 
 
----
![API Flow](https://github.com/Sayujya/Moodify/raw/master/call_flow.png)

### So many environment variables fam
I was lazy. Populate these env variables to make this work.

    LIFX_ACCENT_LAMP 
    LIFX_LEFT_LAMP
    LIFX_RIGHT_LAMP
    LIFX_ACCESS_TOKEN
    SPOTIFY_CLIENT_ID
    SPOTIFY_CLIENT_SECRET
    SPOTIFY_DEVICE_ID
    SPOTIFY_REFRESH_TOKEN
    CLONE_URL
    CLONE_WAIT_TIME

### How are you gonna improve this?
I would like to come up with a DSL for the lights to colors relationship. Decouple things so this works with philips hue as well. You know, stuff like that.
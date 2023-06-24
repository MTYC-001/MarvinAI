import requests
from decouple import config

ELEVEN_LABS_API_KEY = config("ELEVEN_LABS_API_KEY")

#ElevenLabs
#Convert Text to speech
def convert_text_to_speech(message):
    #define data (body)
    body = {
        "text":message,
        "voice_setting": {
            "stability": 0,
            "similarity_boost":0,

        }
    }
    #define voice
    voice_marvin = "F2yaIQF9DuvVYaLHCQM4"
    #constructing headers and endpoint
    headers = { "xi-api-key":  ELEVEN_LABS_API_KEY, "Content-Type": "application/json", "accept":"audio/mpeg"}
    endpoint = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_marvin}"

    #send request
    try:
        response = requests.post(endpoint, json=body, headers=headers)
    except Exception as e:
        return
    #handle responses
    if response.status_code == 200:
        return response.content
    else:
        return 
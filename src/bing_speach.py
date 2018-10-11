import json
import requests

YOUR_API_KEY = '9b512a1bc1514b0e9042ac8f07facdf5'
YOUR_AUDIO_FILE = '/home/admin1/Desktop/dev/VoIPBot/src/input.wav'
REGION = 'westus' # westus, eastasia, northeurope 
MODE = 'interactive'
LANG = 'en-US'
FORMAT = 'simple'


def handler():
    # 1. Get an Authorization Token
    token = get_token()
    print token
    # 2. Perform Speech Recognition
    results = get_text(token, YOUR_AUDIO_FILE)
    # 3. Print Results
#    results = json.loads(results)
    if results["RecognitionStatus"]=="Success":
        return results["DisplayText"]
    print
    print(results)

def get_token():
    # Return an Authorization Token by making a HTTP POST request to Cognitive Services with a valid API key.
    url = 'https://westus.api.cognitive.microsoft.com/sts/v1.0/issueToken'
    headers = {
        'Ocp-Apim-Subscription-Key': YOUR_API_KEY
    }
    r = requests.post(url, headers=headers)
    token = r.content
    return(token)
def get_text(token, audio):
    # Request that the Bing Speech API convert the audio to text
    url = 'https://{0}.stt.speech.microsoft.com/speech/recognition/{1}/cognitiveservices/v1?language={2}&format={3}'.format(REGION, MODE, LANG, FORMAT)
    headers = {
        'Accept': 'application/json',
        'Ocp-Apim-Subscription-Key': YOUR_API_KEY,
        'Transfer-Encoding': 'chunked',
        'Content-type': 'audio/wav; codec=audio/pcm; samplerate=16000',
        'Authorization': 'Bearer {0}'.format(token)
    }
    r = requests.post(url, headers=headers, data=stream_audio_file(audio))
    results = json.loads(r.content)
    return results

def stream_audio_file(speech_file, chunk_size=1024):
    # Chunk audio file
    with open(speech_file, 'rb') as f:
        while 1:
            data = f.read(1024)
            if not data:
                break
            yield data

if __name__ == '__main__':
    print handler()
# -*- coding: utf-8 -*-


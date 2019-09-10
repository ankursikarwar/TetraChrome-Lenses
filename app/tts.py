import os
import requests
from xml.etree import ElementTree
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from pygame import mixer
import time


def setup():
    global access_token
    KEY = 'a5ec1ce3d85b4c08917c4f54a15de334'
    assert KEY
    BASE_URL = 'https://centralindia.api.cognitive.microsoft.com/sts/v1.0/issuetoken'
    headers = {
            'Ocp-Apim-Subscription-Key': KEY
    }
    response = requests.post(BASE_URL, headers=headers)
    access_token = str(response.text)
    print("Text-To-Speech Setup Successful")


def audio_synthesis(text):
    global access_token
    constructed_url = 'https://centralindia.tts.speech.microsoft.com/cognitiveservices/v1'
    headers = {
        'Authorization': 'Bearer ' + access_token,
        'Content-Type': 'application/ssml+xml',
        'X-Microsoft-OutputFormat': 'riff-24khz-16bit-mono-pcm',
        'User-Agent': 'Tetrachrome_Lenses'
    }
    xml_body = ElementTree.Element('speak', version='1.0')
    xml_body.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-US')
    voice = ElementTree.SubElement(xml_body, 'voice')
    voice.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-US')
    voice.set('name', 'en-US-JessaNeural')
    voice.text = text
    body = ElementTree.tostring(xml_body)

    response = requests.post(constructed_url, headers=headers, data=body)

    if response.status_code == 200:
        with open('./data/tts_audio/sample' + '.wav', 'wb') as audio:
            audio.write(response.content)
    else:
        print("\nStatus code: " + str(response.status_code) + "\nSomething went wrong. Check your subscription key and headers.\n")
    
    if (len(os.listdir('./data/tts_audio')) == 0):
        return False
    else:
        print('\n\nAudio Synthesis Successful')
        return True


def audio_play():
    mixer.init()
    mixer.music.load('./data/tts_audio/sample.wav')
    print("Starting the Audio Cue")
    mixer.music.play()
    while mixer.music.get_busy():
        time.sleep(0.1)    
    mixer.quit()


def voice(play_text):
    ret = audio_synthesis(play_text)
    if (ret == True):
        audio_play()
        os.remove('./data/tts_audio/sample.wav')
    else:
        raise Exception('\n\nAudio Synthesis Failed')


setup()
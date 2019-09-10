import os
import requests
import app.utils.capture as capture
from app.tts import voice


def setup():
    global KEY, BASE_URL
    KEY = "913161c6f2b34dd3a3262f6b5cdea761"
    assert KEY
    BASE_URL = "https://vision-feature.cognitiveservices.azure.com/vision/v1.0/ocr"
    print("OCR Setup Successful")


def ocr_decoding():
    global KEY, BASE_URL
    ret = capture.image_capture_and_save(True)
    if (ret == True):
	    headers = {'Ocp-Apim-Subscription-Key': KEY,
	               'Content-Type': 'application/octet-stream'}
	    params = {'language': 'unk', 'detectOrientation': 'true'}
	    img_data = open('./data/capture/capture.jpg', "rb").read()
	    response = requests.post(BASE_URL, headers=headers, params=params, data=img_data)
	    response.raise_for_status()
	    analysis = response.json()
	    os.remove('./data/capture/capture.jpg')
	    return analysis
    else:
        raise Exception('Image Capture Failed')


def ocr_output(analysis):
    print(analysis)
    sentence = ""
    if not analysis["regions"]:
        sentence = "Sorry, I didn't get the text"
        print(sentence)
        return sentence
    else:
        txt1 = analysis["regions"][0]["lines"]
        for i in txt1:
            for j in i["words"]:
                sentence = sentence + j["text"] + " "
        print(sentence)
        return sentence


def ocr():
    analysis = ocr_decoding()
    sentence = ocr_output(analysis)
    voice(sentence)


setup()
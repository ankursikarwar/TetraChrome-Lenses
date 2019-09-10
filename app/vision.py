import os
import requests
import app.utils.capture as capture
from app.tts import voice


def setup():
    global KEY, BASE_URL
    KEY = "913161c6f2b34dd3a3262f6b5cdea761"
    assert KEY
    BASE_URL = "https://vision-feature.cognitiveservices.azure.com/vision/v1.0/analyze/"
    print("Image Captioning Setup Successful")


def img_captioning(image_path):
    global KEY, BASE_URL
    image_data = open(image_path, "rb").read()
    headers = {'Ocp-Apim-Subscription-Key': KEY,
               'Content-Type': 'application/octet-stream'}
    params = {'visualFeatures': 'Categories, Description'}
    response = requests.post(
        BASE_URL, headers=headers, params=params, data=image_data)
    response.raise_for_status()
    analysis = response.json()
    os.remove('./data/capture/capture.jpg')
    print(analysis)
    caption_data = analysis["description"]["captions"]
    if not caption_data:
        image_caption = ""
        confidence = 0.30
    else:
        image_caption = caption_data[0]["text"].capitalize()
        confidence = caption_data[0]["confidence"]
    return image_caption, confidence


def caption_image():
    ret = capture.image_capture_and_save(False)
    if (ret == True):
        print("Image Captured")
        image_path = './data/capture/capture.jpg'
        image_caption, confidence = img_captioning(image_path)
        print("Caption Generated : ", image_caption)
        print("Confidence : ", confidence)
        if(confidence > 0.50):
            voice(image_caption)
        else:
            voice("I didn't get the image")
            print("I didn't get the image")
    else:
        raise Exception('Image Capture Failed')


setup()
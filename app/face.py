import cognitive_face as CF
import os
import app.utils.capture as capture
from app.tts import voice

face_list_id = 419

def setup():
    KEY = '279c4eff0cf04dd8b429f29c2351b40b'
    CF.Key.set(KEY)
    BASE_URL = 'https://face-feature.cognitiveservices.azure.com/face/v1.0'
    CF.BaseUrl.set(BASE_URL)
    print("Face Recogntion Setup Successful")
    print("Emotion Recogntion Setup Successful")


def create_database(face_list_id, face_list_name):
    CF.face_list.create(face_list_id, name=face_list_name)
    print("Face_List Created")


def add_face(image_path, face_list_id, person_name):
    fixed_face_id = CF.face_list.add_face(image_path, face_list_id, person_name)
    return fixed_face_id


def delete_face(face_list_id, fixed_face_id):
    CF.face_list.delete_face(face_list_id, fixed_face_id)
    print("Face Deleted")


def get_face_list(face_list_id):
    face_database = CF.face_list.get(face_list_id)
    face_list = face_database['persistedFaces']
    face_list_dict = {}
    for i in face_list:
        face_list_dict[i['persistedFaceId']] = i['userData']
    return face_list, face_list_dict


def get_faceids_detect(img_path):
    faces_detected_database = CF.face.detect(img_path, attributes='age,gender,emotion')
    faces_detected_ids = []
    no_of_faces_detected = 0
    for i in faces_detected_database:
        no_of_faces_detected = no_of_faces_detected + 1
        faces_detected_ids.append(i['faceId'])
    return faces_detected_database, faces_detected_ids, no_of_faces_detected


def find_who_are_in_picture(face_list_id):
    ret = capture.image_capture_and_save(False)
    if (ret == True):
        img_path = './data/capture/capture.jpg'
        people_name_in_image = []
        stranger_database = []
        friends_database = []
        no_of_faces_recognized = 0
        _, face_list_dict = get_face_list(face_list_id)
        faces_detected_database, faces_detected_ids, no_of_faces_detected = get_faceids_detect(img_path)
        os.remove('./data/capture/capture.jpg')
        for idx, face_id in enumerate(faces_detected_ids):
            detected_face_id, detected = who_is_the_person(face_id, face_list_id)
            if (detected == True):
                people_name_in_image.append(face_list_dict[detected_face_id])
                no_of_faces_recognized = no_of_faces_recognized + 1
                friends_database.append(faces_detected_database[idx])
            else:
                stranger_database.append(faces_detected_database[idx])
        no_of_strangers = no_of_faces_detected - no_of_faces_recognized
        print(people_name_in_image)
        print(faces_detected_database)
        print(no_of_strangers)
        print(stranger_database)
        return people_name_in_image, faces_detected_database, no_of_strangers, stranger_database, friends_database
    else:
        raise Exception('Image Capture Failed')


def who_is_the_person(face_id, face_list_id):
    data = CF.face.find_similars(face_id, face_list_id)
    if not data:
        detected_face_id = None
        detected = False
    else:
        detected_face_id = data[0]['persistedFaceId']
        detected = True
    return detected_face_id, detected


def get_stranger_age_and_gender(stranger):
    attributes = stranger['faceAttributes']
    gender = attributes['gender']
    age = int(attributes['age'])
    return age, gender


def emotion_recognition():
    people_name_in_image, faces_detected_database, no_of_strangers, stranger_database, friends_database = find_who_are_in_picture(face_list_id)
    i = 1
    j = 1
    emotion_database = []
    emotion_detected = []
    strangers_emotion_database = []
    strangers_emotion_detected = []
    confidence = []
    stranger_confidence = []
    say = ""
    for data in friends_database:
        emotion_database.append(data['faceAttributes']['emotion'])
    print(emotion_database)
    for data in stranger_database:
        strangers_emotion_database.append(data['faceAttributes']['emotion'])
    print(strangers_emotion_database)
    for emotion in emotion_database:
        values = list(emotion.values())
        keys = list(emotion.keys())
        what_emotion = keys[values.index(max(values))]
        emotion_detected.append(what_emotion)
        confidence.append(emotion[what_emotion])
    print(emotion_detected)
    print(confidence)
    for emotion in strangers_emotion_database:
        values = list(emotion.values())
        keys = list(emotion.keys())
        what_emotion = keys[values.index(max(values))]
        strangers_emotion_detected.append(what_emotion)
        stranger_confidence.append(emotion[what_emotion])
    print(emotion_detected)
    print(confidence)
    if not people_name_in_image:
        say = "I see none of your friends."
    else:
        for idx, value in enumerate(people_name_in_image):
            if(j < len(people_name_in_image)):
                say = say + str(value) + "'s emotion is " + str(emotion_detected[idx]) + " with a probability of " + str(confidence[idx]) + ", "
            else:
                if(len(people_name_in_image)):
                    say = say + str(value) + "'s emotion is " + str(emotion_detected[idx]) + " with a probability of " + str(confidence[idx]) + ", "
                else:
                    say = say + "and " + str(value) + "'s emotion is " + str(emotion_detected[idx]) + " with a probability of " + str(confidence[idx]) + ", "
            j = j + 1
    if not no_of_strangers:
        say = say + ""
    else:
        if(no_of_strangers > 1):
            say = say + "I see some strangers. "
        else:
            say = say + "I see a stranger. "
        for idx, value in enumerate(stranger_database):
            if(i < no_of_strangers):
                say = say + "Stranger " + str(i) + "'s emotion is " + str(strangers_emotion_detected[idx]) + " with a probability of " + str(stranger_confidence[idx]) + ", "
            else:
                say = say + "and Stranger " + str(i) + "'s emotion is " + str(strangers_emotion_detected[idx]) + " with a probability of " + str(stranger_confidence[idx])
            i = i + 1

    print(say)
    voice(say)


def face_recognition():
    people_name_in_image, faces_detected_database, no_of_strangers, stranger_database, _ = find_who_are_in_picture(face_list_id)
    print(people_name_in_image)
    no_of_known_faces = len(people_name_in_image)
    say = ""
    if ((no_of_known_faces == 0) & (no_of_strangers == 0)):
        say = "I don't recognize anyone in front of you"
        print(say)
        voice(say)
    if ((no_of_known_faces != 0) & (no_of_strangers != 0)):
        say = "I see "
        i = 1
        for people in people_name_in_image:
            if(i < len(people_name_in_image)):
                say = say + str(people) + ", "
            else:
                if(len(people_name_in_image) == 1):
                    say = say + str(people)
                else:
                    say = say + " and " + str(people)
            i = i + 1

        if(no_of_strangers == 1):
            say = say + " and " + str(no_of_strangers) + " stranger. "
            say = say + "Stranger is "
            for stranger in stranger_database:
                age, gender = get_stranger_age_and_gender(stranger)
                say = say + str(gender) + ", of age " + str(age) + ". "
        else:
            say = say + "and " + str(no_of_strangers) + " strangers. "
            k = 1
            for stranger in stranger_database:
                say = say + "Stranger " + str(k) + " is "
                age, gender = get_stranger_age_and_gender(stranger)
                say = say + str(gender) + ", of age " + str(age) + ". "
                k = k + 1
        print(say)
        voice(say)

    if ((no_of_known_faces == 0) & (no_of_strangers != 0)):
        say = "I see "
        if(no_of_strangers == 1):
            say = say + "and " + str(no_of_strangers) + " stranger. "
            say = say + "Stranger is "
            for stranger in stranger_database:
                age, gender = get_stranger_age_and_gender(stranger)
                say = say + str(gender) + ", of age " + str(age) + ". "
        else:
            say = say + "and " + str(no_of_strangers) + " strangers. "
            c = 1
            for stranger in stranger_database:
                say = say + "Stranger " + str(k) + " is "
                age, gender = get_stranger_age_and_gender(stranger)
                say = say + str(gender) + ", of age " + str(age) + ". "
                c = c + 1
        print(say)
        voice(say)
    if ((no_of_known_faces != 0) & (no_of_strangers == 0)):
        say = "I see "
        t = 1
        for people in people_name_in_image:
            if(t < len(people_name_in_image)):
                say = say + str(people) + ", "
            else:
                if(len(people_name_in_image) == 1):
                    say = say + str(people)
                else:
                    say = say + " and " + str(people)
            t = t + 1
        print(say)
        voice(say)


setup()

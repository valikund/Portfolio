#!/usr/bin/env python

import speech_recognition as sr
import time
from gtts import gTTS
import os
import apiai
import uuid
import json
import botActions


def voiceResponse(json):
    text_out = json['result']['fulfillment']['speech']
    if text_out:
        tts = gTTS(text=text_out, lang='en')
        tts.save("temp.mp3")
        os.system("mpg321 temp.mp3")

botDo =botActions.botActions()

with open('gspeech.json', 'r') as myfile:
    GOOGLE_CLOUD_SPEECH_CREDENTIALS=myfile.read()

ai = apiai.ApiAI('e04adfd76c294f628762d676927ff97c')
session_id = uuid.uuid4().hex

r = sr.Recognizer()
m = sr.Microphone(sample_rate=16000,chunk_size=2048)

print("A moment of silence, please...")
with m as source: r.adjust_for_ambient_noise(source)

session_over  = False
#Getting the list of available actions
action_list = os.listdir("LearnedActions")
entries = []
for action in action_list:
    single_action = apiai.UserEntityEntry(action, [action])
    entries.append(single_action)
user_entities_request = ai.user_entities_request(
    [
        apiai.UserEntity("eUserActions", entries, session_id)
    ]
)
user_entities_response = user_entities_request.getresponse()

#Invokng the welcome intent
request = ai.event_request(apiai.events.Event("WELCOME"))
request.session_id = session_id
response = request.getresponse()
response_text = response.read()
json_resp = json.loads(response_text)
voiceResponse(json_resp)

while not session_over:

    #Recording audio
    print('Recording')
    with m as source: audio = r.listen(source)
    print('Finished recording')

    start_time = time.time()
    action_list.extend(['Baxter','tuck','untuck','right','left','open','close','wave'])
    value_g = r.recognize_google_cloud(audio, credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS, preferred_phrases=action_list,show_all=True)
    elapsed_time_g = time.time() - start_time
    print('Google Time needed: %i Response: %s\n', elapsed_time_g, value_g)
    if 'results' not in value_g:
        continue

    #Getting the response from api.ai
    request = ai.text_request()
    request.session_id = session_id
    try:
        user_question = value_g['results'][0]['alternatives'][0]['transcript']
    except KeyError:
        user_question = ''
    request.query = value_g['results'][0]['alternatives'][0]['transcript']
    response = request.getresponse()
    response_text = response.read()
    json_resp = json.loads(response_text)
    print(response_text)

    #Invoking action
    actionPerform = json_resp['result']['action']
    if actionPerform in botDo.actions:
        context = botDo.actions[actionPerform](json_resp)
    if actionPerform == 'aSessionOver':
        session_over = True
    if actionPerform == 'aNameMovement':
        action_list = os.listdir("LearnedActions")
        entries = []
        for action in action_list:
            single_action = apiai.UserEntityEntry(action, [action])
            entries.append(single_action)
        user_entities_request = ai.user_entities_request(
            [
                apiai.UserEntity("eUserActions", entries, session_id)
            ]
        )
        print action_list
        print user_entities_request.getresponse()

    #Giving voice response
    voiceResponse(json_resp)


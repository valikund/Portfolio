#!/usr/bin/env python

import speech_recognition as sr
import time
from gtts import gTTS
import os
import apiai
import uuid
import json
import botActions
from watson_developer_cloud import TextToSpeechV1
from client import Client

def voiceResponse(json):
    text_out = json['result']['fulfillment']['speech']
    if text_out:
        text_to_speech = TextToSpeechV1(url="https://stream-fra.watsonplatform.net/text-to-speech/api",
                                        username=,
                                        password=,
                                        x_watson_learning_opt_out=True)  # Optional flag

        with open('output.wav', 'wb') as audio_file:
            audio_file.write(text_to_speech.synthesize(text_out, accept='audio/wav', voice="en-US_AllisonVoice"))
        os.system("play output.wav")

botDo =botActions.botActions()

ai = apiai.ApiAI('e04adfd76c294f628762d676927ff97c')
session_id = uuid.uuid4().hex

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
action_list.extend(['Baxter','tuck','untuck','right','left','open','close','wave','ball lifting','lifting','wake up'])


#Starting the robot with a voice command
while 1:
    print 'Start with phrase "wake up Baxter"'
    client = Client(action_list)
    value_g = client.listen()
    if ('Baxter' in value_g ) or (value_g in 'Jacob Baxter') or (value_g in 'Abort'):
        break

#Invokng the welcome intent
request = ai.event_request(apiai.events.Event("WELCOME"))
request.session_id = session_id
response = request.getresponse()
response_text = response.read()
json_resp = json.loads(response_text)
voiceResponse(json_resp)


while not session_over:
    client = Client(action_list)
    #Recording audio
    print('Recording')

    start_time = time.time()

    value_g = client.listen()
    elapsed_time_g = time.time() - start_time
    print('Google Time needed: %i Response: %s\n', elapsed_time_g, value_g)
    if not value_g:
        continue


    #Getting the response from api.ai
    request = ai.text_request()
    request.session_id = session_id
    try:
        user_question = value_g
    except KeyError:
        user_question = ''
    request.query = value_g
    response = request.getresponse()
    response_text = response.read()
    json_resp = json.loads(response_text)
    print(response_text)

    # Giving voice response
    voiceResponse(json_resp)

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




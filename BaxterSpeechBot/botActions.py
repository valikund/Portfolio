#!/usr/bin/env python

#This is a list of actions which the robot can perform
#If you add a new function put it into the actions dictionary
import os
import rospy
import baxter_interface
import subprocess
import multiprocessing
import wikipedia
from watson_developer_cloud import TextToSpeechV1

def voiceResponse(text):
    text_out = text
    if text_out:
        text_to_speech = TextToSpeechV1(url="https://stream-fra.watsonplatform.net/text-to-speech/api",
                                        username='0c9d8cf3-f367-4bc7-89df-3f9889b0eb96',
                                        password='v4zRG600FdNY',
                                        x_watson_learning_opt_out=True)  # Optional flag

        with open('output.wav', 'wb') as audio_file:
            audio_file.write(text_to_speech.synthesize(text_out, accept='audio/wav', voice="en-US_AllisonVoice"))
        os.system("play output.wav")

def _learnMovement():
    bashCommand = 'rosrun baxter_examples joint_recorder.py -f LearnedActions/temp'
    subprocess.call(bashCommand.split(), stdout=subprocess.PIPE)

def _showFace(face):
    bashCommand = "rosrun baxter_examples xdisplay_image.py --file='Faces/rsz_" + face + "'"
    print bashCommand
    os.system(bashCommand)

def _parallelCommand(command):
    os.system(command)

class botActions:

    def __init__(self):
        try:
            rospy.init_node('botActions', anonymous=True)
            _showFace('smile.png')
            #os.system('rosrun baxter_interface joint_trajectory_action_server.py --mode velocity &')
        except rospy.ROSInterruptException:
            pass

    def destructor(self):
        _showFace('sad.jpg')

        #Killing the recorder just to be sure
        bashCommand = 'rosnode kill rsdk_joint_recorder'
        p = multiprocessing.Process(target=_parallelCommand, args=(bashCommand,))
        p.start()

        #Tucking the arms, if its already tucked nothing happens
        bashCommand = "rosrun baxter_tools tuck_arms.py -t"
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()

        os.system('rosnode kill botActions')
        return

    def tuckArms(response):

        try:
            value = response['result']['parameters']['eTuckUntuck']
        except KeyError:
            context = {'missing-key': 'tuckArm'}
            return context

        if value == 'untuck':
            bashCommand = "rosrun baxter_tools tuck_arms.py -u"
            process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
            output, error = process.communicate()
        elif value == 'tuck':
            bashCommand = "rosrun baxter_tools tuck_arms.py -t"
            process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
            output, error = process.communicate()

        context = {'action-succes': 'succes'}
        return context

    def gripperControl(response):

        try:
            value_side = response['result']['parameters']['side']
            value_action = response['result']['parameters']['eOpenClose']
        except KeyError:
            return

        if( value_side == 'both'):
            value_sides = {'left','right'}

            for value_side in value_sides:
                gripper = baxter_interface.Gripper(value_side)
                gripper.calibrate()
                if value_action == 'open':
                    gripper.open()
                elif value_action == 'close':
                    gripper.close()

        elif( value_side == 'right' or value_side == 'left'):
            gripper = baxter_interface.Gripper(value_side)
            gripper.calibrate()
            if value_action == 'open':
                gripper.open()
            elif value_action == 'close':
                gripper.close()

        context = {'action-succes': 'succes'}
        return context

    def waveHand(response):
        os.system('rosrun baxter_interface joint_trajectory_action_server.py --mode velocity &')
        _showFace('dope.png')
        try:
            value_side = response['result']['parameters']['side']
        except KeyError:
            return

        if(value_side[0] == 'left'):
            side_explicit = 'left'
        elif(value_side[0] == 'right'):
            side_explicit = 'right'
        print value_side
        print side_explicit

        bashCommand = 'rosrun baxter_examples joint_trajectory_file_playback.py -f wave_hand_' + side_explicit
        subprocess.call(bashCommand.split(), stdout=subprocess.PIPE)

        os.system('rosnode kill rsdk_velocity_joint_trajectory_action_server')

        context = {'action-succes': 'succes'}
        return context



    def learnMovement(response):

        _showFace('contempt.png')
        p = multiprocessing.Process(target=_learnMovement)
        p.start()

        print 'Learning the MOVEMENT'
        context = {'action-succes': 'succes'}
        return context

    def stopRecording(response):
        bashCommand = 'rosnode kill rsdk_joint_recorder'
        subprocess.call(bashCommand.split(), stdout=subprocess.PIPE)

        context = {'action-succes': 'succes'}
        return context

    def nameMovement(response):
        newName = response['result']['parameters']['movement-name']
        for filename in os.listdir("LearnedActions"):
            print filename, newName
            if filename == 'temp':
                print 'Got it'
                os.rename(os.path.join("LearnedActions", filename), os.path.join("LearnedActions", newName))

        context = {'action-succes': 'succes'}
        return context

    def playMovement(response):
        os.system('rosrun baxter_interface joint_trajectory_action_server.py --mode velocity &')
        print response
        _showFace('contempt.png')
        movementName = response['result']['parameters']['eUserActions']
        movementName = movementName.replace(" ", "")
        bashCommand = 'rosrun baxter_examples joint_trajectory_file_playback.py -f LearnedActions/' + movementName
        subprocess.call(bashCommand.split(), stdout=subprocess.PIPE)
        os.system('rosnode kill rsdk_velocity_joint_trajectory_action_server')
        context = {'action-succes': 'succes'}
        return context

    def fallBack(response):
        _showFace('sad.png')
        context = {'action-succes': 'succes'}
        return context

    def wikipediaSearch(response):
        query = response['result']['parameters']['search-query']
        if query:
            try:
                search_result = wikipedia.summary(query,sentences=1)
            except wikipedia.exceptions.DisambiguationError:
                search_result = "Could you please be a bit more specific, there are many " + query + "s"

        voiceResponse(search_result)

        context = {'action-succes': 'succes'}
        return context

    actions = {
        'aTuckArm': tuckArms,
        'aCloseHand':gripperControl,
        'aWaveHand':waveHand,
        'aSessionOver':destructor,
        'aLearnMovement': learnMovement,
        'aStopRecording':stopRecording,
        'aNameMovement':nameMovement,
        'aPlayMovement': playMovement,
        'aFallback':fallBack,
        'aWikipediaSearch':wikipediaSearch,
    }
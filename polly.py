import boto3
import pygame
import os
import time
import io

class Polly():
    OUTPUT_FORMAT='mp3'

    def __init__(self, voiceId):
        self.polly = boto3.client('polly') #access amazon web service
        self.VOICE_ID = voiceId

    def say(self, textToSpeech): #get polly response and play directly
        pollyResponse = self.polly.synthesize_speech(Text=textToSpeech, OutputFormat=self.OUTPUT_FORMAT, VoiceId=self.VOICE_ID)
        
        pygame.mixer.init()
        pygame.init()  # this is needed for pygame.event.* and needs to be called after mixer.init() otherwise no sound is played 
        
        with io.BytesIO() as f: # use a memory stream
            f.write(pollyResponse['AudioStream'].read()) #read audiostream from polly
            f.seek(0)
            pygame.mixer.music.load(f)
            pygame.mixer.music.play()

    def saveToFile(self, textToSpeech, fileName): #get polly response and save to file
        pollyResponse = self.polly.synthesize_speech(Text=textToSpeech, OutputFormat=self.OUTPUT_FORMAT, VoiceId=self.VOICE_ID)
        
        with open(fileName, 'wb') as f:
            f.write(pollyResponse['AudioStream'].read())
            f.close()
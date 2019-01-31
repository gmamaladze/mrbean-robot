import boto3
import os
import time
import io
import wave
import alsaaudio

class Polly():
    OUTPUT_FORMAT='mp3'

    def __init__(self, voiceId):
        self.polly = boto3.client('polly', region_name='eu-central-1') #access amazon web service
        self.VOICE_ID = voiceId

    def say(self, textToSpeech): #get polly response and play directly
        pollyResponse = self.polly.synthesize_speech(Text=textToSpeech, OutputFormat='pcm', SampleRate = '8000', VoiceId=self.VOICE_ID)
        
        device = alsaaudio.PCM(device='default')
        device.setchannels(1)
        device.setformat(alsaaudio.PCM_FORMAT_S16_LE)
        device.setrate(8000)
        with io.BytesIO() as f: # use a memory stream
            data = pollyResponse['AudioStream'].read()
            device.write(data)

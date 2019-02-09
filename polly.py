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
        self.mixer = alsaaudio.Mixer('PCM')
        self.device = alsaaudio.PCM(device='default')
        self.device.setchannels(1)
        self.device.setformat(alsaaudio.PCM_FORMAT_S16_LE)
        self.device.setrate(8000)

    def unmute(self):
        self.mixer.setvolume(100)

    def say(self, textToSpeech): #get polly response and play directly
        pollyResponse = self.polly.synthesize_speech(Text=textToSpeech, OutputFormat='pcm', SampleRate = '8000', VoiceId=self.VOICE_ID)
        data = pollyResponse['AudioStream'].read()
        self.device.write(data)

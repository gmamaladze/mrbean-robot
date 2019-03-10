import boto3
import alsaaudio


class Voice:
    REGION = 'eu-central-1'

    def __init__(self, voice_id='Hans', region=REGION):
        self.polly = boto3.client('polly', region_name=region)
        self.VOICE_ID = voice_id
        self.mixer = alsaaudio.Mixer('PCM')
        self.mixer.setvolume(100)
        self.device = alsaaudio.PCM(device='default')
        self.device.setchannels(1)
        self.device.setformat(alsaaudio.PCM_FORMAT_S16_LE)
        self.device.setrate(8000)

    def say(self, text_to_speech):
        polly_response = self.polly.synthesize_speech(
            Text=text_to_speech,
            OutputFormat='pcm',
            SampleRate='8000',
            VoiceId=self.VOICE_ID)
        data = polly_response['AudioStream'].read()
        self.device.write(data)

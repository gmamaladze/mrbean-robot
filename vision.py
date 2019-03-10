import picamera
import os
import base64
import boto3
import uuid


class Vision:
    REGION = "eu-west-1"

    def __init__(self, resolution=(1024, 768), rotation=90, language='en'):
        self.language = language
        self.rotation = rotation
        self.resolution = resolution
        self.file = os.path.join('/tmp/', str(uuid.uuid4())[:8] + '.jpg')

    def __del__(self):
        if os.path.isfile(self.file):
            os.remove(self.file)

    def detect(self):
        if os.path.isfile(self.file):
            os.remove(self.file)
        self.__capture()
        labels = self.__get_labels()
        text_en = ",".join([l['Name'] for l in labels])
        return self.__translate(text_en)

    def __capture(self):
        with picamera.PiCamera() as camera:
            camera.rotation = self.rotation
            camera.resolution = self.resolution
            camera.__capture(self.file)
            return self.file

    def __get_labels(self):
        with open(self.file, 'rb') as image:
            bytes_encoded = base64.b64encode(image.read())
            base_64_binary = base64.decodebytes(bytes_encoded)
        rekognition = boto3.client("rekognition", Vision.REGION)
        response = rekognition.detect_labels(
            Image={
                "Bytes": base_64_binary
            },
            MaxLabels=3,
            MinConfidence=90,
        )
        return response['Labels']

    def __translate(self, text_en):
        if self.language == 'en':
            return text_en
        translate_client = boto3.client(service_name='translate', region_name=Vision.REGION, use_ssl=True)
        result = translate_client.translate_text(Text=text_en, SourceLanguageCode="en", TargetLanguageCode="de")
        return result['TranslatedText']

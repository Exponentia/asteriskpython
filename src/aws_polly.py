# -*- coding: utf-8 -*-

import boto3
from pygame import mixer
import os
from pydub import AudioSegment
def text_to_voice(Text,VoiceId):
    polly = boto3.client('polly')
    spoken_text = polly.synthesize_speech(Text=Text,
                                          OutputFormat='mp3',
                                          VoiceId=VoiceId)
    
    with open('output.mp3', 'wb') as f:
        f.write(spoken_text['AudioStream'].read())
        f.close()
    sound = AudioSegment.from_mp3("output.mp3")
    sound.export("output.wav", format="wav")        


def voice_to_text(voice,VoiceId,call_slot):
    polly = boto3.client('transcribe')
    job_uri = "/home/admin1/Desktop/dev/VoIPBot/src/botresponse.wav"
    polly.start_transcription_job(TranscriptionJobName="w",Media={'MediaFileUri': job_uri},MediaFormat='wav',LanguageCode='en-US',MediaSampleRateHertz=44100     )
    spoken_text = polly.synthesize_speech(Text='I am Emma. You know me from Ivona, but now I come via Polly.',
                                          OutputFormat='wav',
                                          VoiceId='Salli')
    
    with open('output.mp3', 'wb') as f:
        f.write(spoken_text['AudioStream'].read())
        f.close()

#mixer.init()
#mixer.music.load('output.mp3')
#mixer.music.play()
#
#while mixer.music.get_busy() == True:
#    pass
#e
#mixer.quit()
#os.remove('output.mp3')
        
        
text_to_voice("Thank you that you that was nice speaking to you i Will call back at time","Raveena")

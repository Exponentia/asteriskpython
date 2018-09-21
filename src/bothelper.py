import soundfile as sf
import clipaudiomodule as ca
import bingspeechmodule as bs
import bingttsmodule as bt
import luismodule as luis
import response_checking
from pydub import AudioSegment
class BotHelper():

    def convert_audio(self):
		sound = AudioSegment.from_wav('input.wav')
		sound = sound +10
		sound.export("input.wav","wav")
		myfile = sf.SoundFile('input.wav',mode='r',format='RAW',samplerate=16000,channels=1,subtype='PCM_16')
		sf.write('converted.wav',myfile.read(),16000,subtype='PCM_16',format='WAV')

    def trim_audio(self):
		trimmer = ca.AudioTrimmer()
		# Saves trimmed audio to trimmed.wav
		trimmer.trim_audio('converted.wav') 

    def recognize_speech(self):
		spr = bs.BingSpeech('a6e2cf9447e64d4497b2715e511fc027')
		# Take from trimmed data
		res = spr.transcribe('trimmed.wav')
		print res
		return res

    def get_response(self):
		# speech to text
		translator = bt.Translator('a6e2cf9447e64d4497b2715e511fc027')
		text = self.recognize_speech()
		print text,"@#"*20

        # get bot response
#		reply = response_checking.text_got(text)
        # text to speech
		return text
#		output = translator.speak(reply, "hi-IN", "Male", "riff-16khz-16bit-mono-pcm")
#		with open("botresponse.wav", "w") as f:
#				f.write(output)

    def generate_response(self):
		self.convert_audio()
		self.trim_audio()
		answer = self.get_response()
		return answer

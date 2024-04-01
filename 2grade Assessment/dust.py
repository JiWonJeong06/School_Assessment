from gtts import gTTS
import playsound



def speak(text):

     tts = gTTS(text=text, lang='ko')

     f='dust.mp3'

     tts.save(f)

     playsound.playsound(f)



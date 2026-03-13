
import pyttsx3, sys
text = sys.argv[1]
rate = int(sys.argv[2])
vol  = float(sys.argv[3])
try:
    e = pyttsx3.init()
    e.setProperty('rate', rate)
    e.setProperty('volume', vol)
    voices = e.getProperty('voices')
    for v in voices:
        if any(k in v.name.lower() for k in ['david','mark','george','male']):
            e.setProperty('voice', v.id)
            break
    e.say(text)
    e.runAndWait()
    e.stop()
except Exception:
    pass

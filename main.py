import pywhatkit
import keyboard
import time
from datetime import datetime

contatos = ['+5511930611988', '+5511953199790', '+5511983810826', '+5511979652340', '+5511982775483', '+5511971054402', '+5511997506667', '+5511965939405',
            '+5511946337307', '+5511946119111', '+5511957629767', '+5511997437937', '+5511955527268', '+5511971079076',
            '+5511997506667', '+5511997846445', '+5511975350174', '+5511974051644', '+5511930914094', '+5511977352639',
            '+5511969286140', '+5511961821083', '+5511988211514']

while len(contatos) >= 1:
    pywhatkit.sendwhatmsg(contatos[0], 'Boa Tarde!', datetime.now().hour, datetime.now().minute + 1)
    del contatos[0]
    time.sleep(30)
    keyboard.press_and_release('ctrl+w')











import snowboydecoder
import sys
import signal
import getsound
import os
import time

import tts
import asr
import gpt


interrupted = False
model =['resources/javs.pmdl','resources/new.pmdl']

os.close(sys.stderr.fileno())

callbacks = [lambda: callbacks1(),
             lambda: callbacks2()]

def callbacks1():
    msg=[{"role": "system", "content": "你说话的语气萌萌哒，用词十分可爱"}]
    detector.terminate()
    print("检测成功!")

    os.system('aplay -D default sound/hi.wav')
    try:
        getsound.rec()
        qu=asr.getasr('sound/question.wav')
        print('问:'+qu)
        msg.append({"role": "user", "content": qu})
        if qu!='':
            an=gpt.getgpt(msg)
            print('答:'+an)
            tts.gettts(an)
            os.system('aplay -D default sound/result.wav')
    except:
        os.system('aplay -D default sound/error.wav')
        print("发生错误")

    os.system('aplay -D default sound/bye.wav')
    print("结束对话!")

    print('检测中...')
    detector.start(detected_callback=callbacks,
                interrupt_check=interrupt_callback,
                sleep_time=0.03)
    
def callbacks2():
    msg=[{"role": "system", "content": "你说话的语气萌萌哒，用词十分可爱"}]
    detector.terminate()
    print("检测成功!")

    os.system('aplay -D default sound/start.wav')
    try:
        getsound.rec()
        qu=asr.getasr('sound/question.wav')
        print('输入:'+qu)
        if '我爱你' in qu:
            os.system('aplay -D default sound/right.wav')
            for i in range(5):
                getsound.rec()
                qu=asr.getasr('sound/question.wav')
                print('问:'+qu)
                msg.append({"role": "user", "content": qu})
                if '再见' in qu: break
                if qu=='':break
                an=gpt.getgpt(msg)
                msg.append({"role": "assistant", "content": an})
                print('答:'+an)
                tts.gettts(an)
                os.system('aplay -D default sound/result.wav')
        else:
            os.system('aplay -D default sound/wrong.wav')
            print("密码错误")
    except:
        os.system('aplay -D default sound/error.wav')
        print("发生错误")
    
    os.system('aplay -D default sound/bye.wav')
    print("结束对话!")

    print('检测中...')
    detector.start(detected_callback=callbacks,
                interrupt_check=interrupt_callback,
                sleep_time=0.03)

def signal_handler(signal, frame):
    global interrupted
    interrupted = True


def interrupt_callback():
    global interrupted
    return interrupted

# capture SIGINT signal, e.g., Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

detector = snowboydecoder.HotwordDetector(model, sensitivity=0.5)
    
# main loop

print('检测中...')
detector.start(detected_callback=callbacks,
               interrupt_check=interrupt_callback,
               sleep_time=0.03)


detector.terminate()
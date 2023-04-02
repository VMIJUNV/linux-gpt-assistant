import speech_recognition as sr

#从系统麦克风拾取音频数据，采样率为 16000
def rec():
    rate=16000
    r = sr.Recognizer()
    with sr.Microphone(sample_rate=rate) as source:
        print('正在获取声音中...')
        audio = r.listen(source,timeout=3,phrase_time_limit=13)
    with open("sound/question.wav", "wb") as f:
        f.write(audio.get_wav_data())
        print('声音获取完成.')

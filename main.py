import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
from googletrans import Translator
import random

admin= "eşek"
yanlis=0
zorluk_seviyesi = input("Bir zorluk seviyesi seçin: kolay, orta, zor ")

kelimeler = {
    "kolay": ["bardak", "kitap", "elma", "su", "masa"],
    "orta": ["bilgisayar", "telefon", "araba", "ev", "şehir"],
    "zor": ["ray", "limon", "kamera", "telefon", "bilgisayar"]
}

if zorluk_seviyesi=="kolay":
    kelime = random.choice(kelimeler["kolay"])
    print("Seçilen kelime:", kelime)
elif zorluk_seviyesi=="orta":
    kelime = random.choice(kelimeler["orta"])
    print("Seçilen kelime:", kelime)
elif zorluk_seviyesi=="zor":
    kelime = random.choice(kelimeler["zor"])
    print("Seçilen kelime:", kelime)
else:
    print("hata")

duration = 5  # Duration of recording in seconds
sample_rate = 44100  # Sample rate in Hz
while True:
    print("Şimdi konuşun...")
    recording = sd.rec(
    int(duration * sample_rate), # kaydedilecek örnek sayısı
    samplerate=sample_rate,      # örnekleme hızı
    channels=1,                  # 1, mono kayıt anlamına gelir.
    dtype="int16")               # kayıtlı örnekler için veri türü
    sd.wait()  # kayıt bitene kadar beklemek

    wav.write("output.wav", sample_rate, recording)
    print("Kayıt tamamlandı, şimdi tanıma işlemi devam ediyor...")

    recognizer = sr.Recognizer()
    with sr.AudioFile("output.wav") as source:
        audio = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio, language="en")
        print("Şunu söylediniz:", text)
        translator = Translator()
        translated = translator.translate(text, dest="tr")  # buradaki 'es' İspanyolca için bir koddur
        if translated.text == kelime:
            print("Tebrikler! Doğru kelimeyi söylediniz🥳.")
            break
        elif translated.text == admin:
            print(f"Admin olduğun onaylandı.☠️☠️☠️☠️☠️☠️☠️☠️☠️ Oyun tamamlandı.")
            break
        else:
            yanlis += 1
            print(f"Yanlış kelime😥.")
        if yanlis >= 3:
            print("3 yanlış deneme yaptınız. Oyun sona erdi😾.")
            break

    except sr.UnknownValueError:             # - Google gürültü veya sessizlik nedeniyle konuşmayı anlayamadığında
        print("Konuşma tanınamadı.")
    except sr.RequestError as e:             # - İnternet bağlantısı yoksa veya API kullanılamıyorsa
        print(f"Hizmet hatası: {e}")

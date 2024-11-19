import speech_recognition as sr
import cv2
import threading 
import time 
import msvcrt
import shutil
import unicodedata

unicode_to_vni = {
    'À': 'A2', 'Á': 'A1', 'Ả': 'A3', 'Ã': 'A4', 'Ạ': 'A5',
    'Â': 'A6', 'Ầ': 'A62', 'Ấ': 'A61', 'Ẩ': 'A63', 'Ẫ': 'A64', 'Ậ': 'A65',
    'Ă': 'A8', 'Ằ': 'A82', 'Ắ': 'A81', 'Ẳ': 'A83', 'Ẵ': 'A84', 'Ặ': 'A85',
    'È': 'E2', 'É': 'E1', 'Ẻ': 'E3', 'Ẽ': 'E4', 'Ẹ': 'E5',
    'Ê': 'E6', 'Ề': 'E62', 'Ế': 'E61', 'Ể': 'E63', 'Ễ': 'E64', 'Ệ': 'E65',
    'Ì': 'I2', 'Í': 'I1', 'Ỉ': 'I3', 'Ĩ': 'I4', 'Ị': 'I5',
    'Ò': 'O2', 'Ó': 'O1', 'Ỏ': 'O3', 'Õ': 'O4', 'Ọ': 'O5',
    'Ô': 'O6', 'Ồ': 'O62', 'Ố': 'O61', 'Ổ': 'O63', 'Ỗ': 'O64', 'Ộ': 'O65',
    'Ơ': 'O7', 'Ờ': 'O72', 'Ớ': 'O71', 'Ở': 'O73', 'Ỡ': 'O74', 'Ợ': 'O75',
    'Ù': 'U2', 'Ú': 'U1', 'Ủ': 'U3', 'Ũ': 'U4', 'Ụ': 'U5',
    'Ư': 'U7', 'Ừ': 'U72', 'Ứ': 'U71', 'Ử': 'U73', 'Ữ': 'U74', 'Ự': 'U75',
    'Ỳ': 'Y2', 'Ý': 'Y1', 'Ỷ': 'Y3', 'Ỹ': 'Y4', 'Ỵ': 'Y5', "Đ": "D9"
}

old_image_path = 'video call/video.mp4'

vocab = ["BỆNH", "BỆNHVIỆN", "CÔNG", "CÔNGAN", "BÁC", "BÁCSĨ", "ĐÚNG", "THUỐC", "XIN", "XINLỖI"]
vocab_final =["BENHVIEN", "CONGAN", "THUOC", "XINLOI", "DUNG", "BENH", "BACSI"]

def doit(sentence):
    print(sentence)
    final = []
    tu = sentence.split()
    tu.append('abc')  # Call the split method with parentheses
    a = ''
    b = ''
    for char in tu:
        word_final = '' 
        a += char
        if a in vocab:
            b += char
        else:
            text_normalized = unicodedata.normalize('NFD', b)
            b = ''.join(c for c in text_normalized if unicodedata.category(c) != 'Mn')
            final.append(b)
            a = ''
            b = ''
        if a not in vocab:
            for x in char:
                if x in unicode_to_vni:
                    word_final += unicode_to_vni[x]
                else:
                    word_final += x
            final.append(word_final)
            a = ''
    final = [x for x in final if x != '']
    if final and final[-1] == 'abc':
        final.pop()
    print(final)

    for x in final:
        if x in vocab_final:
            video_path = "C:/Users/TechCare/Desktop/ai python/VSL_new/" + x.lower() + ".mp4"
            shutil.copy(video_path, old_image_path)
            time.sleep(2)
            print(video_path)
        else:
            i = 0 
            while i < len(x):
                print(x[i])
                video_path = "VSL_new/" + x[i].lower() + ".mp4"
                shutil.copy(video_path, old_image_path)
                time.sleep(2)
                print(video_path)
                i += 1
    video_path = "C:/Users/TechCare/Desktop/ai python/VSL_new/transparent.mp4"
    shutil.copy(video_path, old_image_path)
    
def speech_to_text_realtime():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    # Mở microphone và bắt đầu lắng nghe
    with microphone as source:
        print("Bắt đầu lắng nghe...")
        audio_stream = recognizer.listen(source)

    # Sử dụng thư viện SpeechRecognition để chuyển đổi giọng nói thành văn bản
    try:
        text = recognizer.recognize_google(audio_stream, language='vi-VN').split(" ")
        print("Đã nghe được:", recognizer.recognize_google(audio_stream, language='vi-VN'))
        return text
    except sr.UnknownValueError:
        print("Không nhận diện được giọng nói")
        return False
    except sr.RequestError as e:
        print("Lỗi trong quá trình kết nối: {0}".format(e))
        return False

def main_loop():
    while True:
        text = speech_to_text_realtime()
        
        # Check if text is a list (successful speech recognition)
        if isinstance(text, list):
            sentence1 = ' '.join(text) + ' '
            doit(sentence1.upper())
        else:
            print("Không có văn bản hợp lệ để xử lý.")
main_loop()
from flask import Flask, render_template, request, redirect
import speech_recognition as sr


from app import app

from googletrans import Translator
translator = Translator()


# result = translator.translate('Mikä on nimesi', src='fi', dest='fr')

lang_dict = {
    'af': 'afrikaans', 'sq': 'albanian', 'am': 'amharic', 'ar': 'arabic', 'hy': 'armenian', 
    'az': 'azerbaijani', 'eu': 'basque', 'be': 'belarusian', 'bn': 'bengali', 'bs': 'bosnian', 
    'bg': 'bulgarian', 'ca': 'catalan', 'ceb': 'cebuano', 'ny': 'chichewa', 'zh-cn': 'chinese (simplified)', 
    'zh-tw': 'chinese (traditional)', 'co': 'corsican', 'hr': 'croatian', 'cs': 'czech', 'da': 'danish', 
    'nl': 'dutch', 'en': 'english', 'eo': 'esperanto', 'et': 'estonian', 'tl': 'filipino', 'fi': 'finnish', 
    'fr': 'french', 'fy': 'frisian', 'gl': 'galician', 'ka': 'georgian', 'de': 'german', 'el': 'greek', 
    'gu': 'gujarati', 'ht': 'haitian creole', 'ha': 'hausa', 'haw': 'hawaiian', 'iw': 'hebrew', 
    'hi': 'hindi', 'hmn': 'hmong', 'hu': 'hungarian', 'is': 'icelandic', 'ig': 'igbo', 'id': 'indonesian', 
    'ga': 'irish', 'it': 'italian', 'ja': 'japanese', 'jw': 'javanese', 'kn': 'kannada', 'kk': 'kazakh', 
    'km': 'khmer', 'ko': 'korean', 'ku': 'kurdish (kurmanji)','ky': 'kyrgyz', 'lo': 'lao', 'la': 'latin', 
    'lv': 'latvian', 'lt': 'lithuanian', 'lb': 'luxembourgish', 'mk': 'macedonian', 'mg': 'malagasy', 
    'ms': 'malay', 'ml': 'malayalam', 'mt': 'maltese', 'mi': 'maori', 'mr': 'marathi', 'mn': 'mongolian', 
    'my': 'myanmar (burmese)', 'ne': 'nepali', 'no': 'norwegian', 'ps': 'pashto', 'fa': 'persian', 'pl': 'polish', 
    'pt': 'portuguese', 'pa': 'punjabi', 'ro': 'romanian', 'ru': 'russian', 'sm': 'samoan', 'gd': 'scots gaelic', 
    'sr': 'serbian', 'st': 'sesotho', 'sn': 'shona', 'sd': 'sindhi', 'si': 'sinhala', 'sk': 'slovak', 'sl': 'slovenian', 
    'so': 'somali', 'es': 'spanish', 'su': 'sundanese', 'sw': 'swahili', 'sv': 'swedish', 'tg': 'tajik', 'ta': 'tamil', 
    'te': 'telugu', 'th': 'thai', 'tr': 'turkish', 'uk': 'ukrainian', 'ur': 'urdu', 'uz': 'uzbek', 'vi': 'vietnamese', 
    'cy': 'welsh', 'xh': 'xhosa', 'yi': 'yiddish', 'yo': 'yoruba', 'zu': 'zulu', 'fil': 'Filipino', 'he': 'Hebrew'
}


transcript = ""

# TRANSLATE FUNCTION
def translate_text(audio_text):
    english = translator.translate(audio_text, dest='en')
    swahili = translator.translate(audio_text, dest='sw')
    chinese = translator.translate(audio_text, dest='zh-cn')
    japanese = translator.translate(audio_text, dest='ja')
    spanish = translator.translate(audio_text, dest='es')
    return english.text,swahili.text,chinese.text, japanese.text, spanish.text


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/transcribe", methods=["GET", "POST"])
def transcribe():
    global transcript
    if request.method == "POST":
        print("FORM DATA RECEIVED")

        if "file" not in request.files:
            return redirect(request.url)

        file = request.files["file"]
        if file.filename == "":
            return redirect(request.url)

        if file:
            recognizer = sr.Recognizer()
            audioFile = sr.AudioFile(file)
            with audioFile as source:
                recognizer.adjust_for_ambient_noise(source)
                data = recognizer.record(source)
                
            transcript = recognizer.recognize_google(data, key=None)
            print("audio transcribed to text complete")

    return render_template('transcribe.html', transcript=transcript)



@app.route('/language_table', methods= ['GET','POST'])
def language_table():
    english,swahili, chinese, japanese, spanish = translate_text(transcript)
    return render_template("language_table.html",english=english,swahili=swahili,chinese=chinese,japanese=japanese,spanish=spanish)
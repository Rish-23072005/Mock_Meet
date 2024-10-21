### General Imports
import numpy as np
import pandas as pd
import time
import os
from collections import Counter
import speech_recognition as sr
from pydub import AudioSegment

### Flask imports
from flask import Flask, render_template, session, request, redirect, flash, send_file, Response

### Audio imports ###
from library.speech_emotion_recognition import *

# Flask config
app = Flask(__name__)
app.secret_key = b'(\xee\x00\xd4\xce"\xcf\xe8@\r\xde\xfc\xbdJ\x08W'
app.config['UPLOAD_FOLDER'] = 'tmp'

################################################################################
################################## INDEX #######################################
################################################################################

# Home page
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# Audio Index
@app.route('/audio_index', methods=['POST'])
def audio_index():
    # Flash message
    flash("After pressing the button above, you will have 15 seconds to answer the question.")
    return render_template('audio.html', display_button=False)

# Audio Recording
@app.route('/audio_recording', methods=("POST", "GET"))
def audio_recording():
    # Instantiate new SpeechEmotionRecognition object
    SER = speechEmotionRecognition()

    # Voice Recording
    rec_duration = 16 
    rec_sub_dir = os.path.join(app.config['UPLOAD_FOLDER'], 'voice_recording.wav')
    SER.voice_recording(rec_sub_dir, duration=rec_duration)

    # Send Flash message
    flash("The recording is over! You now have the opportunity to do an analysis of your emotions. If you wish, you can also choose to record yourself again.")
    return render_template('audio.html', display_button=True)

# Audio Emotion Analysis
@app.route('/audio_dash', methods=("POST", "GET"))
def audio_dash():
    try:
        # Sub dir to speech emotion recognition model
        model_sub_dir = os.path.join('Models', 'audio.hdf5')

        # Instantiate new SpeechEmotionRecognition object
        SER = speechEmotionRecognition(model_sub_dir)

        # Voice Record sub dir
        rec_sub_dir = os.path.join(app.config['UPLOAD_FOLDER'], 'voice_recording.wav')

        # Predict emotion in voice at each time step
        step = 1 # in sec
        sample_rate = 16000 # in kHz
        emotions, timestamp = SER.predict_emotion_from_file(rec_sub_dir, chunk_step=step*sample_rate)

        if emotions is None or not emotions:
            flash("No emotions detected in the audio recording.")
            return render_template('audio_dash.html', emo=None, prob=[])

        # Export predicted emotions to .txt format
        emotions_file = os.path.join("static/js/db", "audio_emotions.txt")
        SER.prediction_to_csv(emotions, emotions_file, mode='w')

        # Get most common emotion during the interview
        major_emotion = max(set(emotions), key=emotions.count)

        # Calculate emotion distribution
        emotion_dist = [int(100 * emotions.count(emotion) / len(emotions)) for emotion in SER._emotion.values()]

        # Export emotion distribution to .csv format for D3JS
        df = pd.DataFrame(emotion_dist, index=SER._emotion.values(), columns=['VALUE']).rename_axis('EMOTION')
        df.to_csv(os.path.join('static/js/db', 'audio_emotions_dist.txt'), sep=',')

        # Sleep
        time.sleep(0.5)

        return render_template('audio_dash.html', emo=major_emotion, prob=emotion_dist)
    except Exception as e:
        flash(f"An error occurred: {str(e)}")
        return render_template('audio_dash.html', emo=None, prob=[])

# Download Recorded Audio
@app.route('/download_audio', methods=['GET'])
def download_audio():
    audio_path = os.path.join(app.config['UPLOAD_FOLDER'], 'voice_recording.wav')
    try:
        return send_file(audio_path, as_attachment=True)
    except Exception as e:
        flash(f"An error occurred while trying to download the audio file: {str(e)}")
        return redirect('/')

# View Emotions File
@app.route('/view_emotions', methods=['GET'])
def view_emotions():
    try:
        emotions_file = os.path.join("static/js/db", "audio_emotions.txt")
        with open(emotions_file, 'r') as f:
            emotions_data = f.read()
        return Response(emotions_data, mimetype='text/plain')
    except Exception as e:
        flash(f"An error occurred while trying to view the emotions file: {str(e)}")
        return redirect('/')

# Convert Audio to Text
@app.route('/audio_to_text', methods=['GET'])
def audio_to_text():
    audio_path = os.path.join(app.config['UPLOAD_FOLDER'], 'voice_recording.wav')
    recognizer = sr.Recognizer()
    try:
        audio = AudioSegment.from_wav(audio_path)
        audio.export(audio_path.replace('.wav', '.flac'), format='flac')
        with sr.AudioFile(audio_path.replace('.wav', '.flac')) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
            return Response(text, mimetype='text/plain')
    except Exception as e:
        flash(f"An error occurred while trying to convert audio to text: {str(e)}")
        return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)

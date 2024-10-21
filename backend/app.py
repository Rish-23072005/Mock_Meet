from __future__ import division
# Import necessary modules from flask
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session, Response
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import DataRequired, Length, Regexp
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, LoginManager, login_required, current_user, logout_user
from flask_cors import CORS
from flask_socketio import SocketIO, emit, join_room
from authlib.integrations.flask_client import OAuth
import os
import json
import time
import pandas as pd
from library.speech_emotion_recognition import speechEmotionRecognition  # Assuming correct import
from datetime import datetime
from werkzeug.utils import secure_filename
import tempfile
import glob

### General imports ###
import numpy as np
import pandas as pd
import time
import re

from collections import Counter
import altair as alt
from keras.models import load_model
from keras.preprocessing.image import img_to_array
import threading
from pathlib import Path
import cv2

### Flask imports
import requests
from flask import Flask, render_template, session, request, redirect, flash, Response

### Audio imports ###
from library.speech_emotion_recognition import *

### Video imports ###
from library.video_emotion_recognition import *
from flask import Flask, request, jsonify  # Ensure jsonify is imported
from library.speech_emotion_recognition import speechEmotionRecognition


# Initialize Flask
app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = "c1501ed11a0cc8ef5f3e7e8b3260d12f"

# Initialize SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///initial-meet.db"
db = SQLAlchemy(app)
# db = SQLAlchemy()

app.config['UPLOAD_FOLDER'] = 'audio'
app.secret_key = b'(\xee\x00\xd4\xce"\xcf\xe8@\r\xde\xfc\xbdJ\x08W'
app.config['UPLOAD_FOLDER'] = '/Upload'

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

# Initialize SocketIO
socketio = SocketIO(app)



# In-memory rooms structure
rooms = {}

# User loader callback for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return Register.query.get(int(user_id))

# Define User model
class Register(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def is_active(self):
        return True
    
    def get_id(self):
        return str(self.id)
    
    def is_authenticated(self):
        return True
    

# Define Meeting model
class Meeting(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    meeting_id = db.Column(db.String, unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    participants = db.relationship("Participant", back_populates="meeting")

# Define Participant model
class Participant(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    meeting_id = db.Column(db.Integer, db.ForeignKey('meeting.id'), nullable=False)
    participant_id = db.Column(db.String, nullable=False)
    audio_file_path = db.Column(db.String, nullable=False)
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime)
    meeting = db.relationship("Meeting", back_populates="participants")



# Create all database tables
with app.app_context():
    db.create_all()

# Define RegistrationForm
class RegistrationForm(FlaskForm):
    email = EmailField(label='Email', validators=[DataRequired()])
    username = StringField(label="Username", validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField(label="Password", validators=[DataRequired(), Length(min=8, max=120), Regexp('^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$',
               message="Password should have at least one uppercase letter, one lowercase letter, one number, and one special character")])

# Define LoginForm
class LoginForm(FlaskForm):
    email = EmailField(label='Email', validators=[DataRequired()])
    password = PasswordField(label="Password", validators=[DataRequired()])


# class AudioRecording(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     meeting_id = db.Column(db.Integer, db.ForeignKey('meeting.id'), nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('register.id'), nullable=False)
#     audio_file_path = db.Column(db.String(120), nullable=False)

#     user = db.relationship('Register', backref='audio_recordings')
#     meeting = db.relationship('Meeting', backref='audio_recordings')

# class Meeting(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     room_id = db.Column(db.String(50), nullable=False)  # Unique room identifier
#     created_at = db.Column(db.DateTime, default=db.func.current_timestamp())


# @app.route('/view-users', methods=['GET'])
# @login_required  # Optional: restrict access to logged-in users
# def view_users():
#     users = Register.query.all()
#     user_list = [{"ID": user.id, "Username": user.username, "Email": user.email} for user in users]
#     return jsonify(user_list)


# Home route with OAuth and session integration
@app.route("/")
def home():
    return render_template("landing.html", session=session.get("user"), pretty=json.dumps(session.get("user"), indent=4))


# Define route for login page
@app.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if request.method == "POST" and form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = Register.query.filter_by(email=email, password=password).first()
        if user:
            login_user(user)
            return redirect(url_for("dashboard"))
    return render_template("login.html", form=form)

# Define route for logout
@app.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    flash("You have been logged out successfully! Thank you for using MockMeet!", "info")
    return redirect(url_for("login"))

# Define route for registration page
@app.route("/register", methods=["POST", "GET"])
def register():
    form = RegistrationForm()
    if request.method == "POST" and form.validate_on_submit():
        new_user = Register(
            email=form.email.data,
            username=form.username.data,
            password=form.password.data
        )
        db.session.add(new_user)
        db.session.commit()
        flash("Account created Successfully! <br>Now you can log in.", "success")
        return redirect(url_for("login"))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{error}", "danger")
    return render_template("register.html", form=form)

# Define route for dashboard
@app.route("/dashboardMeet")
@login_required
def dashboard():
    return render_template("dashboardMeet.html", username=current_user.username)

# Define route for meeting
# @app.route("/mockmeet")
# @login_required
# def meeting():
#     return render_template("meeting.html", username=current_user.username)


# Define route for meeting
@app.route("/mockmeet")
@login_required
def meeting():
    room_id = request.args.get('roomID')
    if room_id:
        save_meeting_data(room_id, current_user.username, None)
    return render_template("meeting.html", username=current_user.username)


# Define route for join
@app.route("/join", methods=['GET', 'POST'])
@login_required
def join():
    if request.method == "POST":
        room_id = request.form.get("roomID")
        return redirect(f"/mockmeet?roomID={room_id}")
    return render_template("join.html")


# Utility function to save participant audio data
def save_meeting_data(meeting_id, participant_id, audio_file_path=None):
    # Check if the meeting already exists, if not create it
    meeting = Meeting.query.filter_by(meeting_id=meeting_id).first()
    if not meeting:
        meeting = Meeting(meeting_id=meeting_id)
        db.session.add(meeting)
        db.session.commit()

    # Save the participant audio recording metadata if the audio_file_path is provided
    if audio_file_path:
        participant = Participant(
            meeting_id=meeting.id,
            participant_id=participant_id,
            audio_file_path=audio_file_path,
            start_time=datetime.utcnow()
        )
        db.session.add(participant)
        db.session.commit()



    # Define route to view database data


@app.route('/upload-audio', methods=['POST'])
def upload_audio():
    if 'audio_file' not in request.files:
        return 'No audio file found', 400

    audio_file = request.files['audio_file']
    
    # Set the custom directory where the audio file should be saved
    custom_dir = r'F:\MY-PROJECTS\MockMate Final\MockMate\backend\tmp'
    
    # Ensure the directory exists
    os.makedirs(custom_dir, exist_ok=True)

    # Remove all previous audio files in the folder
    for file_path in glob.glob(os.path.join(custom_dir, '*.wav')):
        try:
            os.remove(file_path)
        except Exception as e:
            print(f'Error deleting file {file_path}: {str(e)}')

    # Set the file path for the audio file with a fixed name
    audio_file_path = os.path.join(custom_dir, 'voice_recording.wav')

    # Save the audio file in the custom directory
    try:
        audio_file.save(audio_file_path)
        print(f'Audio file saved at: {audio_file_path}')  # Print the file path
        return 'Audio file saved successfully', 200
    except Exception as e:
        return f'Error saving audio file: {str(e)}', 500
    


    # Audio Index
@app.route('/audio_index', methods=['POST'])
def audio_index():

    # Flash message
    flash("After pressing the button above, you will have 15sec to answer the question.")

    return render_template('audio.html', display_button=False)


@app.route('/audio_recording', methods=["POST"])
def audio_recording():
    data = request.json
    room_id = data.get('roomID')
    user_id = data.get('userID')
    user_name = data.get('userName')

    # Add your audio recording logic here
    print(f"Starting audio recording for Room ID: {room_id}, User ID: {user_id}, User Name: {user_name}")

    try:
        # Instantiate new SpeechEmotionRecognition object
        SER = speechEmotionRecognition()

        # Voice Recording
        rec_duration = 16  # in seconds
        
        # Specify the directory and file path
        tmp_dir = r'D:\MockMate\MockMate\backend\tmp'
        rec_sub_dir = os.path.join(tmp_dir, 'voice_recording.wav')

        # Ensure the directory exists
        if not os.path.exists(tmp_dir):
            os.makedirs(tmp_dir)

        # Start voice recording
        SER.voice_recording(rec_sub_dir, duration=rec_duration)

        # Return a success response
        return jsonify({"status": "success", "message": "Recording is completed. You can now analyze your emotions."}), 200
    
    except Exception as e:
        # Handle exceptions
        print(f"Error during recording: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/prep_recording', methods=["POST"])
def prep_recording():
    

    try:
        # Instantiate new SpeechEmotionRecognition object
        SER = speechEmotionRecognition()

        # Voice Recording
        rec_duration = 10  # in seconds
        
        # Specify the directory and file path
        tmp_dir = r'D:\MockMate\MockMate\backend\tmp2' 
        rec_sub_dir = os.path.join(tmp_dir, 'voice_recording.wav')

        # Ensure the directory exists
        if not os.path.exists(tmp_dir):
            os.makedirs(tmp_dir)

        # Start voice recording
        SER.voice_recording(rec_sub_dir, duration=rec_duration)

        # Return a success response
        return jsonify({"status": "success", "message": "Recording is completed. You can now analyze your emotions."}), 200
    
    except Exception as e:
        # Handle exceptions
        print(f"Error during recording: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


    


# Audio Emotion Analysis
@app.route('/audiodash', methods=("POST", "GET"))
def audiodash():

    # Sub dir to speech emotion recognition model
    model_sub_dir = os.path.join('Models', 'audio.hdf5')

    # Instanciate new SpeechEmotionRecognition object
    SER = speechEmotionRecognition(model_sub_dir)

    # Voice Record sub dir
    rec_sub_dir = os.path.join('tmp','voice_recording.wav')

    # Predict emotion in voice at each time step
    step = 1 # in sec
    sample_rate = 16000 # in kHz
    emotions, timestamp = SER.predict_emotion_from_file(rec_sub_dir, chunk_step=step*sample_rate)

    # Export predicted emotions to .txt format
    SER.prediction_to_csv(emotions, os.path.join("static/js/db", "audio_emotions.txt"), mode='w')
    SER.prediction_to_csv(emotions, os.path.join("static/js/db", "audio_emotions_other.txt"), mode='a')

    # Get most common emotion during the interview
    major_emotion = max(set(emotions), key=emotions.count)

    # Calculate emotion distribution
    emotion_dist = [int(100 * emotions.count(emotion) / len(emotions)) for emotion in SER._emotion.values()]

    # Export emotion distribution to .csv format for D3JS
    df = pd.DataFrame(emotion_dist, index=SER._emotion.values(), columns=['VALUE']).rename_axis('EMOTION')
    df.to_csv(os.path.join('static/js/db','audio_emotions_dist.txt'), sep=',')

    # Get most common emotion of other candidates
    df_other = pd.read_csv(os.path.join("static/js/db", "audio_emotions_other.txt"), sep=",")

  


    # Get most common emotion during the interview for other candidates
    major_emotion_other = df_other.EMOTION.mode()[0]

    


    # Calculate emotion distribution for other candidates
    emotion_dist_other = [int(100 * len(df_other[df_other.EMOTION==emotion]) / len(df_other)) for emotion in SER._emotion.values()]

    # Export emotion distribution to .csv format for D3JS
    df_other = pd.DataFrame(emotion_dist_other, index=SER._emotion.values(), columns=['VALUE']).rename_axis('EMOTION')
    df_other.to_csv(os.path.join('static/js/db','audio_emotions_dist_other.txt'), sep=',')

    # Sleep
    time.sleep(0.5)

    return render_template('audiodash.html', emo=major_emotion, emo_other=major_emotion_other, prob=emotion_dist, prob_other=emotion_dist_other)


# Audio Emotion Analysis
@app.route('/prep_audiodash', methods=("POST", "GET"))
def  prepaudiodash():

    # Sub dir to speech emotion recognition model
    model_sub_dir = os.path.join('Models', 'audio.hdf5')

    # Instanciate new SpeechEmotionRecognition object
    SER = speechEmotionRecognition(model_sub_dir)

    # Voice Record sub dir
    rec_sub_dir = os.path.join('tmp2','voice_recording.wav')

    # Predict emotion in voice at each time step
    step = 1 # in sec
    sample_rate = 16000 # in kHz
    emotions, timestamp = SER.predict_emotion_from_file(rec_sub_dir, chunk_step=step*sample_rate)

    # Export predicted emotions to .txt format
    SER.prediction_to_csv(emotions, os.path.join("static/js/db", "audio_emotions.txt"), mode='w')
    SER.prediction_to_csv(emotions, os.path.join("static/js/db", "audio_emotions_other.txt"), mode='a')

    # Get most common emotion during the interview
    major_emotion = max(set(emotions), key=emotions.count)

    # Calculate emotion distribution
    emotion_dist = [int(100 * emotions.count(emotion) / len(emotions)) for emotion in SER._emotion.values()]

    # Export emotion distribution to .csv format for D3JS
    df = pd.DataFrame(emotion_dist, index=SER._emotion.values(), columns=['VALUE']).rename_axis('EMOTION')
    df.to_csv(os.path.join('static/js/db','audio_emotions_dist.txt'), sep=',')

    # Get most common emotion of other candidates
    df_other = pd.read_csv(os.path.join("static/js/db", "audio_emotions_other.txt"), sep=",")

  


    # Get most common emotion during the interview for other candidates
    major_emotion_other = df_other.EMOTION.mode()[0]

    


    # Calculate emotion distribution for other candidates
    emotion_dist_other = [int(100 * len(df_other[df_other.EMOTION==emotion]) / len(df_other)) for emotion in SER._emotion.values()]

    # Export emotion distribution to .csv format for D3JS
    df_other = pd.DataFrame(emotion_dist_other, index=SER._emotion.values(), columns=['VALUE']).rename_axis('EMOTION')
    df_other.to_csv(os.path.join('static/js/db','audio_emotions_dist_other.txt'), sep=',')

    # Sleep
    time.sleep(0.5)

    return render_template('audiodash.html', emo=major_emotion, emo_other=major_emotion_other, prob=emotion_dist, prob_other=emotion_dist_other)


# Interview questions for different positions
QUESTIONS = {
    "Frontend Developer": [
        "What are the main features of React?",
        "How do you manage state in a React application?",
        "What is the difference between CSS Grid and Flexbox?"
    ],
    "Backend Developer": [
        "What are RESTful APIs?",
        "Explain the MVC architecture.",
        "How do you handle database migrations?"
    ],
    "Full Stack Developer": [
        "Describe the MERN stack.",
        "How do you ensure security in a web application?",
        "What is your approach to debugging?"
    ]
}

@app.route('/get-questions', methods=['POST'])
def get_questions():
    data = request.json
    position = data.get('position')
    questions = QUESTIONS.get(position, [])
    return jsonify(questions)

# # Audio Interview Routes
# @app.route('/audio', methods=['POST'])
# def audio_index():
#     flash("After pressing the button above, you will have 15 seconds to answer the question.")
#     return render_template('audio.html', display_button=False)

# @app.route('/audio_interview', methods=["POST", "GET"])
# def audio_recording():
#     try:
#         SER = speechEmotionRecognition()
#         rec_duration = 16
#         rec_sub_dir = os.path.join('tmp', 'voice_recording.wav')
#         SER.voice_recording(rec_sub_dir, duration=rec_duration)
#         flash("The recording is over! Analyze your emotions or record again.")
#         return render_template('audio.html', display_button=True)
#     except Exception as e:
#         print(f"Error in audio_recording: {str(e)}")
#         return None

# @app.route('/audio_dash', methods=["POST", "GET"])
# def audio_dash():
#     try:
#         model_sub_dir = os.path.join('Models', 'audio.hdf5')
#         SER = speechEmotionRecognition(model_sub_dir)
#         rec_sub_dir = os.path.join('tmp', 'voice_recording.wav')
#         step = 1
#         sample_rate = 16000
#         emotions, timestamp = SER.predict_emotion_from_file(rec_sub_dir, chunk_step=step * sample_rate)
#         SER.prediction_to_csv(emotions, os.path.join("static/js/db", "audio_emotions.txt"), mode='w')
#         SER.prediction_to_csv(emotions, os.path.join("static/js/db", "audio_emotions_other.txt"), mode='a')

#         major_emotion = max(set(emotions), key=emotions.count)
#         emotion_dist = [int(100 * emotions.count(emotion) / len(emotions)) for emotion in SER._emotion.values()]
#         df = pd.DataFrame(emotion_dist, index=SER._emotion.values(), columns=['VALUE']).rename_axis('EMOTION')
#         df.to_csv(os.path.join('static/js/db', 'audio_emotions_dist.txt'), sep=',')

#         df_other = pd.read_csv(os.path.join("static/js/db", "audio_emotions_other.txt"), sep=",")
#         major_emotion_other = df_other.EMOTION.value_counts().idxmax()
#         flash(f"The major emotion of your speech is: {major_emotion}")
#         flash(f"The major emotion of the whole dataset is: {major_emotion_other}")
#     except Exception as e:
#         print(f"Error in audio_dash: {str(e)}")
#     return render_template('audio_dash.html', emotions=emotions, timestamp=timestamp)

################################################################################
############################### VIDEO INTERVIEW ################################
################################################################################

# Load the pre-trained model and cascade classifier
face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
classifier = load_model('FER_model.h5')
emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']

# Global variables for video streaming
frame_lock = threading.Lock()
current_frame = None
# Read the overall dataframe before the user starts to add his own data
# df = pd.read_csv('static/js/db/histo.txt', sep=",")
def detect_emotions(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray, 1.3, 1)
    
    for (x, y, w, h) in faces:
        roi_gray = gray[y:y + h, x:x + w]
        roi_gray = cv2.resize(roi_gray, (48, 48), interpolation=cv2.INTER_AREA)
        if np.sum([roi_gray]) != 0:
            roi = roi_gray.astype('float') / 255.0
            roi = img_to_array(roi)
            roi = np.expand_dims(roi, axis=0)
            prediction = classifier.predict(roi)[0]
            label = emotion_labels[prediction.argmax()]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, label, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    return frame
def generate_frames():
    global current_frame
    cap = cv2.VideoCapture(0)  # Change to your webcam index if needed
    
    while True:
        success, frame = cap.read()
        if not success:
            break
        
        # Lock the current frame
        with frame_lock:
            current_frame = detect_emotions(frame)

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + 
               cv2.imencode('.jpg', current_frame)[1].tobytes() + 
               b'\r\n')
        
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


# Run Flask app
if __name__ == "__main__":
    socketio.run(app, debug=True)

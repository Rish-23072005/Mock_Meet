from __future__ import division

# Import necessary modules from flask

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import DataRequired, Length, Regexp
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, LoginManager, login_required, current_user, logout_user
from datetime import datetime
from werkzeug.utils import secure_filename
import os
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




# Initialize SQLAlchemy
db = SQLAlchemy()

# Initialize Flask
app = Flask(__name__)

# Configure Flask app
app.config['SECRET_KEY'] = "c1501ed11a0cc8ef5f3e7e8b3260d12f"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///initial-meet.db"
app.config['UPLOAD_FOLDER'] = 'audio'
app.secret_key = b'(\xee\x00\xd4\xce"\xcf\xe8@\r\xde\xfc\xbdJ\x08W'
app.config['UPLOAD_FOLDER'] = '/Upload'


# Initialize SQLAlchemy with this Flask app
db.init_app(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

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




# Define route for homepage
@app.route("/")
def home():
    return redirect(url_for("login"))

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
    flash("You have been logged out successfully! Thank you for using Initial Meet!", "info")
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
@app.route("/meeting")
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
        return redirect(f"/meeting?roomID={room_id}")
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
    custom_dir = r'F:\MY-PROJECTS\MockMate Final\MockMate\backend\Initial Meet\tmp'
    
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
        tmp_dir = r'F:\MY-PROJECTS\MockMate Final\MockMate\backend\Initial Meet\tmp'
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
        
        
# Video interview template
@app.route('/video', methods=['POST'])
def video() :
    # Display a warning message
    flash('You will have 45 seconds to discuss the topic mentioned above. Due to restrictions, we are not able to redirect you once the video is over. Please move your URL to /video_dash instead of /video_1 once over. You will be able to see your results then.')
    return render_template('video.html')

# Display the video flow (face, landmarks, emotion)
# @app.route('/video_1', methods=['POST'])
# def video_1() :
#     try :
#         # Response is used to display a flow of information
#         return Response(gen(),mimetype='multipart/x-mixed-replace; boundary=frame')
#     #return Response(stream_template('video.html', gen()))
#     except :
#         return None
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


# Dashboard
@app.route('/video_dash', methods=("POST", "GET"))
def video_dash():

    # Load personal history
    df_2 = pd.read_csv('static/js/db/histo_perso.txt')


    def emo_prop(df_2) :
        return [int(100*len(df_2[df_2.density==0])/len(df_2)),
                    int(100*len(df_2[df_2.density==1])/len(df_2)),
                    int(100*len(df_2[df_2.density==2])/len(df_2)),
                    int(100*len(df_2[df_2.density==3])/len(df_2)),
                    int(100*len(df_2[df_2.density==4])/len(df_2)),
                    int(100*len(df_2[df_2.density==5])/len(df_2)),
                    int(100*len(df_2[df_2.density==6])/len(df_2))]

    emotions = ["Angry", "Disgust", "Fear",  "Happy", "Sad", "Surprise", "Neutral"]
    emo_perso = {}
    emo_glob = {}

    for i in range(len(emotions)) :
        emo_perso[emotions[i]] = len(df_2[df_2.density==i])
        emo_glob[emotions[i]] = len(df[df.density==i])

    df_perso = pd.DataFrame.from_dict(emo_perso, orient='index')
    df_perso = df_perso.reset_index()
    df_perso.columns = ['EMOTION', 'VALUE']
    df_perso.to_csv('static/js/db/hist_vid_perso.txt', sep=",", index=False)

    df_glob = pd.DataFrame.from_dict(emo_glob, orient='index')
    df_glob = df_glob.reset_index()
    df_glob.columns = ['EMOTION', 'VALUE']
    df_glob.to_csv('static/js/db/hist_vid_glob.txt', sep=",", index=False)

    emotion = df_2.density.mode()[0]
    emotion_other = df.density.mode()[0]

    def emotion_label(emotion) :
        if emotion == 0 :
            return "Angry"
        elif emotion == 1 :
            return "Disgust"
        elif emotion == 2 :
            return "Fear"
        elif emotion == 3 :
            return "Happy"
        elif emotion == 4 :
            return "Sad"
        elif emotion == 5 :
            return "Surprise"
        else :
            return "Neutral"

    ### Altair Plot
    df_altair = pd.read_csv('static/js/db/prob.csv', header=None, index_col=None).reset_index()
    df_altair.columns = ['Time', 'Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']


    angry = alt.Chart(df_altair).mark_line(color='orange', strokeWidth=2).encode(
       x='Time:Q',
       y='Angry:Q',
       tooltip=["Angry"]
    )

    disgust = alt.Chart(df_altair).mark_line(color='red', strokeWidth=2).encode(
        x='Time:Q',
        y='Disgust:Q',
        tooltip=["Disgust"])


    fear = alt.Chart(df_altair).mark_line(color='green', strokeWidth=2).encode(
        x='Time:Q',
        y='Fear:Q',
        tooltip=["Fear"])


    happy = alt.Chart(df_altair).mark_line(color='blue', strokeWidth=2).encode(
        x='Time:Q',
        y='Happy:Q',
        tooltip=["Happy"])


    sad = alt.Chart(df_altair).mark_line(color='black', strokeWidth=2).encode(
        x='Time:Q',
        y='Sad:Q',
        tooltip=["Sad"])


    surprise = alt.Chart(df_altair).mark_line(color='pink', strokeWidth=2).encode(
        x='Time:Q',
        y='Surprise:Q',
        tooltip=["Surprise"])


    neutral = alt.Chart(df_altair).mark_line(color='brown', strokeWidth=2).encode(
        x='Time:Q',
        y='Neutral:Q',
        tooltip=["Neutral"])


    chart = (angry + disgust + fear + happy + sad + surprise + neutral).properties(
    width=1000, height=400, title='Probability of each emotion over time')

    chart.save('static/CSS/chart.html')

    return render_template('video_dash.html', emo=emotion_label(emotion), emo_other = emotion_label(emotion_other), prob = emo_prop(df_2), prob_other = emo_prop(df))


@app.route("/view-data")
@login_required
def view_data():
    users = Register.query.all()
    meetings = Meeting.query.all()
    participants = Participant.query.all()
    return render_template("view_data.html", users=users, meetings=meetings, participants=participants)


# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)

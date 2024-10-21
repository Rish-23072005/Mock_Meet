import time
import os
import numpy as np

# Audio Preprocessing
import pyaudio
import wave
import librosa
from scipy.stats import zscore

# Time Distributed CNN
import tensorflow as tf
from tensorflow.keras import backend as K
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense, Dropout, Activation, TimeDistributed
from tensorflow.keras.layers import Conv2D, MaxPooling2D, BatchNormalization, Flatten
from tensorflow.keras.layers import LSTM

class speechEmotionRecognition:
    def __init__(self, subdir_model=None):
        # Load prediction model
        if subdir_model is not None:
            self._model = self.build_model()
            self._model.load_weights(subdir_model)

        # Emotion encoding
        self._emotion = {0: 'Angry', 1: 'Disgust', 2: 'Fear', 3: 'Happy', 4: 'Neutral', 5: 'Sad', 6: 'Surprise'}

    def voice_recording(self, filename, duration=5, sample_rate=16000, chunk=1024, channels=1):
        # Start the audio recording stream
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16,
                        channels=channels,
                        rate=sample_rate,
                        input=True,
                        frames_per_buffer=chunk)

        # Create an empty list to store audio recording
        frames = []

        # Determine the timestamp of the start of the response interval
        print('* Start Recording *')
        stream.start_stream()
        start_time = time.time()
        current_time = time.time()

        # Record audio until timeout
        while (current_time - start_time) < duration:
            # Record audio data
            data = stream.read(chunk)

            # Add the data to a buffer (a list of chunks)
            frames.append(data)

            # Get new timestamp
            current_time = time.time()

        # Close the audio recording stream
        stream.stop_stream()
        stream.close()
        p.terminate()
        print('* End Recording * ')

        # Export audio recording to wav format
        wf = wave.open(filename, 'w')
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(sample_rate)
        wf.writeframes(b''.join(frames))
        wf.close()

    def clean_audio_data(self, audio_data):
        if np.any(np.isnan(audio_data)) or np.any(np.isinf(audio_data)):
            print("Audio data contains NaNs or infinities. Cleaning data...")
            audio_data = np.nan_to_num(audio_data)
        return audio_data

    def pad_audio(self, audio_data, target_length):
        if len(audio_data) < target_length:
            print(f"Padding audio to {target_length} samples.")
            audio_data = np.pad(audio_data, (0, target_length - len(audio_data)), mode='constant')
        return audio_data

    def mel_spectrogram(self, y, sr=16000, n_fft=512, win_length=256, hop_length=128, window='hamming', n_mels=128, fmax=4000):
        try:
            # Ensure audio data is finite
            if np.any(np.isnan(y)) or np.any(np.isinf(y)):
                raise ValueError("Audio data contains NaNs or infinities.")

            # Compute STFT
            stft_result = librosa.stft(y, n_fft=n_fft, window=window, win_length=win_length, hop_length=hop_length)
            mel_spect = np.abs(stft_result) ** 2

            # Compute mel spectrogram
            mel_spect = librosa.feature.melspectrogram(S=mel_spect, sr=sr, n_mels=n_mels, fmax=fmax)
            mel_spect = librosa.power_to_db(mel_spect, ref=np.max)
            return np.asarray(mel_spect)
        except Exception as e:
            print(f"Error in mel_spectrogram: {e}")
            return None

    def frame(self, y, win_step=64, win_size=128):
        # Number of frames
        nb_frames = 1 + int((y.shape[2] - win_size) / win_step)

        # Framing
        frames = np.zeros((y.shape[0], nb_frames, y.shape[1], win_size)).astype(np.float16)
        for t in range(nb_frames):
            frames[:, t, :, :] = np.copy(y[:, :, (t * win_step):(t * win_step + win_size)]).astype(np.float16)

        return frames

    def build_model(self):
        # Clear Keras session
        K.clear_session()

        # Define input
        input_y = Input(shape=(5, 128, 128, 1), name='Input_MELSPECT')

        # First LFLB (local feature learning block)
        y = TimeDistributed(Conv2D(64, kernel_size=(3, 3), strides=(1, 1), padding='same'), name='Conv_1_MELSPECT')(input_y)
        y = TimeDistributed(BatchNormalization(), name='BatchNorm_1_MELSPECT')(y)
        y = TimeDistributed(Activation('elu'), name='Activ_1_MELSPECT')(y)
        y = TimeDistributed(MaxPooling2D(pool_size=(2, 2), strides=(2, 2), padding='same'), name='MaxPool_1_MELSPECT')(y)
        y = TimeDistributed(Dropout(0.2), name='Drop_1_MELSPECT')(y)

        # Second LFLB (local feature learning block)
        y = TimeDistributed(Conv2D(64, kernel_size=(3, 3), strides=(1, 1), padding='same'), name='Conv_2_MELSPECT')(y)
        y = TimeDistributed(BatchNormalization(), name='BatchNorm_2_MELSPECT')(y)
        y = TimeDistributed(Activation('elu'), name='Activ_2_MELSPECT')(y)
        y = TimeDistributed(MaxPooling2D(pool_size=(4, 4), strides=(4, 4), padding='same'), name='MaxPool_2_MELSPECT')(y)
        y = TimeDistributed(Dropout(0.2), name='Drop_2_MELSPECT')(y)

        # Third LFLB (local feature learning block)
        y = TimeDistributed(Conv2D(128, kernel_size=(3, 3), strides=(1, 1), padding='same'), name='Conv_3_MELSPECT')(y)
        y = TimeDistributed(BatchNormalization(), name='BatchNorm_3_MELSPECT')(y)
        y = TimeDistributed(Activation('elu'), name='Activ_3_MELSPECT')(y)
        y = TimeDistributed(MaxPooling2D(pool_size=(4, 4), strides=(4, 4), padding='same'), name='MaxPool_3_MELSPECT')(y)
        y = TimeDistributed(Dropout(0.2), name='Drop_3_MELSPECT')(y)

        # Fourth LFLB (local feature learning block)
        y = TimeDistributed(Conv2D(128, kernel_size=(3, 3), strides=(1, 1), padding='same'), name='Conv_4_MELSPECT')(y)
        y = TimeDistributed(BatchNormalization(), name='BatchNorm_4_MELSPECT')(y)
        y = TimeDistributed(Activation('elu'), name='Activ_4_MELSPECT')(y)
        y = TimeDistributed(MaxPooling2D(pool_size=(4, 4), strides=(4, 4), padding='same'), name='MaxPool_4_MELSPECT')(y)
        y = TimeDistributed(Dropout(0.2), name='Drop_4_MELSPECT')(y)

        # Flatten
        y = TimeDistributed(Flatten(), name='Flat_MELSPECT')(y)

        # LSTM layer
        y = LSTM(256, return_sequences=False, dropout=0.2, name='LSTM_1')(y)

        # Fully connected
        y = Dense(7, activation='softmax', name='FC')(y)

        # Build final model
        model = Model([input_y], y)
        model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

        return model

    def predict_emotion_from_file(self, filename, chunk_step=16000, chunk_size=49100, sample_rate=16000):
        try:
            # Read and normalize audio file
            y, sr = librosa.load(filename, sr=sample_rate, mono=True)
            y = self.clean_audio_data(y)
            y = self.pad_audio(y, chunk_size)

            # Z-score normalization
            y = zscore(y)

            # Framing
            chunk_step = int(chunk_step)
            chunk_size = int(chunk_size)
            chunks = []
            for i in range(0, len(y) - chunk_size + 1, chunk_step):
                chunk = y[i:i + chunk_size]
                mel_spect = self.mel_spectrogram(chunk, sr)
                if (mel_spect is not None) and (mel_spect.shape == (128, 128)):  # Ensure correct shape
                    chunks.append(mel_spect)
            chunks = np.array(chunks)

            # Ensure correct shape for model prediction
            print(f"Chunks shape before reshaping: {chunks.shape}")
            if len(chunks.shape) == 3:
                chunks = np.expand_dims(chunks, axis=-1)
            print(f"Chunks shape after expanding dims: {chunks.shape}")
            chunks = self.frame(chunks)
            print(f"Chunks shape after framing: {chunks.shape}")

            # Prediction
            predict = self._model.predict(chunks)
            predict = [self._emotion.get(np.argmax(emotion)) for emotion in predict]

            K.clear_session()
            timestamp = np.concatenate([[chunk_size], np.ones((len(predict) - 1)) * chunk_step]).cumsum()
            timestamp = np.round(timestamp / sample_rate)

            return predict, timestamp
        except Exception as e:
            print(f"Error in predict_emotion_from_file: {e}")
            return None, None

    def prediction_to_csv(self, predictions, filename, mode='w'):
        try:
            with open(filename, mode) as f:
                if mode == 'w':
                    f.write("EMOTIONS\n")
                for emotion in predictions:
                    f.write(str(emotion) + '\n')
                f.close()
        except Exception as e:
            print(f"Error in prediction_to_csv: {e}")


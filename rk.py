# import cv2
# import streamlit as st
# from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
# import speech_recognition as sr
# import pyttsx3

# # Initialize Text-to-Speech Engine
# engine = pyttsx3.init()

# def speak(text):
#     engine.say(text)
#     engine.runAndWait()

# # Define Face Detection Class
# class VideoProcessor(VideoTransformerBase):
#     def __init__(self):
#         self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

#     def transform(self, frame):
#         img = frame.to_ndarray(format="bgr24")
#         gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#         faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(100, 100))
#         for (x, y, w, h) in faces:
#             cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
#         return img

# # Streamlit App UI
# st.title("Live Camera and Microphone Access App")

# # Camera Integration
# st.header("Camera Access")
# st.write("This section uses your device's camera for real-time face detection.")
# webrtc_streamer(key="camera", video_processor_factory=VideoProcessor)

# # Microphone Integration
# st.header("Live Microphone Access")
# st.write("Speak into the microphone to process your voice.")

# # Speech Recognition using Live Microphone
# recognizer = sr.Recognizer()
# with sr.Microphone() as source:
#     st.write("Adjusting microphone sensitivity, please wait...")
#     recognizer.adjust_for_ambient_noise(source, duration=2)
#     st.success("Microphone is ready! Speak now.")

#     try:
#         with st.spinner("Listening..."):
#             audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
#             command = recognizer.recognize_google(audio)
#             st.success(f"You said: {command}")
#             speak(f"You said: {command}")
#     except sr.UnknownValueError:
#         st.error("Sorry, I couldn't understand your speech. Please try again.")
#     except sr.RequestError as e:
#         st.error(f"Speech recognition error: {e}")
#     except Exception as e:
#         st.error(f"An error occurred: {e}")

# st.write("App built using Streamlit, Streamlit-WebRTC, and SpeechRecognition.")
import cv2
import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
import speech_recognition as sr
import pyttsx3

# Initialize Text-to-Speech Engine
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

# Define Face Detection Class
class VideoProcessor(VideoTransformerBase):
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(100, 100))
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        return img

# Streamlit App UI
st.title("Live Camera and Microphone Access App")

# Camera Integration
st.header("Camera Access")
st.write("This section uses your device's camera for real-time face detection.")
webrtc_streamer(key="camera", video_processor_factory=VideoProcessor)

# Microphone Integration
st.header("Live Microphone Access")
st.write("Speak into the microphone to process your voice.")

# Speech Recognition using Live Microphone
recognizer = sr.Recognizer()
try:
    with sr.Microphone() as source:
        st.write("Adjusting microphone sensitivity, please wait...")
        recognizer.adjust_for_ambient_noise(source, duration=2)
        st.success("Microphone is ready! Speak now.")
        with st.spinner("Listening..."):
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            command = recognizer.recognize_google(audio)
            st.success(f"You said: {command}")
            speak(f"You said: {command}")
except sr.UnknownValueError:
    st.error("Sorry, I couldn't understand your speech. Please try again.")
except sr.RequestError as e:
    st.error(f"Speech recognition error: {e}")
except Exception as e:
    st.error(f"An error occurred: {e}")

st.write("App built using Streamlit, Streamlit-WebRTC, and SpeechRecognition.")

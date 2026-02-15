#
#
#
# #------------- Detect Face and emotion ------
#
#
#
# import cv2
# import face_recognition
# import numpy as np
# from keras.preprocessing import image
# from keras.models import model_from_json
# from pygame import mixer
# import time
# from DBConnection import Db
# import os
# import smtplib
# from email.mime.text import MIMEText
#
# # Configuration
# staticpath = r"C:\Users\DELL\Downloads\real_time_mock_interview\real_time_mock_interview\mock_interview_app\static"
# urgmail = "interviewmock123@gmail.com"
# urpassword = "ehok fmsl tvwk qtcr"
#
#
#
# # Initialize camera, database connection, and sound mixer
# cam = cv2.VideoCapture(2)
# db = Db()
# mixer.init()
# alert_sound_path = os.path.join(staticpath, 'short-beep-countdown-81121.mp3')
#
# # Load emotion detection model
# emotion_model = model_from_json(open("facial_expression_model_structure.json", "r").read())
# emotion_model.load_weights('facial_expression_model_weights.h5')
# emotions = ('angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral')
#
#
# def face_detection_and_emotion(lid, candidate_id):
#     # Function to play alert sound
#     def play_alert_sound():
#         if os.path.isfile(alert_sound_path):
#             mixer.music.load(alert_sound_path)
#             mixer.music.play()
#             time.sleep(5)
#             mixer.music.stop()
#
#     # Function to send alert email
#     def send_alert_email(to_email, student_name):
#         try:
#             gmail = smtplib.SMTP('smtp.gmail.com', 587)
#             gmail.starttls()
#             gmail.login(urgmail, urpassword)
#             msg = MIMEText(f"Student detected: {student_name}")
#             msg['Subject'] = 'Security Alert'
#             msg['To'] = to_email
#             msg['From'] = urgmail
#             gmail.send_message(msg)
#             gmail.quit()
#             print("Alert email sent successfully!")
#         except Exception as e:
#             print(f"Error sending email: {e}")
#
#     # Load known faces from database
#     def load_known_faces():
#         known_faces = []
#         user_ids = []
#         students = db.select("SELECT * FROM mock_interview_app_user_tb WHERE LOGIN_id='" + str(lid) + "'")
#         for student in students:
#             img_path = os.path.join(staticpath, 'photo', student["image"].split("/")[-1])
#             if os.path.isfile(img_path):
#                 face_encoding = face_recognition.face_encodings(face_recognition.load_image_file(img_path))[0]
#                 known_faces.append(face_encoding)
#                 user_ids.append((student["id"], "student"))
#         return known_faces, user_ids
#
#     # Recognize face and detect emotion
#     def recognize_and_emote(frame, known_faces, user_ids):
#         face_locations = face_recognition.face_locations(frame)
#         face_encodings = face_recognition.face_encodings(frame, face_locations)
#
#         # if len(face_encodings) == 0:
#         #     print("No face detected. Retrying...")
#         #     return False  # Return False to capture another image
#         #
#         # if len(face_encodings)>=1:
#         #     db.update("")
#
#         if len(face_encodings) >= 1:
#             no_of_unknown_person = len(face_encodings)
#             multiple_person = 2 if len(face_encodings) > 1 else 1  # Set to 2 if multiple faces are detected, else 1
#
#             db.update(
#                 "UPDATE mock_interview_app_candidate_tb "
#                 "SET no_of_unknown_person = '" + str(no_of_unknown_person) + "', "
#                 "multiple_person = '" + str(multiple_person) + "' "
#                 "WHERE id = '" + str(candidate_id) + "'"
#             )
#
#         for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
#             # Check if face matches a known person
#             matches = face_recognition.compare_faces(known_faces, face_encoding, tolerance=0.45)
#             if True in matches:
#                 match_index = matches.index(True)
#                 student_id, person_type = user_ids[match_index]
#
#                 # Detect and display emotion for the matched face
#                 detected_face = frame[top:bottom, left:right]
#                 emotion = detect_emotion(detected_face)
#                 db.insert("INSERT INTO mmock_interview_app_emotion_tb VALUES ('', '" + str(emotion) + "', '" + candidate_id + "')")
#                 print(f"Detected student {student_id} with emotion: {emotion}")
#                 return "1"  # Return success signal
#
#             else:
#                 print("Unknown individual detected.")
#                 play_alert_sound()
#                 return False  # Return False to retry the face detection
#
#     # Detect emotion from cropped face
#     def detect_emotion(face):
#         gray_face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
#         gray_face = cv2.resize(gray_face, (48, 48))
#         img_pixels = image.img_to_array(gray_face)
#         img_pixels = np.expand_dims(img_pixels, axis=0)
#         img_pixels /= 255
#
#         predictions = emotion_model.predict(img_pixels)
#         max_index = np.argmax(predictions[0])
#         return emotions[max_index]
#
#     # Main loop
#     known_faces, user_ids = load_known_faces()
#
#     start_time = time.time()  # Start timer
#     time_limit = 1 * 60  # 1 minute time limit
#
#     while True:
#         ret, frame = cam.read()
#         if not ret:
#             break
#
#         cv2.imwrite(r"C:\Users\user\PycharmProjects\real_time_mock_interview\mock_interview_app\static\a.jpg", frame)
#
#         result = recognize_and_emote(frame, known_faces, user_ids)
#
#         # If face is not recognized, capture another image
#         if result is False:
#             continue  # Skip the current loop iteration and try again
#
#         return result  # Return success if face is recognized and emotion detected
#
#     # Cleanup
#     cam.release()
#     cv2.destroyAllWindows()
#




#-------------------------------



# ------------- Detect Face and emotion ------



import cv2
import numpy as np
import tensorflow as tf
from keras.models import model_from_json
from django.http import JsonResponse
from pygame import mixer
import time
from DBConnection import Db
import os
import smtplib
from email.mime.text import MIMEText
import face_recognition  # Ensure face_recognition is imported

# Configuration
staticpath = r"C:\Users\DELL\Downloads\real_time_mock_interview\real_time_mock_interview\mock_interview_app\static"
urgmail = "princyz873gmail.com"
urpassword = "kcdu simz axrg qkiw"

# Initialize camera, database connection, and sound mixer
cam = cv2.VideoCapture(0)
db = Db()
mixer.init()
alert_sound_path = os.path.join(staticpath, 'short-beep-countdown-81121.mp3')

# Global variable to store emotion detection model
emotion_model = None
emotion_dict = {0: "Angry", 1: "Disgusted", 2: "Fearful", 3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}

def load_model():
    """
    Loads the emotion detection model only once during the session.
    """
    global emotion_model
    if emotion_model is None:
        # Load the model architecture
        with open("facial_expression_model_structure.json", "r") as json_file:
            model_json = json_file.read()

        # Load the model weights
        emotion_model = model_from_json(model_json)
        emotion_model.load_weights('facial_expression_model_weights.h5')

# Emotion detection function
def emotion(frame):
    """
    Detects the emotion from the given frame.
    """
    load_model()  # Load the model if not already loaded

    # Convert the frame to grayscale for emotion detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Load the face detection model
    face_casc = cv2.CascadeClassifier(
        r'C:\Users\user\Downloads\real_time_mock_interview\real_time_mock_interview\haarcascade_frontalface_default.xml')

    # Detect faces in the frame
    faces = face_casc.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    if len(faces) == 0:
        print("No faces detected.")
        return None  # Return None if no faces detected

    # Assuming we work with the first detected face
    (x, y, w, h) = faces[0]
    roi_gray = gray[y:y + h, x:x + w]

    # Resize the face region to the required input size (48x48)
    cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray, (48, 48)), -1), 0)

    # Make a prediction using the model
    prediction = emotion_model.predict(cropped_img)
    maxindex = int(np.argmax(prediction))  # Get the index of the highest probability

    # Get the corresponding emotion label
    res_emo = emotion_dict[maxindex]

    print(f"Detected emotion: {res_emo}")
    return res_emo  # Return the detected emotion


def play_alert_sound():
    """
    Plays a short alert sound if there is an unknown person detected.
    """
    if os.path.isfile(alert_sound_path):
        mixer.music.load(alert_sound_path)
        mixer.music.play()
        time.sleep(5)
        mixer.music.stop()


def send_alert_email(to_email, student_name):
    """
    Sends an alert email if an unknown person is detected.
    """
    try:
        gmail = smtplib.SMTP('smtp.gmail.com', 587)
        gmail.starttls()
        gmail.login(urgmail, urpassword)
        msg = MIMEText(f"Student detected: {student_name}")
        msg['Subject'] = 'Security Alert'
        msg['To'] = to_email
        msg['From'] = urgmail
        gmail.send_message(msg)
        gmail.quit()
        print("Alert email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")


def load_known_faces(lid):
    """
    Loads known faces from the database for face recognition.
    """
    known_faces = []
    user_ids = []
    students = db.select("SELECT * FROM mock_interview_app_student WHERE LOGIN_id='" + str(lid) + "'")

    for student in students:
        img_path = os.path.join(staticpath, 'photo', student["image"].split("/")[-1])
        if os.path.isfile(img_path):
            face_encoding = face_recognition.face_encodings(face_recognition.load_image_file(img_path))[0]
            known_faces.append(face_encoding)

            # Ensure that student_id is an integer
            student_id = int(student["id"])  # Ensure it's an integer
            user_ids.append((student_id, "student"))
    return known_faces, user_ids


def recognize_and_emote(frame, known_faces, user_ids, lid, candidate_id):
    """
    Recognizes known faces and detects their emotion.
    """
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    if len(face_encodings) >= 1:
        no_of_unknown_person = len(face_encodings)
        multiple_person = 2 if len(face_encodings) > 1 else 1
        db.update(
            "UPDATE mock_interview_app_candidate_tb "
            "SET no_of_unknown_person = '" + str(no_of_unknown_person) + "', "
                                                                         "multiple_person = '" + str(
                multiple_person) + "' "
                                   "WHERE id = '" + str(candidate_id) + "'"
        )

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_faces, face_encoding, tolerance=0.45)
        if True in matches:
            match_index = matches.index(True)
            student_id, person_type = user_ids[match_index]

            # Get emotion using the emotion function
            emotion_result = emotion(frame)

            # Ensure that the emotion result is not None and insert into the database
            if emotion_result is not None:
                try:
                    # Debugging log
                    print(f"Inserting emotion: {emotion_result} for candidate ID: {candidate_id}")

                    # Prepare the query
                    query = "INSERT INTO mock_interview_app_emotions (emotions, CANDIDATE_id) VALUES (%s, %s)"
                    data = (emotion_result, candidate_id)

                    # Debugging the query and data
                    print(f"Executing query: {query} with data: {data}")

                    # Execute the insert query
                    result = db.insert(query, data)

                    # Check if insert was successful
                    if result:
                        print(f"Successfully inserted emotion: {emotion_result} into database.")
                    else:
                        print("Failed to insert emotion into the database.")

                except Exception as e:
                    print(f"Error inserting emotion into database: {e}")

            return "1"  # Return success signal

        else:
            print("Unknown individual detected.")
            play_alert_sound()
            return False  # Return False to retry the face detection


def face_detection_and_emotion(lid, candidate_id):
    """
    Detects faces and their emotions and handles unknown persons.
    """
    known_faces, user_ids = load_known_faces(lid)

    start_time = time.time()  # Start timer
    time_limit = 1 * 60  # 1 minute time limit

    while True:
        ret, frame = cam.read()
        if not ret:
            break

        cv2.imwrite(
            r"C:\Users\user\Downloads\real_time_mock_interview\real_time_mock_interview\mock_interview_app\static\a.jpg",
            frame)

        result = recognize_and_emote(frame, known_faces, user_ids, lid, candidate_id)

        if result is False:
            continue  # Skip the current loop iteration and try again

        return result  # Return success if face is recognized and emotion detected

    # Cleanup
    cam.release()
    cv2.destroyAllWindows()






























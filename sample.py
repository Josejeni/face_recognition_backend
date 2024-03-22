import cv2
import face_recognition
import os
import datetime
import time

# Path to the directory containing pre-trained images
known_faces_dir = r'E:\Jose\Face_recognition\backend\photos'

# Load known faces and their names
known_faces = []
known_names = []
for file_name in os.listdir(known_faces_dir):
    image = face_recognition.load_image_file(os.path.join(known_faces_dir, file_name))
    encoding = face_recognition.face_encodings(image)[0]
    known_faces.append(encoding)
    known_names.append(os.path.splitext(file_name)[0])

# Start capturing video from the default camera
video_capture = cv2.VideoCapture(1)

# Initialize variables to keep track of detected faces and last detection time
detected_faces = set()
last_detection_time = time.time()

# Function to detect and recognize faces
def recognize_faces(frame):
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
  # Convert BGR frame to RGB for face_recognition
    
    # Find all face locations and encodings in the current frame
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
    
    # Loop through each detected face
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # Check if the current face has been detected recently
        if not is_recently_detected(face_encoding):
            # Compare the current face encoding with the known faces
            matches = face_recognition.compare_faces(known_faces, face_encoding)
            name = "Unknown"

            # If a match is found, use the name of the known face
            if True in matches:
                first_match_index = matches.index(True)
                name = known_names[first_match_index]

            # Log the attendance
            log_attendance(name)

            # Add the detected face to the set of detected faces
            detected_faces.add(tuple(face_encoding))  # Convert numpy array to tuple

            # Draw a box around the face and display the name
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 255, 0), 1)
    
    return frame

# Function to check if a face has been detected recently
def is_recently_detected(face_encoding):
    global last_detection_time
    current_time = time.time()
    if current_time - last_detection_time < 60:  # Change the time interval as needed (60 seconds in this example)
        return tuple(face_encoding) in detected_faces  # Convert numpy array to tuple
    else:
        # Reset the set of detected faces after a certain period
        detected_faces.clear()
        last_detection_time = current_time
        return False

# Function to log attendance
def log_attendance(name):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("attendance_log.txt", "a") as f:
        f.write(f"{name} attended at: {current_time}\n")

try:
    while True:
        # Capture frame-by-frame
        ret, frame = video_capture.read()

        # Detect and recognize faces in the frame
        frame_with_faces = recognize_faces(frame)

        # Display the resulting frame
        cv2.imshow('Video', frame_with_faces)

        # Exit the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
except KeyboardInterrupt:
    # Release the video capture object and close all windows
    video_capture.release()
    cv2.destroyAllWindows()

import cv2
import os
import numpy as np
import time
from database import init_db, mark_attendance

def train_recognizer():
    faces = []
    labels = []
    label_dict = {}
    current_id = 0
    
    if not os.path.exists('faces'):
        print("No faces directory found. Please register employees first.")
        return None, None
    
    for employee_name in os.listdir('faces'):
        employee_path = f'faces/{employee_name}'
        if not os.path.isdir(employee_path):
            continue
        
        label_dict[current_id] = employee_name
        
        for img_name in os.listdir(employee_path):
            img_path = f'{employee_path}/{img_name}'
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            if img is not None:
                faces.append(img)
                labels.append(current_id)
        
        current_id += 1
    
    if len(faces) == 0:
        print("No training data found.")
        return None, None
    
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.train(faces, np.array(labels))
    
    return recognizer, label_dict

def start_attendance():
    init_db()
    
    recognizer, label_dict = train_recognizer()
    if recognizer is None:
        return
    
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)
    
    print("Attendance system started. Press Ctrl+C to quit.")
    print("Scanning for faces...\n")
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            
            for (x, y, w, h) in faces:
                face_roi = gray[y:y+h, x:x+w]
                label, confidence = recognizer.predict(face_roi)
                
                if confidence < 70:
                    name = label_dict[label]
                    if mark_attendance(name):
                        print(f"✓ Attendance marked for {name} (Confidence: {int(confidence)})")
                else:
                    print(f"✗ Unknown face detected (Confidence: {int(confidence)})")
            
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nAttendance system stopped.")
    finally:
        cap.release()

if __name__ == '__main__':
    start_attendance()

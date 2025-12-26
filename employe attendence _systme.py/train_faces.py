import cv2
import os
import sqlite3
import time

def register_employee():
    name = input("Enter employee name: ")
    
    if not os.path.exists('faces'):
        os.makedirs('faces')
    
    employee_dir = f'faces/{name}'
    if not os.path.exists(employee_dir):
        os.makedirs(employee_dir)
    
    cap = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    count = 0
    print(f"Capturing 30 images for {name}. Look at camera...")
    print("Starting in 2 seconds...")
    time.sleep(2)
    
    frame_skip = 0
    while count < 30:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame_skip += 1
        if frame_skip % 3 != 0:
            continue
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        if len(faces) > 0:
            for (x, y, w, h) in faces:
                face_img = gray[y:y+h, x:x+w]
                cv2.imwrite(f'{employee_dir}/{count}.jpg', face_img)
                count += 1
                print(f"Captured: {count}/30")
                if count >= 30:
                    break
    
    cap.release()
    
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO employees (name, face_encoding) VALUES (?, ?)", (name, b''))
    conn.commit()
    conn.close()
    
    print(f"\n✓ Employee {name} registered successfully with {count} images!")

if __name__ == '__main__':
    from database import init_db
    init_db()
    try:
        register_employee()
    except KeyboardInterrupt:
        print("\nRegistration cancelled.")
    except Exception as e:
        print(f"Error: {e}")

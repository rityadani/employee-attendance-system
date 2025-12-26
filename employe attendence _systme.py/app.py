from flask import Flask, render_template, request, jsonify, Response
from flask_cors import CORS
import cv2
import os
import numpy as np
from database import init_db, mark_attendance
import sqlite3
from datetime import datetime

app = Flask(__name__)
CORS(app)
init_db()

camera = None
recognizer = None
label_dict = {}

def load_recognizer():
    global recognizer, label_dict
    try:
        faces, labels = [], []
        current_id = 0
        
        if not os.path.exists('faces'):
            return False
        
        for employee_name in os.listdir('faces'):
            employee_path = f'faces/{employee_name}'
            if not os.path.isdir(employee_path):
                continue
            
            label_dict[current_id] = employee_name
            for img_name in os.listdir(employee_path):
                img = cv2.imread(f'{employee_path}/{img_name}', cv2.IMREAD_GRAYSCALE)
                if img is not None:
                    faces.append(img)
                    labels.append(current_id)
            current_id += 1
        
        if len(faces) == 0:
            return False
        
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.train(faces, np.array(labels))
        return True
    except:
        return False

def generate_frames():
    global camera, recognizer, label_dict
    camera = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    while True:
        success, frame = camera.read()
        if not success:
            break
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        for (x, y, w, h) in faces:
            try:
                if recognizer:
                    label, confidence = recognizer.predict(gray[y:y+h, x:x+w])
                    if confidence < 70:
                        name = label_dict[label]
                        color = (0, 255, 0)
                        mark_attendance(name)
                    else:
                        name = "Unknown"
                        color = (0, 0, 255)
                else:
                    name = "Face Detected"
                    color = (255, 165, 0)
                
                cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
                cv2.putText(frame, name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
            except:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 165, 0), 2)
                cv2.putText(frame, "Face Detected", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 165, 0), 2)
        
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard_simple.html')

@app.route('/test')
def test_dashboard():
    return render_template('test_dashboard.html')

@app.route('/register')
def register_page():
    return render_template('register.html')

@app.route('/attendance')
def attendance_page():
    load_recognizer()
    return render_template('attendance.html')

@app.route('/reports')
def reports_page():
    return render_template('reports.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/api/register', methods=['POST'])
def api_register():
    name = request.json.get('name')
    if not name:
        return jsonify({'success': False, 'message': 'Name required'})
    
    if not os.path.exists('faces'):
        os.makedirs('faces')
    
    employee_dir = f'faces/{name}'
    os.makedirs(employee_dir, exist_ok=True)
    
    cap = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    count = 0
    while count < 30:
        ret, frame = cap.read()
        if not ret:
            break
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        for (x, y, w, h) in faces:
            cv2.imwrite(f'{employee_dir}/{count}.jpg', gray[y:y+h, x:x+w])
            count += 1
            if count >= 30:
                break
    
    cap.release()
    
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO employees (name, face_encoding) VALUES (?, ?)", (name, b''))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'message': f'{name} registered successfully!'})

@app.route('/api/daily_report')
def api_daily_report():
    date = datetime.now().strftime('%Y-%m-%d')
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute("SELECT employee_name, time FROM attendance WHERE date=?", (date,))
    records = [{'name': r[0], 'time': r[1]} for r in c.fetchall()]
    conn.close()
    return jsonify({'date': date, 'records': records})

@app.route('/api/monthly_report')
def api_monthly_report():
    month = datetime.now().month
    year = datetime.now().year
    
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute("SELECT DISTINCT employee_name FROM employees")
    employees = [row[0] for row in c.fetchall()]
    
    data = []
    for emp in employees:
        c.execute("SELECT COUNT(*) FROM attendance WHERE employee_name=? AND strftime('%m', date)=? AND strftime('%Y', date)=?",
                  (emp, f'{month:02d}', str(year)))
        count = c.fetchone()[0]
        data.append({'name': emp, 'days': count})
    
    conn.close()
    return jsonify({'month': month, 'year': year, 'data': data})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)

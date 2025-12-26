import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS employees
                 (id INTEGER PRIMARY KEY, name TEXT UNIQUE, face_encoding BLOB)''')
    c.execute('''CREATE TABLE IF NOT EXISTS attendance
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  employee_name TEXT, 
                  date TEXT, 
                  time TEXT,
                  UNIQUE(employee_name, date))''')
    conn.commit()
    conn.close()

def mark_attendance(name):
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    date = datetime.now().strftime('%Y-%m-%d')
    time = datetime.now().strftime('%H:%M:%S')
    try:
        c.execute("INSERT INTO attendance (employee_name, date, time) VALUES (?, ?, ?)", 
                  (name, date, time))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return False

import sqlite3
from datetime import datetime, timedelta
import random

def add_fake_data():
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    
    # Create tables if not exist
    c.execute('''CREATE TABLE IF NOT EXISTS employees
                 (id INTEGER PRIMARY KEY, name TEXT UNIQUE, face_encoding BLOB)''')
    c.execute('''CREATE TABLE IF NOT EXISTS attendance
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  employee_name TEXT, 
                  date TEXT, 
                  time TEXT,
                  UNIQUE(employee_name, date))''')
    
    # Add fake employees
    employees = [
        'Ritesh Kumar', 'Amit Sharma', 'Priya Singh', 'Rahul Verma', 'Sneha Patel',
        'Arjun Mehta', 'Neha Gupta', 'Vikram Singh', 'Anjali Reddy', 'Karan Malhotra',
        'Pooja Desai', 'Rohit Joshi', 'Kavita Nair', 'Sanjay Rao', 'Divya Iyer'
    ]
    
    for emp in employees:
        c.execute("INSERT OR IGNORE INTO employees (name, face_encoding) VALUES (?, ?)", (emp, b''))
    
    # Add today's attendance
    today = datetime.now()
    times = [
        '09:05:12', '09:12:34', '09:18:45', '09:25:23', '09:32:56',
        '09:38:12', '09:45:33', '09:52:18', '09:58:45', '10:05:22',
        '10:12:38', '10:18:55', '10:25:12', '10:32:45', '10:38:29'
    ]
    
    for emp, time in zip(employees, times):
        try:
            c.execute("INSERT INTO attendance (employee_name, date, time) VALUES (?, ?, ?)", 
                      (emp, today.strftime('%Y-%m-%d'), time))
        except:
            pass
    
    # Add monthly data (last 20 days)
    for i in range(1, 21):
        past_date = (today - timedelta(days=i)).strftime('%Y-%m-%d')
        
        # Random attendance for each employee (80-90% attendance)
        for emp in employees:
            if random.random() > 0.15:  # 85% chance of attendance
                time = f"{random.randint(9,10):02d}:{random.randint(0,59):02d}:{random.randint(0,59):02d}"
                try:
                    c.execute("INSERT INTO attendance (employee_name, date, time) VALUES (?, ?, ?)", 
                              (emp, past_date, time))
                except:
                    pass
    
    conn.commit()
    conn.close()
    print("✓ Fake data added successfully!")
    print(f"✓ {len(employees)} employees registered")
    print(f"✓ Today's attendance marked for all employees")
    print(f"✓ Monthly data added for last 20 days")

if __name__ == '__main__':
    add_fake_data()

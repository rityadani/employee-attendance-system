# Employee Attendance System (Face Recognition)

## Features
- Camera-based face detection
- Auto attendance logging
- Daily/Monthly reports
- SQLite database storage

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Initialize database:
```bash
python database.py
```

## Usage

### 1. Register Employees
```bash
python train_faces.py
```
- Enter employee name
- Look at camera (captures 30 images)
- Press 'q' to finish early

### 2. Start Attendance System
```bash
python main.py
```
- System will recognize faces and mark attendance automatically
- Each employee marked once per day
- Press 'q' to quit

### 3. Generate Reports
```bash
python reports.py
```
- Option 1: Daily report (today's attendance)
- Option 2: Monthly report (attendance summary)

## Database
- `attendance.db` - SQLite database
- Tables: `employees`, `attendance`

## Tech Stack
- Python 3.x
- OpenCV (Face Detection & Recognition)
- LBPH Face Recognizer (ML)
- SQLite (Database)

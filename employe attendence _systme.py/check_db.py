import sqlite3

conn = sqlite3.connect('attendance.db')
c = conn.cursor()

print("=== EMPLOYEES ===")
c.execute("SELECT * FROM employees")
employees = c.fetchall()
print(f"Total: {len(employees)}")
for emp in employees:
    print(f"  - {emp}")

print("\n=== TODAY'S ATTENDANCE ===")
from datetime import datetime
today = datetime.now().strftime('%Y-%m-%d')
c.execute("SELECT * FROM attendance WHERE date=?", (today,))
attendance = c.fetchall()
print(f"Total: {len(attendance)}")
for att in attendance[:5]:
    print(f"  - {att}")

conn.close()

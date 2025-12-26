import sqlite3
from datetime import datetime, timedelta

def daily_report(date=None):
    if date is None:
        date = datetime.now().strftime('%Y-%m-%d')
    
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute("SELECT employee_name, time FROM attendance WHERE date=?", (date,))
    records = c.fetchall()
    conn.close()
    
    print(f"\n{'='*50}")
    print(f"Daily Attendance Report - {date}")
    print(f"{'='*50}")
    print(f"{'Employee Name':<30} {'Time':<20}")
    print(f"{'-'*50}")
    
    for record in records:
        print(f"{record[0]:<30} {record[1]:<20}")
    
    print(f"{'-'*50}")
    print(f"Total Present: {len(records)}")
    print(f"{'='*50}\n")

def monthly_report(month=None, year=None):
    if month is None:
        month = datetime.now().month
    if year is None:
        year = datetime.now().year
    
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute("SELECT DISTINCT employee_name FROM employees")
    employees = [row[0] for row in c.fetchall()]
    
    print(f"\n{'='*70}")
    print(f"Monthly Attendance Report - {month}/{year}")
    print(f"{'='*70}")
    print(f"{'Employee Name':<30} {'Days Present':<20}")
    print(f"{'-'*70}")
    
    for emp in employees:
        c.execute("SELECT COUNT(*) FROM attendance WHERE employee_name=? AND strftime('%m', date)=? AND strftime('%Y', date)=?",
                  (emp, f'{month:02d}', str(year)))
        count = c.fetchone()[0]
        print(f"{emp:<30} {count:<20}")
    
    conn.close()
    print(f"{'='*70}\n")

if __name__ == '__main__':
    print("1. Daily Report")
    print("2. Monthly Report")
    choice = input("Enter choice: ")
    
    if choice == '1':
        daily_report()
    elif choice == '2':
        monthly_report()

import sqlite3
import os

# Delete old database
if os.path.exists('attendance.db'):
    os.remove('attendance.db')
    print("✓ Old database deleted")

# Run add_fake_data
from add_fake_data import add_fake_data
add_fake_data()

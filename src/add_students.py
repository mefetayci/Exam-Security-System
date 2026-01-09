import sqlite3
import os


DB_PATH = os.path.join(os.path.dirname(__file__), '../database/exam_system.db')

def add_10_students():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    print("--- Adding 10 Students to Database ---")

    
    students = [
        ('2023001', 'Alice Smith', '/references/ref_1.jpg'),
        ('2023002', 'Mehmet Yilmaz', '/references/ref_2.jpg'),
        ('2023003', 'Ayse Demir', '/references/ref_3.jpg'),
        ('2023004', 'Fatma Kaya', '/references/ref_4.jpg'),
        ('2023005', 'Ali Veli', '/references/ref_5.jpg'),
        ('2023006', 'Zeynep Celik', '/references/ref_6.jpg'),
        ('2023007', 'Mustafa Koc', '/references/ref_7.jpg'),
        ('2023008', 'Elif Ozturk', '/references/ref_8.jpg'),
        ('2023009', 'Burak Can', '/references/ref_9.jpg'),
        ('2023010', 'Hande Er', '/references/ref_10.jpg')
    ]

   
    for s in students:
        try:
            cursor.execute("INSERT INTO students (student_number, full_name, photo_ref_path) VALUES (?, ?, ?)", s)
            print(f"Added: {s[1]}")
        except sqlite3.IntegrityError:
            print(f"Skipped (Already exists): {s[1]}")

    
    roster = [
        (1, 1, 'A1'),
        (1, 2, 'B1'),
        (1, 3, 'C1'),
        (1, 4, 'A2'),
        (1, 5, 'B2'),
        (1, 6, 'C2'),
        (1, 7, 'A3'),
        (1, 8, 'B3'),
        (1, 9, 'C3'),
        (1, 10, 'D1')
    ]

    print("\n--- Assigning Seats ---")
    for r in roster:
        try:
            cursor.execute("INSERT INTO exam_roster (exam_id, student_id, assigned_seat) VALUES (?, ?, ?)", r)
            print(f"Seat Assigned: Student {r[1]} -> {r[2]}")
        except sqlite3.IntegrityError:
            print(f"Assignment exists for Student {r[1]}")

    conn.commit()
    conn.close()
    print("\n--- Operation Completed Successfully ---")

if __name__ == '__main__':
    add_10_students()

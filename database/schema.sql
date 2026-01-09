-- Database Schema for Exam Security System

-- 1. Users Table
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('Admin', 'Proctor'))
);

-- 2. Students Table
CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_number TEXT NOT NULL UNIQUE,
    full_name TEXT NOT NULL,
    photo_ref_path TEXT -- Path to the reference image
);

-- 3. Exams Table
CREATE TABLE exams (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    room_number TEXT NOT NULL,
    date_time TEXT NOT NULL
);

-- 4. Roster & Seating Table
CREATE TABLE exam_roster (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    exam_id INTEGER NOT NULL,
    student_id INTEGER NOT NULL,
    assigned_seat TEXT,
    FOREIGN KEY (exam_id) REFERENCES exams(id),
    FOREIGN KEY (student_id) REFERENCES students(id)
);

-- 5. Check-ins Table
CREATE TABLE check_ins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    exam_id INTEGER NOT NULL,
    student_id INTEGER NOT NULL,
    verification_status TEXT, -- 'Match' or 'No Match'
    seat_status TEXT, -- 'Correct' or 'Incorrect'
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (exam_id) REFERENCES exams(id),
    FOREIGN KEY (student_id) REFERENCES students(id)
);

-- 6. Violations Table
CREATE TABLE violations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    exam_id INTEGER NOT NULL,
    student_id INTEGER NOT NULL,
    violation_type TEXT,
    description TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (exam_id) REFERENCES exams(id),
    FOREIGN KEY (student_id) REFERENCES students(id)
);

-- DUMMY DATA FOR TESTING
INSERT INTO users (username, password, role) VALUES ('admin', 'admin123', 'Admin');
INSERT INTO users (username, password, role) VALUES ('proctor', 'proctor123', 'Proctor');

INSERT INTO students (student_number, full_name, photo_ref_path) VALUES ('ST001', 'John Doe', 'photos/st001.jpg');
INSERT INTO students (student_number, full_name, photo_ref_path) VALUES ('ST002', 'Jane Smith', 'photos/st002.jpg');

INSERT INTO exams (name, room_number, date_time) VALUES ('Software Validation Final', 'Hall-A', '2025-01-20 10:00');

INSERT INTO exam_roster (exam_id, student_id, assigned_seat) VALUES (1, 1, 'A1');
INSERT INTO exam_roster (exam_id, student_id, assigned_seat) VALUES (1, 2, 'A2');
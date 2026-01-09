# Exam Security System

## 1. Project Overview
The Exam Security System is a web-based application designed to manage exam identity verification, seating compliance, and violation logging. It integrates a Computer Vision component (OpenCV) for face verification.

### Key Features
* **Role-Based Access:** Admin (Dashboard) and Proctor (Check-in & Violations).
* **Identity Verification:** Face comparison using Histogram Correlation (OpenCV).
* **Seating Compliance:** Automatically verifies if the student is sitting in the assigned seat.
* **Violation Logging:** Module to record academic dishonesty incidents.
* **Reporting:** Admin dashboard with real-time statistics.

## 2. Repository Structure
* `analysis/` - Requirements and business rules.
* `database/` - SQL Schema and database file.
* `diagrams/` - UML diagrams (Use Case, ERD, Sequence, Activity).
* `jira/` - Sprint planning evidence.
* `src/` - Source code (Flask App, ML Service, Templates).
* `tests/` - Unit tests for critical logic.
* `test-docs/` - Test cases documentation.

## 3. Setup & Installation

### Prerequisites
* Python 3.x
* Libraries: `flask`, `pytest`, `numpy`, `opencv-python`

### Installation
1. Install dependencies:
   ```bash
   pip install -r requirements.txt

Run the application:
python src/app.py
The App will start at http://127.0.0.1:5000/

4. Demo Scenario (How to Test)
Step 1: Login
Admin: Username: admin, Password: 1234 (Goes to Dashboard)

Proctor: Username: proctor, Password: 1234 (Goes to Check-in)

Step 2: Student Check-in (Happy Path)
Login as Proctor.

Select "Mehmet Yilmaz" (Seat: B1).

Upload src/references/ref_2.jpg (or the corresponding photo).

Enter Seat Code: B1.

Click Verify. Result should be Success.

Step 3: Violation Logging
Click "Log Violation" button.

Select a student and violation type.

Submit. You will be redirected to the Admin Dashboard.

5. Running Tests
To validate the system logic (ML wrapper mock, validations):

pytest tests/
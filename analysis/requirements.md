# Exam Security System - Requirements Specification

## 1. Project Overview
The Exam Security System is a web-based application designed to manage exam identity verification, seating compliance, and violation logging using simple computer vision techniques.

## 2. Actors
* **Admin (Exam Coordinator):** Manages exams, students, and seating plans.
* **Proctor (Invigilator):** Performs check-ins using the verification system and logs violations.
* **Student:** The individual attending the exam (subject of verification).

## 3. Functional Requirements

### 3.1 Authentication & Authorization
* **REQ-AUTH-01:** The system shall require users (Admin, Proctor) to log in.
* **REQ-AUTH-02:** The system shall enforce Role-Based Access Control (RBAC).
    * Admins have full access to Exam and Roster management.
    * Proctors have access only to Check-in and Violation modules.

### 3.2 Exam & Roster Management (Admin)
* **REQ-EXAM-01:** Admin shall create exams with details: Name, Room, Date, Time.
* **REQ-EXAM-02:** Admin shall import or enter student roster data (ID, Name, Reference Photo).
* **REQ-EXAM-03:** Admin shall define a seating plan (assigning seats to students).

### 3.3 Check-in Workflow (Proctor)
* **REQ-CHECK-01:** Proctor shall select the current exam.
* **REQ-CHECK-02:** System shall capture or upload a photo of the student.
* **REQ-CHECK-03:** System shall verify the student's identity using Face Verification (ML Wrapper).
    * Compares live photo vs. stored reference photo.
* **REQ-CHECK-04:** System shall validate Seating Compliance (Is the student in the correct seat?).
* **REQ-CHECK-05:** System shall record the check-in result (Timestamp, Status).

### 3.4 Violation Logging
* **REQ-LOG-01:** Proctor shall be able to manually log a violation.
* **REQ-LOG-02:** Violation records must include: Student ID, Violation Type, Description, and Timestamp.

### 3.5 Reporting
* **REQ-REP-01:** System shall generate a summary report showing total check-ins, failed verifications, and recorded violations.

## 4. Technical Constraints
* Implementation must include a wrapper for an ML library (e.g., face_recognition).
* Unit tests must mock the ML component.
# Software Testing & Validation - Test Cases Document

## 1. Authentication Module (Kimlik Doğrulama)

| Test ID | Scenario | Precondition | Steps | Input Data | Expected Result |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-001** | Valid Admin Login | User exists in DB | 1. Navigate to Login<br>2. Enter valid admin credentials | `{"username": "admin_jane", "password": "secret123"}` | JSON 200 OK, Role: "Admin" returned. |
| **TC-002** | Invalid Password | User exists in DB | 1. Navigate to Login<br>2. Enter valid user but wrong password | `{"username": "admin_jane", "password": "wrongpass"}` | JSON 401 Unauthorized "Invalid credentials". |
| **TC-003** | Non-existent User | DB initialized | 1. Navigate to Login<br>2. Enter unknown username | `{"username": "ghost_user", "password": "123"}` | JSON 401 Unauthorized. |

## 2. Check-in & Verification Module (Giriş ve Kontrol)

| Test ID | Scenario | Precondition | Steps | Input Data | Expected Result |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-004** | Successful Check-in (Happy Path) | Student & Exam exist, Correct Seat | 1. Open Check-in Form<br>2. Select Student & Exam<br>3. Upload correct photo<br>4. Enter assigned seat code | `Student: Alice`<br>`Photo: ref_1.jpg copy`<br>`Seat: A1` | **Status: Success**<br>ML: Match<br>Seat: Correct |
| **TC-005** | Identity Mismatch (Negative Case) | Student exists | 1. Open Check-in Form<br>2. Upload wrong person's photo | `Student: Alice`<br>`Photo: unrelated_face.jpg` | **Status: Failed**<br>ML: No Match |
| **TC-006** | Seating Violation (Business Rule) | Student assigned to A1 | 1. Open Check-in Form<br>2. Upload correct photo<br>3. Enter wrong seat code | `Student: Alice`<br>`Seat: B5` | **Status: Failed**<br>Seat: Incorrect |
| **TC-007** | Missing Photo (Edge Case) | - | 1. Submit form without uploading file | `Photo: (empty)` | HTTP 400 "No photo uploaded" error. |
| **TC-008** | Reference Photo Missing (Edge Case) | Reference file deleted | 1. Attempt check-in for student with no ref photo | `Student: John` | HTTP 404 "Reference photo not found". |

## 3. Violation Logging (İhlal Kaydı)

| Test ID | Scenario | Precondition | Steps | Input Data | Expected Result |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-009** | Log Violation Successfully | Exam is active | 1. Call Violation API<br>2. Submit details | `Type: Phone Usage`<br>`Desc: Found in pocket` | Database record created in `violations` table. |
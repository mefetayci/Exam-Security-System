from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from db import get_db_connection
from ml_service import FaceVerificationService
import os

app = Flask(__name__)
app.secret_key = 'super_secret_key' # Session için gerekli

# Klasör Ayarları
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
REF_FOLDER = os.path.join(os.path.dirname(__file__), 'references')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REF_FOLDER, exist_ok=True)

ml_service = FaceVerificationService()

# --- 1. LOGIN EKRANI (Açılış Sayfası) ---
@app.route('/', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def perform_login():
    username = request.form.get('username')
    password = request.form.get('password')
    role = request.form.get('role')

    # Basit bir kontrol (Demo olduğu için veritabanı sorgusu yapmadan geçiyoruz)
    if password == "1234":
        session['role'] = role # Rolü hafızaya al
        if role == 'Admin':
            return redirect(url_for('web_dashboard')) # Admin ise Raporlara git
        else:
            return redirect(url_for('web_checkin'))   # Gözetmen ise Check-in'e git
    else:
        return "Invalid Password! Try '1234'", 401

# --- 2. LOGOUT ---
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# --- 3. CHECK-IN SAYFASI (Proctor) ---
@app.route('/checkin', methods=['GET', 'POST'])
def web_checkin():
    # Güvenlik Kontrolü: Giriş yapmamışsa login'e at
    if 'role' not in session: return redirect(url_for('login'))
    
    result = None
    if request.method == 'POST':
        student_id = request.form.get('student_id')
        exam_id = request.form.get('exam_id')
        actual_seat = request.form.get('actual_seat')
        
        if 'photo' not in request.files: return "No photo uploaded", 400
        file = request.files['photo']
        if file.filename == '': return "No file selected", 400

        live_photo_path = os.path.join(UPLOAD_FOLDER, f"live_{student_id}.jpg")
        file.save(live_photo_path)

        conn = get_db_connection()
        student = conn.execute('SELECT * FROM students WHERE id = ?', (student_id,)).fetchone()
        roster = conn.execute('SELECT * FROM exam_roster WHERE exam_id = ? AND student_id = ?', (exam_id, student_id)).fetchone()
        
        if not student: return "Student not found", 404

        ref_photo_path = os.path.join(REF_FOLDER, f"ref_{student_id}.jpg")
        if not os.path.exists(ref_photo_path):
            conn.close()
            return f"Error: Reference photo not found at {ref_photo_path}", 404

        verification = ml_service.verify_identity(live_photo_path, ref_photo_path)
        ml_status = verification['result']
        assigned_seat = roster['assigned_seat']
        seat_status = 'Correct' if actual_seat == assigned_seat else 'Incorrect'
        final_status = 'Success' if (ml_status == 'Match' and seat_status == 'Correct') else 'Failed'

        conn.execute('''
            INSERT INTO check_ins (exam_id, student_id, verification_status, seat_status)
            VALUES (?, ?, ?, ?)
        ''', (exam_id, student_id, ml_status, seat_status))
        conn.commit()
        conn.close()

        result = {
            "status": final_status,
            "ml_result": ml_status,
            "seat_status": seat_status,
            "confidence": verification.get('confidence', 0)
        }

    return render_template('checkin.html', result=result)

# --- 4. DASHBOARD (Admin) ---
@app.route('/dashboard')
def web_dashboard():
    if 'role' not in session: return redirect(url_for('login'))
    
    conn = get_db_connection()
    checkins = conn.execute('''
        SELECT c.id, s.full_name, c.verification_status, c.seat_status, c.timestamp 
        FROM check_ins c JOIN students s ON c.student_id = s.id ORDER BY c.timestamp DESC
    ''').fetchall()
    
    violations = conn.execute('''
        SELECT v.id, s.full_name, v.violation_type, v.description, v.timestamp
        FROM violations v JOIN students s ON v.student_id = s.id ORDER BY v.timestamp DESC
    ''').fetchall()
    
    stats = {
        "total": len(checkins),
        "failed": len([c for c in checkins if c['verification_status'] == 'No Match' or c['seat_status'] == 'Incorrect']),
        "violations": len(violations)
    }
    conn.close()
    return render_template('dashboard.html', checkins=checkins, violations=violations, stats=stats)

# --- 5. VIOLATION LOGGING ---
@app.route('/violation', methods=['GET', 'POST'])
def log_violation():
    if 'role' not in session: return redirect(url_for('login'))
    
    if request.method == 'POST':
        exam_id = request.form.get('exam_id')
        student_id = request.form.get('student_id')
        violation_type = request.form.get('violation_type')
        description = request.form.get('description')
        
        conn = get_db_connection()
        conn.execute('INSERT INTO violations (exam_id, student_id, violation_type, description) VALUES (?, ?, ?, ?)',
                     (exam_id, student_id, violation_type, description))
        conn.commit()
        conn.close()
        return redirect(url_for('web_dashboard'))

    return render_template('violation.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
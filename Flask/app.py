from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Replace with a secure key

# Dummy patient data (replace with database later)
patients_data = {
    "1": {
        "patient_id": "1",
        "patient_name": "John Doe",
        "schedule": [
            {"drug": "Aspirin", "time": "08:00 AM", "dose": "1 tablet", "doctornotes": "Take one pill in the morning every day for 14 days."},
            {"drug": "Metformin", "time": "12:00 PM", "dose": "2 tablets", "doctornotes": "Take one pill in the morning and one pill in the night after a meal."}
        ],
        "drug_history": [
            {"drug": "Aspirin", "date": "2025-03-28", "time": "08:05 AM"},
        ],
        "health_history": [
            {"event": "Blood Pressure Check", "date": "2025-03-28", "result": "120/80 mmHg"},
        ],
        "alerts": [
            {"type": "Missed Dose", "drug": "Metformin", "time": "2025-03-29 12:00 PM"},
            {"type": "Overdose Risk", "drug": "Aspirin", "time": "2025-03-29 08:00 AM"}
        ],
        "vitals": {"heart_rate": "72 bpm", "temperature": "98.6°F"}
    },
    "2": {
        "patient_id": "2",
        "patient_name": "Jane Smith",
        "schedule": [
            {"drug": "Lisinopril", "time": "09:00 AM", "dose": "1 tablet"},
            {"drug": "Ibuprofen", "time": "03:00 PM", "dose": "2 tablets"}
        ],
        "drug_history": [
            {"drug": "Lisinopril", "date": "2025-03-28", "time": "09:10 AM"},
        ],
        "health_history": [
            {"event": "Blood Sugar Test", "date": "2025-03-28", "result": "110 mg/dL"},
        ],
        "alerts": [
            {"type": "Missed Dose", "drug": "Ibuprofen", "time": "2025-03-29 03:00 PM"}
        ],
        "vitals": {"heart_rate": "68 bpm", "temperature": "98.4°F"}
    }
}

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        role = request.form['role']
        session['role'] = role
        if role == 'patient':
            return redirect(url_for('patient_home'))
        elif role == 'doctor':
            return redirect(url_for('doctor_dashboard'))
    return render_template('login.html')

# Patient Routes
@app.route('/patient/home')
def patient_home():
    if session.get('role') != 'patient':
        return redirect(url_for('login'))
    return render_template('patient/home.html', schedule=patients_data["1"]["schedule"])  # Default to patient 1 for demo

@app.route('/patient/drug_history')
def patient_drug_history():
    if session.get('role') != 'patient':
        return redirect(url_for('login'))
    return render_template('patient/drug_history.html', history=patients_data["1"]["drug_history"])

@app.route('/patient/health_history')
def patient_health_history():
    if session.get('role') != 'patient':
        return redirect(url_for('login'))
    return render_template('patient/health_history.html', health=patients_data["1"]["health_history"])

@app.route('/patient/add_drug', methods=['GET', 'POST'])
def patient_add_drug():
    if session.get('role') != 'patient':
        return redirect(url_for('login'))
    if request.method == 'POST':
        drug = request.form['drug']
        time = request.form['time']
        dose = request.form['dose']
        patients_data["1"]["schedule"].append({"drug": drug, "time": time, "dose": dose})  # Default to patient 1
        return redirect(url_for('patient_home'))
    return render_template('patient/add_drug.html')

# Doctor Routes
@app.route('/doctor/dashboard')
def doctor_dashboard():
    if session.get('role') != 'doctor':
        return redirect(url_for('login'))
    return render_template('doctor/dashboard.html', patients=patients_data)

@app.route('/doctor/patient/<patient_id>')
def doctor_patient_detail(patient_id):
    if session.get('role') != 'doctor':
        return redirect(url_for('login'))
    if patient_id not in patients_data:
        return "Patient not found", 404
    return render_template('doctor/patient_detail.html', data=patients_data[patient_id])

# Logout Route
@app.route('/logout')
def logout():
    session.pop('role', None)  # Clear the role from session
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
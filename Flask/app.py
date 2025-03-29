from flask import Flask, flash, render_template, request, redirect, url_for, session
from openFDA import get_drug_info

app = Flask(__name__)
app.secret_key = 'frenuirh4281y43icnew'  # Replace with a secure key

patients_data = {
    "1": {
        "patient_id": "1",
        "patient_name": "John Doe",
        "schedule": [
            {"drug": "Aspirin", "warnings" : "Aspirin", "active_ingredients" : ["ibuprofen"],
             "do_not_use" : "Do not use if you have a history of allergic reaction to aspirin or other NSAIDs.",
                "indications_and_usage" : "For the temporary relief of minor aches and pains.",
                "effective_time" : "2025-03-01",
              "time": "08:00 AM", "dose": "1 tablet", "doctornotes": "Take one pill in the morning every day for 14 days."
              , "type": "OTC"},
            {"drug": "Metformin", 
             "warnings" : "Aspirin", "active_ingredients" : ["acetylsalicylic acid"],
             "do_not_use" : "Do not use if you have a history of allergic reaction to aspirin or other NSAIDs.",
                "indications_and_usage" : "For the temporary relief of minor aches and pains.",
                "effective_time" : "2025-03-01",
                "time": "12:00 PM", "dose": "2 tablets", "doctornotes": "Take one pill in the morning and one pill in the night after a meal."
                , "type": "Prescription"}
        ],
        "drug_history": [
            {"drug": "Acetaminophen", "start_date": "2020-01-26","end_date": "2025-01-26", "time": "02:00 PM"}
        ],
        "health_history": [
            {"event": "Blood Pressure Check", "date": "2025-03-28", "result": "120/80 mmHg"}
        ],
        "alerts": [
            {"type": "Missed Dose", "drug": "Metformin", "time": "2025-03-29 12:00 PM"}
        ],
        "vitals": {"heart_rate": "72 bpm", "temperature": "98.6°F"}
    },
    "2": {
        "patient_id": "2",
        "patient_name": "Jane Smith",
        "schedule": [
            {"drug": "Lisinopril", "warnings" : "Aspirin", "active_ingredients" : ["acetylsalicylic acid"],
             "do_not_use" : "Do not use if you have a history of allergic reaction to aspirin or other NSAIDs.",
                "indications_and_usage" : "For the temporary relief of minor aches and pains.",
                "effective_time" : "2025-03-01","time": "09:00 AM", "dose": "1 tablet"},
            {"drug": "Ibuprofen", "warnings" : "Aspirin", "active_ingredients" : ["acetylsalicylic acid"],
             "do_not_use" : "Do not use if you have a history of allergic reaction to aspirin or other NSAIDs.",
                "indications_and_usage" : "For the temporary relief of minor aches and pains.",
                "effective_time" : "2025-03-01", "time": "03:00 PM", "dose": "2 tablets"
                , "type": "OTC"},
            {"drug": "Losartan", "time": "09:00 AM", "dose": "1 tablet", "doctornotes": "Take in morning"}
        ],
        "drug_history": [
            {"drug": "Zyrtec", "start_date": "2023-04-26","end_date": "2025-04-26", "time": "08:00 PM"}
        ],
        "health_history": [
            {"event": "Blood Pressure Check", "date": "2025-03-28", "result": "130/85 mmHg"}
        ],
        "alerts": [
            {"type": "Missed Dose", "drug": "Losartan", "time": "2025-03-29 09:00 AM"}
        ],
        "vitals": {"heart_rate": "68 bpm", "temperature": "98.4°F"}
    },
    "3": {
        "patient_id": "3",
        "patient_name": "Michael Brown",
        "schedule": [
            {"drug": "Omeprazole", "time": "07:00 AM", "dose": "1 capsule", "doctornotes": "Take before breakfast"}
        ],
        "drug_history": [
            {"drug": "Acetaminophen", "start_date": "2020-01-26","end_date": "2025-01-26", "time": "02:00 PM"}
        ],
        "health_history": [
            {"event": "Acid Reflux Check", "date": "2025-03-28", "result": "Mild symptoms"}
        ],
        "alerts": [],
        "vitals": {"heart_rate": "70 bpm", "temperature": "98.5°F"}
    },
    "4": {
        "patient_id": "4",
        "patient_name": "Emily Davis",
        "schedule": [
            {"drug": "Amoxicillin", "time": "08:00 AM", "dose": "1 capsule", "doctornotes": "Take every 8 hours"}
        ],
        "health_history": [
            {"event": "Infection Check", "date": "2025-03-28", "result": "Improving"}
        ],
        "alerts": [],
        "vitals": {"heart_rate": "75 bpm", "temperature": "99.1°F"}
    },
    "5": {
        "patient_id": "5",
        "patient_name": "Robert Wilson",
        "schedule": [
            {"drug": "Gabapentin", "time": "09:00 PM", "dose": "1 capsule", "doctornotes": "Take at bedtime"}
        ],
        "drug_history": [
            {"drug": "Ibuprofen", "start_date": "2020-01-26","end_date": "2025-01-26", "time": "03:00 PM"}
        ],
        "health_history": [
            {"event": "Pain Assessment", "date": "2025-03-28", "result": "Moderate"}
        ],
        "alerts": [],
        "vitals": {"heart_rate": "73 bpm", "temperature": "98.7°F"}
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

        # Checking drug interactions
        fdacode = "brand_name"
        drug_info, bad_interactions = get_drug_info(drug, patients_data["1"]["schedule"], fdacode)

        #print(bad_interactions)
        #print(drug_info)
        if(len(bad_interactions) > 0):
            return render_template('patient/add_drug.html', error=f"Warning: {drug} interacts with {', '.join(bad_interactions)}")
        else:
            drug_info["time"] = time
            drug_info["dose"] = dose
            drug_info["type"] = "OTC"
            patients_data["1"]["schedule"].append(drug_info)  # Default to patient 1
            print("added the item to the list")
            return redirect(url_for('patient_home'))
    return render_template('patient/add_drug.html')

# Doctor Routes
@app.route('/doctor/dashboard')
def doctor_dashboard():
    if session.get('role') != 'doctor':
        return redirect(url_for('login'))
    return render_template('doctor/dashboard.html', patients_data=patients_data)

@app.route('/doctor/patient/<patient_id>')
def doctor_patient_detail(patient_id):
    if session.get('role') != 'doctor':
        return redirect(url_for('login'))
    if patient_id not in patients_data:
        return "Patient not found", 404
    return render_template('patient/health_history.html', data=patient_id)

@app.route('/doctor/edit_drug/<patient_id>', methods=['GET', 'POST'])
def doctor_edit_drug(patient_id):
    if session.get('role') != 'doctor':
        return redirect(url_for('login'))
    if request.method == 'POST':
        if 'drug' in request.form and request.form['drug']:
            drug = request.form['drug']
        # Checking drug interactions
        fdacode = "substance_name"

        try:
            # Attempt to get drug information and identify bad interactions
            drug_info, bad_interactions = get_drug_info(drug, patients_data[patient_id]["schedule"], fdacode)
        except Exception as e:
            # Catch all exceptions and log or handle the error
            print(f"An error occurred while fetching drug information: {e}")
            drug_info, bad_interactions = None, None

        #print(bad_interactions)
        #print(drug_info)
        if(len(bad_interactions) > 0):
            return render_template('patient/add_drug.html', error=f"Warning: {drug} interacts with {', '.join(bad_interactions)}")
        else:

            if 'time' in request.form and request.form['time']:
                drug_info['time'] = request.form['time']

            if 'dose' in request.form and request.form['dose']:
                drug_info['dose'] = request.form['dose']

            if 'doctornotes' in request.form and request.form['doctornotes']:
                drug_info['doctornotes'] = request.form['doctornotes']

            drug_info["type"] = "Prescription"
            
            patients_data[patient_id]["schedule"].append(drug_info)  
            print("added the item to the list")
            return redirect(url_for('doctor_dashboard'))
    return render_template('doctor/edit_drug.html')

# Logout Route
@app.route('/logout')
def logout():
    session.pop('role', None)  # Clear the role from session
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
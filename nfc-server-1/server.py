from flask import Flask, request, jsonify, send_file
import json
import os

app = Flask(__name__)

def load_data():
    try:
        db_path = os.path.join(os.path.dirname(__file__), 'db.json')
        with open(db_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        # Create default structure if file doesn't exist
        default_data = {
            "students_view": {
                "read_only": []
            },
            "instructors_view": {
                "read_write": {
                    "attendance_history": []
                }
            }
        }
        save_data(default_data)
        return default_data

def save_data(data):
    with open('db.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# Initialize data
data = load_data()

# Default Route
@app.route('/')
def home():
    return "NFC-CALS Server is Running!"

@app.route('/students_view', methods=['GET'])
def get_students_view():
    data = load_data()
    return jsonify(data['students_view'])

@app.route('/instructors_view', methods=['GET'])
def get_instructors_view():
    data = load_data()
    return jsonify(data['instructors_view'])

@app.route('/attendance', methods=['POST'])
def add_attendance():
    try:
        data = load_data()
        new_attendance = request.json
        data['instructors_view']['read_write']['attendance_history'].append(new_attendance)
        save_data(data)
        return jsonify({"message": "Attendance added successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/student/<string:student_id>', methods=['GET'])
def get_student_info(student_id):
    data = load_data()
    student = next((s for s in data['students_view']['read_only'] 
                   if s['student_id'] == student_id), None)
    if student:
        return jsonify(student)
    return jsonify({"error": "Student not found"}), 404

# New route to display db.json
@app.route('/db.json')
def get_db():
    try:
        data = load_data()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# New route to display raw db.json
@app.route('/raw/db.json')
def get_raw_db():
    try:
        db_path = os.path.join(os.path.dirname(__file__), 'db.json')
        return send_file(db_path, mimetype='application/json')
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/student/<string:student_id>/course/<string:course>/percentage', methods=['GET'])
def get_course_percentage(student_id, course):
    data = load_data()
    student = next((s for s in data['students_view']['read_only'] 
                   if s['student_id'] == student_id), None)
    if not student:
        return jsonify({"error": "Student not found"}), 404
    
    course_info = next((c for c in student['courses'] 
                       if c['course'] == course), None)
    if not course_info:
        return jsonify({"error": "Course not found for this student"}), 404
    
    return jsonify({
        "student_id": student_id,
        "course": course,
        "current_percentage": course_info['current_percentage']
    })

if __name__ == '__main__':
    # Use environment variable for port (required for Heroku)
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)


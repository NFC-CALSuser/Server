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
            "courses": [],
            "instructors": [],
            "students": []
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

@app.route('/students', methods=['GET'])
def get_students():
    data = load_data()  # Reload data for each request
    return jsonify(data['students'])

@app.route('/students', methods=['POST'])
def add_student():
    try:
        data = load_data()
        new_student = request.json
        data['students'].append(new_student)
        save_data(data)
        return jsonify({"message": "Student added successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/students/<string:student_id>', methods=['GET'])
def get_student(student_id):
    data = load_data()
    student = next((s for s in data['students'] if s['id'] == student_id), None)
    if student:
        return jsonify(student)
    return jsonify({"error": "Student not found"}), 404

@app.route('/instructors', methods=['GET'])
def get_instructors():
    data = load_data()
    return jsonify(data['instructors'])

@app.route('/instructors', methods=['POST'])
def add_instructor():
    try:
        data = load_data()
        new_instructor = request.json
        data['instructors'].append(new_instructor)
        save_data(data)
        return jsonify({"message": "Instructor added successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/instructors/<string:instructor_id>', methods=['GET'])
def get_instructor(instructor_id):
    data = load_data()
    instructor = next((i for i in data['instructors'] if i['id'] == instructor_id), None)
    if instructor:
        return jsonify(instructor)
    return jsonify({"error": "Instructor not found"}), 404

@app.route('/courses', methods=['GET'])
def get_courses():
    data = load_data()
    return jsonify(data['courses'])

@app.route('/courses', methods=['POST'])
def add_course():
    try:
        data = load_data()
        new_course = request.json
        data['courses'].append(new_course)
        save_data(data)
        return jsonify({"message": "Course added successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/courses/<int:course_id>', methods=['GET'])
def get_course(course_id):
    data = load_data()
    course = next((c for c in data['courses'] if c['id'] == course_id), None)
    if course:
        return jsonify(course)
    return jsonify({"error": "Course not found"}), 404

@app.route('/courses/<int:course_id>/attendance', methods=['GET'])
def get_course_attendance(course_id):
    data = load_data()
    course = next((c for c in data['courses'] if c['id'] == course_id), None)
    if not course:
        return jsonify({"error": "Course not found"}), 404
    
    # Optionally filter by student_id if provided in query params
    student_id = request.args.get('student_id')
    if student_id:
        attendance = [a for a in course['attendance'] if a['student_id'] == student_id]
        return jsonify(attendance)
    return jsonify(course['attendance'])

@app.route('/courses/<int:course_id>/attendance', methods=['POST'])
def add_attendance(course_id):
    try:
        data = load_data()
        course = next((c for c in data['courses'] if c['id'] == course_id), None)
        if not course:
            return jsonify({"error": "Course not found"}), 404

        attendance_record = request.json
        if 'student_id' not in attendance_record:
            return jsonify({"error": "student_id is required"}), 400

        # Verify student exists
        student = next((s for s in data['students'] if s['id'] == attendance_record['student_id']), None)
        if not student:
            return jsonify({"error": "Student not found"}), 404

        # Add timestamp if not provided
        if 'timestamp' not in attendance_record:
            from datetime import datetime
            attendance_record['timestamp'] = datetime.now().isoformat()

        course['attendance'].append(attendance_record)
        save_data(data)
        return jsonify({"message": "Attendance recorded successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

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

if __name__ == '__main__':
    # Use environment variable for port (required for Heroku)
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)


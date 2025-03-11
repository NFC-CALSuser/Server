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
        default_data = {
            "students": [],
            "instructors": [],
            "classes": [],
            "courses": [],
            "attendance": []  # Added attendance key to default structure
        }
        save_data(default_data)
        return default_data

def save_data(data):
    with open('db.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

data = load_data()

@app.route('/')
def home():
    return "NFC-CALS Server is Running!"

@app.route('/students', methods=['GET'])
def get_students():
    data = load_data()
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

@app.route('/students/<int:student_id>', methods=['GET'])
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

@app.route('/instructors/<int:employee_id>', methods=['GET'])
def get_instructor(employee_id):
    data = load_data()
    instructor = next((i for i in data['instructors'] if i['employee_id'] == employee_id), None)
    if instructor:
        return jsonify(instructor)
    return jsonify({"error": "Instructor not found"}), 404

@app.route('/classes', methods=['GET'])
def get_classes():
    data = load_data()
    return jsonify(data['classes'])

@app.route('/classes', methods=['POST'])
def add_class():
    try:
        data = load_data()
        new_class = request.json
        data['classes'].append(new_class)
        save_data(data)
        return jsonify({"message": "Class added successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/classes/<string:class_number>', methods=['GET'])
def get_class(class_number):
    data = load_data()
    class_data = next((c for c in data['classes'] if c['class_number'] == class_number), None)
    if class_data:
        return jsonify(class_data)
    return jsonify({"error": "Class not found"}), 404

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

@app.route('/courses/<string:course_code>', methods=['GET'])
def get_course(course_code):
    data = load_data()
    course = next((c for c in data['courses'] if c['course_code'] == course_code), None)
    if course:
        return jsonify(course)
    return jsonify({"error": "Course not found"}), 404

# New Attendance Endpoints
@app.route('/attendance', methods=['POST'])
def add_attendance():
    try:
        data = load_data()
        new_attendance = request.json

        if 'attendance' not in data:
            data['attendance'] = []

        for record in new_attendance.get('attendance', []):
            if 'id' not in record:
                record['id'] = str(len(data['attendance']) + 1)
        
        data['attendance'].extend(new_attendance['attendance'])
        save_data(data)

        return jsonify({"message": "Attendance added successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/attendance', methods=['GET'])
def get_attendance():
    data = load_data()
    return jsonify(data.get('attendance', []))

# Display db.json
@app.route('/db.json')
def get_db():
    try:
        data = load_data()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/raw/db.json')
def get_raw_db():
    try:
        db_path = os.path.join(os.path.dirname(__file__), 'db.json')
        return send_file(db_path, mimetype='application/json')
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)


from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

def load_data():
    try:
        with open('db.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        # Create default structure if file doesn't exist
        default_data = {
            "students": [],
            "instructors": [],
            "classes": [],
            "courses": []
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

if __name__ == '__main__':
    # Use environment variable for port (required for Heroku)
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)


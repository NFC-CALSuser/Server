from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

DATA_FILE = 'data.json'

# Load data from file
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    return {"attendance": []}

# Save data to file
def save_data(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)

# GET all attendance entries
@app.route('/attendance', methods=['GET'])
def get_attendance():
    data = load_data()
    return jsonify(data['attendance'])

# POST new attendance entry
@app.route('/attendance', methods=['POST'])
def add_attendance():
    data = load_data()
    new_entry = request.json
    new_entry['id'] = str(int(os.urandom(4).hex(), 16))  # Generate random ID
    data['attendance'].append(new_entry)
    save_data(data)
    return jsonify({"message": "Attendance added successfully!"}), 201

# PUT (Replace an entry)
@app.route('/attendance/<string:attendance_id>', methods=['PUT'])
def replace_attendance(attendance_id):
    data = load_data()
    updated_entry = request.json
    for idx, entry in enumerate(data['attendance']):
        if entry['id'] == attendance_id:
            data['attendance'][idx] = updated_entry
            save_data(data)
            return jsonify({"message": "Attendance entry replaced successfully!"}), 200
    return jsonify({"error": "Attendance entry not found"}), 404

# PATCH (Update specific fields)
@app.route('/attendance/<string:attendance_id>', methods=['PATCH'])
def update_attendance(attendance_id):
    data = load_data()
    attendance_entry = next((a for a in data['attendance'] if a['id'] == attendance_id), None)

    if not attendance_entry:
        return jsonify({"error": "Attendance entry not found"}), 404

    # Merge new data with existing entry
    updated_data = request.json
    attendance_entry.update(updated_data)

    save_data(data)
    return jsonify({"message": "Attendance updated successfully!"}), 200

# DELETE attendance entry
@app.route('/attendance/<string:attendance_id>', methods=['DELETE'])
def delete_attendance(attendance_id):
    data = load_data()
    filtered_data = [entry for entry in data['attendance'] if entry['id'] != attendance_id]

    if len(filtered_data) == len(data['attendance']):
        return jsonify({"error": "Attendance entry not found"}), 404

    data['attendance'] = filtered_data
    save_data(data)
    return jsonify({"message": "Attendance entry deleted successfully!"}), 200

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, request, jsonify, send_from_directory
import os

app = Flask(__name__)

# Directory to store uploaded files
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Store messages with IDs
messages = [{"id": 1, "username": "MAXWAR", "message": "Hello!"}]
message_counter = 2  # To generate unique IDs for each message

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    global message_counter
    data = request.get_json()
    username = data.get('username')
    message = data.get('message')
    
    # Add a new message with a unique ID
    new_message = {"id": message_counter, "username": username, "message": message}
    messages.append(new_message)
    message_counter += 1
    
    return jsonify({"status": "Message received!"})

@app.route('/get_messages', methods=['GET'])
def get_messages():
    return jsonify(messages)

@app.route('/delete_message/<int:id>', methods=['DELETE'])
def delete_message(id):
    global messages
    # Remove the message with the given ID
    messages = [msg for msg in messages if msg['id'] != id]
    return jsonify({"status": "Message deleted!"})

@app.route('/edit_message/<int:id>', methods=['PUT'])
def edit_message(id):
    data = request.get_json()
    new_message = data.get('message')
    
    # Find the message by ID and update its content
    for msg in messages:
        if msg['id'] == id:
            msg['message'] = new_message
            return jsonify({"status": "Message updated!"})
    
    return jsonify({"status": "Message not found!"}), 404

@app.route('/upload_file', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"status": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"status": "No selected file"}), 400
    if file:
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        # Add a new message with file information
        global message_counter
        new_message = {"id": message_counter, "username": "System", "message": filename, "file_url": f"/uploads/{filename}"}
        messages.append(new_message)
        message_counter += 1
        return jsonify({"status": "File uploaded successfully!"})

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(host='192.168.1.7', port=8080, debug=True)

from flask import Flask, request, jsonify, send_from_directory, render_template
import sqlite3
import os
import requests

app = Flask(__name__, static_folder="static", template_folder="templates")

DATABASE = "expirer.db"

# Initialize Database

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_id TEXT UNIQUE,
            encrypted_data BLOB,
            iv BLOB,
            salt BLOB
        )
    """)
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def serve_index():
    return render_template('index.html') 

# Route for checking email breaches
@app.route('/check-breach', methods=['GET'])
def check_breach():
    email = request.args.get('email')

    if not email:
        return jsonify({"error": "Email is required"}), 400
    
    url = f"https://leakcheck.io/api/public?check={email}"
    
    try:
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            return jsonify(data)
        else:
            return jsonify({"error": "Failed to fetch data from LeakCheck API"}), 500
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# Upload & Store Encrypted PDF
@app.route("/upload", methods=["POST"])
def upload_file():
    file = request.files["file"].read()
    salt = request.files["salt"].read()
    iv = request.files["iv"].read()

    file_id = os.urandom(12).hex()

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO files (file_id, encrypted_data, iv, salt) VALUES (?, ?, ?, ?)",
                   (file_id, file, iv, salt))
    conn.commit()
    conn.close()

    share_url = f"http://127.0.0.1:5000/view/{file_id}"
    return jsonify({"message": "File uploaded & encrypted!", "share_url": share_url})

# Download & Return Encrypted PDF
@app.route("/download/<file_id>", methods=["GET"])
def download_file(file_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT encrypted_data, iv, salt FROM files WHERE file_id = ?", (file_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return jsonify({"error": "File not found"}), 404

    encrypted_data, iv, salt = row

    return {
        "encrypted_data": encrypted_data.hex(),
        "iv": iv.hex(),
        "salt": salt.hex()
    }

@app.route("/view/<file_id>", methods=['GET'])
def view_pdf(file_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM files WHERE file_id = ?", (file_id,))
    file_data = cursor.fetchone()
    conn.close()

    #Use expiration function here?
    if not file_data:
        return jsonify({"error": "File not found"}), 404

    return render_template("viewer.html", file_id=file_id), 200


if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request, jsonify, send_from_directory, render_template
import sqlite3
import os
import requests
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime, timezone
from dateutil.parser import isoparse

app = Flask(__name__, static_folder="static", template_folder="templates")

cred = credentials.Certificate("bus-expirer-firebase-adminsdk-fbsvc-34c2895d64.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

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
    expiration_str = request.form["expiration"]

    expiration_time = isoparse(expiration_str)

    doc_ref = db.collection("documents").document(file_id)
    doc_ref.set({"file": file, "salt": salt, "iv": iv, "expiration": expiration_time.isoformat()})
    # doc_ref.set({"file": file, "salt": salt, "iv": iv})

    share_url = f"http://127.0.0.1:5000/view/{file_id}"
    return jsonify({"message": "File uploaded & encrypted!", "share_url": share_url})



@app.route("/download/<file_id>", methods=["GET"])
def download_file(file_id):
    doc_ref = db.collection("documents").document(file_id)
    doc = doc_ref.get()

    if not doc.exists:
        return jsonify({"error": "File not found"}), 404

    data = doc.to_dict()
    if is_file_expired(data["expiration"]):
        return jsonify({"error": "File link has expired"}), 403

    return {
        "encrypted_data": data["file"].hex(),
        "iv": data["iv"].hex(),
        "salt": data["salt"].hex()
    }

# Checks the file expiration date and time
def is_file_expired(expiration_str):
    try:
        expiration_time = isoparse(expiration_str)
        return datetime.now(timezone.utc) > expiration_time
    except Exception as e:
        print(f"Error parsing expiration time: {e}")
        return False


@app.route("/view/<file_id>", methods=['GET'])
def view_pdf(file_id):
    doc_ref = db.collection("documents").document(file_id)
    doc = doc_ref.get()

    if not doc.exists:
        return jsonify({"error": "File not found"}), 404

    data = doc.to_dict()
    if is_file_expired(data["expiration"]):
        return render_template("expired.html"), 403

    return render_template("viewer.html", file_id=file_id), 200





if __name__ == '__main__':
    app.run(debug=True)

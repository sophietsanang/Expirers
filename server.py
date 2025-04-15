from flask import Flask, request, jsonify, send_from_directory, render_template
import sqlite3
import os
import requests
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

app = Flask(__name__, static_folder="static", template_folder="templates")

cred = credentials.Certificate("bus-expirer-firebase-adminsdk-fbsvc-b1a5218fad.json")
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

    doc_ref = db.collection("documents").document(file_id)
    doc_ref.set({"file": file, "salt": salt, "iv": iv})

    share_url = f"http://127.0.0.1:5000/view/{file_id}"
    return jsonify({"message": "File uploaded & encrypted!", "share_url": share_url})

# Download & Return Encrypted PDF
@app.route("/download/<file_id>", methods=["GET"])
def download_file(file_id):
    doc_ref = db.collection("documents").document(file_id)

    doc = doc_ref.get()
    print(type(doc))
    if doc.exists:
        print(f"Document data: {doc.to_dict()}")
    else:
        print("No such document!")

    temp_dict = doc.to_dict()

    encrypted_data, iv, salt = temp_dict["file"], temp_dict["iv"], temp_dict["salt"]

    return {
        "encrypted_data": encrypted_data.hex(),
        "iv": iv.hex(),
        "salt": salt.hex()
    }

@app.route("/view/<file_id>", methods=['GET'])
def view_pdf(file_id):
    doc_ref = db.collection("documents").document(file_id)

    #Use expiration function here?
    if not doc_ref:
        return jsonify({"error": "File not found"}), 404

    return render_template("viewer.html", file_id=file_id), 200


if __name__ == '__main__':
    app.run(debug=True)
